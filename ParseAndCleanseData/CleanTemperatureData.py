# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 18:55:17 2020

@author: Dominic
"""
import pandas as pd
import descartes
import geopandas as gpd
from geopandas.tools import sjoin
from shapely.geometry import Point, Polygon, shape

class CleanTemperatureData(object):
    
    def __init__(self,csv_file_path, cleansed_csv_name, country_file_path):
        self.csv_file_path = csv_file_path
        self.country_file_path = country_file_path
        self.cleansed_csv_name = cleansed_csv_name
        self.__read_files()
        
    def __read_files(self):
        self.dataset = pd.read_csv(self.csv_file_path)
        self.argentina = gpd.read_file(self.country_file_path)
        
    def clean_and_save_data(self):
        latitudes = self.dataset.get("Latitudes")
        longitudes = self.dataset.get("Longitudes")
        geometry = [Point(xy) for xy in zip(longitudes, latitudes)]
        points = gpd.GeoDataFrame(self.dataset, geometry = geometry)
        points.crs = self.argentina.crs
        
        final_df = sjoin(points, self.argentina, how = 'inner', op = 'intersects')
        
        # TODO: Temporary fix for now; need to analyze why the sjoin is causing 
        #       the latitudes and longitudes to flip
        corrected_points = []
        for point in final_df["geometry"]:
            corrected_point = Point(point.y, point.x)
            corrected_points.append(corrected_point)
        final_df["geometry"] = corrected_points
        
        final_df = final_df[["Latitudes", "Longitudes", "Temperature", "geometry"]].reset_index(drop = True)
        final_df.to_csv(self.cleansed_csv_name, index = False)
