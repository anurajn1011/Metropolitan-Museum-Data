# Metropolitan-Museum-Data
The Metropolitan Museum of Art in New York city is one of the largest and most prestigious museums in the world. This repository contains code to pull information about the objects in the collection of the Met by department from the publically-accessible MET API, which is directly maintained by the museum. The pipeline results in a Flask application with data visualizations for cross-department analysis of the collection, as well as department-specific visualizations.

## Data
This repository builds a sqlite database, met.db, from information directly pulled from the MET API. Users can query for infomation on the objects in the collection, including department and artist information, as well as information on object title, composition, creation year, and more. The schema for the met.db database, including types and linking foreign keys, can be found in the docs directory.

### Data Disclaimer
The MET API limits requests to 80 per minute. A single department with over 10,000 objects will take over 2 hours to extract before cleaning. A single department with over 30,000 objects can run for close to 8 hours. Users should plan for a long extraction time if pulling from the larger departments.

### Department Key
1 - American Decorative Arts                     : 18976 objects  
3 - Ancient West Asian Art                       : 6309 objects  
4 - Arms and Armor                               : 13747 objects  
5 - Arts of Africa, Oceania, and the Americas    : 12235 objects  
6 - Asian Art                                    : 37187 objects  
7 - The Cloisters                                : 2348 objects  
8 - The Costume Institute                        : 31567 objects  
9 - Drawings and Prints                          : 182103 objects  
10 - Egyptian Art                                : 27976 objects  
11 - European Paintings                          : 2639 objects  
12 - European Sculpture and Decorative Arts      : 43946 objects  
13 - Greek and Roman Art                         : 33674 objects  
14 - Islamic Art                                 : 15689 objects  
15 - The Robert Lehman Collection                : 2586 objects  
16 - The Libraries                               : 788 objects  
17 - Medieval Art                                : 7135 objects  
18 - Musical Instruments                         : 5249 objects  
19 - Photographs                                 : 39162 objects  
21 - Modern Art                                  : 15170 objects  

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

## Step 5 -- Run the Flask Application (Fully in Docker)

Once `met.db` has been created and populated (Steps 2–4), you can launch
the Flask app from inside the same Docker image.

### Windows PowerShell:

```powershell
docker run -it -p 5000:5000 -v "${PWD}\data:/app/data" met python src/app.py
```

### Mac/Linux:

```powershell
docker run -it -p 5000:5000 -v "${PWD}/data:/app/data" met python src/app.py
```


------------------------------------------------------------------------

## Code Files Overview:
app.py - Launches Flask data exploration application
explorer.py - Set up grouped data exploration for the flask application
interactive_vis.py - Set up interactive data exploration for the flask application
main.py - Runs entire data pipeline
met-build.py - Loads cleaned data into the met.db database
met-databuild.py - Extracts data from the met api department-by-department
met-schema.py - Sets up met.db database schema
met_data_vis.ipynb - Loads interactive visualizations from interactive_vis.py
general-cleaning-script.py - Cleans extracted json data from met-databuild.py

## End of README
