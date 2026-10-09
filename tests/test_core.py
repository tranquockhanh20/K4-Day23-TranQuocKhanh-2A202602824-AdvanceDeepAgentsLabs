"""Focused regression tests for the lab's deterministic safety checks."""
import unittest
from unittest.mock import patch

from check_citations import check
from research import slugify
from tools import RetryableError, with_retry


class CoreTests(unittest.TestCase):
    def test_retry_respects_retry_after_without_sleeping_after_final_failure(self):
        calls = 0

        def fail():
            nonlocal calls
            calls += 1
            raise RetryableError("busy", retry_after=4)

        with patch("tools.time.sleep") as sleep:
            with self.assertRaises(RetryableError):
                with_retry(fail, attempts=3, cap=5)
        self.assertEqual(calls, 3)
        self.assertEqual([call.args[0] for call in sleep.call_args_list], [4, 4])

    def test_retry_does_not_hide_non_retryable_error(self):
        with patch("tools.time.sleep") as sleep:
            with self.assertRaises(ValueError):
                with_retry(lambda: (_ for _ in ()).throw(ValueError("bad")))
        sleep.assert_not_called()

    def test_slug_stays_inside_reports(self):
        self.assertEqual(slugify("../../x"), "x")
        self.assertEqual(slugify(""), "topic")
        self.assertLessEqual(len(slugify("a" * 200)), 60)

    def test_citations_count_groups_but_not_code_or_markdown_links(self):
        sources = [{"n": 1, "url": "https://example.org/a"},
                   {"n": 2, "url": "https://example.org/b"}]
        report = ("Facts [1, 2] and `[3]` and [4](https://example.org).\n"
                  "## References\n"
                  "[1] A. https://example.org/a (2026)\n"
                  "[2] B. https://example.org/b (2026)\n")
        self.assertEqual(check(report, sources), [])
        bad = report.replace("https://example.org/b (2026)", "https://example.org/wrong (2026)")
        self.assertTrue(any("URL does not match" in issue for issue in check(bad, sources)))


if __name__ == "__main__":
    unittest.main()
