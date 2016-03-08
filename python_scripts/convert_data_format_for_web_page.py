import os
import csv


# This list will hold final selected activity points data
data_filtered_checked_osm = list()


# Open act_pt_checked_against_osm.csv file and collect contained data.
proj_dir = os.getcwd()
rel_file_path = "data/act_pt_checked_against_osm.csv";
abs_file_path = os.path.join(proj_dir, rel_file_path)
with open(abs_file_path, 'rb') as new_data_csv:
	rows = csv.reader(new_data_csv, delimiter = ',')
	for row in rows:
		# Append rows into data_filtered_checked_osm list
		data_filtered_checked_osm.append(row);


# Create text file containing Bus Stops derived from activity_points.geojson file in suitable format for our web-page 
rel_file_path = "data/activity_pts_filtered_for_webpage.txt";
abs_file_path = os.path.join(proj_dir, rel_file_path)
with open(abs_file_path, 'w') as f:
	# Making text file for bus stops data.
	string_for_act_pt = "";
	for feature in data_filtered_checked_osm:
		if (feature[0] == "x" and feature[1] == "y"):
			# Ignore first row, which is attributes name.
			pass;
		else:
			string_for_act_pt += "{x: ";
			string_for_act_pt += str(feature[0]);
			string_for_act_pt += ", y: ";
			string_for_act_pt += str(feature[1]);
			string_for_act_pt += ", accuracy: ";
			string_for_act_pt += str(feature[2]);
			string_for_act_pt += ", total_confidence: ";
			string_for_act_pt += str(feature[3]);
			string_for_act_pt += ", osm_flag: ";
			string_for_act_pt += str(feature[4]);
			string_for_act_pt += "}, ";
	f.write(string_for_act_pt);


# This list will hold derived Bus Stop locations from OSM data
data_osm_bus_stations = list()


# Open osm_bus_stations.csv file and collect contained data.
rel_file_path = "data/osm_bus_stations.csv";
abs_file_path = os.path.join(proj_dir, rel_file_path)
with open(abs_file_path, 'rb') as new_data_csv:
	rows = csv.reader(new_data_csv, delimiter = ',')
	for row in rows:
		# Append all rows into data_osm_bus_stations list
		data_osm_bus_stations.append(row);


# Create text file containing Bus Stops derived from downloaded OSM data in suitable format for our web-page
rel_file_path = "data/osm_bus_stations_for_webpage.txt";
abs_file_path = os.path.join(proj_dir, rel_file_path)
with open(abs_file_path, 'w') as f:
	# Making text file for OSM bus stops data.
	string_for_osm_bus_stop = "";
	for feature in data_osm_bus_stations:
		if (feature[0] == "x" and feature[1] == "y"):
			# Ignore first row, which is attributes name.
			pass;
		else:
			string_for_osm_bus_stop += "{x: ";
			string_for_osm_bus_stop += str(feature[0]);
			string_for_osm_bus_stop += ", y: ";
			string_for_osm_bus_stop += str(feature[1]);
			string_for_osm_bus_stop += ", name: \"";
			string_for_osm_bus_stop += str(feature[2]);
			string_for_osm_bus_stop += "\"}, ";
	f.write(string_for_osm_bus_stop);


