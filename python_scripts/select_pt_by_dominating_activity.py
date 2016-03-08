import json
import csv
import os


# Open activity_points.geojson file and collect contained data.
proj_dir = os.getcwd()
rel_file_path = "data/activity_points.geojson";
abs_file_path = os.path.join(proj_dir, rel_file_path)
with open(abs_file_path) as data_file:
	data = json.load(data_file)


# Create text file containing activity_points.geojson file data in suitable format for our web-page 
rel_file_path = "data/activity_pts_for_webpage.txt";
abs_file_path = os.path.join(proj_dir, rel_file_path)
with open(abs_file_path, 'w') as f:
	# Making text file for activity points.
	string_for_act_pt = "";
	for feature in data['features']:
		string_for_act_pt += "{x: ";
		string_for_act_pt += str(feature['geometry']['coordinates'][0]);
		string_for_act_pt += ", y: ";
		string_for_act_pt += str(feature['geometry']['coordinates'][1]);
		string_for_act_pt += ", pda: \"";
		string_for_act_pt += str(feature['properties']['previous_dominating_activity']);
		string_for_act_pt += "\", pdac: ";
		string_for_act_pt += str(feature['properties']['previous_dominating_activity_confidence']);
		string_for_act_pt += ", cda: \"";
		string_for_act_pt += str(feature['properties']['current_dominating_activity']);
		string_for_act_pt += "\", cdac: ";
		string_for_act_pt += str(feature['properties']['current_dominating_activity_confidence']);
		string_for_act_pt += ", speed: ";
		string_for_act_pt += str(feature['properties']['speed']);
		string_for_act_pt += ", accuracy: ";
		string_for_act_pt += str(feature['properties']['accuracy']);
		string_for_act_pt += "}, ";
	f.write(string_for_act_pt);


# A list which will store the filtered features based on dominating activity
data_filtered = list()


# A for loop to collect activity pts based on previous_dominating_activity and current_dominating_activity
for feature in data['features']:	
	pda = feature['properties']['previous_dominating_activity'] # Make a read-able variable
	cda = feature['properties']['current_dominating_activity'] # Make a read-able variable
	if ((pda == "still" or pda == "on_foot" or pda == "on_bicycle") and cda == "in_vehicle"):
		data_filtered.append(feature)
	elif (pda == "in_vehicle" and (cda == "still" or cda == "on_foot" or cda == "on_bicycle")):
		data_filtered.append(feature)
	elif (pda is None and cda == "in_vehicle"):
		data_filtered.append(feature)
	elif (pda == "in_vehicle" and cda is None):
		data_filtered.append(feature)
	else:
		# These are the cases when neither previous nor current dominating activity is "in_vehicle". 
		# And hence, not considered because of very less probability of showing any bus stop.
		pass;
		

# A list to contain above selected activity pts along with their total confidence value.
data_filtered_modified = list()


# A for loop to populate data_filtered_modified list.
for feature in data_filtered:
	pdac = feature['properties']['previous_dominating_activity_confidence']
	cdac = feature['properties']['current_dominating_activity_confidence']
	speed = feature['properties']['speed']
	# The following formula to calculate total_confidence of an activity pt being a bus stop is entirely based upon observation.
	# Ideally, high pdac and cdac, and low speed will strengthen the possibility of a near by bus stop.
	# Speed has been further added by 1 to avoid 0 value of denominator.  
	total_confidence = (pdac * cdac)/(speed + 1)
	dic = {}
	dic['geometry'] = feature['geometry']['coordinates']
	dic['accuracy'] = feature['properties']['accuracy']
	dic['total_confidence'] = total_confidence
	data_filtered_modified.append(dic)


# Output data_filtered_modified list to a csv file
rel_file_path = "data/act_pt_selected_by_dominating_activity.csv";
abs_file_path = os.path.join(proj_dir, rel_file_path)
with open(abs_file_path, 'wb') as f:
	writer = csv.writer(f, delimiter = ',')
	data_input = ['x', 'y', 'accuracy', 'total_confidence']
	writer.writerow(data_input)
	for feature in data_filtered_modified:
		data_input = [feature['geometry'][0], feature['geometry'][1], feature['accuracy'], feature['total_confidence']]
		writer.writerow(data_input)


