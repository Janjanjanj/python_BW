# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 11:21:53 2022

@author: j.kraemer
"""

from osgeo import gdal
from osgeo import osr
import os

# path of the raster without coordinate system 
path = 'R:/2022/22-037_Bundesanstalt_Bundesimmobilien_Sued_Aussenanlagen/07_Pix4D/5_001_Konstanz_Berchenstr/orthofoto_vlx/'


files = [f for f in os.listdir(path) if f.endswith('.tif')]


for k in range(len(files)):
    ds = gdal.Open(path+files[1])
    sr = osr.SpatialReference()
    sr.ImportFromEPSG(25832)
    ds.SetProjection(sr.ExportToWkt())
    del ds










