"""Host-side research source tools. Credentials never enter the sandbox."""
import json
import os
import random
import re
import threading
import time
import xml.etree.ElementTree as ET

import httpx
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()
ARXIV_URL = "https://export.arxiv.org/api/query"
HF_DAILY_URL = "https://huggingface.co/api/daily_papers"
HF_SEARCH_URL = "https://huggingface.co/api/papers/search"
EXA_URL = "https://mcp.exa.ai/mcp"
RETRY_STATUSES = {429, 500, 502, 503, 504}
_ARXIV_LOCK = threading.Lock()
_last_arxiv_call = 0.0


class RetryableError(Exception):
    def __init__(self, message, retry_after=None):
        super().__init__(message)
        self.retry_after = retry_after


def with_retry(fn, *, attempts=5, base=1.0, cap=30.0):
    """Retry only RetryableError with bounded exponential backoff and jitter."""
    if attempts < 1:
        raise ValueError("attempts must be positive")
    for attempt in range(attempts):
        try:
            return fn()
        except RetryableError as exc:
            if attempt == attempts - 1:
                raise
            if exc.retry_after is not None:
                delay = min(cap, max(0.0, float(exc.retry_after)))
            else:
                delay = min(cap, base * 2 ** attempt + random.uniform(0, base))
            time.sleep(delay)


def _request(method, url, **kwargs):
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.request(method, url, **kwargs)
        if response.status_code in RETRY_STATUSES:
            raw = response.headers.get("Retry-After", "")
            try:
                delay = float(raw)
            except ValueError:
                delay = None
            raise RetryableError(f"HTTP {response.status_code}", delay)
        response.raise_for_status()
        return response
    except httpx.TransportError as exc:
        raise RetryableError(f"{type(exc).__name__}: {exc}") from exc


def _error(exc):
    message = f"ERROR: {type(exc).__name__}: {exc}"
    key = os.getenv("EXA_API_KEY", "")
    return message.replace(key, "[REDACTED]") if key else message


def _compact(text, limit=600):
    return " ".join(str(text or "").split())[:limit]


def _result(records):
    return json.dumps(records, ensure_ascii=False) if records else "NO RESULTS"


def _arxiv_get(params):
    global _last_arxiv_call
    with _ARXIV_LOCK:
        delay = 3.0 - (time.monotonic() - _last_arxiv_call)
        if delay > 0:
            time.sleep(delay)
        _last_arxiv_call = time.monotonic()
        return _request("GET", ARXIV_URL, params=params)


@tool
def arxiv_search(query: str, max_results: int = 10) -> str:
    """Search recent arXiv papers by keywords. Returns JSON records with id, canonical URL, published date, title and summary; NO RESULTS or ERROR on failure."""
    try:
        terms = re.findall(r"\w+", query, flags=re.UNICODE)
        terms = [term for term in terms if term.upper() not in {"AND", "OR", "NOT", "ALL"}]
        if not terms:
            return "NO RESULTS"
        params = {"search_query": " AND ".join(f"all:{term}" for term in terms),
                  "sortBy": "submittedDate", "sortOrder": "descending",
                  "max_results": max(1, min(30, int(max_results))), "start": 0}
        response = with_retry(lambda: _arxiv_get(params), attempts=7, cap=60)
        root = ET.fromstring(response.text)
        ns = {"a": "http://www.w3.org/2005/Atom"}
        records = []
        for entry in root.findall("a:entry", ns):
            raw_id = (entry.findtext("a:id", default="", namespaces=ns)).rsplit("/abs/", 1)[-1]
            paper_id = re.sub(r"v\d+$", "", raw_id)
            if not paper_id:
                continue
            records.append({"id": paper_id, "url": f"https://arxiv.org/abs/{paper_id}",
                            "published": entry.findtext("a:published", default="", namespaces=ns)[:10],
                            "title": _compact(entry.findtext("a:title", default="", namespaces=ns)),
                            "summary": _compact(entry.findtext("a:summary", default="", namespaces=ns))})
        return _result(records)
    except Exception as exc:
        return _error(exc)


def _hf_record(item, prefer_ai=False):
    paper = item.get("paper") or {}
    paper_id = paper.get("id")
    if not paper_id:
        return None
    summary = (paper.get("ai_summary") or item.get("ai_summary")) if prefer_ai else None
    return {"id": paper_id, "url": f"https://huggingface.co/papers/{paper_id}",
            "published": str(paper.get("publishedAt") or item.get("publishedAt") or "")[:10],
            "title": _compact(paper.get("title") or item.get("title")),
            "summary": _compact(summary or paper.get("summary") or item.get("summary")),
            "upvotes": paper.get("upvotes", item.get("upvotes", 0)) or 0,
            "github": paper.get("githubRepo") or item.get("githubRepo"),
            "stars": paper.get("githubStars", item.get("githubStars", 0)) or 0}


@tool
def hf_daily_papers(limit: int = 30, date: str = "", keyword: str = "") -> str:
    """Get Hugging Face trending Daily Papers, optionally for YYYY-MM-DD and filtered by keyword in title/summary. Returns JSON records or NO RESULTS/ERROR."""
    try:
        params = {"limit": max(1, min(100, int(limit)))}
        if date:
            params["date"] = date
        data = with_retry(lambda: _request("GET", HF_DAILY_URL, params=params)).json()
        records = [_hf_record(item) for item in data]
        records = [record for record in records if record]
        if keyword:
            records = [record for record in records if keyword.casefold() in
                       (record["title"] + " " + record["summary"]).casefold()]
        records.sort(key=lambda record: record["upvotes"], reverse=True)
        return _result(records)
    except Exception as exc:
        return _error(exc)


@tool
def hf_search_papers(query: str, limit: int = 10) -> str:
    """Search Hugging Face papers by topic and return JSON records with id, URL, date, summary and popularity; NO RESULTS/ERROR otherwise."""
    try:
        data = with_retry(lambda: _request("GET", HF_SEARCH_URL,
                          params={"q": query, "limit": max(1, min(50, int(limit)))})).json()
        return _result([record for item in data if (record := _hf_record(item, prefer_ai=True))])
    except Exception as exc:
        return _error(exc)


def _exa_call(name, arguments):
    key = os.getenv("EXA_API_KEY", "").strip()
    params = {"exaApiKey": key} if key else None
    payload = {"jsonrpc": "2.0", "id": 1, "method": "tools/call",
               "params": {"name": name, "arguments": arguments}}
    response = _request("POST", EXA_URL, params=params, json=payload,
                        headers={"Accept": "application/json, text/event-stream"})
    lines = [line[5:].strip() for line in response.text.splitlines() if line.startswith("data:")]
    data = json.loads(lines[-1] if lines else response.text)
    if "error" in data:
        raise RuntimeError(str(data["error"]))
    result = data.get("result") or {}
    meta = result.get("_meta") or {}
    content = "\n".join(block.get("text", "") for block in result.get("content", [])
                        if block.get("type") == "text")
    meta_text = json.dumps(meta).lower()
    if any(word in meta_text for word in ("ratelimit", "rate_limit", "rate limit", "throttl")) or (
        "rate limit" in content.lower() and ("exa" in content.lower() or "retry" in content.lower())
    ):
        raise RetryableError("Exa rate limit")
    if result.get("isError"):
        raise RuntimeError(content or "Exa tool error")
    return content or "NO RESULTS"


@tool
def web_search(query: str, objective: str = "", num_results: int = 5) -> str:
    """Search the web via Exa for pages matching a research objective. Returns result text with URLs, NO RESULTS or ERROR."""
    try:
        return with_retry(lambda: _exa_call("web_search_exa", {
            "query": query, "objective": objective or f"Find reliable sources about {query}",
            "numResults": max(1, min(10, int(num_results)))}), attempts=7, cap=60)
    except Exception as exc:
        return _error(exc)


@tool
def web_fetch(url: str) -> str:
    """Fetch one web page via Exa for citation verification. Returns markdown text truncated to 12000 characters, NO RESULTS or ERROR."""
    try:
        return with_retry(lambda: _exa_call("web_fetch_exa", {"urls": [url]}),
                          attempts=7, cap=60)[:12000]
    except Exception as exc:
        return _error(exc)


SOURCE_TOOLS = [arxiv_search, hf_daily_papers, hf_search_papers, web_search, web_fetch]


if __name__ == "__main__":
    for name, fn, args in [
        ("arxiv_search", arxiv_search, {"query": "world model", "max_results": 3}),
        ("hf_daily_papers", hf_daily_papers, {"limit": 20}),
        ("hf_search_papers", hf_search_papers, {"query": "world model", "limit": 3}),
        ("web_search", web_search, {"query": "survey paper on world models", "num_results": 2}),
        ("web_fetch", web_fetch, {"url": "https://arxiv.org/abs/1803.10122"}),
    ]:
        print(f"== {name}\n{fn.invoke(args)[:400]}\n")
