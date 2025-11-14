import os
import pandas as pd
import numpy as np

### Loading JSON files into dataframes ###

artists_df = pd.read_json("data/10_Egyptian_Art/artists.jsonl", lines=True)
objects_df = pd.read_json("data/10_Egyptian_Art/objects.jsonl", lines=True)

### Checking the null counts of ever column in each dataframe ###

print(f"Artists data:\n {artists_df.isna().sum()}\n")
print(f"Artists data shape: {artists_df.shape}\n")
print(f"Objects data:\n {objects_df.isna().sum()}\n")
print(f"Objects data shape: {objects_df.shape}\n")

'''
Artists data:
 artist_name           0
artistAlphaSort       0
artistNationality     0
artistBeginDate      12
artistEndDate        13
dtype: int64

Artists data shape: (23, 5)

Objects data:
 object_id                0
department_id            0
isHighlight              0
accessionYear          475
isPublicDomain           0
primaryImage             0
objectName               0
title                    0
culture                  0
period                   0
dynasty                  0
reign                    0
portfolio                0
artist_id            27976
objectBeginDate      27626
objectEndDate        26711
medium                   0
height               13191
width                13284
length               17718
creditLine               0
city                     0
state                    0
county                   0
country                  0
region                   0
subregion                0
excavation               0
classification           0
isOnView                 0
artistDisplayName        0
metadataDate             0
objectURL                0
dtype: int64

Objects data shape: (27976, 33)

    Descriptions:
        Artists: Missing begin and end date, impute with 'Unknown'

        Objects: Missing height, width, length, begin/end date, artist_id, accession year. 
        Impute height, width, length, begin/end, and accession year with 'Unknown'. Leave
        accession year as is. 
'''

### Imputations ###
artists_df = artists_df.fillna("Unknown")
objects_df[["objectBeginDate", "objectEndDate", "height", "width", "length", "accessionYear"]] = objects_df[["objectBeginDate", "objectEndDate", "height", "width", "length", "accessionYear"]].fillna("Unknown")
# there are some '' strings in title which we replace with 'Unknown'
objects_df['title'] = objects_df['title'].fillna('Unknown').replace('', 'Unknown')

# verifying successful imputations
print(f"Artists data:\n {artists_df.isna().sum()}\n")
print(f"Objects data:\n {objects_df.isna().sum()}\n")

### Exporting to CSV ###
artists_df.to_csv("data//cleaned_data/artists_egyptian_art.csv", index=False)
objects_df.to_csv("data/cleaned_data/objects_egyptian_art.csv",index=False)