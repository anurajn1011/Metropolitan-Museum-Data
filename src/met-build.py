'''
met-build.py
Build the Met Museum of Art DB in SQLite
'''

import os
import pandas as pd
import numpy as np
import sqlite3

# Create tables in sqlite
conn = sqlite3.connect("data/met.db")
cursor = conn.cursor()

### Loading the Departments table into the db ###
departments = pd.read_csv("data/cleaned_data/departments.csv")
departments\
    .drop_duplicates()\
    .to_sql("Department", conn, index=False, if_exists="replace")

### Loading the Objects, Art, and Artists table ###

path_extension = "data/cleaned_data"
file_ids = [d for d in os.listdir(path_extension) if os.path.isfile(os.path.join(path_extension, d))]
file_ids.remove("departments.csv")
object_ids = [f for f in file_ids if f.startswith("objects_")]
artist_ids = [f for f in file_ids if f.startswith("artists_")]

for id in object_ids:
    # --- Objects Table -- #
    objects = pd.read_csv(f"data/cleaned_data/{id}",  dtype={"accessionYear": str})
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
            "artistWikidata_URL",
            "artistAlphaSort",
            "objectBeginDate",
            "objectEndDate",
            "medium",
            "dimensions",
            "creditLine",
            "city",
            "state",
            "county",
            "country",
            "region",
            "subregion",
            "excavation",
            "classification"
            ]]\
                .drop_duplicates()\
                .to_sql("Art", conn, index=False, if_exists="append")

for id in artist_ids:
    # --- Artists Table --- #

    # reading in the artists, and ignoring all the ones with unknown, "", or null alphaSorts.
    artists = pd.read_csv(f"data/cleaned_data/{id}")
    artists = artists[
    artists["artistAlphaSort"].notna() &
    (artists["artistAlphaSort"] != "") &
    (artists["artistAlphaSort"].str.lower() != "unknown")
    ]

    # loading wikidata url as null
    artists["artistWikidata_URL"] = pd.NA

    existing_keys = pd.read_sql("SELECT artistAlphaSort FROM Artists", conn)
    existing_keys_set = set(existing_keys["artistAlphaSort"])

    # Keep only rows not already in the table
    artists = artists[~artists["artistAlphaSort"].isin(existing_keys_set)]
    
    # removes all duplicates in the leftover rows, on artistAlphaSort
    artists_to_insert = artists[
        ["artistWikidata_URL", "artist_name", "artistAlphaSort", "artistNationality", "artistBeginDate", "artistEndDate"]
    ].drop_duplicates(subset=["artistAlphaSort"])

    # Insert into SQL
    if not artists_to_insert.empty:
        artists_to_insert.to_sql("Artists", conn, if_exists="append", index=False)

conn.close()