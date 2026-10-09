"""Fetch canonical paper titles on the host; apply them only inside the sandbox."""
import json
import re
from html import unescape
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import quote, unquote

import httpx
from tools import with_retry, _request

TITLE_MAP_PATH = "/tmp/work/research/title_map.json"
APPLY_TITLES_PATH = "/tmp/work/research/apply_titles.py"
PAPER_ID = re.compile(r"(?:arxiv\.org/abs/|huggingface\.co/papers/)(\d{4}\.\d{4,5})(?:v\d+)?")
DOI = re.compile(r"(10\.\d{4,9}/[^?#]+)", re.I)
_TITLE_CACHE = {}


def _canonical_title(url):
    match = PAPER_ID.search(url)
    if match:
        paper_id = match.group(1)
        try:
            data = with_retry(lambda: _request(
                "GET", f"https://huggingface.co/api/papers/{paper_id}"),
                attempts=3, base=1, cap=5).json()
            title = " ".join((data.get("title") or "").split())
            if title:
                return title
        except (httpx.HTTPError, ValueError):
            pass
        page = with_retry(lambda: _request(
            "GET", f"https://arxiv.org/abs/{paper_id}"),
            attempts=3, base=1, cap=5)
        titles = re.findall(
            r'<meta[^>]+name="citation_title"[^>]+content="([^"]+)"',
            page.text, re.I)
        return " ".join(unescape(titles[0]).split()) if titles else None
    match = DOI.search(unquote(url))
    if match:
        doi = match.group(1).rstrip("/")
        response = with_retry(lambda: _request(
            "GET", f"https://api.crossref.org/works/{quote(doi, safe='/')}"),
            attempts=3, base=1, cap=5)
        titles = response.json().get("message", {}).get("title") or []
        return " ".join(titles[0].split()) if titles else None
    return None


def collect_titles(sources):
    """Return URL -> exact public metadata title; leave failures untouched."""
    urls = {item.get("url") for item in sources if isinstance(item, dict) and item.get("url")}
    pending = urls - _TITLE_CACHE.keys()
    with ThreadPoolExecutor(max_workers=3) as pool:
        tasks = {pool.submit(_canonical_title, url): url for url in pending}
        for future in as_completed(tasks):
            try:
                title = future.result()
                if title:
                    _TITLE_CACHE[tasks[future]] = title
            except (httpx.HTTPError, ValueError, TypeError, RuntimeError):
                pass
    return {url: _TITLE_CACHE[url] for url in urls if url in _TITLE_CACHE}


def normalize_titles(backend, sources_path, upload, download, script_bytes):
    """Fetch metadata on host, then edit only sources.json inside the sandbox."""
    raw = download(backend, [sources_path]).get(sources_path)
    if not raw:
        return 0
    sources = json.loads(raw.decode("utf-8"))
    mapping = collect_titles(sources)
    if not mapping:
        return 0
    upload(backend, {TITLE_MAP_PATH: json.dumps(mapping, ensure_ascii=False).encode("utf-8"),
                     APPLY_TITLES_PATH: script_bytes})
    result = backend.execute(f"python3 {APPLY_TITLES_PATH}")
    if result.exit_code != 0:
        raise RuntimeError(f"title normalization failed: {result.output[:500]}")
    return len(mapping)
