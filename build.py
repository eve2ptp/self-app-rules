#!/usr/bin/env python3
"""Build direct, proxy, Bybit EU and Google Play rules for sing-box and mihomo."""

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parent
RULE_GROUPS = ("direct", "proxy", "bybit-eu", "google-play")
RULE_TYPES = {"package_name", "domain_suffix"}


def render_clash_meta(source, root=ROOT):
    data = json.loads(source.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("rules"), list):
        raise ValueError(f"{source}: expected a rules list")
    domains = []
    processes = []
    for rule in data["rules"]:
        # Splitting fields would turn sing-box AND conditions into OR rules.
        if not isinstance(rule, dict) or len(rule) != 1 or next(iter(rule)) not in RULE_TYPES:
            raise ValueError(f"{source}: expected one supported field per rule")
        field, values = next(iter(rule.items()))
        if not isinstance(values, list) or not values:
            raise ValueError(f"{source}: {field} must be a non-empty list")
        for value in values:
            if not isinstance(value, str) or not value or any(c in value for c in ",\r\n"):
                raise ValueError(f"{source}: invalid {field} value: {value!r}")
            if field == "domain_suffix":
                # +. matches both the domain itself and its subdomains.
                domains.append(f"+.{value}")
            else:
                processes.append("  - " + json.dumps(f"PROCESS-NAME,{value}"))
    if not domains:
        raise ValueError(f"{source}: domain MRS requires at least one domain_suffix")
    source_name = source.resolve().relative_to(root.resolve()).as_posix()
    process_lines = [
        f"# Generated from {source_name} by build.py.",
        "# Process rules are separate because MRS does not support PROCESS-NAME.",
        "# Clash Meta / mihomo: behavior: classical, format: yaml",
        "payload:" if processes else "payload: []",
        *processes,
    ]
    return "\n".join(domains) + "\n", "\n".join(process_lines) + "\n"


def build_rules(root=ROOT, sing_box="sing-box", mihomo="mihomo"):
    root = root.resolve()
    sources = [root / f"{group}.json" for group in RULE_GROUPS]
    # Validate every source before starting any compiler.
    providers = [(source, render_clash_meta(source, root)) for source in sources]
    # Compile everything before replacing checked-in artifacts.
    with tempfile.TemporaryDirectory(prefix="financial-rules-build-") as temporary:
        staging = Path(temporary)
        outputs = []
        for source, (domains, processes) in providers:
            domain_source = staging / f"{source.stem}.txt"
            domain_source.write_text(domains, encoding="utf-8", newline="\n")
            srs = staging / f"{source.stem}.srs"
            mrs = staging / f"{source.stem}.mrs"
            process_yaml = staging / f"{source.stem}-process.yaml"
            subprocess.run(
                [sing_box, "rule-set", "compile", "--output", str(srs), str(source)],
                check=True,
            )
            subprocess.run(
                [mihomo, "convert-ruleset", "domain", "text", str(domain_source), str(mrs)],
                check=True,
            )
            process_yaml.write_text(processes, encoding="utf-8", newline="\n")
            outputs.extend([
                (srs, source.with_suffix(".srs")),
                (mrs, source.parent / "clash-meta" / mrs.name),
                (process_yaml, source.parent / "clash-meta" / process_yaml.name),
            ])
        for staged, output in outputs:
            output.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(staged, output)
            print(f"Built {output.relative_to(root).as_posix()}")


def resolve_executable(executable, root=ROOT):
    path = Path(executable)
    if path.is_absolute() or path.parent != Path("."):
        if path.is_file():
            return str(path)
        raise FileNotFoundError(executable)
    suffixes = (".exe", "") if os.name == "nt" else ("",)
    for suffix in suffixes:
        candidate = root / "tools" / f"{executable}{suffix}"
        if candidate.is_file():
            return str(candidate)
    found = shutil.which(executable)
    if found is None:
        raise FileNotFoundError(executable)
    return found


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sing-box", default="sing-box",
        help="sing-box executable name or path (default: tools/sing-box, then PATH)",
    )
    parser.add_argument(
        "--mihomo", default="mihomo",
        help="mihomo executable name or path (default: tools/mihomo, then PATH)",
    )
    args = parser.parse_args()
    try:
        sing_box = resolve_executable(args.sing_box)
        mihomo = resolve_executable(args.mihomo)
    except FileNotFoundError as error:
        parser.error(f"executable not found: {error.args[0]}")
    build_rules(sing_box=sing_box, mihomo=mihomo)


if __name__ == "__main__":
    main()
