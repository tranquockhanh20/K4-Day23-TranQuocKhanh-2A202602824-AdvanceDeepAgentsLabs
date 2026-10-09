"""Validate report citations against sources.json (standard library only)."""
import json
import re
import sys

REPORT = "/tmp/work/report/report.md"
SOURCES = "/tmp/work/research/sources.json"


def check(report_text, sources):
    """Return citation and reference consistency problems."""
    if not isinstance(sources, list) or not sources:
        return ["no sources in sources.json"]
    problems = []
    by_number = {}
    urls_seen = set()
    for index, source in enumerate(sources, 1):
        if not isinstance(source, dict):
            problems.append(f"source {index} is not an object")
            continue
        number, url = source.get("n"), source.get("url")
        if type(number) is not int:
            problems.append(f"source {index} has invalid n")
        elif number in by_number:
            problems.append(f"duplicate source number [{number}]")
        else:
            by_number[number] = source
        if not isinstance(url, str) or not re.match(r"^https?://", url):
            problems.append(f"source {index} has invalid URL")
        elif url in urls_seen:
            problems.append(f"duplicate URL: {url}")
        else:
            urls_seen.add(url)

    parts = re.split(r"(?m)^## References\s*$", report_text, maxsplit=1)
    if len(parts) != 2:
        problems.append("missing ## References heading")
        body, references = report_text, ""
    else:
        body, references = parts
    body = re.sub(r"(?ms)^\s*\x60\x60\x60.*?^\s*\x60\x60\x60[^\n]*$", "", body)
    body = re.sub(r"\x60[^\x60\n]*\x60", "", body)
    body = re.sub(r"\[\d+\]\([^)]*\)", "", body)
    cited = set()
    for match in re.finditer(r"\[([\d,\s-]+)\]", body):
        expression = match.group(1).strip()
        if not re.fullmatch(r"\d+(?:\s*(?:,|-)\s*\d+)*", expression):
            continue
        for item in re.split(r"\s*,\s*", expression):
            range_match = re.fullmatch(r"(\d+)\s*-\s*(\d+)", item)
            if range_match:
                first, last = map(int, range_match.groups())
                cited.update(range(first, last + 1))
            elif item.isdigit():
                cited.add(int(item))
    for number in sorted(cited - by_number.keys()):
        problems.append(f"[{number}] cited but missing from sources.json")
    for number in sorted(by_number.keys() - cited):
        problems.append(f"source [{number}] never cited")

    reference_counts = {}
    for line in references.splitlines():
        match = re.match(r"^\[(\d+)\]\s+(.+)$", line)
        if not match:
            continue
        number = int(match.group(1))
        reference_counts[number] = reference_counts.get(number, 0) + 1
        urls = re.findall(r"https?://[^\s<>]+", match.group(2))
        if len(urls) != 1:
            problems.append(f"reference [{number}] must contain exactly one URL")
        elif number in by_number and urls[0] != by_number[number].get("url"):
            problems.append(f"reference [{number}] URL does not match sources.json")
        if re.search(r";\s+(?:\[\d+\]|https?://)", match.group(2)):
            problems.append(f"reference [{number}] bundles multiple sources")
    for number in sorted(by_number):
        if reference_counts.get(number, 0) != 1:
            problems.append(f"source [{number}] needs exactly one reference line")
    for number in sorted(reference_counts.keys() - by_number.keys()):
        problems.append(f"reference [{number}] missing from sources.json")
    for number, count in sorted(reference_counts.items()):
        if count > 1:
            problems.append(f"duplicate reference [{number}]")
    return problems


def main(argv):
    report_path = argv[1] if len(argv) > 1 else REPORT
    sources_path = argv[2] if len(argv) > 2 else SOURCES
    try:
        with open(report_path, encoding="utf-8") as f:
            report = f.read()
        with open(sources_path, encoding="utf-8") as f:
            sources = json.load(f)
    except (OSError, ValueError) as exc:
        print(f"cannot read inputs: {exc}")
        return 1
    problems = check(report, sources)
    if problems:
        print("\n".join(problems))
        return 1
    print(f"OK: {len(sources)} sources, all citations resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
