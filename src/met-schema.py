'''
met-schema.py
Set up the Met Museum of Art Schema in SQLite
'''

import pandas as pd
import numpy as np
import sqlite3

# Create tables in sqlite
conn = sqlite3.connect("../data/met.db")
cursor = conn.cursor()

conn.execute(
    '''
    CREATE TABLE IF NOT EXISTS Department (
        department_id INTEGER PRIMARY KEY,
        display_name TEXT not null
    )
'''
)

conn.execute(
    '''
    CREATE TABLE IF NOT EXISTS Objects (
        department_id INTEGER PRIMARY KEY,
        object_id INTEGER NOT NULL
    )
    '''
)

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
        artist_id INTEGER,
        objectBeginDate TEXT,
        objectEndDate TEXT,
        medium TEXT,
        height REAL,
        width REAL,
        length REAL,
        weight REAL,
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

conn.execute(
    '''
    CREATE TABLE IF NOT EXISTS Artists (
        artist_id INTEGER PRIMARY KEY,
        artistName TEXT,
        artistAlphaSort TEXT,
        artistNationality TEXT,
        artistBeginDate TEXT,
        artistEndDate TEXT
    )
    '''
)

conn.close()