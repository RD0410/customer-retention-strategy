# Business case | Retention priority and measurable pilots

## Executive question
Where should a fictional subscription telecom operator investigate churn and pilot retention interventions, given a one-time customer snapshot with churn labels, contract terms, service type, tenure, and monthly charges?

## Scope
- **Population:** 7,043 customer records in IBM's educational sample.
- **Decision:** allocate discovery and experiment effort, not automate customer targeting.
- **Outputs:** cohort metrics, charge exposure proxies, suggested priority segments, transparent what-if financial model.
- **Exclusions:** customer lifetime value (not available), true retention uplift, customer satisfaction (not available), causal findings, predicted probability of individual churn, time-series trend (no observation date field).

## Business questions
1. Which contract terms and service tiers show elevated historical churn?
2. Which segments represent the greatest monthly-charge exposure among churn-labeled records?
3. Does tenure suggest a useful onboarding hypothesis?
4. How sensitive is a hypothetical pilot's economics to outreach cost and assumed prevention effectiveness?
5. What extra data must be collected before adopting a policy?

## Evidence from this source

| Segment | Customers | Churned | Observed rate | Churner monthly charges |
|---|---:|---:|---:|---:|
| Month-to-month | 3,875 | 1,655 | 42.71% | $120,847.10 |
| One year | 1,473 | 166 | 11.27% | $14,118.45 |
| Two year | 1,695 | 48 | 2.83% | $4,165.30 |
| Month-to-month + fiber | 2,128 | 1,162 | 54.61% | $100,482.00 |
| Tenure 0–11 months | 2,069 | 999 | 48.28% | $66,022.30 |

## Suggested pilot design
A product/service-quality team should investigate the experience of flexible-contract fiber customers, including onboarding friction, service tickets, satisfaction, and billing issues. If feasible, randomize eligible *current* customers into treatment and control, carefully defining eligibility without using historical churn labels as future outcomes. Define a primary outcome such as incremental 90-day retention, and secondary outcomes such as net contribution, repeat complaints, and intervention cost.

## Assumptions and caveats
- Historical churn labels may reflect selection effects; comparisons are not causal.
- The source represents a fictional company and is unsuitable for real-world investment claims.
- The charge exposure measure is *not* revenue loss or future revenue by itself.
- Segment labels A/B/C are explicit business rules, not a trained prediction model.
- Revenue scenarios are sensitivity analyses, not verified uplift or actual savings.

## Stakeholder acceptance criteria
- Source totals reconcile to 7,043 customers and 1,869 churned.
- Every KPI states the numerator, denominator, unit, and limitations.
- Dashboard cohort filters preserve correct denominators.
- Scenario model responds to user inputs and outputs are labeled hypothetical.
- Recommendations distinguish observational evidence from experiments needed.
