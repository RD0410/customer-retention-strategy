-- These views are intended for stakeholders and direct Tableau import.
-- Observed churned monthly charges is a descriptive exposure proxy, not booked revenue lost.
CREATE VIEW v_contract_performance AS
SELECT contract,
       COUNT(*) AS customers,
       SUM(churn_flag) AS churned,
       ROUND(100.0 * SUM(churn_flag) / COUNT(*), 2) AS churn_rate_pct,
       ROUND(SUM(monthly_charges), 2) AS monthly_charges,
       ROUND(SUM(churned_monthly_charges), 2) AS churned_monthly_charges
FROM customers GROUP BY contract ORDER BY churn_rate_pct DESC;

CREATE VIEW v_internet_performance AS
SELECT internet_service,
       COUNT(*) AS customers,
       SUM(churn_flag) AS churned,
       ROUND(100.0 * SUM(churn_flag) / COUNT(*), 2) AS churn_rate_pct,
       ROUND(SUM(monthly_charges), 2) AS monthly_charges,
       ROUND(SUM(churned_monthly_charges), 2) AS churned_monthly_charges
FROM customers GROUP BY internet_service ORDER BY churn_rate_pct DESC;

CREATE VIEW v_contract_internet_matrix AS
SELECT contract, internet_service, COUNT(*) AS customers,
       SUM(churn_flag) AS churned,
       ROUND(100.0 * SUM(churn_flag) / COUNT(*), 2) AS churn_rate_pct,
       ROUND(SUM(churned_monthly_charges), 2) AS churned_monthly_charges
FROM customers GROUP BY contract, internet_service
ORDER BY CASE contract WHEN 'Month-to-month' THEN 1 WHEN 'One year' THEN 2 ELSE 3 END,
         internet_service;

CREATE VIEW v_retention_priorities AS
SELECT priority_group, COUNT(*) AS customers,
       SUM(churn_flag) AS churned,
       ROUND(100.0 * SUM(churn_flag) / COUNT(*), 2) AS churn_rate_pct,
       ROUND(SUM(churned_monthly_charges), 2) AS churned_monthly_charges
FROM customers GROUP BY priority_group ORDER BY churn_rate_pct DESC;

CREATE VIEW v_tenure_cohorts AS
SELECT tenure_band, COUNT(*) AS customers,
       SUM(churn_flag) AS churned,
       ROUND(100.0 * SUM(churn_flag) / COUNT(*), 2) AS churn_rate_pct
FROM customers GROUP BY tenure_band;

CREATE VIEW v_payment_methods AS
SELECT payment_method, COUNT(*) AS customers,
       SUM(churn_flag) AS churned,
       ROUND(100.0 * SUM(churn_flag) / COUNT(*), 2) AS churn_rate_pct
FROM customers GROUP BY payment_method;
