import unittest
from src.pipeline import normalize_row, group_summary, tenure_band, priority_group

BASE = {
    "customerID": "0001-TEST1", "gender": "Female", "SeniorCitizen": "0",
    "tenure": "0", "PhoneService": "Yes", "MultipleLines": "No",
    "InternetService": "Fiber optic", "OnlineSecurity": "No", "OnlineBackup": "No",
    "DeviceProtection": "No", "TechSupport": "No", "StreamingTV": "No",
    "StreamingMovies": "No", "Contract": "Month-to-month",
    "PaperlessBilling": "Yes", "PaymentMethod": "Electronic check",
    "MonthlyCharges": "90.25", "TotalCharges": " ", "Churn": "Yes",
}

class PipelineTests(unittest.TestCase):
    def test_clean_zero_tenure_missing_total(self):
        row = normalize_row(BASE)
        self.assertEqual(row["total_charges"], 0.0)
        self.assertEqual(row["total_charges_was_blank"], 1)
        self.assertEqual(row["churn_flag"], 1)
        self.assertEqual(row["churned_monthly_charges"], 90.25)

    def test_missing_total_with_positive_tenure_rejected(self):
        with self.assertRaises(ValueError):
            normalize_row({**BASE, "tenure": "3"})

    def test_cohorts_are_exhaustive(self):
        self.assertEqual([tenure_band(n) for n in [0, 11, 12, 23, 24, 47, 48, 72]],
                         ["0–11 months", "0–11 months", "12–23 months", "12–23 months", "24–47 months", "24–47 months", "48+ months", "48+ months"])

    def test_segment_rates_use_correct_denominators(self):
        a = normalize_row(BASE)
        b = normalize_row({**BASE,"customerID":"0002-TEST2","Churn":"No","MonthlyCharges":"50","TotalCharges":"150","tenure":"3"})
        s = group_summary([a,b], ("contract",))[0]
        self.assertEqual((s["customers"], s["churned"]), (2,1))
        self.assertEqual(s["churn_rate"], 0.5)
        self.assertEqual(s["churned_monthly_charges"], 90.25)

    def test_priority_is_rule_based_not_a_model(self):
        r = normalize_row(BASE)
        self.assertEqual(priority_group(r), "Priority A · flexible fiber")

if __name__ == "__main__":
    unittest.main()
