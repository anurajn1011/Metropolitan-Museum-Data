'''
the_cloisters-clean.py
Cleaning the the_cloisters data from the MET API.
'''

import os
import pandas as pd
import numpy as np

### Loading JSON files into dataframes ###

artists_df = pd.read_json("data/7_The_Cloisters/artists.jsonl", lines=True)
departments_df = pd.read_json("data/departments.jsonl", lines=True) # department loaded here
objects_df = pd.read_json("data/7_The_Cloisters/objects.jsonl", lines=True)

# replacing empty strings with nulls for analysis
artists_df = artists_df.replace("", pd.NA)
departments_df = departments_df.replace("", pd.NA)
objects_df = objects_df.replace("", pd.NA)

### Checking the null counts of ever column in each dataframe ###

print(f"Artists data:\n {artists_df.isna().sum()}\n")
print(f"Artists data shape: {artists_df.shape}\n")
print(f"Departments data:\n {departments_df.isna().sum()}\n")
print(f"Departments data shape: {departments_df.shape}\n")
print(f"Objects data:\n {objects_df.isna().sum()}\n")
print(f"Objects data shape: {objects_df.shape}\n")

'''
   Artists data:
 artist_name           0
artistAlphaSort       0
artistNationality    11
artistBeginDate      22
artistEndDate        22
dtype: int64

Artists data shape: (93, 5)

Departments data:
 department_id    0
displayName      0
dtype: int64

Departments data shape: (19, 2)

Objects data:
 objectID                    0
isHighlight                 0
accessionNumber             0
accessionYear              33
isPublicDomain              0
primaryImage               72
primaryImageSmall          72
additionalImages            0
constituents             2220
department                  0
objectName                  4
title                       7
culture                     0
period                   2348
dynasty                  2348
reign                    2348
portfolio                2348
artistRole               2220
artistPrefix             2293
artistDisplayName        2220
artistDisplayBio         2238
artistSuffix             2333
artistAlphaSort          2220
artistNationality        2231
artistBeginDate          2251
artistEndDate            2251
artistGender             2348
artistWikidata_URL       2269
artistULAN_URL           2271
objectDate                  0
objectBeginDate             0
objectEndDate               0
medium                      0
dimensions                 31
measurements              118
creditLine                  0
geographyType             995
city                     1934
state                    1488
county                   2348
country                  1140
region                   2277
subregion                2348
locale                   2348
locus                    2348
excavation               2348
river                    2348
classification              0
rightsAndReproduction    2348
linkResource             2348
metadataDate                0
repository                  0
objectURL                   0
tags                     1182
objectWikidata_URL        937
isTimelineWork              0
GalleryNumber            1176
department_id               0
object_id                   0
dtype: int64

Objects data shape: (2348, 59)

    Discussion: 
        Artists: Impute the null values in Artists with "Unknown"

        Departments: No missing data

        Objects: 
            Columns with Missing Data :  "accessionYear", "primaryImage", "primaryImageSmall", "constituents", "objectName", "title", 
            "period", "dynasty", "reign", "portfolio", "artistRole", "artistPrefix", "artistDisplayName", "artistDisplayBio", 
            "artistSuffix", "artistAlphaSort", "artistNationality", "artistBeginDate", "artistEndDate", "artistGender", 
            "artistWikidata_URL", "artistULAN_URL", "dimensions", "measurements", "geographyType", "city", "state", "county", "country", 
            "region", "subregion", "locale", "locus", "excavation", "river", "rightsAndReproduction", "linkResource", "tags", 
            "objectWikidata_URL", "GalleryNumber"

            We will not be storing the majority of these columns. For the ones we will be storing, we can simply list them as unknown EXCEPT
            for artistAlphaSort, which we will use a primary key in our Artists table in the database. 

            Art columns:
                object_id INTEGER PRIMARY KEY, isHighlight INTEGER, accessionYear TEXT, isPublicDomain INTEGER, primaryImage TEXT, 
                objectName TEXT, title TEXT NOT NULL, culture TEXT, period TEXT, dynasty TEXT, reign TEXT, portfolio TEXT, 
                artistWikidata_URL TEXT, artistAlphaSort TEXT, objectBeginDate TEXT, objectEndDate TEXT, medium TEXT, dimensions TEXT, 
                creditLine TEXT, city TEXT, state TEXT, county TEXT, country TEXT, region TEXT, subregion TEXT, excavation TEXT, 
                classification TEXT, isOnView INTEGER
            
            Artists columns:
                artistWikidata_URL TEXT, artistName TEXT, artistAlphaSort TEXT PRIMARY KEY, artistNationality TEXT, artistBeginDate TEXT, 
                artistEndDate TEXT
'''

### Imputations ###
artists_df = artists_df.fillna("Unknown")
objects_df[["accessionYear", "primaryImage", "objectName", "title", "period", "dynasty", "reign", 
            "portfolio", "artistWikidata_URL", "artistAlphaSort", "artistDisplayName", 
            "artistNationality", "artistBeginDate", "artistEndDate", "dimensions", 
            "city", "state", "county", "country", "region", "subregion", "excavation"
]] = objects_df[["accessionYear", "primaryImage", "objectName", "title", "period", "dynasty", "reign", 
            "portfolio", "artistWikidata_URL", "artistAlphaSort", "artistDisplayName", 
            "artistNationality", "artistBeginDate", "artistEndDate", "dimensions", 
            "city", "state", "county", "country", "region", "subregion", "excavation"
]].fillna("Unknown")

# # verifying successful imputations
print(f"Artists data:\n {artists_df.isna().sum()}\n")
print(f"Departments data:\n {departments_df.isna().sum()}\n")
print(f"Objects data:\n {objects_df.isna().sum()}\n")


# ### Exporting as CSV ####
path = "data/cleaned_data"
os.makedirs(path, exist_ok=True)
artists_df.to_csv("data//cleaned_data/artists_cloisters.csv", index=False)
departments_df.to_csv("data/cleaned_data/departments_cloisters.csv", index=False)
objects_df.to_csv("data/cleaned_data/objects_cloisters.csv",index=False)