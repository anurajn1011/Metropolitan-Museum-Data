# Metropolitan-Museum-Data
Repo for collecting and analyzing data from the MET. 

## Resources
The API for the MET can be found [here](https://metmuseum.github.io/). No key is required. 

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
