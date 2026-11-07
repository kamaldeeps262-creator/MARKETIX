"""
MARKETIX Database Queries Module
Handles all SQL queries and data persistence operations for PostgreSQL / SQLite.
"""

import pandas as pd
from sqlalchemy import text
from database.connection import get_engine, get_session
import logging

logger = logging.getLogger("marketix.queries")


def log_upload(file_name: str, total_records: int, status: str = "Processed") -> int:
    """Logs dataset upload metadata to database."""
    engine = get_engine()
    if engine is None:
        return -1
    with engine.connect() as conn:
        result = conn.execute(
            text("INSERT INTO dataset_uploads (file_name, total_records, status) VALUES (:fn, :tr, :st)"),
            {"fn": file_name, "tr": total_records, "st": status}
        )
        conn.commit()
        return result.rowcount


def sync_processed_data_to_db(df: pd.DataFrame) -> tuple[bool, str]:
    """
    Synchronizes the cleaned/processed marketing dataset into the relational tables:
    customers, campaigns, and campaign_responses.
    """
    engine = get_engine()
    if engine is None:
        return False, "Database is currently unavailable"

    try:
        with engine.begin() as conn:
            # 1. Populate Campaigns table if empty
            campaign_definitions = [
                (1, "Campaign 1", "Direct Email", "2013-01-01", "2013-02-15"),
                (2, "Campaign 2", "Direct Mail", "2013-03-01", "2013-04-15"),
                (3, "Campaign 3", "Discount Voucher", "2013-05-01", "2013-06-15"),
                (4, "Campaign 4", "Catalog Special", "2013-07-01", "2013-08-15"),
                (5, "Campaign 5", "Premium Club", "2013-09-01", "2013-10-15"),
                (6, "Latest Campaign (Response)", "Integrated Multi-Channel", "2014-01-01", "2014-03-31"),
            ]
            for cid, cname, ctype, sdate, edate in campaign_definitions:
                conn.execute(
                    text("""
                        INSERT INTO campaigns (campaign_id, campaign_name, campaign_type, start_date, end_date)
                        VALUES (:cid, :cname, :ctype, :sdate, :edate)
                        ON CONFLICT (campaign_id) DO UPDATE SET campaign_name = EXCLUDED.campaign_name
                    """ if "PostgreSQL" in str(engine.url) else """
                        INSERT OR REPLACE INTO campaigns (campaign_id, campaign_name, campaign_type, start_date, end_date)
                        VALUES (:cid, :cname, :ctype, :sdate, :edate)
                    """),
                    {"cid": cid, "cname": cname, "ctype": ctype, "sdate": sdate, "edate": edate}
                )

            # 2. Insert or replace customers
            for _, row in df.iterrows():
                cid = int(row["ID"])
                yob = int(row["Year_Birth"]) if "Year_Birth" in row else 1970
                edu = str(row.get("Education", "Graduation"))
                mar = str(row.get("Marital_Status", "Single"))
                inc = float(row["Income"]) if pd.notnull(row.get("Income")) else 0.0
                dt_join = str(row.get("Dt_Customer", "2013-01-01"))
                kid = int(row.get("Kidhome", 0))
                teen = int(row.get("Teenhome", 0))
                rec = int(row.get("Recency", 0))
                mw = float(row.get("MntWines", 0))
                mf = float(row.get("MntFruits", 0))
                mm = float(row.get("MntMeatProducts", 0))
                mfi = float(row.get("MntFishProducts", 0))
                ms = float(row.get("MntSweetProducts", 0))
                mg = float(row.get("MntGoldProds", 0))
                tot_spend = float(row.get("Total_Spending", mw + mf + mm + mfi + ms + mg))
                nd = int(row.get("NumDealsPurchases", 0))
                nw = int(row.get("NumWebPurchases", 0))
                nc = int(row.get("NumCatalogPurchases", 0))
                ns = int(row.get("NumStorePurchases", 0))
                tot_purch = int(row.get("Total_Purchases", nd + nw + nc + ns))
                nwv = int(row.get("NumWebVisitsMonth", 0))
                comp = int(row.get("Complain", 0))

                conn.execute(
                    text("""
                        INSERT INTO customers (
                            customer_id, year_of_birth, education, marital_status, income, date_joined,
                            kidhome, teenhome, recency, mnt_wines, mnt_fruits, mnt_meat, mnt_fish,
                            mnt_sweets, mnt_gold, total_spending, num_deals_purchases, num_web_purchases,
                            num_catalog_purchases, num_store_purchases, total_purchases, num_web_visits_month, complain
                        ) VALUES (
                            :cid, :yob, :edu, :mar, :inc, :dt_join, :kid, :teen, :rec,
                            :mw, :mf, :mm, :mfi, :ms, :mg, :tot_spend, :nd, :nw, :nc, :ns, :tot_purch, :nwv, :comp
                        )
                        ON CONFLICT (customer_id) DO UPDATE SET
                            income = EXCLUDED.income,
                            total_spending = EXCLUDED.total_spending,
                            total_purchases = EXCLUDED.total_purchases
                    """ if "PostgreSQL" in str(engine.url) else """
                        INSERT OR REPLACE INTO customers (
                            customer_id, year_of_birth, education, marital_status, income, date_joined,
                            kidhome, teenhome, recency, mnt_wines, mnt_fruits, mnt_meat, mnt_fish,
                            mnt_sweets, mnt_gold, total_spending, num_deals_purchases, num_web_purchases,
                            num_catalog_purchases, num_store_purchases, total_purchases, num_web_visits_month, complain
                        ) VALUES (
                            :cid, :yob, :edu, :mar, :inc, :dt_join, :kid, :teen, :rec,
                            :mw, :mf, :mm, :mfi, :ms, :mg, :tot_spend, :nd, :nw, :nc, :ns, :tot_purch, :nwv, :comp
                        )
                    """),
                    {
                        "cid": cid, "yob": yob, "edu": edu, "mar": mar, "inc": inc, "dt_join": dt_join,
                        "kid": kid, "teen": teen, "rec": rec, "mw": mw, "mf": mf, "mm": mm, "mfi": mfi,
                        "ms": ms, "mg": mg, "tot_spend": tot_spend, "nd": nd, "nw": nw, "nc": nc,
                        "ns": ns, "tot_purch": tot_purch, "nwv": nwv, "comp": comp
                    }
                )

                # Campaign responses
                cmp_mappings = [
                    (1, bool(row.get("AcceptedCmp1", 0))),
                    (2, bool(row.get("AcceptedCmp2", 0))),
                    (3, bool(row.get("AcceptedCmp3", 0))),
                    (4, bool(row.get("AcceptedCmp4", 0))),
                    (5, bool(row.get("AcceptedCmp5", 0))),
                    (6, bool(row.get("Response", 0))),
                ]
                for camp_id, resp in cmp_mappings:
                    conn.execute(
                        text("""
                            INSERT INTO campaign_responses (customer_id, campaign_id, response, response_date)
                            VALUES (:cid, :camp_id, :resp, :rdate)
                            ON CONFLICT (customer_id, campaign_id) DO UPDATE SET response = EXCLUDED.response
                        """ if "PostgreSQL" in str(engine.url) else """
                            INSERT OR REPLACE INTO campaign_responses (customer_id, campaign_id, response, response_date)
                            VALUES (:cid, :camp_id, :resp, :rdate)
                        """),
                        {"cid": cid, "camp_id": camp_id, "resp": resp, "rdate": dt_join}
                    )

        return True, f"Successfully synchronized {len(df)} customer records and campaign responses to database."
    except Exception as e:
        logger.error(f"Error syncing data to database: {e}")
        return False, str(e)


def get_dashboard_metrics_from_db():
    """Calculates high-level metrics directly from database."""
    engine = get_engine()
    if engine is None:
        return None

    try:
        with engine.connect() as conn:
            total_cust = conn.execute(text("SELECT COUNT(*) FROM customers")).scalar() or 0
            avg_income = conn.execute(text("SELECT AVG(income) FROM customers WHERE income > 0")).scalar() or 0.0
            avg_spending = conn.execute(text("SELECT AVG(total_spending) FROM customers")).scalar() or 0.0
            
            # Response rate on latest campaign (ID 6)
            latest_responses = conn.execute(
                text("SELECT COUNT(*) FROM campaign_responses WHERE campaign_id = 6 AND response = TRUE")
            ).scalar() or 0

            response_rate = (latest_responses / total_cust * 100) if total_cust > 0 else 0.0

            return {
                "total_customers": total_cust,
                "total_campaigns": 5, # Previous 5 campaigns + target
                "positive_responses": latest_responses,
                "response_rate": response_rate,
                "average_income": avg_income,
                "average_spending": avg_spending
            }
    except Exception as e:
        logger.error(f"Error getting metrics from DB: {e}")
        return None


def save_customer_segments_to_db(df_segments: pd.DataFrame) -> tuple[bool, str]:
    """Persists customer segmentation results."""
    engine = get_engine()
    if engine is None:
        return False, "Database offline"

    try:
        with engine.begin() as conn:
            conn.execute(text("DELETE FROM customer_segments"))
            for _, row in df_segments.iterrows():
                conn.execute(
                    text("INSERT INTO customer_segments (customer_id, cluster_number, segment_name) VALUES (:cid, :cn, :sn)"),
                    {"cid": int(row["ID"]), "cn": int(row["Cluster"]), "sn": str(row.get("Segment_Name", f"Segment {row['Cluster']}"))}
                )
        return True, f"Saved segments for {len(df_segments)} customers."
    except Exception as e:
        return False, str(e)


def save_prediction_to_db(customer_id: int, predicted_response: bool, probability: float, model_version: str = "v1.0-logreg"):
    """Saves ML prediction record to database."""
    engine = get_engine()
    if engine is None:
        return False
    try:
        with engine.begin() as conn:
            conn.execute(
                text("""
                    INSERT INTO predictions (customer_id, predicted_response, probability, model_version)
                    VALUES (:cid, :pr, :prob, :mv)
                """),
                {"cid": int(customer_id), "pr": predicted_response, "prob": float(probability), "mv": model_version}
            )
        return True
    except Exception as e:
        logger.error(f"Error saving prediction: {e}")
        return False
