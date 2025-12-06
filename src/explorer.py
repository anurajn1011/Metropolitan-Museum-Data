#!/usr/bin/env python
# coding: utf-8

import sqlite3
import pandas as pd

# Fields available for category breakdown in the Explorer
FIELDS = [
    "classification",
    "culture",
    "country",
    "isHighlight",
    "isPublicDomain",
]

# Fields whose values should be displayed as Yes/No
BINARY_FIELDS = ["isHighlight", "isPublicDomain"]


# ================================================================
# Load departments
# ================================================================
def get_departments(db_path):
    """Return a list of all departments, with an 'ALL' option prepended."""
    conn = sqlite3.connect(db_path)
    df = pd.read_sql(
        "SELECT DISTINCT displayName FROM Department ORDER BY displayName;",
        conn,
    )
    conn.close()

    departments = df["displayName"].tolist()
    departments.insert(0, "ALL")
    return departments


# ================================================================
# Summary table for Explorer chart
# ================================================================
def run_group_query(db_path, selected_dept, selected_field):
    """Return grouped counts for building the Explorer chart."""

    if selected_dept == "ALL":
        query = f"""
            SELECT 
                a.{selected_field} AS category,
                COUNT(*) AS num_objects
            FROM Art a
            JOIN Objects o ON a.object_id = o.object_id
            GROUP BY a.{selected_field}
            ORDER BY num_objects DESC
        """
        params = ()
    else:
        query = f"""
            SELECT 
                a.{selected_field} AS category,
                COUNT(*) AS num_objects
            FROM Art a
            JOIN Objects o ON a.object_id = o.object_id
            JOIN Department d ON d.department_id = o.department_id
            WHERE d.displayName = ?
            GROUP BY a.{selected_field}
            ORDER BY num_objects DESC
        """
        params = (selected_dept,)

    conn = sqlite3.connect(db_path)
    df = pd.read_sql(query, conn, params=params)
    conn.close()

    df["category"] = df["category"].fillna("Unknown")

    if selected_field in BINARY_FIELDS:
        df["category"] = df["category"].map({0: "No", 1: "Yes"}).fillna("Unknown")

    return df


# ================================================================
# Detail table for Explorer
# ================================================================
def run_detail_query(db_path, selected_dept):
    """Return detailed metadata records for the Explorer table."""

    if selected_dept == "ALL":
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
            LEFT JOIN Artists ar ON a.artistAlphaSort = ar.artistAlphaSort
        """
        params = ()
    else:
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
        params = (selected_dept,)

    conn = sqlite3.connect(db_path)
    df = pd.read_sql(query, conn, params=params)
    conn.close()

    df["isHighlight"] = df["isHighlight"].map({0: "No", 1: "Yes"}).fillna("Unknown")
    df["isPublicDomain"] = df["isPublicDomain"].map({0: "No", 1: "Yes"}).fillna("Unknown")

    return df


# ================================================================
# Collapse small groups into "Other"
# ================================================================
def collapse_small_groups(df, field, cutoff_ratio=0.01):
    """Collapse groups under <cutoff_ratio of total into 'Other <field>'."""
    cutoff = df["num_objects"].sum() * cutoff_ratio

    df[field] = df.apply(
        lambda row: f"Other {field}" if row["num_objects"] < cutoff else row[field],
        axis=1,
    )

    return df.groupby(field, as_index=False)["num_objects"].sum()
