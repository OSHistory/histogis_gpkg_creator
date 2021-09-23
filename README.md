# README 

## PSA: ogr2ogr dependency 

## You need to install ogr2ogr to run this script. 


This simple python script is a wrapper around `ogr2ogr` to 
convert a data dump from the excellent [HistoGis Project](https://histogis.acdh.oeaw.ac.at/)
into a single geopackage. 

You should read the [Project presentation](https://zenodo.org/record/2611667#.YUzj4DqxU5k) (in german)

## Usage 

See `python3 histogis_dump_to_geopackage.py -h`

The script tries to group features in convenient layers. 

## Data 

Download a zipped thematic data download, e.g. [this one](https://zenodo.org/record/3726852#.YUzqcTqxU5k)


## Examples 

### Group by attribute

By default the features are grouped by the `source_name` attribute (that is the original layer that the histogis team relied upon). Since that would lead 
in multiple layers with the timestamp at the end, the script strips 
digits at the end of the string (you can turn that behaviour off with `--no-year-strip`)

```
python3 histogis_dump_to_geopackage.py -d path/to/single_files/ -g histogis-geodata-source-group.gpkg -s 3857 
```

### Group by parent 

Alternatively you can group the features by their top level parent. 

The following will create a geopackage where all features are grouped by their (last) 
parent, or if no parent is present by their name-attribute. 

```sh
python3 histogis_dump_to_geopackage.py -d path/to/single_files/ -g histogis-geodata.gpkg -s 3857  -p
```



