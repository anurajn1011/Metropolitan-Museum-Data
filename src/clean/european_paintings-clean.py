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
artistBeginDate      51
artistEndDate        51
dtype: int64

Artists data shape: (1120, 5)

Objects data:
object_id               0
department_id           0
isHighlight             0
accessionYear           0
isPublicDomain          0
primaryImage            0
objectName              0
title                   0
culture                 0
period                  0
dynasty                 0
reign                   0
portfolio               0
artist_id            2639
objectBeginDate         1
objectEndDate           1
medium                  0
height                  4
width                   4
length               2636
creditLine              0
city                    0
state                   0
county                  0
country                 0
region                  0
subregion               0
excavation              0
classification          0
isOnView                0
artistDisplayName       0
metadataDate            0
objectURL               0
dtype: int64

Objects data shape: (2639, 33)

    Description:
        Artists: artistBegin/EndDate are missing some values, just impute them with 'Unknown'

        Objects: Most common missing are artist_id and length. Leave artist_id as is and we can impute length with 
        0, since paintings can be assumed to have no depth. We also have objectBegin/EndDate and 
        4 entries of height and width. For the dates, just use 'Unknown' and for height, width use median.
'''

### Imputations ###
artists_df = artists_df.fillna("Unknown")
objects_df["length"] = objects_df["length"].fillna(0)
objects_df["height"] = objects_df["height"].fillna(objects_df["height"].median())
objects_df["width"] = objects_df["width"].fillna(objects_df["width"].median())
objects_df[["objectBeginDate", "objectEndDate"]] = objects_df[["objectBeginDate", "objectEndDate"]].fillna("Unknown")
# there are some '' strings in title which we replace with 'Unknown'
objects_df['title'] = objects_df['title'].fillna('Unknown').replace('', 'Unknown')

# verifying successful imputations
print(f"Artists data:\n {artists_df.isna().sum()}\n")
print(f"Objects data:\n {objects_df.isna().sum()}\n")

### Exporting to CSV ###
artists_df.to_csv("data//cleaned_data/artists_european_paintings.csv", index=False)
objects_df.to_csv("data/cleaned_data/objects_european_paintings.csv",index=False)