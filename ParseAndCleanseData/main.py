'''
Created on Apr 1, 2020

@author: Dominic
'''

import os

from ConvertTemperatureHDFToCSV import ConvertTemperatureHDFToCSV
from CleanTemperatureData import CleanTemperatureData

DIRECTORY = ### Insert your File Directory Path for your Data #######
COUNTRY_FILE = "country/ARG_adm0.shp"
FILE_DATE_START_INDEX = ### 
FILE_DATE_END_INDEX = ###

if __name__ == '__main__':
    for filename in os.listdir(DIRECTORY):
        if filename.endswith(".hdf"):
            
            #Append the name of the file without the typing incase we need to append more later on
            name_of_file = DIRECTORY + "\\" + filename[FILE_DATE_START_INDEX:FILE_DATE_END_INDEX]
            csv_name = name_of_file + ".csv"
            
            print(csv_name)
            
            converter = ConvertTemperatureHDFToCSV(DIRECTORY + "\\" + filename, csv_name)
            converter.convert_hdf_to_csv()
            
            cleansed_csv_name = name_of_file + "_final.csv"
            cleanser = CleanTemperatureData(csv_name, cleansed_csv_name,COUNTRY_FILE)
            cleanser.clean_and_save_data()
            
            continue
        else:
            continue
    print("Done")