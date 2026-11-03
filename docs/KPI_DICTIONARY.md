# KPI dictionary

| KPI | Formula / definition | Caveats |
|---|---|---|
| Customers | `COUNT(DISTINCT customer_id)` | One row per sample customer |
| Churn labels | `SUM(churn_flag)` where `Yes` = 1 | Historical, not forecast |
| Observed churn rate | `SUM(churn_flag) / COUNT(*)` within group | Cross-sectional rate; not causal |
| Total monthly charges | `SUM(monthly_charges)` | Customer charges, not financial-statement revenue |
| Churner monthly charges | `SUM(monthly_charges)` only where churn flag = 1 | Exposure proxy, not booked realized loss |
| Tenure cohort | `0–11`, `12–23`, `24–47`, `48+` months | Thresholds are analytical choices |
| Priority A | Month-to-month + fiber optic | Segmentation hypothesis, not risk prediction |
| Priority B | Month-to-month + non-fiber | Segmentation hypothesis |
| Priority C | One- or two-year contract | Segmentation hypothesis |
| Model contact count | `cohort customers × contact coverage` | A proposed outreach volume |
| Model avoided churn count | `cohort churned × coverage × assumed prevention` | Hypothetical, potentially fractional expectation |
| Model gross retained charges | `churner monthly charges × coverage × assumed prevention × months` | Assumes stable charges and coverage |
| Model program costs | `contact count × unit contact cost + avoided churn × unit incentive` | Omits implementation/other overhead |
| Model net value | `model gross − model program costs` | Illustrative only; not actual ROI |

Data lineage: IBM sample CSV → `src/pipeline.py` normalization → `data/processed/customer_retention.db` / `tableau/*.csv` → dashboards.
