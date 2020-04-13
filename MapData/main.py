# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 15:55:57 2020

@author: Dominic
"""
from flask import Flask, render_template
from geopy.geocoders import Nominatim
import folium
import pandas as pd

ARGENTINA_GEO_DATA = "argentina-provinces.json"

app = Flask(__name__)
app.add_url_rule('/images/<path:filename>', endpoint='images', view_func=app.send_static_file)

@app.route('/')
def homepage():
    
    start_coords = (-22.5, -66.5)
    folium_map = folium.Map(location=start_coords, zoom_start=4)
    
    arg_data = pd.read_csv(####### INSERT FILE NAME HERE ################)
    
    folium.Choropleth(
        geo_data="ARG_adm1.json",
        name='choropleth',
        data=arg_data,
        columns=['Providences', 'Temperatures'],
        key_on='feature.properties.NAME_1',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Temperature (K)',
        show=False
    ).add_to(folium_map)
    
    folium.LayerControl().add_to(folium_map)
    
    folium_map.save('templates/map.html')
    
    return render_template("index.html")

@app.route('/background')
def project_background():
    return render_template("background.html")

@app.route('/team')
def project_members():
    return render_template("the_team.html")

if __name__ == '__main__':
    app.run(debug=False)
