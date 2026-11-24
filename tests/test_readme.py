import json
import re
import unittest

import build


class ReadmeTests(unittest.TestCase):
    def test_documented_counts_match_sources(self):
        readme = (build.ROOT / "README.md").read_text(encoding="utf-8")
        totals = [0, 0]
        for group in build.RULE_GROUPS:
            data = json.loads((build.ROOT / f"{group}.json").read_text(encoding="utf-8"))
            counts = [0, 0]
            for rule in data["rules"]:
                for field, values in rule.items():
                    counts[field == "domain_suffix"] += len(values)
            totals = [total + count for total, count in zip(totals, counts)]
            row = re.search(
                rf"^\| \[{re.escape(group)}\]\({re.escape(group)}\.json\) \|.*\| (\d+) / (\d+) \|$",
                readme,
                re.MULTILINE,
            )
            self.assertIsNotNone(row, f"README table is missing {group}")
            self.assertEqual(
                [int(row[1]), int(row[2])], counts, f"README counts for {group} are stale"
            )
        summary = re.search(r"共包含 \*\*(\d+) 个应用包名、(\d+) 个域名后缀\*\*", readme)
        self.assertIsNotNone(summary, "README summary counts are missing")
        self.assertEqual(
            [int(summary[1]), int(summary[2])], totals, "README summary counts are stale"
        )


if __name__ == "__main__":
    unittest.main()
