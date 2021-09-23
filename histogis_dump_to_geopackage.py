import argparse 
import glob 
import json
import os
import re
import subprocess 

# TODO: Test for ogr2ogr in path 

ap = argparse.ArgumentParser("Read all single .geojson files into one geopackage layer")
ap.add_argument("-d", "--directory", required="True")
ap.add_argument("-g", "--geopackage", required="True")
ap.add_argument("-l", "--layer-name")
ap.add_argument("-a", "--attribute", help="Group the features by this attribute (overrides layername)", default="source_name")
ap.add_argument("--no-year-strip", action="store_true", help="Strip the year from the attribute (usefull if attribute grouping by source_name)")
ap.add_argument("-p", "--parent-grouping", action="store_true", help="Use the features parent info for the layer grouping (overrides attribute and layername)")
ap.add_argument("--force-single", action="store_true", help="Force mergin all objects into a single layer (same as geopackage, except set by -l")
ap.add_argument("-s", "--srs", type=int, help="EPSG:Code (Integer)")

args = ap.parse_args()


all_geojson = glob.glob(os.path.join(args.directory, "*.geojson"))

target_dir = os.path.dirname(args.geopackage)

if not args.layer_name:
    default_layer_name = os.path.basename(args.geopackage).replace(".gpkg", "")
else:
    default_layer_name = args.layer_name

if not os.path.exists(target_dir) and target_dir.strip() != "":
    os.makedirs(target_dir)

for geojson in all_geojson:
    print(geojson)
    # Needs to read from the properties
    if not args.force_single:
        try:
            with open(geojson) as fh:
                geo_cont = json.load(fh)
        except Exception as e:
            print("Error decoding " + geojson)
            print("Adding to default layer: " + default_layer_name)
            layer_name = default_layer_name
            print(e)
        if args.parent_grouping:
            parents = geo_cont["properties"]["parents"]
            # no parents -> Top Level, use the features name as the layer
            if not len(parents):
                layer_name = geo_cont["properties"]["name"]
            else:
                layer_name = parents[-1]["name"]
        # no parent grouping and no forced single layer 
        # -> use the default attribute (as defined by argparser)
        else:
            layer_name = geo_cont["properties"][args.attribute]
            if not args.no_year_strip:
                layer_name = re.sub(" +\d+", "", layer_name)
        # sample dataset had invalid json data (UTF-8 encoding)
    ogr_call = ["ogr2ogr", 
        args.geopackage,
        "-nln", layer_name, 
        "-append"]
    if args.srs:
        ogr_call.extend(["-t_srs", "EPSG:" + str(args.srs)])
    ogr_call.append(geojson)
    subprocess.call(ogr_call)
