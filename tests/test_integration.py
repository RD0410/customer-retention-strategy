import csv
import sqlite3
import tempfile
import unittest
from pathlib import Path
from src.pipeline import run
from tests.test_pipeline import BASE

class IntegrationTests(unittest.TestCase):
    def test_sql_and_exports_reconcile_with_fixture(self):
        columns=list(BASE)
        rows=[BASE,{**BASE,'customerID':'0002-TEST2','Churn':'No','TotalCharges':'180','tenure':'2'}]
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            fixture=root/'input.csv'
            with fixture.open('w',newline='',encoding='utf8') as f:
                w=csv.DictWriter(f,fieldnames=columns);w.writeheader();w.writerows(rows)
            snapshot=run(source=fixture,output=root/'output',tableau_dir=root/'tableau')
            self.assertEqual(snapshot['observed_customers'],2)
            self.assertEqual(snapshot['observed_churned'],1)
            self.assertTrue((root/'tableau/contract_internet_summary.csv').is_file())
            with sqlite3.connect(root/'output/customer_retention.db') as db:
                self.assertEqual(db.execute('SELECT COUNT(*) FROM customers').fetchone()[0],2)
                self.assertEqual(db.execute('SELECT churned FROM v_retention_priorities').fetchone()[0],1)
                self.assertEqual(db.execute('SELECT COUNT(*) FROM v_contract_internet_matrix').fetchone()[0],1)

if __name__=='__main__':
    unittest.main()
