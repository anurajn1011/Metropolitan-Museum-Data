import os
import sqlite3
import pandas as pd
import plotly.express as px
from skimage import io

# Path to SQLite database
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "met.db")


# ================================================================
# Box Plot: Artwork Creation Year Distribution
# ================================================================
def create_box_chart():
    conn = sqlite3.connect(DB_PATH)
    query = """
        SELECT 
            CAST(a.objectBeginDate AS INTEGER) AS earliest,
            CAST(a.objectEndDate AS INTEGER) AS latest,
            d.displayName
        FROM Art a
        JOIN Objects o ON a.object_id = o.object_id
        JOIN Department d ON o.department_id = d.department_id
        WHERE CAST(a.objectBeginDate AS INTEGER) != 0
          AND CAST(a.objectEndDate AS INTEGER) <= 2025
    """
    df = pd.read_sql(query, conn)
    conn.close()

    fig = px.box(
        df,
        x="earliest",
        y="displayName",
        title="Creation Year of Art Objects per Department"
    )
    fig.update_layout(xaxis_title="Creation Year")
    return fig


# ================================================================
# Histogram: Accession Year Trends
# ================================================================
def acq_bar_chart():
    conn = sqlite3.connect(DB_PATH)
    query = """
        SELECT 
            CAST(a.accessionYear AS INTEGER) AS accessionYear,
            d.displayName
        FROM Art a
        JOIN Objects o ON a.object_id = o.object_id
        JOIN Department d ON o.department_id = d.department_id
        WHERE CAST(a.accessionYear AS INTEGER) != 0
    """
    df = pd.read_sql(query, conn)
    conn.close()

    fig = px.histogram(
        df,
        x="accessionYear",
        color="displayName",
        title="Accession Year Histogram",
        nbins=20
    )
    fig.update_layout(bargap=0.2, yaxis_title="Count")
    return fig


# ================================================================
# Highlights Viewer (Single Image with Prev/Next)
# ================================================================
def show_highlights(i, dept):
    conn = sqlite3.connect(DB_PATH)
    query = """
        SELECT *
        FROM Art a
        JOIN Objects o ON a.object_id = o.object_id
        JOIN Department d ON o.department_id = d.department_id
        WHERE d.displayName = ?
          AND primaryImage NOT LIKE 'Unknown'
          AND isHighlight = 1
    """
    df = pd.read_sql(query, conn, params=(dept,))
    conn.close()

    if df.empty:
        return None

    idx = i % len(df)
    img_path = df.iloc[idx]["primaryImage"]

    # load image
    try:
        img = io.imread(img_path)
    except Exception:
        return None

    caption = (
        f"{df.iloc[idx]['title']}<br>"
        f"{df.iloc[idx]['objectBeginDate']} - {df.iloc[idx]['objectEndDate']}<br>"
        f"{df.iloc[idx]['artistAlphaSort']}"
    )

    fig = px.imshow(img, title=caption)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    fig.update_layout(title_x=0.5)

    return fig
