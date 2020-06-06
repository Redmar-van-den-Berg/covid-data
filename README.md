# covid-data
Scripts to parse the covid data released by the RIVM

The raw data these scripts can parse can be found on the website of the
[RIVM](https://data.rivm.nl/covid-19/).

## to_daily.py
This script converts the `COVID-19_aantallen_gemeente_cumulatief.csv` file to
the daily changes for each municipality.

Usage:
```bash
# First, dowload the data
wget https://data.rivm.nl/covid-19/COVID-19_aantallen_gemeente_cumulatief.csv
./to_daily.py --input COVID-19_aantallen_gemeente_cumulatief.csv > COVID-19-daily.csv
```
