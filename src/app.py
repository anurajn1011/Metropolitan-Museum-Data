#!/usr/bin/env python
# coding: utf-8

import os
from flask import Flask, render_template, request
import plotly.express as px
import plotly.io as pio
import pandas as pd

from explorer import (
    FIELDS,
    get_departments,
    run_group_query,
    run_detail_query,
    collapse_small_groups
)

from eda_cloisters import run_eda

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "met.db")


# ================================================================
# Main Page
# ================================================================
@app.route("/", methods=["GET", "POST"])
def index():
    departments = get_departments(DB_PATH)

    selected_dept = departments[0]
    selected_field = FIELDS[0]
    collapse_checked = False
    chart_html = ""
    detail_df = pd.DataFrame()

    if request.method == "POST":
        selected_dept = request.form.get("department", selected_dept)
        selected_field = request.form.get("field", selected_field)
        collapse_checked = request.form.get("collapse") == "on"

        df = run_group_query(DB_PATH, selected_dept, selected_field)

        if df.empty:
            chart_html = "<p><b>No matching data for this selection.</b></p>"
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

        detail_df = run_detail_query(DB_PATH, selected_dept)

    if detail_df.empty:
        detail_df = pd.DataFrame(columns=[
            "title", "culture", "country",
            "classification", "artist",
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


# ================================================================
# Cloisters EDA Page
# ================================================================
@app.route("/eda")
def eda_page():
    heatmap_html, sankey_html = run_eda(DB_PATH)
    return render_template(
        "eda.html",
        heatmap_html=heatmap_html,
        sankey_html=sankey_html
    )


if __name__ == "__main__":
    app.run()
