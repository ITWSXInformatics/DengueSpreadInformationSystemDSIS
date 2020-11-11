# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 15:55:57 2020

@author: Dominic
"""
from flask import Flask, render_template, request, session, redirect
from geopy.geocoders import Nominatim
import folium
import pandas as pd
import json
import math

app = Flask(__name__)
# Required in order to use session cookies
app.secret_key = "super secret key"

# Required so the map html template is updated automatically
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Required so Flask knows where to fetch the images
app.add_url_rule('/images/<path:filename>', endpoint='images', view_func=app.send_static_file)

# Constants for the data
POPULATION_COLUMN = "population"
AVG_SURFACE_TEMPERATURE_COLUMN = "TAVG"
AVG_AIR_TEMP_COLUMN = "air_temperature"
AVG_DEW_PNT_TEMP_COLUMN = "dew_point_temperature"
AVG_RELATIVE_HUMIDITY_COLUMN = "relative_humidity"
PRECIPITATION_COLUMN = "PRCP"
CITIES_COLUMN = "place"
DATE_COLUMN = "date"
DENGUE_CASES_COLUMN = "total_cases"

YEAR_KEY = "year"
MONTH_KEY = "month"

@app.route('/', methods=["POST","GET"])
def homepage():
    
    dengue_data = pd.read_csv("../data/complete_data.csv")
    
    # Default to the first item in our select list
    if (MONTH_KEY not in session):
        session[MONTH_KEY] = "January"
    
    if (YEAR_KEY not in session):
        session[YEAR_KEY] = 1990
    
    # Persist the values selected by the user in their session
    if request.method == 'POST':
        session.clear()
        session[MONTH_KEY] = str(request.form[MONTH_KEY])
        session[YEAR_KEY] = int(request.form[YEAR_KEY])

    # Convert the month and year to the proper format for parsing the dataframe
    date = format_for_date_column(session[MONTH_KEY], session[YEAR_KEY])
    
    filtered_data = dengue_data[dengue_data[DATE_COLUMN] == date]
    
    # Set the coordinates and zoom so we can see both points
    start_coords = (10.7437, -73.2516)
    folium_map = folium.Map(location=start_coords, zoom_start=4)

    # Add a map layer to allow for a heat map using the GeoJSON we created
    folium.Choropleth(
        geo_data="iquitos_san_juan_geo.json",
        name='Iquitos and San Juan Dengue Cases',
        data=filtered_data,
        columns=[CITIES_COLUMN, DENGUE_CASES_COLUMN],
        key_on='feature.properties.name',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Number of Dengue Cases',
        show=True
    ).add_to(folium_map)
    
    folium.LayerControl().add_to(folium_map)
    
    # Iquitos Marker creation
    iquitos_data = filtered_data[filtered_data[CITIES_COLUMN] == "Iquitos"]
    coordinates = [-3.7437, -73.2516]
    create_info_marker(iquitos_data, coordinates, folium_map)
    
    # San Juan Marker creation
    san_juan_data = filtered_data[filtered_data[CITIES_COLUMN] == "San Juan"]
    coordinates = [18.4655, -66.1057]
    create_info_marker(san_juan_data, coordinates, folium_map)
    
    date_selected = {
                        "month_selected" : session[MONTH_KEY],
                        "year_selected"  : session[YEAR_KEY]
                    }
    
    folium_map.save('templates/map.html')
    
    return render_template("index.html", data = date_selected)

@app.route('/background')
def project_background():
    return render_template("background.html")

@app.route('/contacts')
def project_members():
    return render_template("contacts.html")

@app.route('/plots')
def data_plots():
    return render_template("data_plots.html")

@app.route('/map')
def show_map():
    return render_template('map.html')

def create_info_marker(data, coordinates, folium_map):
    
    # In case a user decides to select a month and year we dont have data for
    if data.empty:
        folium.Marker(
                    location = coordinates,
                    popup = "No data found for this location.",
                    icon = folium.Icon(color='gray')
                ).add_to(folium_map)
        return
    
    # In case we don't have data for a specific column
    population = "Unknown"
    surface_temperature = "Unknown"
    precipitation = "Unknown"
    air_temp = "Unknown"
    dew_pnt_temp = "Unknown"
    relative_humidity = "Unknown"
    
    population_vals = data[POPULATION_COLUMN].values
    surf_temperature_vals = data[AVG_SURFACE_TEMPERATURE_COLUMN].values
    precipitation_vals = data[PRECIPITATION_COLUMN].values
    air_temp_vals = data[AVG_AIR_TEMP_COLUMN].values
    dew_pnt_temp_vals = data[AVG_DEW_PNT_TEMP_COLUMN].values
    relative_humidity_vals = data[AVG_RELATIVE_HUMIDITY_COLUMN].values

    if len(surf_temperature_vals) > 0 and not math.isnan(surf_temperature_vals[0]):
        surface_temperature = convert_temperature_to_fahrenheit(
                                                                    surf_temperature_vals[0], 
                                                                    celsius=True
                                                               )
    if len(air_temp_vals) > 0 and not math.isnan(air_temp_vals[0]):
        air_temp = convert_temperature_to_fahrenheit(
                                                        air_temp_vals[0] 
                                                    )
    if len(dew_pnt_temp_vals) > 0 and not math.isnan(dew_pnt_temp_vals[0]):
        dew_pnt_temp = convert_temperature_to_fahrenheit(
                                                            dew_pnt_temp_vals[0] 
                                                        )
    
    if len(population_vals) > 0 and not math.isnan(population_vals[0]):
        population = int(population_vals[0])
        
    if len(precipitation_vals) > 0 and not math.isnan(precipitation_vals[0]):
        precipitation = round(precipitation_vals[0],2)
    
    if len(relative_humidity_vals) > 0 and not math.isnan(relative_humidity_vals[0]):
        relative_humidity = round(relative_humidity_vals[0],2)
    
    info_message = f"""Avg Surface Temp: {surface_temperature} K<br>
                       Avg Air Temp: {air_temp} K<br>
                       Avg Dew Point Temp: {dew_pnt_temp} K<br>
                       Total Precipitation: {precipitation} mm<br>
                       Avg Relative Humidity: {relative_humidity} kg/cubic m<br>
                       Population: {population} <br>
                    """ 

    folium.Marker(location = coordinates,
                     popup = folium.Popup(info_message, max_width=250,min_width=250),
                     icon = folium.Icon(color='blue')
                 ).add_to(folium_map)

"""
Reformat the specified year and month into the 
appropriate format for selecting data
"""
def format_for_date_column(month, year):
    
    month_to_insert = "01"
    
    if month == "January":
        month_to_insert = "01"
    elif month == "February":
        month_to_insert = "02"
    elif month == "March":
        month_to_insert = "03"
    elif month == "April":
        month_to_insert = "04"
    elif month == "May":
        month_to_insert = "05"
    elif month == "June":
        month_to_insert = "06"
    elif month == "July":
        month_to_insert = "07"
    elif month == "August":
        month_to_insert = "08"
    elif month == "September":
        month_to_insert = "09"
    elif month == "October":
        month_to_insert = "10"
    elif month == "November":
        month_to_insert = "11"
    elif month == "December":
        month_to_insert = "12"
        
    return f"{year}-{month_to_insert}"

def convert_temperature_to_fahrenheit(degrees, celsius=False, farenheit=False):
    if (not celsius and not farenheit):
        return int(degrees)
    
    if (celsius):
       return int(degrees + 273.15)
   
    if (farenheit):
        return int((degrees - 32) * (5/9) + 273.15)

if __name__ == '__main__':
    app.run(debug=False)
