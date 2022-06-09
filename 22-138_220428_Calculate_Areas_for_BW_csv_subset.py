# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 13:38:30 2022

@author: J.Kraemer
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 09:10:19 2022

@author: J.Kraemer
"""

import geopandas as gpd
import glob
import pandas as pd
import numpy as np
import os
from shapely.ops import cascaded_union
import openpyxl

# strassennamen
strassenname = '220412_BW_Otto-Konz-Strasse'

# open the csv file were data is stored 
csv = pd.read_csv('V:/_Projekte/22-037_Bundesanstalt_Bundesimmobilien_Sued_Aussenanlagen/01_Vorgaben/Python_Vorlagen/BW_tabelle_nur_flur.csv', sep = ';')

# path of the shapefile
path_flaeche = "V:/_Projekte/22-037_Bundesanstalt_Bundesimmobilien_Sued_Aussenanlagen/04_Auswertung/02_Auswertung_GIS/BW/Auswertung/"+strassenname+'/'
path_flur = "V:/_Projekte/22-037_Bundesanstalt_Bundesimmobilien_Sued_Aussenanlagen/04_Auswertung/02_Auswertung_GIS/BW/flurstuecke/"


# import flurstueck shapefile 
flur = gpd.read_file(path_flur + 'flurstuecke_bw.shp')

# import the flaeche shapefile 
flaeche = gpd.read_file(path_flaeche+"flaeche/flaeche.shp")
linie = gpd.read_file(path_flaeche+"linie/VF_oef_Gehweg.shp")

# dissolve the flaeche layer 
flaeche_diss = flaeche.dissolve(by = 'Layer')

# intersect flur and flaeche 
#inter_flaeche = gpd.sjoin(flaeche, flur, how="inner", op='intersects')
inter_flur = gpd.sjoin(flur, flaeche, how="inner", op='intersects')

# get all flurstuck names and than select the first one 
flurnames_all = inter_flur.flurstnr.value_counts()

# subset the csv table (optinal)
liste_flurnames = list(flurnames_all.index)
csv = csv[csv["Flurstnr"].isin(liste_flurnames)].reset_index(drop=True)

i = 1
for i in range(len(csv)):
    
    flurnr = flurnames_all.index[i]

    # subset flurstuck Nr 1
    subs = flur[flur['flurstnr'] == flurnr]

    # clip 
    clip = gpd.clip(flaeche_diss, subs)
    clip['a'] = clip.area

    # two lists: first is the area of each Layer and second Layername  
    list_area = [round(num,1) for num in clip['a']]
    list_name = list(clip.index)

    data1 = pd.DataFrame(list_area)
    data2 = pd.DataFrame(list_name)

    bigdata = pd.concat([data2, data1], axis=1)
    bigdata = bigdata.set_axis(["Layer","a"], axis=1)


    # get index of the fitting flurstrnummer and select row
    #flur_index = flur[flur['flurstnr'] == flurnr].index[0]
    flur_index = csv[csv["Flurstnr"] == flurnr].index[0]

    # this loops through for one flurstueck and adds the fitting flache areas to the csv  
    liste_layer = bigdata['Layer'].tolist()
    liste_area  = bigdata['a'].tolist()

    for x in range(len(bigdata)):
       
        a = csv.columns.get_loc(liste_layer[x])
        csv.iloc[[flur_index],a] = liste_area[x]
    
    print(sum(clip.area)-sum(subs.area))
    print(i) 
    
    
    

# calculate the sum area for each row (quality check)
csv['Vermessen_area'] = csv.iloc[:,].sum(axis=1)

# merge the 
merged =  pd.merge(flur,csv, left_on='Flurstï_1', right_on= 'Flurstnr').drop(['geometry','path','gescannt'], axis=1)

# qualitycheck differenz zsischen Fläche und Vermessen  
merged['Qualitycheck_differenz'] = merged['flaeche']-merged['Vermessen_area']

###### part for the line 
linie = gpd.read_file(path_flaeche+"linie/VF_oef_Gehweg.shp")
linie = linie.to_crs(epsg=25832)
linie_diss = linie.dissolve(by = 'Layer')
linie = gpd.overlay(linie, flur, how="intersection")
linie['length'] = linie.length
test = pd.merge(merged,linie, on = ['width'] how = 'outer')
linie.columns
test = pd.merge(merged, linie, how ='outer')
merged['VF_oef_Gehweg_leange'] = test['length']
merged['VF_oef_Gehweg_flaeche'] = test['length']*1.70

# save the csv file 
file_name = 'V:/_Projekte/22-037_Bundesanstalt_Bundesimmobilien_Sued_Aussenanlagen/04_Auswertung/04_Auswertung_Tabellen/BW/'+strassenname+'.xlsx' 
merged.to_excel(file_name)




#xyz









