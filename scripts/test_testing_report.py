"""Regression checks for all-seeds verdicts and unavailable human evidence."""
import unittest
from report_testing import run_log


class VerdictTests(unittest.TestCase):
    def test_one_failed_seed_cannot_pass_on_average(self):
        runs = [dict(seed=seed, accuracy=acc, per_label={'x': {'f1': .9}},
                     confidence={'accuracy_most_confident_third': 1.0})
                for seed, acc in zip((42, 7, 2024), (.9, .74, .9))]
        report = run_log(runs)
        accuracy_row = next(row for row in report.splitlines() if '1. Overall' in row)
        self.assertIn('MISSED', accuracy_row)
        audit_row = next(row for row in report.splitlines() if '4. Independent' in row)
        self.assertIn('PENDING', audit_row)

    def test_incomplete_trials_remain_pending(self):
        report = run_log([])
        self.assertNotIn('| MET |', report)
        self.assertEqual(report.count('| PENDING |'), 5)


if __name__ == '__main__':
    unittest.main()
