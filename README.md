# Ally-gis-code-challenge-Solution
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
| -------- |:------:| :--------: |
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
