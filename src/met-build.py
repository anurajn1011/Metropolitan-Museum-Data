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

# Loading the Departments table in the db
departments = pd.read_csv("data/cleaned_data/departments_cloisters.csv")
# departments.rename(columns={"displayName": "display_name"})\
#     .drop_duplicates()\
#     .to_sql("Department", conn, index=False, if_exists="replace")
print(pd.read_sql("""SELECT * FROM Department""", conn)) # Checking

# Loading the Objects table
objects = pd.read_csv("data/cleaned_data/objects_cloisters.csv")
# objects[["department_id", "object_id"]]\
#     .drop_duplicates()\
#     .to_sql("Objects", conn, index=False, if_exists="append")
print(pd.read_sql("""SELECT * FROM Objects LIMIT 5""", conn)) # checking

# Loading the Art table
# objects[["object_id",
#         "isHighlight",
#         "accessionYear",
#         "isPublicDomain",
#         "primaryImage",
#         "objectName",
#         "title",
#         "culture",
#         "period",
#         "dynasty",
#         "reign",
#         "portfolio",
#         "artist_id",
#         "objectBeginDate",
#         "objectEndDate",
#         "medium",
#         "height",
#         "width",
#         "length",
#         "creditLine",
#         "city",
#         "state",
#         "county",
#         "country",
#         "region",
#         "subregion",
#         "excavation",
#         "classification",
#         "isOnView"]]\
#             .drop_duplicates()\
#             .to_sql("Art", conn, index=False, if_exists="append")
print(pd.read_sql("""SELECT height FROM Art WHERE height <> 'Unknown' LIMIT 5""", conn)) # checking

# loading Artists table
artists = pd.read_csv("data/cleaned_data/artists_cloisters.csv")
# artists.rename(columns={"artist_name": "artistName"})\
#     .drop_duplicates()\
#     .to_sql("Artists", conn, index=False, if_exists="append")
print(pd.read_sql("""SELECT * FROM Artists LIMIT 5""", conn))

conn.close()