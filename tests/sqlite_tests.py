'''
sqlite_tests.py
Testing the contents of the db, verifying proper loading.
'''

import pandas as pd
import numpy as np
import sqlite3

# Connecting to our db
conn = sqlite3.connect("data/met.db")
cursor = conn.cursor()

# --- Queries --- #

# Checking to see if all departments are indeed to be found in the db
# print(pd.read_sql("""SELECT DISTINCT department_id FROM Objects;""", conn))

# Checking the size of our Art table 
# print(pd.read_sql("""SELECT COUNT(*) FROM Art""", conn))

# checking the contents of the artists table
# print(pd.read_sql("""SELECT artistAlphaSort FROM artists LIMIT 5""", conn))

# # checking the end dates of objects
# print(pd.read_sql("""SELECT title, artistAlphaSort, CAST(objectEndDate AS INTEGER) AS objectEndDate FROM Art WHERE CAST(objectEndDate AS INTEGER) > 2024""", conn))

print(pd.read_sql("""SELECT country FROM Art LIMIT 5""", conn))

conn.close()