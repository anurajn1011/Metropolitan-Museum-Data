# Met Museum Data Pipeline (Docker Only Version)

Final Project -- Topics in Data Engineering\
Northwestern University -- Fall 2025

------------------------------------------------------------------------

## Overview

This repository contains a complete ETL pipeline based on the
Metropolitan Museum of Art Collection API. The project runs entirely
inside Docker and requires no local Python installation.

Pipeline includes: - API data extraction - Resume-safe incremental
downloading - Local raw JSONL storage - SQLite database schema and
loading - EDA support

------------------------------------------------------------------------

## Repository Structure

    src/
        met-databuild.py      Fetch data from API
        met-schema.py         Create SQLite schema
        met-build.py          Load cleaned data into database
        clean/                Data cleaning scripts
    data/                     SQLite database output
    met_data/                 Raw API data
    Dockerfile
    requirements.txt
    README.md

------------------------------------------------------------------------

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

## Step 5 -- Optional: Run EDA or Analysis

    docker run -it -v "${PWD}\data:/app/data" met python src/met_data_vis.py

------------------------------------------------------------------------

## Volume Mapping Summary

Local folder → Container path:

    data/      -> /app/data
    met_data/  -> /app/met_data

------------------------------------------------------------------------

## Summary of Commands

    docker build -t met .
    docker run -v "${PWD}/data:/app/data" met python src/met-schema.py
    docker run -it -v "${PWD}/met_data:/app/met_data" met python src/met-databuild.py 6 --auto
    docker run -v "${PWD}/data:/app/data" met python src/met-build.py

------------------------------------------------------------------------

## End of README
