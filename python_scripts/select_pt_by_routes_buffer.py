import json
import csv
from osgeo import ogr
import os


# Open routes.geojson file and collect contained data.
proj_dir = os.getcwd()
rel_file_path = "data/routes.geojson";
abs_file_path = os.path.join(proj_dir, rel_file_path)
with open(abs_file_path) as data_file:
	data = json.load(data_file)


# Create text file containing bus routes data in suitable format for our web-page 
rel_file_path = "data/routes_for_webpage.txt";
abs_file_path = os.path.join(proj_dir, rel_file_path)
with open(abs_file_path, 'w') as f:
	# Making text file for bus routes data.
	string_for_route = "";
	for feature in data['features']:
		string_for_route += "[";
		for coord in feature['geometry']['coordinates']:
			string_for_route += "{lng: ";
			string_for_route += str(coord[0]);
			string_for_route += ", lat: ";
			string_for_route += str(coord[1]);
			string_for_route += "},"
		string_for_route += "],"
	f.write(string_for_route)


# Create a Well-Known-Text file and store the WKT data of the polygon formed by buffering (at a given width) routes.geojson lines.
rel_file_path = "data/routes_buffered.wkt";
abs_file_path = os.path.join(proj_dir, rel_file_path)
with open(abs_file_path, 'w') as f:
	# Making WKT for data in routes.geojson
	multilinestring = "MULTILINESTRING ("
	for feature in data['features']:
		multilinestring += "("
		for coord in feature['geometry']['coordinates']:
			multilinestring += str(coord[0])
			multilinestring += " "
			multilinestring += str(coord[1])
			multilinestring += ","
		multilinestring = multilinestring[:-1]
		multilinestring += ")"
		multilinestring += ","
	multilinestring = multilinestring[:-1]
	multilinestring += ")"
	# Creating geometry from WKT
	multilinestring_geom = ogr.CreateGeometryFromWkt(multilinestring)
	# This following buffer_in_deg value is a matter of preference. Since CRS is in WGS84, degree unit has been used. 
	# For Dar Es Salam, 0.001 deg is approx. 110 meters.
	buffer_in_deg = 0.001
	# Buffering routes data.
	multilinestring_buffered = multilinestring_geom.Buffer(buffer_in_deg)
	# Saving buffered polygon into WKT file in WKT format
	f.write(multilinestring_buffered.ExportToWkt())


# This list will hold those activity pts which are inside the buffer of routes data.
data_filtered_buffered = list()


# Read act_pt_selected_by_dominating_activity.csv file and check for whether they are inside the routes buffer or not.
rel_file_path = "data/act_pt_selected_by_dominating_activity.csv";
abs_file_path = os.path.join(proj_dir, rel_file_path)
with open(abs_file_path, 'rb') as new_data_csv:
	rows = csv.reader(new_data_csv, delimiter = ',')
	for row in rows:
		if (row[0] == "x" and row[1] == "y"):
			# Ignore first row, which is attributes name.
			pass;
		else:
			# Making WKT for activity points
			point = "POINT ("
			point += str(row[0])
			point += " "
			point += str(row[1])
			point += ")"
			# Creating geometry from WKT
			point_geom = ogr.CreateGeometryFromWkt(point)
			multilinestring_buffered_polygon = ogr.CreateGeometryFromWkt(multilinestring_buffered.ExportToWkt())
			# Calculate intersected geometry in WKT
			intersection = point_geom.Intersection(multilinestring_buffered_polygon)
			# If the intersected geometry is "GEOMETRYCOLLECTION EMPTY", then there is no intersection, otherwise there is.
			# Eventually, append activity pt WKT into data_filtered_buffered list
			if (intersection.ExportToWkt() == "GEOMETRYCOLLECTION EMPTY"):
				pass;
			else:
				data_filtered_buffered.append(row);



# Output data_filtered_buffered list to a csv file
rel_file_path = "data/act_pt_selected_by_routes_buffer.csv";
abs_file_path = os.path.join(proj_dir, rel_file_path)
with open(abs_file_path, 'wb') as f:
	writer = csv.writer(f, delimiter = ',')
	data_input = ['x', 'y', 'accuracy', 'total_confidence']
	writer.writerow(data_input)
	for feature in data_filtered_buffered:
		data_input = [feature[0], feature[1], feature[2], feature[3]]
		writer.writerow(data_input)
		
		