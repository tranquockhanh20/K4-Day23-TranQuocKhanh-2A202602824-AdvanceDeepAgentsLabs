"""Refresh generated reference titles in a sandbox without hand-editing reports.

Usage: python revalidate_reports.py
Each report body stays as the research agent wrote it. Only sources.json titles
and the generated References section can change. Outputs are downloaded from
the sandbox after the provided finalizer and citation validator succeed.
"""
import json
import sys
from pathlib import Path

from agents import FINALIZER_PATH, REPORT_PATH, SOURCES_PATH, VALIDATOR_PATH, WORKDIR
from check_citations import check
from normalize_titles import normalize_titles
from research import (FINALIZER_SOURCE, REPORTS, ROOT, TITLE_SCRIPT_SOURCE,
                      VALIDATOR_SOURCE, source_url_problems)
from sandbox import download, open_sandbox, upload


def refresh(report_path):
    sources_path = Path(str(report_path).removesuffix(".md") + ".sources.json")
    meta_path = Path(str(report_path).removesuffix(".md") + ".meta.json")
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    original = json.loads(sources_path.read_text(encoding="utf-8"))
    with open_sandbox() as backend:
        setup = backend.execute(f"mkdir -p {WORKDIR}/research {WORKDIR}/report")
        if setup.exit_code:
            raise RuntimeError(setup.output)
        upload(backend, {REPORT_PATH: report_path.read_bytes(),
                         SOURCES_PATH: sources_path.read_bytes(),
                         VALIDATOR_PATH: VALIDATOR_SOURCE.read_bytes(),
                         FINALIZER_PATH: FINALIZER_SOURCE.read_bytes()})
        normalize_titles(backend, SOURCES_PATH, upload, download,
                         TITLE_SCRIPT_SOURCE.read_bytes())
        finalized = backend.execute(f"python3 {FINALIZER_PATH}")
        if finalized.exit_code:
            raise RuntimeError(finalized.output)
        validated = backend.execute(f"python3 {VALIDATOR_PATH}")
        if validated.exit_code or "OK:" not in validated.output:
            raise RuntimeError(validated.output)
        files = download(backend, [REPORT_PATH, SOURCES_PATH])
        report_bytes, sources_bytes = files[REPORT_PATH], files[SOURCES_PATH]
        sources = json.loads(sources_bytes.decode("utf-8"))
        issues = check(report_bytes.decode("utf-8"), sources) + source_url_problems(sources)
        if issues or len(sources) != len(original) or len(sources) != meta["n_sources"]:
            raise RuntimeError("; ".join(issues) or "source count changed")
        if len({item["source"] for item in sources}) < 3:
            raise RuntimeError("fewer than three source families")
    # The two delivered files are exactly the bytes downloaded from the sandbox.
    report_path.write_bytes(report_bytes)
    sources_path.write_bytes(sources_bytes)
    print(f"OK: {report_path.name} ({len(sources)} sources)")


def main():
    for report in sorted(REPORTS.glob("*.md")):
        try:
            refresh(report)
        except Exception as exc:
            print(f"FAILED {report.name}: {type(exc).__name__}: {exc}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
