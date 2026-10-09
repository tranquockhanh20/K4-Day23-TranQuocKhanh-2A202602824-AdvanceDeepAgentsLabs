"""Apply host-fetched canonical titles inside the sandbox (standard library only)."""
import json

SOURCES = "/tmp/work/research/sources.json"
TITLE_MAP = "/tmp/work/research/title_map.json"


def main():
    with open(SOURCES, encoding="utf-8") as stream:
        sources = json.load(stream)
    with open(TITLE_MAP, encoding="utf-8") as stream:
        titles = json.load(stream)
    changed = 0
    for source in sources:
        canonical = titles.get(source.get("url"))
        if canonical and source.get("title") != canonical:
            source["title"] = canonical
            changed += 1
    with open(SOURCES, "w", encoding="utf-8") as stream:
        json.dump(sources, stream, ensure_ascii=False, indent=2)
    print(f"TITLES: normalized {changed}")


if __name__ == "__main__":
    main()
