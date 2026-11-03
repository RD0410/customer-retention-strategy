# Validation checklist

## Dataset checks
- 7,043 unique customer IDs; 1,869 historical churn labels.
- 11 blank `TotalCharges` values occur at tenure 0 and become 0 after cleaning with a flag retained.
- Total sample monthly charges: **$456,116.60**.
- Monthly charges for churn-labeled customers: **$139,130.85**.
- Contract, internet, payment, and tenure group totals each reconcile to the overall population.
- Contract × internet matrix contains nine combinations; counts and charges reconcile.

## Formula checks
- Workbook Dashboard uses formulas pointing to `Segment Metrics`, not manually typed KPI totals.
- Workbook churn rates use `churned / customers` at the correct cohort granularity.
- Scenario Planner cohort lookup is formula-driven using the editable cohort dropdown.
- Scenario values change with coverage, prevention assumption, unit costs, and horizon.
- Excel formulas are not evidence of causal campaign results.

## Local tests
```bash
python3 -m unittest discover -s tests -v
```

The shipped tests exercise cleaning safeguards, tenure bins, segmentation rate denominators, source-summary reconciliation, and priority-group rules. Run the full pipeline with network access to independently regenerate the IBM totals.
