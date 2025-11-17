'''
medieval_art-clean.py
Cleaning the medieval_art data from the MET API.
'''

import os
import pandas as pd
import numpy as np

### Loading JSON files into dataframes ###

artists_df = pd.read_json("data/17_Medieval_Art/artists.jsonl", lines=True)
objects_df = pd.read_json("data/17_Medieval_Art/objects.jsonl", lines=True)

# replacing empty strings with nulls for analysis
artists_df = artists_df.replace("", pd.NA)
objects_df = objects_df.replace("", pd.NA)

### Checking the null counts of ever column in each dataframe ###

print(f"Artists data:\n {artists_df.isna().sum()}\n")
print(f"Artists data shape: {artists_df.shape}\n")
print(f"Objects data:\n {objects_df.isna().sum()}\n")
print(f"Objects data shape: {objects_df.shape}\n")

'''
Artists data:
 artist_name           0
artistAlphaSort       0
artistNationality    25
artistBeginDate      38
artistEndDate        36
dtype: int64

Artists data shape: (97, 5)

Objects data:
 objectID                    0
isHighlight                 0
accessionNumber             0
accessionYear             100
isPublicDomain              0
primaryImage              220
primaryImageSmall         220
additionalImages            0
constituents             6972
department                  0
objectName                  5
title                       2
culture                     0
period                   7135
dynasty                  7135
reign                    7135
portfolio                7135
artistRole               6972
artistPrefix             7079
artistDisplayName        6972
artistDisplayBio         7018
artistSuffix             7124
artistAlphaSort          6972
artistNationality        7019
artistBeginDate          7033
artistEndDate            7031
artistGender             7134
artistWikidata_URL       7046
artistULAN_URL           7041
objectDate                  5
objectBeginDate             0
objectEndDate               0
medium                      0
dimensions                  6
measurements              687
creditLine                  0
geographyType            3666
city                     5767
state                    5717
county                   7135
country                  3955
region                   7102
subregion                7135
locale                   7135
locus                    7135
excavation               7135
river                    7135
classification              0
rightsAndReproduction    7135
linkResource             7135
metadataDate                0
repository                  0
objectURL                   0
tags                     4712
objectWikidata_URL       5802
isTimelineWork              0
GalleryNumber            6028
department_id               0
object_id                   0
dtype: int64

Objects data shape: (7135, 59)
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

# ### Exporting to CSV ###
artists_df.to_csv("data//cleaned_data/artists_medieval_art.csv", index=False)
objects_df.to_csv("data/cleaned_data/objects_medieval_art.csv",index=False)