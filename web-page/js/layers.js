// This array will hold all markers which will display calculated filterted bus stations
var markers = [];

// This fun will be called by fun_cal_bus_stops fun
function setMapOnAll(map) {
	// Loop through all calculated filtered bus stations
	for (var i=0; i < list.length; ++i){
		var location = {lat: list[i].y, lng: list[i].x};
		// We are using total_confidence value to alter marker's size. 
		// Bigger size means high total_confidence, and vice versa.
		var scale = 0.003*(list[i].total_confidence)+15
		// Infowindow which will show the accuracy value of each location
		infoWindow = new google.maps.InfoWindow({})
		// The following if else will change the color of marker, depending upon
		// the proximity with respect to the selected OSM bus stations.
		// Red marker means close, and vice versa.
		if (list[i].osm_flag == 1){
			// Defining image, which will be used in google.map.marker
			var image = {
		    	url: 'icon/calculated_bus_stop_close_from_osm_bus_stop.png',
		    	scaledSize: new google.maps.Size(scale, scale),
		  	};
		}
		else {
			var image = {
		    	url: 'icon/calculated_bus_stop_away_from_osm_bus_stop.png',
		    	scaledSize: new google.maps.Size(scale, scale),
		  	};
		}
		// Defining marker
		var mar = new google.maps.Marker({
	      position: location,
	      map: var_map,
	      content: "Accuracy: " + String(list[i].accuracy),
	      icon: image, // More icons: http://kml4earth.appspot.com/icons.html
	      zIndex: 2,
	    });
		// Defining mouseover event handler
		google.maps.event.addListener(mar, 'mouseover', function() {
			infoWindow.setContent(this.content),
			infoWindow.open(var_map, this);
		});
		// Defining mouseout event handler
		google.maps.event.addListener(mar, 'mouseout', function() {
			infoWindow.close(var_map, this);
		});
		// Append all markers into markers array
	    markers.push(mar);
	}
	// Loop through all elements of markers array and feed into the map
	for (var i = 0; i < markers.length; i++) {
	  markers[i].setMap(map);
	}
}

// This fun is attached to "Crowdsourced Bus Stops" checkbox
function fun_cal_bus_stops(){
  var remember = document.getElementById('cb_cal_bus_stops');
  // Following if else is for toggle functionality
  if (remember.checked){ 
    setMapOnAll(var_map);
  }
  else{
    setMapOnAll(null);
  }
}

//-------------------------------------------------------------------------------

// This array will hold all markers which will display OSM selected bus stations
var markers_osm = [];

// This fun will be called by fun_osm_bus_stops fun
function setMapOnAll_osm(map) {
	// Loop through all OSM bus stations
	for (var i=0; i < list_osm.length; ++i){
		var location = {lat: list_osm[i].y, lng: list_osm[i].x};
		// Infowindow which will show the name value of each location
		infoWindow = new google.maps.InfoWindow({})
		// Defining image, which will be used in google.map.marker
		var image = {
		    url: 'icon/osm_bus_stop.png',
		    scaledSize: new google.maps.Size(20, 20),
		  };
		// Defining marker
		var mar = new google.maps.Marker({
	      position: location,
	      map: var_map,
	      icon: image,
	      content: "Bus Stop: " + String(list_osm[i].name),
	      zIndex: 1,
	    });
		// Defining mouseover event handler
	    google.maps.event.addListener(mar, 'mouseover', function() {
			infoWindow.setContent(this.content),
			infoWindow.open(var_map, this);
		});
		// Defining mouseout event handler
		google.maps.event.addListener(mar, 'mouseout', function() {
			infoWindow.close(var_map, this);
		});
		// Append all markers into markers_osm array
	    markers_osm.push(mar);
	}
	// Loop through all elements of markers_osm array and feed into the map
	for (var i = 0; i < markers_osm.length; i++) {
	  markers_osm[i].setMap(map);
	}
}

// This fun is attached to "OpenStreetMap Bus Stops" checkbox
function fun_osm_bus_stops(){
  var remember = document.getElementById('cb_osm_bus_stops');
  // Following if else is for toggle functionality
  if (remember.checked){
    setMapOnAll_osm(var_map);
  }
  else{
    setMapOnAll_osm(null);
  }
}

//-------------------------------------------------------------------------------

// This array will hold all roads present in the data/routes.geojson file
var routes = [];

// This fun will be called by fun_cal_bus_route fun
function setMapOnAll_routes(map) {
	// Loop through all bus routes roads
	for (var i = 0; i < bus_routes.length; i++) {
		// Defining polyline
		var one_road = new google.maps.Polyline({
			path: bus_routes[i],
			geodesic: true,
			strokeColor: '#008000',
			strokeOpacity: 1.0,
			strokeWeight: 1,
		});
		// Append all polyline into routes array
		routes.push(one_road);
	}
	// Loop through all elements of routes array and feed into the map
	for (var i = 0; i < routes.length; i++) {
	  routes[i].setMap(map);
	}
}

// This fun is attached to "Bus Routes" checkbox
function fun_cal_bus_route(){
  var remember = document.getElementById('cb_cal_bus_route');
  // Following if else is for toggle functionality
  if (remember.checked){
    setMapOnAll_routes(var_map);
  }
  else{
    setMapOnAll_routes(null);
  }
}

//-------------------------------------------------------------------------------

// This array will hold all markers which will display Activity Points
var markers_act_pts = [];

// This fun will be called by fun_act_pts fun
function setMapOnAll_act(map) {
	// Loop through all Activity Points
	for (var i=0; i < list_act_pts.length; ++i){
		var location = {lat: list_act_pts[i].y, lng: list_act_pts[i].x};
		// Infowindow which will show the name value of each activity point
		infoWindow = new google.maps.InfoWindow({})
		// Defining image, which will be used in google.map.marker
		var image = {
		    url: 'icon/activity_points.png',
		    scaledSize: new google.maps.Size(20, 20),
		  };
		// Defining marker
		var mar = new google.maps.Marker({
	      position: location,
	      map: var_map,
	      icon: image,
	      //content: "Name: " + String(list_osm[i].name),
	      content: "<table class=\"table table-bordered\">"+
	      				"<thead>"+
			      			"<tr>"+
				      			"<td><p align=\"center\"><b>Attribute</b></p></td>"+
				      			"<td><p align=\"center\"><b>Value</b></p></td>"+
			      			"</tr>"+
			      		"</thead>"+
			      		"<tbody>"+
			      			"<tr>"+
				      			"<td>Previous Dominating Activity</td>"+
				      			"<td>"+
				      			String(list_act_pts[i].pda)+
				      			"</td>"+
				      		"</tr>"+
			      			"<tr>"+
				      			"<td>Previous Dominating Activity Confidence</td>"+
				      			"<td>"+
				      			String(list_act_pts[i].pdac)+
				      			"</td>"+
			      			"</tr>"+
			      			"<tr>"+
				      			"<td>Current Dominating Activity</td>"+
				      			"<td>"+
				      			String(list_act_pts[i].cda)+
				      			"</td>"+
				      		"</tr>"+
			      			"<tr>"+
				      			"<td>Current Dominating Activity Confidence</td>"+
				      			"<td>"+
				      			String(list_act_pts[i].cdac)+
				      			"</td>"+
			      			"</tr>"+
			      			"<tr>"+
				      			"<td>Speed</td>"+
				      			"<td>"+
				      			String(list_act_pts[i].speed)+
				      			"</td>"+
				      		"</tr>"+
			      			"<tr>"+
				      			"<td>Accuracy</td>"+
				      			"<td>"+
				      			String(list_act_pts[i].accuracy)+
				      			"</td>"+
			      			"</tr>"+
			      		"</tbody>"+
	      			"</table>",
	      zIndex: 1,
	    });
		// Defining mouseover event handler
	    google.maps.event.addListener(mar, 'mouseover', function() {
			infoWindow.setContent(this.content),
			infoWindow.open(var_map, this);
		});
		// Defining mouseout event handler
		google.maps.event.addListener(mar, 'mouseout', function() {
			infoWindow.close(var_map, this);
		});
		// Append all markers into markers_osm array
	    markers_act_pts.push(mar);
	}
	// Loop through all elements of markers_osm array and feed into the map
	for (var i = 0; i < markers_act_pts.length; i++) {
	  markers_act_pts[i].setMap(map);
	}
}

// This fun is attached to "Activity Points" checkbox
function fun_act_pts(){
  var remember = document.getElementById('cb_act_pts');
  // Following if else is for toggle functionality
  if (remember.checked){
    setMapOnAll_act(var_map);
  }
  else{
    setMapOnAll_act(null);
  }
}