import contextlib
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import build


class RenderTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.source = self.root / "direct.json"

    def render(self, rules):
        self.source.write_text(json.dumps({"version": 1, "rules": rules}), encoding="utf-8")
        return build.render_clash_meta(self.source, self.root)

    def test_independent_domain_and_package_matches_preserve_case(self):
        domains, processes = self.render([
            {"package_name": ["com.MobileTreeApp", "com.outSystems.FubonHKeKYC.prd"]},
            {"domain_suffix": ["example.com", "service.example.net"]},
        ])
        self.assertEqual(domains, "+.example.com\n+.service.example.net\n")
        payload = [json.loads(line[4:]) for line in processes.splitlines() if line.startswith("  - ")]
        self.assertEqual(payload, [
            "PROCESS-NAME,com.MobileTreeApp",
            "PROCESS-NAME,com.outSystems.FubonHKeKYC.prd",
        ])
        self.assertIn("Generated from direct.json", processes)

    def test_rejects_conditions_that_would_change_matching_semantics(self):
        for rule in (
            {"package_name": ["com.example"], "domain_suffix": ["example.com"]},
            {"domain": ["example.com"]},
            {"type": "logical", "mode": "and", "rules": []},
            {},
            "invalid",
        ):
            with self.subTest(rule=rule), self.assertRaises(ValueError):
                self.render([rule])

    def test_rejects_invalid_values(self):
        for field in ("package_name", "domain_suffix"):
            for values in ([], "example.com", [""], [None], [42], ["a,b"], ["a\nb"], ["a\rb"]):
                with self.subTest(field=field, values=values), self.assertRaises(ValueError):
                    self.render([{field: values}])

    def test_requires_domains_for_mrs(self):
        for rules in ([], [{"package_name": ["com.example"]}]):
            with self.subTest(rules=rules), self.assertRaisesRegex(ValueError, "at least one domain_suffix"):
                self.render(rules)

    def test_domain_only_source_has_empty_process_payload(self):
        _, processes = self.render([{"domain_suffix": ["example.com"]}])
        self.assertTrue(processes.endswith("payload: []\n"))

    def test_rejects_invalid_rule_set_structure(self):
        for data in ([], {}, {"rules": None}, {"rules": {}}):
            self.source.write_text(json.dumps(data), encoding="utf-8")
            with self.subTest(data=data), self.assertRaisesRegex(ValueError, "rules list"):
                build.render_clash_meta(self.source, self.root)


class BuildTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.sources = []
        for group in build.RULE_GROUPS:
            source = self.root / f"{group}.json"
            data = {"version": 1, "rules": [
                {"package_name": [f"com.{group}"]},
                {"domain_suffix": [f"{group}.example"]},
            ]}
            source.write_text(json.dumps(data), encoding="utf-8")
            self.sources.append(source)

    def artifacts(self, source):
        return (
            source.with_suffix(".srs"),
            source.parent / "clash-meta" / f"{source.stem}.mrs",
            source.parent / "clash-meta" / f"{source.stem}-process.yaml",
        )

    @staticmethod
    def fake_compile(command, check):
        # Stand in for the external compilers while preserving distinct inputs.
        if command[0] == "sing-box":
            Path(command[-2]).write_bytes(b"srs\n" + Path(command[-1]).read_bytes())
        else:
            Path(command[-1]).write_bytes(b"mrs\n" + Path(command[-2]).read_bytes())

    def snapshot(self):
        return {path.relative_to(self.root): path.read_bytes() for path in self.root.rglob("*") if path.is_file()}

    def run_build(self):
        with contextlib.redirect_stdout(io.StringIO()):
            build.build_rules(self.root)

    def test_flat_groups_keep_distinct_outputs(self):
        with patch("build.subprocess.run", side_effect=self.fake_compile) as compiler:
            self.run_build()
        self.assertEqual(compiler.call_count, 2 * len(self.sources))
        for source in self.sources:
            srs, mrs, processes = self.artifacts(source)
            self.assertEqual(srs.read_bytes(), b"srs\n" + source.read_bytes())
            expected_domain = f"mrs\n+.{source.stem}.example\n"
            self.assertEqual(mrs.read_text(encoding="utf-8"), expected_domain)
            self.assertIn(f"PROCESS-NAME,com.{source.stem}", processes.read_text(encoding="utf-8"))
        self.assertEqual(len(self.snapshot()), 4 * len(self.sources))  # One source and three artifacts per group.

    def test_failed_compilers_leave_all_existing_artifacts_untouched(self):
        for source in self.sources:
            for output in self.artifacts(source):
                output.parent.mkdir(exist_ok=True)
                output.write_bytes(b"original " + output.relative_to(self.root).as_posix().encode())
        before = self.snapshot()
        compiler_count = 2 * len(self.sources)
        for failure_index in (compiler_count - 2, compiler_count - 1):  # Fail the last SRS or MRS.
            calls = []

            def fail_late(command, check):
                calls.append(command)
                if len(calls) - 1 == failure_index:
                    raise subprocess.CalledProcessError(1, command)
                self.fake_compile(command, check)

            with self.subTest(compiler=failure_index), patch("build.subprocess.run", side_effect=fail_late):
                with self.assertRaises(subprocess.CalledProcessError):
                    self.run_build()
            self.assertEqual(self.snapshot(), before)

    def test_invalid_last_source_prevents_all_compilation(self):
        self.sources[-1].write_text('{"rules": [{"domain_suffix": []}]}', encoding="utf-8")
        before = self.snapshot()
        with patch("build.subprocess.run") as compiler:
            with self.assertRaises(ValueError):
                self.run_build()
        compiler.assert_not_called()
        self.assertEqual(self.snapshot(), before)


class RoutingTests(unittest.TestCase):
    def test_bybit_eu_matches_stay_out_of_general_groups(self):
        def values(group, field):
            data = json.loads((build.ROOT / f"{group}.json").read_text(encoding="utf-8"))
            return {value for rule in data["rules"] for value in rule.get(field, [])}

        self.assertIn("com.bybit.eu", values("bybit-eu", "package_name"))
        self.assertTrue({"bybit.eu", "bycsi.com"} <= values("bybit-eu", "domain_suffix"))
        for group in ("direct", "proxy"):
            with self.subTest(group=group):
                self.assertFalse(values(group, "package_name") & values("bybit-eu", "package_name"))
                for general in values(group, "domain_suffix"):
                    for dedicated in values("bybit-eu", "domain_suffix"):
                        self.assertFalse(
                            general == dedicated
                            or general.endswith("." + dedicated)
                            or dedicated.endswith("." + general),
                            f"{general} overlaps the dedicated Bybit EU rule {dedicated}",
                        )

    def test_sing_box_example_binds_dedicated_exit_before_general_rules(self):
        example = json.loads((build.ROOT / "examples" / "sing-box.json").read_text(encoding="utf-8"))
        route = example["route"]
        self.assertEqual(route["rules"][0], {
            "rule_set": ["bybit-eu"], "action": "route", "outbound": "Bybit-EU-DE",
        })
        destinations = {group: rule["outbound"] for rule in route["rules"] for group in rule["rule_set"]}
        self.assertEqual(destinations, {"direct": "direct", "proxy": "proxy", "bybit-eu": "Bybit-EU-DE"})
        providers = {provider["tag"]: provider for provider in route["rule_set"]}
        self.assertEqual(set(providers), set(destinations))
        for group, provider in providers.items():
            self.assertEqual(provider["url"], f"https://raw.githubusercontent.com/eve2ptp/hk-bank/main/{group}.srs")
            self.assertTrue((build.ROOT / f"{group}.json").is_file())
        selector = next(outbound for outbound in example["outbounds"] if outbound["tag"] == "Bybit-EU-DE")
        self.assertEqual(selector["outbounds"], ["德国节点01"])
        self.assertEqual(selector["default"], "德国节点01")


if __name__ == "__main__":
    unittest.main()
