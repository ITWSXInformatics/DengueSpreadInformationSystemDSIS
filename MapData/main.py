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
TEMPERATURE_COLUMN = "TAVG"
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
    start_coords = (-3.7437, -73.2516)
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
        show=False
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
    
    folium_map.save('templates/map.html')
    
    return render_template("index.html")

@app.route('/background')
def project_background():
    return render_template("background.html")

@app.route('/team')
def project_members():
    return render_template("the_team.html")

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
    temperature = "Unknown"
    precipitation = "Unknown"
    
    population_vals = data[POPULATION_COLUMN].values
    temperature_vals = data[TEMPERATURE_COLUMN].values
    precipitation_vals = data[PRECIPITATION_COLUMN].values
    
    if len(population_vals) > 0 and not math.isnan(population_vals[0]):
        population = data[POPULATION_COLUMN].values[0]
    
    if len(temperature_vals) > 0 and not math.isnan(temperature_vals[0]):
        temperature = data[TEMPERATURE_COLUMN].values[0]
        
    if len(precipitation_vals) > 0 and not math.isnan(precipitation_vals[0]):
        precipitation = data[PRECIPITATION_COLUMN].values[0]
    
    info_message = f"""Temp: {temperature}\n
                       Precip: {precipitation}\n
                       Pop: {population}
                    """ 
    folium.Marker(
                     location = coordinates,
                     popup = info_message,
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

if __name__ == '__main__':
    app.run(debug=False)
