# Dataset, licensing and reproduction

**Publisher:** IBM, Telco Customer Churn educational sample (fictional telecommunications company).

- Repository: https://github.com/IBM/telco-customer-churn-on-icp4d
- CSV: https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv
- IBM description: https://www.ibm.com/docs/en/cognos-analytics/12.0.x?topic=samples-telco-customer-churn
- Code pattern license: https://github.com/IBM/telco-customer-churn-on-icp4d/blob/master/LICENSE
- Expected SHA-256: `16320c9c1ec72448db59aa0a26a0b95401046bef5d02fd3aeb906448e3055e91`

## Columns of interest
`customerID`, `tenure`, `Contract`, `InternetService`, `PaymentMethod`, `MonthlyCharges`, `TotalCharges`, `Churn`, `TechSupport`, `OnlineSecurity`, `PaperlessBilling`, `SeniorCitizen`, `gender`.

## Cleaning decisions
- Source `TotalCharges` includes 11 blanks for zero-tenure customers. Convert blank to `0.0` **only for tenure 0**, and retain `total_charges_was_blank` to make this transformation auditable.
- Reject blank IDs, duplicate IDs, invalid churn labels, or negative monetary values.
- Preserve the original `MonthlyCharges` values. Compute charge exposures from original customer charges.
- Create explicit tenure cohorts and an interpretable business-priority grouping.

## Reproducibility
The raw CSV is intentionally not bundled. Run `python3 -m src.pipeline` from project root to download, checksum-verify, clean, and generate reproducible data assets. The prebuilt aggregated JSON and Tableau CSV extracts are included so visualizations can be explored without first downloading the individual-level data.

## Ethical/statistical note
IBM describes these as fictional customer records. No personally identifying real subscriber information is implied, and no causal claim is supported by a cross-sectional observational dataset.
