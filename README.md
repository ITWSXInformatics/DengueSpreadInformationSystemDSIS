# Dengue Spread Information System (DSIS)

An information system that describes the change in Dengue cases and environmental factors across various years (month-wise) for *Iquitos, Peru* and *San Juan, Puerto Rico*.
The project is now published as a research paper and can be found [here](https://dl.acm.org/doi/10.1145/3418094.3418133).

**NOTE:** Recently, the application was updated to make it more streamlined and thus, the images used in the paper might not exactly match with the application. However, the content has just been tweaked and has not been removed completely.

## Requirements

- [Python 3.7](https://www.python.org) or Python 3.6

## Installing

Using requirements.txt
```
git clone git@github.com:ITWSXInformatics/DengueSpreadInformationAndEarlyWarningSystem.git
cd DengueSpreadInformationAndEarlyWarningSystem
pip3 install -r requirements.txt
```

Using pipenv
```
git clone git@github.com:ITWSXInformatics/DengueSpreadInformationAndEarlyWarningSystem.git
cd DengueSpreadInformationAndEarlyWarningSystem
pipenv install
```

## Running 

Without virtual environment
```
cd MapData
python3 main.py
```

Using pipenv
```
pipenv shell
cd MapData
python main.py
```
Then go to localhost:5000 or 127.0.0.1:5000

## Data 

The data files are stored in the data folder. As this work deals with two cities, Iquitos in Peru and San Juan in Puero Rico, the data has been arranged into the respecive folders. Each directory includes:
- **data/<CITY_NAME>/dengue_data.csv:** contains the total number of dengue cases
- **data/<CITY_NAME>/population_data.csv:** contains the estimated population of the city for the year
- **data/<CITY_NAME>/environment_data.csv:** contains environmental information including precipitation and temperature
- **data/<CITY_NAME>/combined_data.csv:** combines all the data sources above using some preprocessing and creates a common CSV file.
- **data/<CITY_NAME>/temperature_humidity_data.xlsx:** contains air temperature and humidity values for the city.

There is also the **data/complete_data.csv** file which includes the data from all the files for both cities in one file.

#### Original data source

The data is taken from the [Dengue forecasting GitHub repository](https://github.com/cdcepi/dengue-forecasting-project-2015) containing environmental and Dengue data from NOAA and CDC.
