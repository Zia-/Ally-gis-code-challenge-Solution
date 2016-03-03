import csv
from xml.dom import minidom
from osgeo import ogr
import os


# This list will hold collected OSM bus stop locations from osm file.
osm_bus_stations = list()


# OSM data of Dar Es Salam can be downloaded from http://overpass.osm.rambler.ru/cgi/xapi_meta?*[bbox=39.0640,-7.1170,39.5269,-6.5767]
proj_dir = os.getcwd()
rel_file_path = "data/dar_es_salam.osm";
abs_file_path = os.path.join(proj_dir, rel_file_path)
xmldoc = minidom.parse(abs_file_path)


# Collecting lat, long, and name values of bus stations from OSM data
node = xmldoc.getElementsByTagName("node")
for n in node:
        lat = n.getAttribute("lat")
        lon = n.getAttribute("lon")
        tag = n.getElementsByTagName("tag")
        for t in tag:
        	v = t.getAttribute('v')
        	# In OSM we can only define bus stations by two type of values ie. "bus_stop" or "bus_station"
        	# Link http://wiki.openstreetmap.org/wiki/Map_Features 
        	if (v == "bus_stop" or v == "bus_station"): # If YES then implies this is a bus station node
        		count = 0;
        		for t1 in tag:
        			k1 = t1.getAttribute('k')
        			v1 = t1.getAttribute('v')
        			if (k1 == "name"): # If YES then implies there is name also available for that bus station
        				# Append lat, lon, and name values into osm_bus_station list
        				dic = {}
        				dic['x'] = lon;
        				dic['y'] = lat;
        				dic['name'] = v1;
        				osm_bus_stations.append(dic)
        				count += 1;
        				break;
        		if (count == 0):
        			# Append lat, and lon values into osm_bus_station list
        			dic = {}
        			dic['x'] = lon;
        			dic['y'] = lat;
        			dic['name'] = " ";
        			osm_bus_stations.append(dic)
        	else:
        		# Ignore, since these nodes are not bus station
        		pass;


# Output osm_bus_stations list to a csv file. This will be our data from OSM for comparision
rel_file_path = "data/osm_bus_stations.csv";
abs_file_path = os.path.join(proj_dir, rel_file_path)
with open(abs_file_path, 'wb') as f:
	writer = csv.writer(f, delimiter = ',')
	data_input = ['x', 'y', 'name']
	writer.writerow(data_input)
	for feature in osm_bus_stations:
		data_input = [feature['x'], feature['y'], feature['name']]
		writer.writerow(data_input)


# This list will hold act_pt_clubbed_nearby_pts.csv data
data_club_pts = list()


# Feed data_club_pts list 
rel_file_path = "data/act_pt_clubbed_nearby_pts.csv";
abs_file_path = os.path.join(proj_dir, rel_file_path)
with open(abs_file_path, 'rb') as buff_data_csv:
	rows = csv.reader(buff_data_csv, delimiter = ',')
	for row in rows:
		# Append data into data_club_pts list
		data_club_pts.append(row)


# This list will hold data_club_pts data along with "osm_flag" flag valuel.
# This flag value will let us know whether our act_pt_clubbed_nearby_pts.csv pts are nearby to any osm bus station, or not.
# We will use any arbitrary threshold value to update "osm_flag" value 
data_filtered_osm = list()


# For loop to traverse all act_pt_clubbed_nearby_pts pts to compare them against osm bus station points.
for row1 in data_club_pts:
	if (row1[0] == "x" and row1[1] == "y"):
		# Ignore first row, which is attributes name.
		pass;
	else:
		count = 0;
		for row2 in osm_bus_stations:
			# Making WKT for activity points
			cal_point = "POINT ("
			cal_point += str(row1[0])
			cal_point += " "
			cal_point += str(row1[1])
			cal_point += ")"
			# Creating geometry from WKT
			cal_point_geom = ogr.CreateGeometryFromWkt(cal_point)
			# Making WKT for osm bus station points
			osm_point = "POINT ("
			osm_point += str(row2['x'])
			osm_point += " "
			osm_point += str(row2['y'])
			osm_point += ")"
			# Creating geometry from WKT
			osm_point_geom = ogr.CreateGeometryFromWkt(osm_point)
			# This following buffer_in_deg value is a matter of preference. Since CRS is in WGS84, degree unit has been used. 
			# For Dar Es Salam, 0.009 deg is approx. 1000 meters.
			buffer_in_deg = 0.009
			# Buffering osm bus station data.
			osm_point_geom_buffered = osm_point_geom.Buffer(buffer_in_deg)
			# Calculate intersected geometry in WKT
			intersection = cal_point_geom.Intersection(osm_point_geom_buffered)
			# If the intersected geometry is "GEOMETRYCOLLECTION EMPTY", then there is no intersection (means they are close), otherwise there is.
			if (intersection.ExportToWkt() == "GEOMETRYCOLLECTION EMPTY"):
				# Do not increment the value of count
				pass;
			else:
				# Increment the value of count, and break the for loop. Because there is no need to check for other osm bus stations about proximity.
				count += 1;
				break;
		# If count is 1 there that act_pt_clubbed_nearby_pts pt is close to an osm bus station. Assign 1 value to "osm_flag" flag
		if (count == 1):
			dic = {}
			dic['x'] = row1[0];
			dic['y'] = row1[1];
			dic['accuracy'] = row1[2];
			dic['total_confidence'] = row1[3];
			dic['osm_flag'] = 1;
			# Append data_filtered_osm list
			data_filtered_osm.append(dic)
		# Else assign 0 value to "osm_flag" flag
		else:
			dic = {}
			dic['x'] = row1[0];
			dic['y'] = row1[1];
			dic['accuracy'] = row1[2];
			dic['total_confidence'] = row1[3];
			dic['osm_flag'] = 0;
			# Append data_filtered_osm list
			data_filtered_osm.append(dic)


# Output data_filtered_osm list to a csv file
rel_file_path = "data/act_pt_checked_against_osm.csv";
abs_file_path = os.path.join(proj_dir, rel_file_path)
with open(abs_file_path, 'wb') as f:
	writer = csv.writer(f, delimiter = ',')
	data_input = ['x', 'y', 'accuracy', 'total_confidence', 'osm_flag']
	writer.writerow(data_input)
	for feature in data_filtered_osm:
		data_input = [feature['x'], feature['y'], feature['accuracy'], feature['total_confidence'], feature['osm_flag']]
		writer.writerow(data_input)