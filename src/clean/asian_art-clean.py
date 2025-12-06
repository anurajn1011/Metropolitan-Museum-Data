'''
asian_art-clean.py
Cleaning the asian_art data from the MET API.
'''

import os
import pandas as pd
import numpy as np

### Loading JSON files into dataframes ###

artists_df = pd.read_json("data/6_Asian_Art/artists.jsonl", lines=True)
objects_df = pd.read_json("data/6_Asian_Art/objects.jsonl", lines=True)

# replacing empty strings with nulls for analysis
artists_df = artists_df.replace("", pd.NA)
objects_df = objects_df.replace("", pd.NA)

### Checking the null counts of ever column in each dataframe ###

print(f"Artists data:\n {artists_df.isna().sum()}\n")
print(f"Artists data shape: {artists_df.shape}\n")
print(f"Artists data types: {artists_df.dtypes}\n")
print(f"Objects data:\n {objects_df.isna().sum()}\n")
print(f"Objects data shape: {objects_df.shape}\n")

'''
Column description in each dataframe: 

Artists data:
 artist_name            0
artistAlphaSort        0
artistNationality    188
artistBeginDate      382
artistEndDate        360
dtype: int64

Artists data shape: (2232, 5)

Artists data types: artist_name          object
artistAlphaSort      object
artistNationality    object
artistBeginDate      object
artistEndDate        object
dtype: object

Objects data:
 objectID                     0
isHighlight                  0
accessionNumber              0
accessionYear              192
isPublicDomain               0
primaryImage              5736
primaryImageSmall         5736
additionalImages             0
constituents             26874
department                   0
objectName                  54
title                        9
culture                     10
period                    9913
dynasty                  37187
reign                    37187
portfolio                37187
artistRole               26915
artistPrefix             36257
artistDisplayName        26915
artistDisplayBio         28231
artistSuffix             36581
artistAlphaSort          27049
artistNationality        28218
artistBeginDate          28514
artistEndDate            28469
artistGender             37122
artistWikidata_URL       30140
artistULAN_URL           30216
objectDate                5729
objectBeginDate              0
objectEndDate                0
medium                     249
dimensions                  76
measurements               411
creditLine                  11
geographyType            37187
city                     37187
state                    37187
county                   37187
country                  37187
region                   37187
subregion                37187
locale                   37187
locus                    37187
excavation               37187
river                    37187
classification               0
rightsAndReproduction    36556
linkResource             37187
metadataDate                 0
repository                   0
objectURL                    0
tags                     17881
objectWikidata_URL       30924
isTimelineWork               0
GalleryNumber            35533
department_id                0
object_id                    0
dtype: int64

Objects data shape: (37187, 59)
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
print(f"Objects data:\n {objects_df.isna().sum()}\n")

### Exporting to CSV ###
artists_df.to_csv("data/cleaned_data/artists_asian_art.csv", index=False)
objects_df.to_csv("data/cleaned_data/objects_asian_art.csv",index=False)