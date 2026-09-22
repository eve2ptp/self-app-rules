#!/usr/bin/env python3
"""Generate a Clash Meta classical provider from a sing-box source rule set."""

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
RULE_TYPES = {"package_name": "PROCESS-NAME", "domain_suffix": "DOMAIN-SUFFIX"}


def render_clash_meta(source):
    data = json.loads(source.read_text(encoding="utf-8"))
    try:
        source_name = source.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        source_name = source.name
    lines = [
        f"# Generated from {source_name} by clash-meta/build.py.",
        "# Clash Meta / mihomo: behavior: classical, format: yaml",
        "payload:",
    ]
    for rule in data["rules"]:
        # Combining fields would turn sing-box AND conditions into YAML OR rules.
        if len(rule) != 1 or next(iter(rule)) not in RULE_TYPES:
            raise ValueError(f"{source.name}: expected one supported field per rule")
        field, values = next(iter(rule.items()))
        if not isinstance(values, list) or not values:
            raise ValueError(f"{source.name}: {field} must be a non-empty list")
        for value in values:
            if not isinstance(value, str) or not value or any(c in value for c in ",\r\n"):
                raise ValueError(f"{source.name}: invalid {field} value: {value!r}")
            lines.append("  - " + json.dumps(f"{RULE_TYPES[field]},{value}"))
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT / "hk-bank.json")
    parser.add_argument("--output", type=Path, default=ROOT / "clash-meta/hk-bank.yaml")
    args = parser.parse_args()
    content = render_clash_meta(args.source)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(content)
    print(f"Built {args.output.name}")


if __name__ == "__main__":
    main()
