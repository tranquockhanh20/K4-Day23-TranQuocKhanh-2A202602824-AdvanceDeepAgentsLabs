"""Run the deep research workflow for one topic."""
import json
import os
import re
import sys
import time
from collections import Counter
from pathlib import Path

from agents import FINALIZER_PATH, REPORT_PATH, SOURCES_PATH, VALIDATOR_PATH, WORKDIR, build_lead_agent
from model import make_model
from normalize_titles import normalize_titles
from sandbox import download, open_sandbox, upload

ROOT = Path(__file__).parent
REPORTS = ROOT / "reports"
VALIDATOR_SOURCE = ROOT / "check_citations.py"
FINALIZER_SOURCE = ROOT / "finalize_citations.py"
TITLE_SCRIPT_SOURCE = ROOT / "apply_titles.py"


def slugify(topic):
    slug = re.sub(r"[^\w]+", "-", topic.strip().lower(), flags=re.UNICODE).strip("-")
    return slug[:60].rstrip("-") or "topic"


def build_prompt(topic):
    return (f"Research and write the complete cited survey for: {topic}. "
            "Follow all lead instructions and the REPORT_TEMPLATE structure. "
            "Use at least three independent researcher tasks and at least three source families. "
            "Complete finalization, validation and citation spot checks in the sandbox.")


def summarize(messages, elapsed, model_name):
    calls = Counter()
    input_tokens = output_tokens = 0
    for message in messages:
        for call in getattr(message, "tool_calls", None) or []:
            calls[call.get("name", "unknown")] += 1
        usage = getattr(message, "usage_metadata", None) or {}
        input_tokens += usage.get("input_tokens", 0) or 0
        output_tokens += usage.get("output_tokens", 0) or 0
    return {"model": model_name, "elapsed_s": round(elapsed, 1),
            "subagent_calls": calls.get("task", 0),
            "tool_calls": dict(calls),
            "tokens": {"input": input_tokens, "output": output_tokens}}


def source_url_problems(sources):
    problems = []
    for source in sources:
        family, paper_id, url = source.get("source"), source.get("id"), source.get("url")
        if family == "arxiv" and url != f"https://arxiv.org/abs/{paper_id}":
            problems.append(f"source [{source.get('n')}] arxiv URL/id mismatch")
        elif family in {"hf-daily", "hf-search"} and url != f"https://huggingface.co/papers/{paper_id}":
            problems.append(f"source [{source.get('n')}] {family} URL/id mismatch")
        elif family not in {"arxiv", "hf-daily", "hf-search", "web"}:
            problems.append(f"source [{source.get('n')}] invalid family {family}")
    return problems

def save_outputs(backend, topic, messages, elapsed, model_name, reports_dir=REPORTS):
    files = download(backend, [REPORT_PATH, SOURCES_PATH])
    report_bytes, sources_bytes = files.get(REPORT_PATH), files.get(SOURCES_PATH)
    if not report_bytes or not report_bytes.strip() or not sources_bytes:
        raise RuntimeError("report.md or sources.json is missing/empty in sandbox")
    try:
        report_text = report_bytes.decode("utf-8")
        sources = json.loads(sources_bytes.decode("utf-8"))
    except (UnicodeError, ValueError) as exc:
        raise RuntimeError(f"invalid report or sources encoding/JSON: {exc}") from exc
    if not isinstance(sources, list) or not sources:
        raise RuntimeError("sources.json must be a nonempty JSON array")
    from check_citations import check
    issues = check(report_text, sources) + source_url_problems(sources)
    if issues:
        raise RuntimeError("citation validation failed: " + "; ".join(issues[:5]))
    meta = {"topic": topic, **summarize(messages, elapsed, model_name),
            "n_sources": len(sources),
            "source_families": sorted({source.get("source", "") for source in sources})}
    if meta["subagent_calls"] < 3:
        raise RuntimeError("fewer than three subagent calls")
    if len(meta["source_families"]) < 3:
        raise RuntimeError("fewer than three source families")
    reports_dir.mkdir(parents=True, exist_ok=True)
    stem = slugify(topic)
    report_path = reports_dir / f"{stem}.md"
    # All validation above completes before writing anything.
    (reports_dir / f"{stem}.sources.json").write_bytes(sources_bytes)
    (reports_dir / f"{stem}.meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_path.write_bytes(report_bytes)
    return report_path


def main(topic):
    if not topic.strip():
        print('Usage: python research.py "<topic>"', file=sys.stderr)
        return 2
    try:
        model = make_model()
        started = time.monotonic()
        with open_sandbox() as backend:
            setup = backend.execute(f"mkdir -p {WORKDIR}/research/notes {WORKDIR}/report")
            if setup.exit_code != 0:
                raise RuntimeError(f"cannot create sandbox directories: {setup.output}")
            upload(backend, {VALIDATOR_PATH: VALIDATOR_SOURCE.read_bytes(),
                             FINALIZER_PATH: FINALIZER_SOURCE.read_bytes()})
            agent = build_lead_agent(backend, model)
            result = agent.invoke({"messages": [{"role": "user", "content": build_prompt(topic)}]},
                                  config={"recursion_limit": 1000})
            # Restore trusted scripts and allow bounded, in-sandbox repair of model mistakes.
            for repair_attempt in range(3):
                upload(backend, {VALIDATOR_PATH: VALIDATOR_SOURCE.read_bytes(),
                                 FINALIZER_PATH: FINALIZER_SOURCE.read_bytes()})
                normalize_titles(backend, SOURCES_PATH, upload, download,
                                 TITLE_SCRIPT_SOURCE.read_bytes())
                finalized = backend.execute(f"python3 {FINALIZER_PATH}")
                if finalized.exit_code == 0:
                    validated = backend.execute(f"python3 {VALIDATOR_PATH}")
                    if validated.exit_code == 0 and "OK:" in validated.output:
                        current = download(backend, [SOURCES_PATH]).get(SOURCES_PATH)
                        try:
                            current_sources = json.loads(current.decode("utf-8"))
                            family_issues = source_url_problems(current_sources)
                            families = {s.get("source") for s in current_sources}
                            if len(families) < 3:
                                family_issues.append(
                                    f"only {len(families)} source families remain: {sorted(families)}; "
                                    "add a verified source from a missing family to the report body")
                        except (AttributeError, UnicodeError, ValueError) as exc:
                            family_issues = [f"invalid sources.json: {exc}"]
                        if not family_issues:
                            break
                        problem = "source label/URL check failed: " + "; ".join(family_issues)
                    else:
                        problem = f"citation validator failed: {validated.output[:1000]}"
                else:
                    problem = f"citation finalizer failed: {finalized.output[:1000]}"
                if repair_attempt == 2:
                    raise RuntimeError(problem)
                repair_prompt = (
                    f"The trusted citation check found this problem in the sandbox: {problem}. "
                    f"Repair {REPORT_PATH} and, only from verified notes, {SOURCES_PATH}. "
                    "For missing citation numbers, either add the real source from a researcher note "
                    "or remove the unsupported claim/citation. Never invent a source or edit the "
                    "finalizer/validator scripts. Finish by rerunning finalizer and validator."
                )
                result = agent.invoke({"messages": result["messages"] + [
                    {"role": "user", "content": repair_prompt}]},
                    config={"recursion_limit": 1000})
            path = save_outputs(backend, topic, result["messages"],
                                time.monotonic() - started, os.getenv("LAB_MODEL", "unknown"))
        print(f"Saved {path}")
        return 0
    except Exception as exc:
        print(f"FAILED: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main(" ".join(sys.argv[1:])))
