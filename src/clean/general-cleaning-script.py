'''
general-cleaning-script.py
Given any data pulled from the MET API, ensure data consistency for DB.
'''

import os
import pandas as pd
import numpy as np

def clean_MET_data(artists_df, objects_df):
    '''
        Function to parse two data frames containing artists and objects data from the MET API.
        Replaces empty strings with pd.NA's and ensures columns found in DB are non-null. 
        Returns a cleaned artists_df and objects_df, respectively. 
    '''
    
    # replacing the empty strings with Nulls
    artists_df = artists_df.replace("", pd.NA)
    objects_df = objects_df.replace("", pd.NA)

    # handle the empty entries
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

    return artists_df, objects_df

def export_art_to_csv(name, artists_df, objects_df):
    '''
        Given cleaned artist and objects data from the MET API, we export the 
        dataframe to a csv stored in data/cleaned_data. Named with the art type.
    '''

    # exporting to csv
    artists_df.to_csv(f"data/cleaned_data/artists_{name}.csv", index=False)
    objects_df.to_csv(f"data/cleaned_data/objects_{name}.csv",index=False)

def extract_MET_data(path, name):
    '''
        Given a department, extract the csvs and load into dataframes. 
        Returns uncleaned artists_df and objects_df. 
    '''

    # returning a dataframe of artists and objects
    return pd.read_json(f"{path}/{name}/artists.jsonl", lines=True), pd.read_json(f"{path}/{name}/objects.jsonl", lines=True)

def data_dir():
    '''
        Obtains the directories in which the data is stored. Returns a list of strings.
    '''

    # set a variable from the root of the repo which holds the start of the relative path for the directories
    PATH = "data"
    return [d for d in os.listdir(PATH) if os.path.isdir(os.path.join(PATH, d))]

def department_to_csv(path):
    '''
        Given the departments json file, load the departments into csv for loading into a db. Departments json
        has already been verified for nulls. 
    '''

    df = pd.read_json(f"{path}/departments.jsonl", lines=True)
    df.to_csv(f"{path}/cleaned_data/departments.csv", index=False)

def main():
    '''
        Obtains the directories of data relative to the data folder. Loads the data into dataframes, artists_df and objects_df.
        Then, cleans it, preparing the data to be loaded into a SQLite db. Lastly, exports the data to csv's in the cleaned_data
        directory. 
    '''

    try:

        # obtain directories of data
        folders = data_dir()

        # construct cleaned_data if it does not exist
        path = "data/cleaned_data"
        os.makedirs(path, exist_ok=True)

        # make departments.csv
        department_to_csv("data")

        # iterate over the folders
        for dir in folders:
            artists_df, objects_df = extract_MET_data("data", dir) # extract the data into df
            artists_df, objects_df = clean_MET_data(artists_df, objects_df) # transform the data
            export_art_to_csv(dir, artists_df, objects_df) # load into csv
    except Exception as e :
        print(f"Exception raised: {e}")

if __name__ == "__main__":
    main()
