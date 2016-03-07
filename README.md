# WS 2016 Project 1
 Predicting future vaccination uptake using web-mined time-series data. Experiment based on Hansen et al. "Predicting Vaccination Uptake using Web Search Queries"

##  Usage
1.  Downloading and exporting CSV data from Google Trends by using vaccine description text files:
    ```bash
    usage: FileSanitizer.py [-h] [-d D] file [file ...]
    ```
2.  Clear up unnecessary information from the exported CSV files using your favourite CSV Editor
3.  Apply the CSVAnalyser.py file to the specified directory and inputing a terget file.
    ```bash
    usage: CSVAnalyser.py [-h] [-dir DIR [DIR ...]] [-t T]
    ```
