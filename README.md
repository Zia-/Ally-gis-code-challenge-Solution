# Ally-gis-code-challenge-Solution
Complete solution of [GIS Code Challenge of Ally](https://github.com/allyapp/gis-code-challenge)

### TASK 

To derive Bus Stop locations from the given [acitvity points geojson file](https://github.com/Zia-/Ally-gis-code-challenge-Solution/blob/master/data/activity_points.geojson) of Dar Es Salam, Tanzania.

### Inspecting the [activity_points.geojson file](https://github.com/Zia-/Ally-gis-code-challenge-Solution/blob/master/data/activity_points.geojson)

| Available Attributes of Features | Could it be used to locate Bus Stop locations? | Reason |
| -------- |:------:| :--------: |
| type    | [&nbsp;&nbsp;] | It is constant for all features. |
| properties/previous_dominating_activity | [X] | It tells what the user was doing before. |
| properties/bearing | [&nbsp;&nbsp;] | It gives the direction of user's current movement, which cannot be used any logically for Bus Stop locations estimation. |
| properties/previous_dominating_activity_confidence | [X] | It gives the confidence level of information about previous dominating activity. |
| properties/current_dominating_activity | [X] | It tells what the user is doing now. |
| properties/timestamp | [&nbsp;&nbsp;] | It is the time of data acquisition. Since we do not know if one user has generated this activity points data or more, no time relationship could be established between different timestamps. |
| properties/created_at | [&nbsp;&nbsp;] | It is the time of data storing. It is always few seconds after timestamp (except for one feature, which could be considered as an error). Again the same timestamp logic is applicable here also. |
| properties/altitude | [&nbsp;&nbsp;] | This information could be of some help is the Mean Sea Level of whole Dar Es Salam was constant and all buses had some definite height. Since, it is not the case, no direct usage is possible. |
| properties/feature | [&nbsp;&nbsp;]| No useful as it is same for all the features. |
| properties/id | [&nbsp;&nbsp;] | Not useful. |
| properties/speed | [X] | It gives the current speed of the user. Useful in combination with previous and current dominating activity. |
| properties/route | [&nbsp;&nbsp;] | It is same for all the features, hence, useless. |
| properties/current_dominating_activity_confidence | [X] | It gives the confidence level of information about current dominating activity. |
| properties/accuracy | [X] | It gives the accuracy level of stored lat-long data. Could be used to drop activity points to the nearest bus route. |
| goemetry/type     | [&nbsp;&nbsp;]     |  Same for all the features. Not usefull. | 
|   geometry/coordinates       |    [&nbsp;&nbsp;]    | Not useful. |


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

![alt tag](https://raw.githubusercontent.com/Zia-/Ally-gis-code-challenge-Solution/master/web-page/icon/legend.png)
