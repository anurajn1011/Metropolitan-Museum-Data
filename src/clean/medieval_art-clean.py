import os
import pandas as pd
import numpy as np

### Loading JSON files into dataframes ###

artists_df = pd.read_json("data/17_Medieval_Art/artists.jsonl", lines=True)
objects_df = pd.read_json("data/17_Medieval_Art/objects.jsonl", lines=True)

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
    artistBeginDate      38
    artistEndDate        36
    dtype: int64

    Artists data shape: (97, 5)

    Objects data:
    object_id               0
    department_id           0
    isHighlight             0
    accessionYear         100
    isPublicDomain          0
    primaryImage            0
    objectName              0
    title                   0
    culture                 0
    period                  0
    dynasty                 0
    reign                   0
    portfolio               0
    artist_id            7134
    objectBeginDate        99
    objectEndDate          79
    medium                  0
    height               2783
    width                2579
    length               5280
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

    Objects data shape: (7134, 33)

    Discussion:
        Artists: Only missing data is artistBeginDate and artistEndDate. Fill in nulls with "Unknown"

        Objects: Nulls in accessionYear, artistID, objectBeginDate, objectEndDate, height, width, and length.
        We can impute accessionYear, objectBegin/EndDate, height, width, and length with "Unknown". 
        Leave ArtistID as Null. 
'''

### Imputations ###
artists_df = artists_df.fillna("Unknown")
objects_df[["accessionYear", "objectBeginDate", "objectEndDate", "height", "width", "length"]] = objects_df[["accessionYear", "objectBeginDate", "objectEndDate", "height", "width", "length"]].fillna("Unknown")
# there are some '' strings in title which we replace with 'Unknown'
objects_df['title'] = objects_df['title'].fillna('Unknown').replace('', 'Unknown')

# verifying successful imputations
print(f"Artists data:\n {artists_df.isna().sum()}\n")
print(f"Objects data:\n {objects_df.isna().sum()}\n")

### Exporting to CSV ###
artists_df.to_csv("data//cleaned_data/artists_medieval_art.csv", index=False)
objects_df.to_csv("data/cleaned_data/objects_medieval_art.csv",index=False)