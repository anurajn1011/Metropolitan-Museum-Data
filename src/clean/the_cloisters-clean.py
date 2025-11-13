import os
import pandas as pd
import numpy as np

### Loading JSON files into dataframes ###

artists_df = pd.read_json("data/The Cloisters/artists.jsonl", lines=True)
departments_df = pd.read_json("data/The Cloisters/departments.jsonl", lines=True)
objects_df = pd.read_json("data/The Cloisters/objects.jsonl", lines=True)

### Checking the null counts of ever column in each dataframe ###

print(f"Artists data:\n {artists_df.isna().sum()}\n")
print(f"Artists data shape: {artists_df.shape}\n")
print(f"Departments data:\n {departments_df.isna().sum()}\n")
print(f"Departments data shape: {departments_df.shape}\n")
print(f"Objects data:\n {objects_df.isna().sum()}\n")
print(f"Objects data shape: {objects_df.shape}\n")

'''
    Result:
    Artists data:
    artist_name           0
    artistAlphaSort       0
    artistNationality     0
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
    object_id               0
    department_id           0
    isHighlight             0
    accessionYear          33
    isPublicDomain          0
    primaryImage            0
    objectName              0
    title                   0
    culture                 0
    period                  0
    dynasty                 0
    reign                   0
    portfolio               0
    artist_id            2348
    objectBeginDate         0
    objectEndDate           0
    medium                  0
    height                527
    width                 837
    length               2008
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

    Objects data shape: (2348, 33)

    Discussion: 
        Artists: Only missing data is in the artistBeginDate, artistEndDate columns. Both have 
        22 empty entries. A comprehensive next step is to see if the missing entries are for the same 
        rows. Regardless, we will simply fill in all Nulls with "Unknown", since db expects text.

        Departments: No missing data

        Objects: Missing data in accessionYear, artistID, height, width, and length. We can fill
        in the accessionYear as "unknown" as well. For height, width, and length we can simply
        leave it as is, could be handled later on since we do not want any EDA to be done with 
        0's imputed. As for artistID, this is the more concerning one. None of the pieces have 
        an artistID associated with them, since all 2348 rows are missing this column.
        For the purposes of loading the db, we will simply preserve the nulls. 
'''

### Imputations ###
artists_df = artists_df.fillna("Unknown")
objects_df[["accessionYear", "height", "width", "length"]] = objects_df[["accessionYear", "height", "width", "length"]].fillna("Unknown")

# verifying successful imputations
print(f"Artists data:\n {artists_df.isna().sum()}\n")
print(f"Departments data:\n {departments_df.isna().sum()}\n")
print(f"Objects data:\n {objects_df.isna().sum()}\n")


### Exporting as CSV ####
path = "data/The Cloisters/cleaned_data"
os.makedirs(path, exist_ok=True)
artists_df.to_csv("data/The Cloisters/cleaned_data/artists.csv")
departments_df.to_csv("data/The Cloisters/cleaned_data/departments.csv")
objects_df.to_csv("data/The Cloisters/cleaned_data/objects.csv")