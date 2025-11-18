#!/usr/bin/env python
# coding: utf-8

"""
MET Department Explorer (Flask UI)
---------------------------------
A lightweight interactive dashboard to browse MET Museum collections
by department, field, and metadata.

Features:
- Department & Field selection
- "ALL" mode for departments without fields
- Optional collapsing of <1% categories
- Full detail table with search & pagination
- Includes artist join + highlight/public domain flags
"""

import os
import sqlite3
import pandas as pd
from flask import Flask, render_template, request
import plotly.express as px
import plotly.io as pio

# =============================================================================
# 0. Configuration
# =============================================================================

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "met.db")

FIELDS = [
    "ALL",
    "classification",
    "culture",
    "country",
    "isHighlight",
    "isPublicDomain",
]

BINARY_FIELDS = ["isHighlight", "isPublicDomain"]


# =============================================================================
# 1. Database Queries
# =============================================================================

def get_departments():
    """Return list of department names (sorted)."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT DISTINCT displayName FROM Department ORDER BY displayName", conn)
    conn.close()
    return df["displayName"].tolist()


def run_group_query(selected_dept, selected_field):
    """Return group counts for chart. Handles ALL mode."""
    # ALL MODE: count objects per classification by default
    if selected_field == "ALL":
        selected_field = "classification"

    query = f"""
        SELECT a.{selected_field} AS category,
               COUNT(*) AS num_objects
        FROM Art a
        JOIN Objects o ON a.object_id = o.object_id
        JOIN Department d ON d.department_id = o.department_id
        WHERE d.displayName = ?
        GROUP BY a.{selected_field}
        ORDER BY num_objects DESC
    """

    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql(query, conn, params=(selected_dept,))
    conn.close()

    # standardize null values
    df["category"] = df["category"].fillna("Unknown")

    # boolean fields to human labels
    if selected_field in BINARY_FIELDS:
        df["category"] = df["category"].map({0: "No", 1: "Yes", None: "Unknown"})

    return df


def run_detail_query(selected_dept):
    """Return detail metadata list for table."""
    query = f"""
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

    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql(query, conn, params=(selected_dept,))
    conn.close()

    df["isHighlight"] = df["isHighlight"].map({0: "No", 1: "Yes", None: "Unknown"})
    df["isPublicDomain"] = df["isPublicDomain"].map({0: "No", 1: "Yes", None: "Unknown"})
    return df


def collapse_small_groups(df, field, cutoff_ratio=0.01):
    """Group small categories into other."""
    cutoff = df["num_objects"].sum() * cutoff_ratio
    df[field] = df.apply(
        lambda row: f"Other {field}" if row["num_objects"] < cutoff else row[field],
        axis=1,
    )
    return df.groupby(field, as_index=False)["num_objects"].sum()


# =============================================================================
# 2. Flask Route
# =============================================================================

@app.route("/", methods=["GET", "POST"])
def index():
    departments = get_departments()
    selected_dept = departments[0]
    selected_field = FIELDS[0]
    collapse_checked = False
    chart_html = ""
    detail_df = pd.DataFrame()

    if request.method == "POST":
        selected_dept = request.form.get("department")
        selected_field = request.form.get("field")
        collapse_checked = request.form.get("collapse") == "on"

        df = run_group_query(selected_dept, selected_field)

        if df.empty:
            chart_html = "<p><b>⚠ No data available for this selection.</b></p>"
        else:
            if collapse_checked:
                df = collapse_small_groups(df, "category")

            fig = px.pie(
                df,
                values="num_objects",
                names="category",
                title=f"{selected_dept} – {selected_field} breakdown"
            )
            chart_html = pio.to_html(fig, full_html=False, include_plotlyjs="cdn")

        detail_df = run_detail_query(selected_dept)

    if detail_df.empty:
        detail_df = pd.DataFrame(columns=[
            "title", "culture", "country", "classification", "artist",
            "isHighlight", "isPublicDomain"
        ])

    return render_template(
        "index.html",
        departments=departments,
        fields=FIELDS,
        selected_dept=selected_dept,
        selected_field=selected_field,
        collapse_checked=collapse_checked,
        chart_html=chart_html,
        detail_df=detail_df
    )


# =============================================================================
# 3. Entry Point
# =============================================================================

if __name__ == "__main__":
    print("\nUsing database:", os.path.abspath(DB_PATH), "\n")
    app.run(debug=True)
