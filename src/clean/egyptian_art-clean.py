'''
egyptian_art-clean.py
Cleaning the egyptian_art data from the MET API.
'''

import os
import pandas as pd
import numpy as np

### Loading JSON files into dataframes ###

artists_df = pd.read_json("data/10_Egyptian_Art/artists.jsonl", lines=True)
objects_df = pd.read_json("data/10_Egyptian_Art/objects.jsonl", lines=True)

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
artistNationality    12
artistBeginDate      12
artistEndDate        13
dtype: int64

Artists data shape: (23, 5)

Objects data:
 objectID                     0
isHighlight                  0
accessionNumber              0
accessionYear              475
isPublicDomain               0
primaryImage             14429
primaryImageSmall        14429
additionalImages             0
constituents             27273
department                   0
objectName                  38
title                        4
culture                  27819
period                       0
dynasty                   4661
reign                    16574
portfolio                27819
artistRole               27273
artistPrefix             27817
artistDisplayName        27273
artistDisplayBio         27452
artistSuffix             27768
artistAlphaSort          27273
artistNationality        27655
artistBeginDate          27359
artistEndDate            27362
artistGender             27665
artistWikidata_URL       27347
artistULAN_URL           27347
objectDate                  32
objectBeginDate              0
objectEndDate                0
medium                       5
dimensions                4993
measurements              3116
creditLine                  18
geographyType               12
city                     27819
state                    27819
county                   27819
country                   1256
region                    8498
subregion                 9296
locale                   12194
locus                    20326
excavation               11528
river                    27819
classification           27819
rightsAndReproduction    27819
linkResource             27819
metadataDate                 0
repository                   0
objectURL                    0
tags                     23093
objectWikidata_URL        8312
isTimelineWork               0
GalleryNumber             6976
department_id                0
object_id                    0
dtype: int64

Objects data shape: (27819, 59)
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
artists_df.to_csv("data//cleaned_data/artists_egyptian_art.csv", index=False)
objects_df.to_csv("data/cleaned_data/objects_egyptian_art.csv",index=False)