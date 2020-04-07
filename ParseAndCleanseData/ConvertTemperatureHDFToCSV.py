'''
Created on Apr 1, 2020

@author: Dominic
'''
import pandas as pd
from pyhdf import SD

class ConvertTemperatureHDFToCSV(object):

    def __init__(self, hdf_file_path, csv_file_path):
        self.hdf_file_path = hdf_file_path
        self.csv_file_path = csv_file_path
        
    def convert_hdf_to_csv(self):
        try:
            hdf = SD.SD(self.hdf_file_path)
        except:
            print("Unable to open the file: ",self.hdf_file_path)
        
        """
        Flatten and remove duplicates from the Latitudes and
        Logititude datasets
        """
        lat_dataset = hdf.select('Latitude')
        latitudes = lat_dataset[:].flatten()
        
        long_dataset = hdf.select('Longitude')
        longitudes = long_dataset[:].flatten()
        
        surface_temp_dataset = hdf.select('SurfSkinTemp_Forecast_A')
        surface_temps = surface_temp_dataset[:].flatten()
        
        pandas_dict = {}
        
        pandas_dict["Latitudes"] = latitudes
        pandas_dict["Longitudes"] = longitudes
        pandas_dict["Temperature"] = surface_temps
        
        data_frame = pd.DataFrame(pandas_dict, columns=["Latitudes", "Longitudes", "Temperature"])
        data_frame.to_csv(self.csv_file_path)            