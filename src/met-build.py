'''
met-build.py
Build the Met Museum of Art DB in SQLite
'''

import pandas as pd
import numpy as np
import sqlite3

# Create tables in sqlite
conn = sqlite3.connect("data/met.db")
cursor = conn.cursor()

### Loading the Departments table into the db ###
departments = pd.read_csv("data/cleaned_data/departments_cloisters.csv")
departments.rename(columns={"displayName": "display_name"})\
    .drop_duplicates()\
    .to_sql("Department", conn, index=False, if_exists="replace")

### Loading the Objects, Art, and Artists table ###

path_extension = "data/cleaned_data"
file_ids = ["_asian_art", "_cloisters", "_egyptian_art", "_european_paintings", "_medieval_art"]

for id in file_ids:
    # --- Objects Table -- #
    objects = pd.read_csv(f"data/cleaned_data/objects{id}.csv")
    objects[["department_id", "object_id"]]\
        .drop_duplicates()\
        .to_sql("Objects", conn, index=False, if_exists="append")

    # --- Art Table --- #
    objects[["object_id",
            "isHighlight",
            "accessionYear",
            "isPublicDomain",
            "primaryImage",
            "objectName",
            "title",
            "culture",
            "period",
            "dynasty",
            "reign",
            "portfolio",
            "artist_id",
            "objectBeginDate",
            "objectEndDate",
            "medium",
            "height",
            "width",
            "length",
            "creditLine",
            "city",
            "state",
            "county",
            "country",
            "region",
            "subregion",
            "excavation",
            "classification",
            "isOnView"]]\
                .drop_duplicates()\
                .to_sql("Art", conn, index=False, if_exists="append")

    # --- Artists Table --- #
    artists = pd.read_csv(f"data/cleaned_data/artists{id}.csv")
    artists = artists.rename(columns={"artist_name": "artistName"}).drop_duplicates()
    # Load the data to a  temporary table
    artists.to_sql("Artists_temp", conn, index=False, if_exists="replace")
    # insert only unique rows from the temp table into Artists
    conn.execute("""
        INSERT OR IGNORE INTO Artists (artistName, artistAlphaSort, artistNationality, artistBeginDate, artistEndDate)
        SELECT artistName, artistAlphaSort, artistNationality, artistBeginDate, artistEndDate
        FROM Artists_temp;
    """)
    conn.commit()
    # drop the temp table
    conn.execute("DROP TABLE IF EXISTS Artists_temp;")

conn.close()