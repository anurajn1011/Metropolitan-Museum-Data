# Metropolitan-Museum-Data
Repo for collecting and analyzing data from the MET. 

## Resources
The API for the MET can be found [here](https://metmuseum.github.io/). No key is required. 

## Directory Structure
```
Metropolitan-Museum-Data:.
|   .gitignore
|   an_eda.ipynb
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
|   +---10_Egyptian_Art (*)
|   |       artists.jsonl
|   |       fetch_stats.json
|   |       objects.jsonl
|   |       progress.json
|   |
|   \---cleaned_data (*)
|
+---docs
|       base.txt
|       DAG.png
|
+---met_data
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

All directories with a '*' by them are to be constructed and loaded with data appropriately, they are not found in the repository. 

## Requirements

Only Docker Desktop is required. All Python dependencies are installed
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

## End of README
