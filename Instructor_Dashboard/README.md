# Instructor dashboard

The scripts included here are used to construct the instructor dashboard where instructors can interactively engage with data from their class.

`Get_Bio-MAPS_Data.py` includes functions to download all data collected for a given assessment and construct a master data file.

`app.R` is the main dashboard application script and calls `BioMAPS_Server.R` and `BioMAPS_UI.R`, which contain the server and user-interface functions for the app, respectively. `BioMAPS_Processing.R` includes functions to process data specifcally to be used in `app.R`.

`helpfiles` contains helper markdown files included in the dashboard, while `www` contains `.css` files for styling the dashboard.
