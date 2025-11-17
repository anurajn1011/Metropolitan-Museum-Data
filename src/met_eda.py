#!/usr/bin/env python
# coding: utf-8

import sqlite3
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", font_scale=1.2)

import plotly.graph_objects as go


# =============================================================================
# 1. Load Database
# =============================================================================
def load_db(db_path):
    """Load the MET database and merge Art + Objects + Department tables."""
    conn = sqlite3.connect(db_path)

    query = """
    SELECT 
        Art.*,
        Objects.department_id,
        Department.display_name AS department_name
    FROM Art
    JOIN Objects ON Art.object_id = Objects.object_id
    JOIN Department ON Objects.department_id = Department.department_id
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    print(f"[INFO] Loaded database: {df.shape[0]} rows, {df.shape[1]} columns")
    return df


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
    """Return standardized material family based on keyword mapping."""
    m = str(medium).lower()
    for family, keywords in material_map.items():
        if any(k in m for k in keywords):
            return family
    return "Other"


# =============================================================================
# 3. Preprocessing (Year → Century)
# =============================================================================
def preprocess(df):
    """Convert year to int and extract century; assign material family."""
    df["material_family"] = df["medium"].apply(assign_material_family)

    # Extract year
    df["year"] = df["objectBeginDate"].astype(str).str[:4]
    df = df[df["year"].str.isnumeric()]  # remove invalid years
    df["year"] = df["year"].astype(int)
    df["century"] = df["year"] // 100 + 1

    return df


# =============================================================================
# 4. EDA — Material Across Centuries (Top 3)
# =============================================================================
def run_material_eda(df):
    """Plot heatmap of top 3 materials across key medieval centuries."""

    focus_centuries = [12, 13, 14, 15, 16]
    df_focus = df[df["century"].isin(focus_centuries)]

    # Top 3 materials
    top3 = df_focus["material_family"].value_counts().head(3).index.tolist()
    df_focus = df_focus[df_focus["material_family"].isin(top3)]

    pivot = pd.crosstab(df_focus["century"], df_focus["material_family"])

    plt.figure(figsize=(8, 6))
    sns.heatmap(pivot, cmap="YlGnBu", annot=True, fmt="d", linewidths=0.5)
    plt.title("Top 3 Materials Across Medieval Centuries — Cloisters Collection")
    plt.xlabel("Material Family")
    plt.ylabel("Century")
    plt.tight_layout()
    plt.show()


# =============================================================================
# 5. EDA — Cultural Flow (Sankey Diagram)
# =============================================================================
def run_culture_sankey(df):
    """Generate a Sankey Diagram showing cultural flow across centuries."""

    focus_centuries = [12, 13, 14, 15, 16]
    df_focus = df[df["century"].isin(focus_centuries)]
    df_focus = df_focus[df_focus["culture"] != "European"]  # Remove vague label

    top5 = df_focus["culture"].value_counts().head(5).index
    df_focus = df_focus[df_focus["culture"].isin(top5)]

    # Build nodes: all centuries then all cultures
    nodes = []
    node_index = {}

    # Add century nodes
    for c in focus_centuries:
        label = f"Century {c}"
        node_index[label] = len(nodes)
        nodes.append(label)

    # Add culture nodes
    for cul in top5:
        label = f"Culture: {cul}"
        node_index[label] = len(nodes)
        nodes.append(label)

    # Colors
    culture_colors = {
        top5[0]: "rgba(199, 21, 133, 0.9)",
        top5[1]: "rgba(30, 144, 255, 0.9)",
        top5[2]: "rgba(46, 139, 87, 0.9)",
        top5[3]: "rgba(255, 165, 0, 0.9)",
        top5[4]: "rgba(138, 43, 226, 0.9)"
    }
    century_color = "rgba(180,180,180,0.50)"

    node_colors = [century_color] * len(focus_centuries) + [culture_colors[c] for c in top5]

    # Build links
    source = []
    target = []
    value = []
    link_colors = []

    for c in focus_centuries:
        df_c = df_focus[df_focus["century"] == c]
        counts = df_c["culture"].value_counts()

        for cul, v in counts.items():
            source.append(node_index[f"Century {c}"])
            target.append(node_index[f"Culture: {cul}"])
            value.append(v)
            link_colors.append(culture_colors[cul].replace("0.9", "0.35"))

    # Draw Sankey
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
        title="Cultural Flow Across Medieval Centuries — Cloisters Collection",
        font_size=12,
        width=1100,
        height=650
    )

    fig.show()


# =============================================================================
# 6. Unified Entry Point (what main.py will call)
# =============================================================================
def run_eda(db_path):
    """Run EDA pipeline. Currently supports Cloisters collection only."""

    print("[STEP 1] Loading database...")
    df = load_db(db_path)

    print("[STEP 2] Preprocessing...")
    df = preprocess(df)

    print("[STEP 3] Running Material EDA...")
    run_material_eda(df)

    print("[STEP 4] Running Cultural Flow EDA...")
    run_culture_sankey(df)

    # Future extension:
    # Add other exhibition-specific EDA modules here when available.
    # Example:
    # run_asian_eda(df)
    # run_egyptian_eda(df)

    print("[DONE] EDA pipeline completed.")

# Allows manual running: python eda.py
if __name__ == "__main__":
    run_eda("met.db")
