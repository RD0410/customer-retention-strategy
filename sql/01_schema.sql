-- Verified customer-level table with one row per IBM sample customer.
-- Python handles the blank-to-zero TotalCharges cleaning with an explicit indicator.
CREATE TABLE customers (
    customer_id TEXT PRIMARY KEY,
    gender TEXT NOT NULL,
    senior_citizen INTEGER NOT NULL CHECK(senior_citizen IN (0,1)),
    tenure_months INTEGER NOT NULL,
    tenure_band TEXT NOT NULL,
    contract TEXT NOT NULL,
    internet_service TEXT NOT NULL,
    payment_method TEXT NOT NULL,
    paperless_billing TEXT NOT NULL,
    tech_support TEXT NOT NULL,
    online_security TEXT NOT NULL,
    monthly_charges REAL NOT NULL,
    total_charges REAL NOT NULL,
    churn_flag INTEGER NOT NULL CHECK(churn_flag IN (0,1)),
    total_charges_was_blank INTEGER NOT NULL CHECK(total_charges_was_blank IN (0,1)),
    priority_group TEXT NOT NULL,
    churned_monthly_charges REAL NOT NULL
);
CREATE INDEX idx_customers_contract ON customers(contract);
CREATE INDEX idx_customers_internet ON customers(internet_service);
CREATE INDEX idx_customers_payment ON customers(payment_method);
CREATE INDEX idx_customers_tenure ON customers(tenure_band);
