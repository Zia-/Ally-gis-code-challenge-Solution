// This variable will hold google map object instance
var var_map;

// Define init_map fun, which will fire on window load
function init_map() {
  // Center of the map
  var var_location = new google.maps.LatLng(-6.809245, 39.261146);
  // Map variables
  var var_mapoptions = {
    center: var_location,
    zoom: 12,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };
  // Making map object
  var_map = new google.maps.Map(document.getElementById("map-container"),
    var_mapoptions);
}

// Defining event handler
google.maps.event.addDomListener(window, 'load', init_map);
