# Metropolitan-Museum-Data
The Metropolitan Museum of Art in New York city is one of the largest and most prestigious museums in the world. This repository contains code to pull information about the objects in the collection of the Met by department from the publically-accessible MET API, which is directly maintained by the museum. The pipeline results in a Flask application with data visualizations for cross-department analysis of the collection, as well as department-specific visualizations.

## Data
This repository builds a sqlite database, met.db, from information directly pulled from the MET API. Users can query for infomation on the objects in the collection, including department and artist information, as well as information on object title, composition, creation year, and more. The schema for the met.db database, including types and linking foreign keys, can be found in the docs directory.

### Data Disclaimer
The MET API limits requests to 80 per minute. A single department with over 10,000 objects will take over 2 hours to extract before cleaning. A single department with over 30,000 objects can run for close to 8 hours. Users should plan for a long extraction time if pulling from the larger departments.

## Resources
The API for the MET can be found [here](https://metmuseum.github.io/). No key is required. 

## Directory Structure
```
Metropolitan-Museum-Data:.
|   .gitignore
|   Dockerfile
|   README.md
|   requirements.txt
|
+---.github
|       CODEOWNERS
|
+---data (*)
|   |   departments.jsonl
|   |
|   +---10_Egyptian_Art (*)        # Example department data and contents
|   |       artists.jsonl
|   |       fetch_stats.json
|   |       objects.jsonl
|   |       progress.json
|   |
|   \---cleaned_data (*)
|
+---docs
|       base.txt
|       met-art.png 
|       DAG.png
|
+---met_data (*)
|       met.db
|
+---src
|   |   app.py
|   |   eda_cloisters.py
|   |   explorer.py
|   |   interactive_vis.py
|   |   main.py
|   |   met-build.py
|   |   met-databuild.py
|   |   met-schema.py
|   |   met_data_vis.ipynb
|   |
|   +---clean
|   |       asian_art-clean.py
|   |       egyptian_art-clean.py
|   |       european_paintings-clean.py
|   |       general-cleaning-script.py
|   |       medieval_art-clean.py
|   |       the_cloisters-clean.py
|   |
|   \---templates
|           eda.html
|           index.html
|
\---tests
        sqlite_tests.py
```

All directories with a `(*)` by them are to be constructed and loaded with data appropriately, they are not found in the repository. 

## Requirements

The data pipeline assumes that a directory called met_data exists within the src folder. Only Docker Desktop is required. All Python dependencies are installed
inside the container.

------------------------------------------------------------------------

## Step 1 -- Build Docker Image

    docker build -t met .

------------------------------------------------------------------------

## Step 2 -- Create SQLite Schema

### Windows PowerShell:

    docker run -v "${PWD}\data:/app/data" met python src/met-schema.py

### Mac/Linux:

    docker run -v "${PWD}/data:/app/data" met python src/met-schema.py

This generates `data/met.db`

------------------------------------------------------------------------

## Step 3 -- Fetch Data from Met API

Example: Department 6 (Asian Art)

### Windows PowerShell:

    docker run -it -v "${PWD}\met_data:/app/met_data" met python src/met-databuild.py 6 --auto

### Mac/Linux:

    docker run -it -v "${PWD}/met_data:/app/met_data" met python src/met-databuild.py 6 --auto

Notes: - `--auto` enables continuous execution - `progress.json` allows
resume after interruption - raw JSONL files are stored in `met_data/`

To resume later:

    docker run -it -v "${PWD}\met_data:/app/met_data" met python src/met-databuild.py 6 --auto

------------------------------------------------------------------------

## Step 4 -- Load Cleaned Data into SQLite

    docker run -v "${PWD}\data:/app/data" met python src/met-build.py

This loads cleaned CSVs into `met.db`



------------------------------------------------------------------------

## Code Files Overview:
app.py -
eda_cloisters.py -
explorer.py -
interactive_vis.py -
main.py -
met-build.py -
met-databuild.py -
met-schema.py -
met_data_vis.ipynb - 
general-cleaning-script.py - 

## End of README
