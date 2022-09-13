library(raster)
library(mapview)

# path
in_path<-  'R:/2022/22-037_Bundesanstalt_Bundesimmobilien_Sued_Aussenanlagen/07_Pix4D/5_001_Konstanz_Berchenstr/orthofoto_vlx'
out_path<- 'R:/2022/22-037_Bundesanstalt_Bundesimmobilien_Sued_Aussenanlagen/07_Pix4D/5_001_Konstanz_Berchenstr/orthofoto_vlx/geor'


rast_list<- list.files('R:/2022/22-037_Bundesanstalt_Bundesimmobilien_Sued_Aussenanlagen/07_Pix4D/5_001_Konstanz_Berchenstr/orthofoto_vlx', pattern = 'tif')
i<- 1
for (i in 1:length(rast_list)) {
  
  rast<- stack(paste0(in_path,'/',rast_list[i]))
  crs(rast)<- 25832
  writeRaster(rast,paste0(out_path,'/',rast_list[i]))
  print(i)
  
}



