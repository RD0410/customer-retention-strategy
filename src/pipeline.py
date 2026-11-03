"""Reproducible analysis pipeline for the IBM Telco Customer Churn sample.

Usage:
  python3 -m src.pipeline
  python3 -m src.pipeline --source /path/to/Telco-Customer-Churn.csv
  python3 -m src.pipeline --no-download  # after first run

The project intentionally uses the Python standard library only.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sqlite3
from collections import defaultdict
from pathlib import Path
from urllib.request import urlopen, Request

ROOT = Path(__file__).resolve().parents[1]
DATA_URL = (
    "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/"
    "master/data/Telco-Customer-Churn.csv"
)
DATA_SHA256 = "16320c9c1ec72448db59aa0a26a0b95401046bef5d02fd3aeb906448e3055e91"
RAW_PATH = ROOT / "data/raw/telco_customer_churn.csv"
OUT = ROOT / "data/processed"
TABLEAU = ROOT / "tableau"


def download_raw(path: Path = RAW_PATH) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        check_sha(path)
        return path
    req = Request(DATA_URL, headers={"User-Agent": "portfolio-data-analysis/1.0"})
    with urlopen(req, timeout=45) as response:
        blob = response.read()
    digest = hashlib.sha256(blob).hexdigest()
    if digest != DATA_SHA256:
        raise ValueError(f"Unexpected source file hash: {digest}. Source dataset may have changed.")
    path.write_bytes(blob)
    return path


def check_sha(path: Path) -> None:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != DATA_SHA256:
        raise ValueError(f"Raw dataset checksum mismatch: {path} ({digest})")


def tenure_band(months: int) -> str:
    if months < 12:
        return "0–11 months"
    if months < 24:
        return "12–23 months"
    if months < 48:
        return "24–47 months"
    return "48+ months"


def priority_group(record: dict) -> str:
    """Transparent business rule, NOT an individualized churn probability."""
    if record["contract"] == "Month-to-month" and record["internet_service"] == "Fiber optic":
        return "Priority A · flexible fiber"
    if record["contract"] == "Month-to-month":
        return "Priority B · other flexible"
    return "Priority C · longer contract"


def normalize_row(row: dict) -> dict:
    customer_id = row["customerID"].strip()
    if not customer_id:
        raise ValueError("Missing customer ID")
    churn = row["Churn"].strip()
    if churn not in {"Yes", "No"}:
        raise ValueError(f"Unexpected churn label for customer {customer_id}: {churn}")
    tenure = int(row["tenure"])
    monthly = float(row["MonthlyCharges"])
    total_str = row["TotalCharges"].strip()
    if not total_str and tenure != 0:
        raise ValueError(f"Unexpected blank total charges for customer {customer_id}")
    total = float(total_str) if total_str else 0.0
    if not 0 <= tenure <= 72 or monthly < 0 or total < 0:
        raise ValueError(f"Invalid monetary or tenure values for customer {customer_id}")
    record = {
        "customer_id": customer_id,
        "gender": row["gender"].strip(),
        "senior_citizen": int(row["SeniorCitizen"]),
        "tenure_months": tenure,
        "tenure_band": tenure_band(tenure),
        "contract": row["Contract"].strip(),
        "internet_service": row["InternetService"].strip(),
        "payment_method": row["PaymentMethod"].strip(),
        "paperless_billing": row["PaperlessBilling"].strip(),
        "tech_support": row["TechSupport"].strip(),
        "online_security": row["OnlineSecurity"].strip(),
        "monthly_charges": round(monthly, 2),
        "total_charges": round(total, 2),
        "churn_flag": int(churn == "Yes"),
        "total_charges_was_blank": int(not total_str),
    }
    record["priority_group"] = priority_group(record)
    record["churned_monthly_charges"] = round(monthly if record["churn_flag"] else 0.0, 2)
    return record


def load_clean(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        required = {"customerID", "tenure", "MonthlyCharges", "TotalCharges", "Churn", "Contract", "InternetService", "PaymentMethod", "gender", "SeniorCitizen", "PaperlessBilling", "TechSupport", "OnlineSecurity"}
        if not required.issubset(reader.fieldnames or ()):
            raise ValueError(f"Missing columns: {sorted(required - set(reader.fieldnames or []))}")
        result = [normalize_row(r) for r in reader]
    ids = [r["customer_id"] for r in result]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate customer IDs detected")
    if not result:
        raise ValueError("Source CSV is empty")
    return result


def group_summary(records: list[dict], dimensions: tuple[str, ...]) -> list[dict]:
    grouped = defaultdict(lambda: {"customers": 0, "churned": 0, "monthly_charges": 0.0, "churned_monthly_charges": 0.0})
    for r in records:
        key = tuple(r[c] for c in dimensions)
        s = grouped[key]
        s["customers"] += 1
        s["churned"] += r["churn_flag"]
        s["monthly_charges"] += r["monthly_charges"]
        s["churned_monthly_charges"] += r["churned_monthly_charges"]
    results = []
    for key, s in grouped.items():
        results.append({
            **dict(zip(dimensions, key)),
            "customers": s["customers"],
            "churned": s["churned"],
            "retained": s["customers"] - s["churned"],
            "churn_rate": round(s["churned"] / s["customers"], 8),
            "monthly_charges": round(s["monthly_charges"], 2),
            "churned_monthly_charges": round(s["churned_monthly_charges"], 2),
            "avg_monthly_charge_churned": round(s["churned_monthly_charges"] / s["churned"], 2) if s["churned"] else 0.0,
        })
    return sorted(results, key=lambda r: tuple(str(r[c]) for c in dimensions))


def write_csv(path: Path, data: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not data:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(data[0]))
        writer.writeheader()
        writer.writerows(data)


def make_database(records: list[dict], db_path: Path, tableau_dir: Path = TABLEAU) -> None:
    if db_path.exists():
        db_path.unlink()
    with sqlite3.connect(db_path) as conn:
        schema = (ROOT / "sql/01_schema.sql").read_text(encoding="utf-8")
        queries = (ROOT / "sql/02_views.sql").read_text(encoding="utf-8")
        conn.executescript(schema)
        cols = list(records[0])
        conn.executemany(
            "INSERT INTO customers (" + ",".join(cols) + ") VALUES (" + ",".join("?" for _ in cols) + ")",
            [tuple(r[c] for c in cols) for r in records]
        )
        conn.executescript(queries)
        for view, file in [
            ("v_contract_performance", "contract_performance.csv"),
            ("v_internet_performance", "internet_performance.csv"),
            ("v_retention_priorities", "retention_priorities.csv"),
            ("v_contract_internet_matrix", "contract_internet_matrix.csv"),
        ]:
            cursor = conn.execute(f"SELECT * FROM {view}")
            fields = [d[0] for d in cursor.description]
            write_csv(tableau_dir / file, [dict(zip(fields, row)) for row in cursor.fetchall()])


def run(source: Path | None = None, download: bool = True, output: Path = OUT, tableau_dir: Path = TABLEAU) -> dict:
    raw = source or RAW_PATH
    if source is None and download:
        raw = download_raw(raw)
    elif not raw.exists():
        raise FileNotFoundError(f"No CSV at {raw}. Run without --no-download or use --source.")
    if source is None:
        check_sha(raw)
    records = load_clean(raw)
    output.mkdir(parents=True, exist_ok=True)
    tableau_dir.mkdir(parents=True, exist_ok=True)
    write_csv(output / "clean_customers.csv", records)
    by = {
        "contract": group_summary(records, ("contract",)),
        "internet": group_summary(records, ("internet_service",)),
        "tenure": group_summary(records, ("tenure_band",)),
        "payment": group_summary(records, ("payment_method",)),
        "priority": group_summary(records, ("priority_group",)),
        "contract_internet": group_summary(records, ("contract", "internet_service")),
    }
    n = len(records)
    churned = sum(r["churn_flag"] for r in records)
    snapshot = {
        "dataset": "IBM Telco Customer Churn · fictional sample",
        "observed_customers": n,
        "observed_churned": churned,
        "observed_churn_rate": round(churned / n, 8),
        "sum_monthly_charges": round(sum(r["monthly_charges"] for r in records), 2),
        "churned_monthly_charges": round(sum(r["churned_monthly_charges"] for r in records), 2),
        "blank_total_charges_cleaned": sum(r["total_charges_was_blank"] for r in records),
        "by": by,
    }
    (output / "analysis_snapshot.json").write_text(json.dumps(snapshot, indent=2, ensure_ascii=False), encoding="utf-8")
    for name, items in by.items():
        write_csv(tableau_dir / f"{name}_summary.csv", items)
    make_database(records, output / "customer_retention.db", tableau_dir)
    print(f"Validated {n:,} customers; {churned:,} historical churn labels; snapshot written to {output}")
    return snapshot


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, help="Path to an existing local copy of the IBM CSV")
    parser.add_argument("--no-download", action="store_true", help="Use existing data/raw/telco_customer_churn.csv")
    args = parser.parse_args()
    run(source=args.source, download=not args.no_download)


if __name__ == "__main__":
    main()
