#!/usr/bin/env python
# coding: utf-8

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import io
import base64

sns.set_theme(style="whitegrid", font_scale=1.2)


# =============================================================================
# 1. Load Database
# =============================================================================
def load_db(db_path):
    """Load Art + Objects + Department tables and filter to Cloisters."""
    conn = sqlite3.connect(db_path)
    query = """
        SELECT 
            Art.*,
            Objects.department_id,
            Department.displayName AS department_name
        FROM Art
        JOIN Objects ON Art.object_id = Objects.object_id
        JOIN Department ON Objects.department_id = Department.department_id
    """
    df = pd.read_sql(query, conn)
    conn.close()

    return df[df["department_name"] == "The Cloisters"]


# =============================================================================
# 2. Material Classification
# =============================================================================
material_map = {
    "Stone": ["stone", "limestone", "marble", "sandstone", "alabaster", "cement"],
    "Wood": ["wood", "oak", "walnut"],
    "Metal": ["iron", "silver", "bronze", "copper", "brass", "lead", "gilt", "alloy"],
    "Glass": ["glass", "vitreous", "stained", "pot-metal"],
    "Organic": ["ivory", "bone", "parchment", "vellum", "human remains"],
    "Ceramic": ["earthenware", "ceramic", "terracotta", "tile"],
    "Textile": ["wool", "linen", "silk", "tapestry", "embroidered"],
    "Mixed": ["tempera", "painted", "gilded", "gold", "polychrome"]
}


def assign_material_family(medium):
    """Assign standardized material family based on keyword rules."""
    m = str(medium).lower()
    for family, keywords in material_map.items():
        if any(k in m for k in keywords):
            return family
    return "Other"


# =============================================================================
# 3. Preprocessing
# =============================================================================
def preprocess(df):
    """Assign material family and compute century from objectBeginDate."""
    df["material_family"] = df["medium"].apply(assign_material_family)

    df["year"] = df["objectBeginDate"].astype(str).str[:4]
    df = df[df["year"].str.isnumeric()]  # Filter invalid years

    df["year"] = df["year"].astype(int)
    df["century"] = df["year"] // 100 + 1

    return df


# =============================================================================
# 4. Material Heatmap
# =============================================================================
def run_material_eda(df):
    """Return heatmap (Top 3 materials × centuries) as HTML <img> tag."""
    centuries = [12, 13, 14, 15, 16]
    df_c = df[df["century"].isin(centuries)]

    top3 = df_c["material_family"].value_counts().head(3).index.tolist()
    df_c = df_c[df_c["material_family"].isin(top3)]

    pivot = pd.crosstab(df_c["century"], df_c["material_family"])

    plt.figure(figsize=(9, 6))
    sns.heatmap(
        pivot,
        cmap="YlGnBu",
        annot=True,
        fmt="d",
        linewidths=0.6,
        annot_kws={"color": "black", "size": 11}
    )
    plt.title("Top 3 Materials Across Medieval Centuries")
    plt.xlabel("Material Family")
    plt.ylabel("Century")
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png", dpi=130, bbox_inches="tight")
    buffer.seek(0)

    img_html = "<img src='data:image/png;base64,{}'/>".format(
        base64.b64encode(buffer.getvalue()).decode()
    )
    plt.close()

    return img_html


# =============================================================================
# 5. Cultural Flow Sankey Diagram
# =============================================================================
def run_culture_sankey(df):
    """Return Sankey diagram (century → culture) as Plotly HTML."""
    centuries = [12, 13, 14, 15, 16]
    df_c = df[df["century"].isin(centuries)]
    df_c = df_c[df_c["culture"] != "European"]

    top5 = df_c["culture"].value_counts().head(5).index.tolist()
    df_c = df_c[df_c["culture"].isin(top5)]

    nodes = []
    node_index = {}

    # Century nodes
    for c in centuries:
        label = f"Century {c}"
        node_index[label] = len(nodes)
        nodes.append(label)

    # Culture nodes
    for cul in top5:
        label = f"Culture: {cul}"
        node_index[label] = len(nodes)
        nodes.append(label)

    # Color palette (you defined manually — preserved)
    culture_colors = {
        top5[0]: "rgba(199, 21, 133, 0.9)",
        top5[1]: "rgba(30, 144, 255, 0.9)",
        top5[2]: "rgba(46, 139, 87, 0.9)",
        top5[3]: "rgba(255, 165, 0, 0.9)",
        top5[4]: "rgba(138, 43, 226, 0.9)"
    }
    century_color = "rgba(180,180,180,0.50)"

    node_colors = [century_color] * len(centuries) + [
        culture_colors[c] for c in top5
    ]

    source, target, value, link_colors = [], [], [], []

    for c in centuries:
        df_cen = df_c[df_c["century"] == c]
        counts = df_cen["culture"].value_counts()

        for cul, v in counts.items():
            source.append(node_index[f"Century {c}"])
            target.append(node_index[f"Culture: {cul}"])
            value.append(v)
            link_colors.append(culture_colors[cul].replace("0.9", "0.35"))

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=20,
            thickness=20,
            label=nodes,
            color=node_colors
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            color=link_colors
        )
    )])

    fig.update_layout(
        title="Cultural Flow Across Medieval Centuries",
        font_size=12,
        width=1100,
        height=650
    )

    return fig.to_html(full_html=False)


# =============================================================================
# 6. Unified Entry Point for Flask
# =============================================================================
def run_eda(db_path):
    """Return two HTML components: heatmap + Sankey."""
    df = load_db(db_path)
    df = preprocess(df)

    heatmap_html = run_material_eda(df)
    sankey_html = run_culture_sankey(df)

    return heatmap_html, sankey_html
