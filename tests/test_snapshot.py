import json
import unittest
from pathlib import Path

SNAPSHOT_PATH = Path(__file__).resolve().parents[1] / "data/processed/analysis_snapshot.json"

class SnapshotReconciliationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s = json.loads(SNAPSHOT_PATH.read_text(encoding="utf8"))

    def test_source_totals(self):
        self.assertEqual(self.s['observed_customers'], 7043)
        self.assertEqual(self.s['observed_churned'], 1869)
        self.assertAlmostEqual(self.s['churned_monthly_charges'], 139130.85, places=2)

    def test_each_dimension_reconciles(self):
        for dimension in ['contract','internet','tenure','payment','priority','contract_internet']:
            rows = self.s['by'][dimension]
            with self.subTest(dimension=dimension):
                self.assertEqual(sum(r['customers'] for r in rows), 7043)
                self.assertEqual(sum(r['churned'] for r in rows), 1869)
                self.assertAlmostEqual(sum(r['churned_monthly_charges'] for r in rows), 139130.85, places=2)

    def test_priority_segment_definition(self):
        a = next(r for r in self.s['by']['priority'] if r['priority_group'].startswith('Priority A'))
        f = next(r for r in self.s['by']['contract_internet'] if r['contract']=='Month-to-month' and r['internet_service']=='Fiber optic')
        self.assertEqual((a['customers'], a['churned']), (f['customers'], f['churned']))

if __name__=='__main__':
    unittest.main()
