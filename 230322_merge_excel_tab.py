# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 11:22:23 2023

@author: r.proelss
"""


# importing the required modules
import glob
import pandas as pd
 
# specifying the path to csv files
path = "V:/_Projekte/22-037_Bundesanstalt_Bundesimmobilien_Sued_Aussenanlagen/04_Auswertung/04_Auswertung_Tabellen/überarbeitet/Stand_März_By"
 
# csv files in the path
file_list = glob.glob(path + "/*.xlsx")
 
# list of excel files we want to merge.
# pd.read_excel(file_path) reads the excel
# data into pandas dataframe.
excl_list = []
 
for file in file_list:
    excl_list.append(pd.read_excel(file))
 
# create a new dataframe to store the
# merged excel file.
excl_merged = pd.DataFrame()
 
for excl_file in excl_list:
     
    # appends the data into the excl_merged
    # dataframe.
    excl_merged = excl_merged.append(
      excl_file, ignore_index=True)
 
# exports the dataframe into excel file with
# specified name.
excl_merged.to_excel('V:/_Projekte/22-037_Bundesanstalt_Bundesimmobilien_Sued_Aussenanlagen/04_Auswertung/04_Auswertung_Tabellen/überarbeitet/Tabelle_By.xlsx', index=False)
