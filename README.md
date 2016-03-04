# Ally GIS Code Challenge Solution
Complete solution of [GIS Code Challenge of Ally](https://github.com/allyapp/gis-code-challenge)

---

### TASK 

To derive Bus Stop locations from the given [acitvity points geojson file](https://github.com/Zia-/Ally-gis-code-challenge-Solution/blob/master/data/activity_points.geojson) of Dar Es Salam, Tanzania.

---

### Inspecting the [activity_points.geojson file](https://github.com/Zia-/Ally-gis-code-challenge-Solution/blob/master/data/activity_points.geojson)

| Available Attributes of Features | Could it be used to locate Bus Stop locations? | Reason |
| :--------: |:------:| :--------: |
| type    | :heavy_multiplication_x: | It is constant for all features. |
| properties/previous_dominating_activity | :heavy_check_mark: | It tells what the user was doing before. |
| properties/bearing | :heavy_multiplication_x: | It gives the direction of user's current movement, which cannot be used any logically for Bus Stop locations estimation. |
| properties/previous_dominating_activity_confidence | :heavy_check_mark: | It gives the confidence level of information about previous dominating activity. |
| properties/current_dominating_activity | :heavy_check_mark: | It tells what the user is doing now. |
| properties/timestamp | :heavy_multiplication_x: | It is the time of data acquisition. Since we do not know if one user has generated this activity points data or more, no time relationship could be established between different timestamps. |
| properties/created_at | :heavy_multiplication_x: | It is the time of data storing. It is always few seconds after timestamp (except for one feature, which could be considered as an error). Again the same timestamp logic is applicable here also. |
| properties/altitude | :heavy_multiplication_x: | This information could be of some help is the Mean Sea Level of whole Dar Es Salam was constant and all buses had some definite height. Since, it is not the case, no direct usage is possible. |
| properties/feature | :heavy_multiplication_x: | No useful as it is same for all the features. |
| properties/id | :heavy_multiplication_x: | Not useful. |
| properties/speed | :heavy_check_mark: | It gives the current speed of the user. Useful in combination with previous and current dominating activity. |
| properties/route | :heavy_multiplication_x: | It is same for all the features, hence, useless. |
| properties/current_dominating_activity_confidence | :heavy_check_mark: | It gives the confidence level of information about current dominating activity. |
| properties/accuracy | :heavy_check_mark: | It gives the accuracy level of stored lat-long data. Could be used to drop activity points to the nearest bus route. |
| goemetry/type     | :heavy_multiplication_x:     |  Same for all the features. Not usefull. | 
|   geometry/coordinates       |    :heavy_multiplication_x:    | Not useful. |

---

### Methodology to derive Bus Stop locations from [activity_points.geojson data](https://github.com/Zia-/Ally-gis-code-challenge-Solution/blob/master/data/activity_points.geojson)

* Filter crowdsourced points based on previous and current dominating acitivity.
* Filter filtered points using [Bus Routes geojson data](https://github.com/Zia-/Ally-gis-code-challenge-Solution/blob/master/data/routes.geojson).
* Merge nearby points to avoid redundency.
* Compare final filtered data with OSM derived Bus Stop locations.
  
#### 1. Filter crowdsourced points based on previous and current dominating acitivity

Following table will demonstrate conditions where there is a possibility of user being at a Bus Stop. ***Note:*** *According to the activity data, there are only four type of dominating activities: still, on_foot, on_bicycyle, in_vehicle, and none (attribute value is missing).*

| previous_dominating_activity | current_dominating_activity | Possibility of being at a Bus Stop |
| :--------: |:------:| :--------: |
| still or on_foot or on_bicycle | in_vehicle | High probability |
| in_vehicle | still or on_foot or on_bicycle | High probability |
| none | in_vehicle | Medium probability |
| in_vehicle | none | Medium probability |
| none | still or on_foot or on_bicycle | Low probability | 
| still or on_foot or on_bicycle | none | Low probability |
| still or on_foot or on_bicycle | still or on_foot or on_bicycle | Least probability |

Activity points corresponding to the **High probability** and **Medium probability** were selected at this stage.

#### 2. Filter filtered points using [Bus Routes geojson data](https://github.com/Zia-/Ally-gis-code-challenge-Solution/blob/master/data/routes.geojson)

Now, since, the **in_vehicle** dominating activity could correspond to any "in vehicle" state of the user, not only Bus but also other personal or shared vehicles, activity points lying in the proximity of the available [Bus Routes data](https://github.com/Zia-/Ally-gis-code-challenge-Solution/blob/master/data/routes.geojson) were selected by creating buffer around the routes. 

![bufferring explained](https://raw.githubusercontent.com/Zia-/Ally-gis-code-challenge-Solution/master/web-page/icon/buffer_explain.png)

#### 3. Merge nearby points to avoid redundency

Since there are many activity points lying spatially close to each other, they practically cannot represent different Bus Stations, as Bus Stations must be separated by some distance. Thus, only one among many nearby activity points was selected to represent a possible Bus Station. ***Note:*** *Those nearby points were not merged or averaged as this may generate a point far away from Bus Routes, especially at curved Bus Route locations.*

![clubbing explained](https://raw.githubusercontent.com/Zia-/Ally-gis-code-challenge-Solution/master/web-page/icon/clubbing_explain.png)

#### 4. Compare final filtered data with OSM derived Bus Stop locations

Finally filtered activity points were compared with OpenStreetMap derived Bus Sations. It is a good practice to validate your findings from other sources. Proper flag value was assigned to different activity points, depending upon closeness with OSM Bus Stop, for better representation in the final Web-Page. ***Note:*** *Data was not filtered using OSM derived data because both are crowdsourced generated and no one is believed to be the true picture of Bus Stops in Dar Es Salam.*

![osm proximity explained](https://raw.githubusercontent.com/Zia-/Ally-gis-code-challenge-Solution/master/web-page/icon/osm_proximity_explain.png)

---

### Data Processing using Python Scripts

* Make a clone of this repository into your desired directory using git clone command. Else download the [zipped file](https://github.com/Zia-/Ally-gis-code-challenge-Solution/archive/master.zip). 

    ```c
    $git clone https://github.com/Zia-/Ally-gis-code-challenge-Solution.git
    ```

* Now before any data processing we need Dar Es Salam OpenStreetMap data. Download it into data directory of this repository at your local machine, and rename it to *dar_es_salam.osm*. ***Note:*** *This OSM file has not been provided into the repository because of being very large in size (approx. 0.5 Gb).*

    ```c
    $wget http://overpass.osm.rambler.ru/cgi/xapi_meta?*[bbox=39.0640,-7.1170,39.5269,-6.5767]
    ```

* Now in your terminal, navigate to the parent directory of this repository, ie. */Ally-gis-code-challenge-Solution$*. All the following commands must be executed being into this path.

* Execute [select_pt_by_dominating_activity.py](https://github.com/Zia-/Ally-gis-code-challenge-Solution/blob/master/python_scripts/select_pt_by_dominating_activity.py) script. It will generate [act_pt_selected_by_dominating_activity.csv](https://github.com/Zia-/Ally-gis-code-challenge-Solution/blob/master/data/act_pt_selected_by_dominating_activity.csv). This csv is the outcome of *Filter crowdsourced points based on previous and current dominating acitivity* filtering above :point_up_2:.

    ```c
    $python python/select_pt_by_dominating_activity.py
    ```

* Now execute [select_pt_by_routes_buffer.py](https://github.com/Zia-/Ally-gis-code-challenge-Solution/blob/master/python_scripts/select_pt_by_routes_buffer.py) script. It will generate [act_pt_selected_by_routes_buffer.csv](https://github.com/Zia-/Ally-gis-code-challenge-Solution/blob/master/data/act_pt_selected_by_routes_buffer.csv), [routes_buffered.wkt](https://github.com/Zia-/Ally-gis-code-challenge-Solution/blob/master/data/routes_buffered.wkt), and [routes_for_webpage.txt](https://github.com/Zia-/Ally-gis-code-challenge-Solution/blob/master/data/routes_for_webpage.txt) files. [routes_for_webpage.txt](https://github.com/Zia-/Ally-gis-code-challenge-Solution/blob/master/data/routes_for_webpage.txt) will be used in  our final Web-page. [routes_buffered.wkt](https://github.com/Zia-/Ally-gis-code-challenge-Solution/blob/master/data/routes_buffered.wkt) could be used for data visualization purposes in GIS software like QGIS. And, [act_pt_selected_by_routes_buffer.csv](https://github.com/Zia-/Ally-gis-code-challenge-Solution/blob/master/data/act_pt_selected_by_routes_buffer.csv) is the outcome of *Filter filtered points using [Bus Routes geojson data](https://github.com/Zia-/Ally-gis-code-challenge-Solution/blob/master/data/routes.geojson)* filtering above :point_up_2:.

    ```c
    $python python/select_pt_by_routes_buffer.py
    ```

* Club nearby activity points by running [club_nearby_act_pts.py](https://github.com/Zia-/Ally-gis-code-challenge-Solution/blob/master/python_scripts/club_nearby_act_pts.py) script. It will result into [act_pt_clubbed_nearby_pts.csv](https://github.com/Zia-/Ally-gis-code-challenge-Solution/blob/master/data/act_pt_clubbed_nearby_pts.csv) data, which is the result of *Merge nearby points to avoid redundency* filtering above :point_up_2:.
 
    ```c
    $python python/club_nearby_act_pts.py
    ```

* Finally, execute [select_pt_compare_with_osm.py](https://github.com/Zia-/Ally-gis-code-challenge-Solution/blob/master/python_scripts/select_pt_compare_with_osm.py) python script to derive [OSM Bus Stops](https://github.com/Zia-/Ally-gis-code-challenge-Solution/blob/master/data/osm_bus_stations.csv), and generate final activity points data ([act_pt_checked_against_osm.csv](https://github.com/Zia-/Ally-gis-code-challenge-Solution/blob/master/data/act_pt_checked_against_osm.csv)) with OSM flag (which will let us know if the activity pt is close to a Bus Stop derived from OSM or not). This is the filtering of *Compare final filtered data with OSM derived Bus Stop locations* filter above :point_up_2:.

    ```c
    $python python/select_pt_compare_with_osm.py
    ```



