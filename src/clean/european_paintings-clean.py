'''
european_paintings-clean.py
Cleaning the european_paintings data from the MET API.
'''

import os
import pandas as pd
import numpy as np

### Loading JSON files into dataframes ###

artists_df = pd.read_json("data/11_European_Paintings/artists.jsonl", lines=True)
objects_df = pd.read_json("data/11_European_Paintings/objects.jsonl", lines=True)

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
artistNationality     6
artistBeginDate      51
artistEndDate        51
dtype: int64

Artists data shape: (1120, 5)

Objects data:
 objectID                    0
isHighlight                 0
accessionNumber             0
accessionYear               0
isPublicDomain              0
primaryImage              284
primaryImageSmall         284
additionalImages            0
constituents                3
department                  0
objectName                 11
title                       0
culture                  2639
period                   2639
dynasty                  2639
reign                    2639
portfolio                2639
artistRole                  3
artistPrefix             2389
artistDisplayName           3
artistDisplayBio           18
artistSuffix             2616
artistAlphaSort             4
artistNationality           9
artistBeginDate           186
artistEndDate             186
artistGender             2595
artistWikidata_URL        204
artistULAN_URL            204
objectDate                610
objectBeginDate             0
objectEndDate               0
medium                      1
dimensions                  1
measurements                4
creditLine                  0
geographyType            2639
city                     2639
state                    2639
county                   2639
country                  2639
region                   2639
subregion                2639
locale                   2639
locus                    2639
excavation               2639
river                    2639
classification              0
rightsAndReproduction    2637
linkResource             2639
metadataDate                0
repository                  0
objectURL                   0
tags                       18
objectWikidata_URL         14
isTimelineWork              0
GalleryNumber            1478
department_id               0
object_id                   0
dtype: int64

Objects data shape: (2639, 59)
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
artists_df.to_csv("data//cleaned_data/artists_european_paintings.csv", index=False)
objects_df.to_csv("data/cleaned_data/objects_european_paintings.csv",index=False)