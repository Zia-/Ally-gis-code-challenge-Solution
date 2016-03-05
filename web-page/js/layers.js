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
