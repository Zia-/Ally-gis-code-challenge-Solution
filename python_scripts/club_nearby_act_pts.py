import csv
import math
import os


# This list will hold act_pt_selected_by_routes_buffer.csv data along with two flags.
data_club_pts = list()


# Open routes.geojson file and collect contained data.
proj_dir = os.getcwd()
rel_file_path = "data/act_pt_selected_by_routes_buffer.csv";
abs_file_path = os.path.join(proj_dir, rel_file_path)
with open(abs_file_path, 'rb') as buff_data_csv:
	rows = csv.reader(buff_data_csv, delimiter = ',')
	for row in rows:
		if (row[0] == "x" and row[1] == "y"):
			# Ignore first row, which is attributes name.
			pass;
		else:
			# Feed data_club_pts list.
			dic = {}
			dic['x'] = row[0];
			dic['y'] = row[1];
			dic['accuracy'] = row[2];
			dic['total_confidence'] = row[3];
			# We need "flag_repeat" and "flag_done" flags to for loops in the following code section
			dic['flag_repeat'] = 0;
			dic['flag_done'] = 0;
			# Append dictionary into list
			data_club_pts.append(dic)


# Loop through data_club_pts list and check if there are pts with displacement less than a particular threshold.
# Thus we will remove duplicated activity points refering to same bus stop.
for row1 in data_club_pts:
	# Change "flag_done" value to -1 for already inspected points
	row1['flag_done'] = -1
	for row2 in data_club_pts:
		if (row2['flag_done'] == -1):
			pass;
		else:
			# Calculate the great circle distance between every possible pair of act_pt_selected_by_routes_buffer.csv points.
			long1 = float(row1['x'])
			lat1 = float(row1['y'])
			long2 = float(row2['x'])
			lat2 = float(row2['y'])
			rLat1 = math.radians(lat1)
			rLong1 = math.radians(long1)
			rLat2 = math.radians(lat2)
			rLong2 = math.radians(long2)
			dLat = rLat2 - rLat1
			dLong = rLong2 - rLong1
			a = math.sin(dLat/2)**2 + math.cos(rLat1) * math.cos(rLat2) * math.sin(dLong/2)**2
			c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
			# 6371000 meter is the radius of Earth
			distance = 6371000 * c
			# If above calculated distance between any two pt is less than a particular threshold, then change "flag_repeat" of the second pt.
			# Here, 200 meter corresponds to 0.002 degree spatial displacement. It is a matter of statistics.
			if (distance < 200): 
				row2['flag_repeat'] = 1
			else:
				# Ignore. Do not change "flag_repeat" default value ie. 0.
				pass;


# This list will hold only those activity pts which are separated more than the above declared threshold
data_club_pts_final = list()


# For loop to descard repeated, so called, bus stop locations
for row in data_club_pts:
	if (row['flag_repeat'] == 0):
		# Append row into data_club_pts_final list.
		data_club_pts_final.append(row)
	else:
		# Ignore.
		pass;


# Output data_club_pts_final list to a csv file
rel_file_path = "data/act_pt_clubbed_nearby_pts.csv";
abs_file_path = os.path.join(proj_dir, rel_file_path)
with open(abs_file_path, 'wb') as f:
	writer = csv.writer(f, delimiter = ',')
	data_input = ['x', 'y', 'accuracy', 'total_confidence']
	writer.writerow(data_input)
	for feature in data_club_pts_final:
		data_input = [feature['x'], feature['y'], feature['accuracy'], feature['total_confidence']]
		writer.writerow(data_input)



