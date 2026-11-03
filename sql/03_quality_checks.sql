-- Expected results for the unmodified IBM source: 7043 customers, 1869 churned,
-- 11 zero-tenure customers with missing TotalCharges populated as zero.
SELECT 'row_count' AS check_name, COUNT(*) AS actual FROM customers;
SELECT 'unique_ids' AS check_name, COUNT(DISTINCT customer_id) AS actual FROM customers;
SELECT 'historical_churned' AS check_name, SUM(churn_flag) AS actual FROM customers;
SELECT 'missing_total_charges_cleaned' AS check_name,
       SUM(total_charges_was_blank) AS actual FROM customers;
SELECT 'invalid_flags' AS check_name, COUNT(*) AS actual FROM customers
WHERE churn_flag NOT IN (0,1) OR total_charges_was_blank NOT IN (0,1);
SELECT 'negative_amounts' AS check_name, COUNT(*) AS actual FROM customers
WHERE monthly_charges < 0 OR total_charges < 0;
SELECT 'charge_exposure_reconciliation' AS check_name,
       ROUND(SUM(CASE WHEN churn_flag=1 THEN monthly_charges ELSE 0 END)
             - SUM(churned_monthly_charges),2) AS actual FROM customers;
