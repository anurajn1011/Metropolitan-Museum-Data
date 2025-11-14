'''
met-schema.py
Set up the Met Museum of Art Schema in SQLite
'''

import pandas as pd
import numpy as np
import sqlite3

# Create tables in sqlite
conn = sqlite3.connect("data/met.db")
cursor = conn.cursor()

# Department table - contains department name and id
conn.execute(
    '''
    CREATE TABLE IF NOT EXISTS Department (
        department_id INTEGER PRIMARY KEY,
        display_name TEXT NOT NULL
    )
'''
)

# Objects table - linking table between Art and Departments
# all objects must have a department
conn.execute(
    '''
    CREATE TABLE IF NOT EXISTS Objects (
        department_id INTEGER NOT NULL,
        object_id INTEGER PRIMARY KEY
    )
    '''
)


# Art table - contains all information about the piece in question
# Links to the Artists table via artist_id, but not a required link
conn.execute(
    '''
    CREATE TABLE IF NOT EXISTS Art (
        object_id INTEGER PRIMARY KEY,
        isHighlight INTEGER,
        accessionYear TEXT,
        isPublicDomain INTEGER,
        primaryImage text,
        objectName TEXT,
        title TEXT NOT NULL,
        culture TEXT,
        period TEXT,
        dynasty TEXT,
        reign TEXT,
        portfolio TEXT,
        artistWikidata_URL TEXT,
        artistAlphaSort TEXT,
        objectBeginDate TEXT,
        objectEndDate TEXT,
        medium TEXT,
        height REAL,
        width REAL,
        length REAL,
        creditLine TEXT,
        city TEXT,
        state TEXT,
        county TEXT,
        country TEXT,
        region TEXT,
        subregion TEXT,
        excavation TEXT,
        classification TEXT,
        isOnView INTEGER
    )
    '''
)

# Artists table - contains all information about the artist
conn.execute(
    '''
    CREATE TABLE IF NOT EXISTS Artists (
        artistWikidata_URL INTEGER,
        artistName TEXT,
        artistAlphaSort TEXT PRIMARY KEY,
        artistNationality TEXT,
        artistBeginDate TEXT,
        artistEndDate TEXT
    )
    '''
)

conn.close()