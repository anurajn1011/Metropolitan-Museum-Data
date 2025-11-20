#!/usr/bin/env python
# coding: utf-8

import sqlite3
import pandas as pd

# ================================================================
# Configuration
# ================================================================
FIELDS = [
    "ALL",
    "classification",
    "culture",
    "country",
    "isHighlight",
    "isPublicDomain",
]

BINARY_FIELDS = ["isHighlight", "isPublicDomain"]


# ================================================================
def get_departments(db_path):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql(
        "SELECT DISTINCT displayName FROM Department ORDER BY displayName;",
        conn,
    )
    conn.close()
    return df["displayName"].tolist()


# ================================================================
def run_group_query(db_path, selected_dept, selected_field):
    # ALL → fallback to classification
    actual_field = "classification" if selected_field == "ALL" else selected_field

    query = f"""
        SELECT a.{actual_field} AS category,
               COUNT(*) AS num_objects
        FROM Art a
        JOIN Objects o ON a.object_id = o.object_id
        JOIN Department d ON d.department_id = o.department_id
        WHERE d.displayName = ?
        GROUP BY a.{actual_field}
        ORDER BY num_objects DESC
    """

    conn = sqlite3.connect(db_path)
    df = pd.read_sql(query, conn, params=(selected_dept,))
    conn.close()

    df["category"] = df["category"].fillna("Unknown")

    if actual_field in BINARY_FIELDS:
        df["category"] = df["category"].map({0: "No", 1: "Yes"}).fillna("Unknown")

    return df


# ================================================================
def run_detail_query(db_path, selected_dept):
    query = """
        SELECT 
            a.title,
            a.culture,
            a.country,
            a.classification,
            COALESCE(ar.artist_name, 'Unknown') AS artist,
            a.isHighlight,
            a.isPublicDomain
        FROM Art a
        JOIN Objects o ON a.object_id = o.object_id
        JOIN Department d ON d.department_id = o.department_id
        LEFT JOIN Artists ar ON a.artistAlphaSort = ar.artistAlphaSort
        WHERE d.displayName = ?
    """

    conn = sqlite3.connect(db_path)
    df = pd.read_sql(query, conn, params=(selected_dept,))
    conn.close()

    df["isHighlight"] = df["isHighlight"].map({0: "No", 1: "Yes"}).fillna("Unknown")
    df["isPublicDomain"] = df["isPublicDomain"].map({0: "No", 1: "Yes"}).fillna("Unknown")

    return df


# ================================================================
def collapse_small_groups(df, field, cutoff_ratio=0.01):
    cutoff = df["num_objects"].sum() * cutoff_ratio
    df[field] = df.apply(
        lambda row: f"Other {field}" if row["num_objects"] < cutoff else row[field],
        axis=1,
    )
    return df.groupby(field, as_index=False)["num_objects"].sum()
