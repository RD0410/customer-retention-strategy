# Tableau Public build guide | Retention strategy dashboard

These CSVs are **real Tableau-ready data extracts**. They are not screenshots and do not depend on an existing `.twbx`. The final native Tableau workbook is created and verified in Tableau Desktop / Tableau Public by the analyst.

## Data sources

For the broad business dashboard, import `tableau/contract_internet_summary.csv`, `tableau/contract_summary.csv`, and `tableau/tenure_summary.csv`, each as a separate data source. The included files contain verified aggregate data and can be used immediately.

For independent row-level filtering across dimensions, run `python3 -m src.pipeline` and import `data/processed/clean_customers.csv` as the principal data source. A single customer-level data source is preferable for linked filters and a correct consolidated KPI view.

## Core calculated fields (row-level source)

**Churn Count**
```tableau
SUM([churn_flag])
```

**Customers**
```tableau
COUNTD([customer_id])
```

**Historical Churn Rate**
```tableau
SUM([churn_flag]) / COUNTD([customer_id])
```

**Historical Churner Monthly Charges**
```tableau
SUM([churned_monthly_charges])
```

**Historical rate difference vs overall sample**
```tableau
SUM([churn_flag]) / COUNTD([customer_id]) - 1869.0 / 7043.0
```
Use the explicit benchmark only for the unmodified IBM sample, or create a reference calculated measure for a different source.

## Recommended original dashboard layout

**Canvas:** approximately 1360 × 860, automatic fit for presentation. Use a single restrained accent color; use a distinct alert color for high observed churn. Avoid copying third-party screenshot designs.

1. **Header:** `Customer Retention Strategy` and a sentence explaining the dataset and decision.
2. **KPI row:** distinct customers, historical churn rate, churn-labeled customer charges, total monthly charges.
3. **Contract chart:** contract type on rows, observed churn rate on columns; use labels plus customer counts in tooltip.
4. **Service chart:** service type versus observed churn rate; avoid treating service as a causal driver.
5. **Tenure chart:** tenure band versus observed churn rate, sorted in logical duration order.
6. **Contract × service heatmap:** contract on rows, internet service on columns, churn percentage on color and label. Show cohort count in tooltip.
7. **Segment exposure chart:** business-priority tier against churner monthly charges. Label this as exposure proxy.
8. **Filter sidebar:** contract, internet service, tenure band; apply to relevant worksheets.
9. **Footnote:** IBM fictional sample, observational findings, no predictive or causal claims.

## Recommended colors
- Charcoal / navy labels: `#112438`
- Optional teal accent: `#15A58F`
- High observed churn alert: `#D65C51`
- Background: `#F4F7FA`

Colors are presentation choices and may be changed freely. The original contribution is the coherent business question, reproducible calculations, design decisions, and documented limitations — not a palette swap.

## Validate before publishing
- Overall customer count = 7,043.
- Overall observed churn labels = 1,869 (26.54%).
- Month-to-month + fiber = 2,128 customers, 1,162 churn labels, **54.61%** churn.
- Monthly charges for churn-labeled records = $139,130.85.
- Check that Tableau row-level filters do not change the definition of the denominator unexpectedly.
- Tableau Public is public: do not publish proprietary or sensitive customer data. This particular educational dataset is fictional and publicly available.

If you publish your workbook, add its actual Tableau Public link and a validated screenshot to the README; do not describe a planned visualization as already published.
