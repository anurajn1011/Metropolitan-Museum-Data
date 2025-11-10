'''
met-schema.py
Set up the Met Museum of Art Schema in SQLite
'''

import pandas as pd
import numpy as np
import sqlite3

# Create tables in sqlite
conn = sqlite3.connect("met.db")
cursor = conn.cursor()

conn.close()