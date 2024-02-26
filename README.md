ETL microservice that takes aqi data from AtmosPur and logs to a json. The data is averaged after one day.

Run by creating a log.json file in the same directory as etl.py and app.py. Then start app.py and etl.py. The default port is 5002 and an http request can be made at http://localhost:5002/api 

Sample get request:

[["Feb 24 Average", [{"Indoor AQI": 74, "Outdoor AQI": 17}]], ["Feb 25", [{"Indoor AQI": 86, "Outdoor AQI": 17, "Time": "04:14 PM"}, {"Indoor AQI": 85, "Outdoor AQI": 17, "Time": "04:15 PM"}, {"Indoor AQI": 85, "Outdoor AQI": 17, "Time": "04:16 PM"}, {"Indoor AQI": 85, "Outdoor AQI": 17, "Time": "04:17 PM"}, {"Indoor AQI": 85, "Outdoor AQI": 17, "Time": "04:18 PM"}, {"Indoor AQI": 85, "Outdoor AQI": 17, "Time": "04:19 PM"}, {"Indoor AQI": 84, "Outdoor AQI": 17, "Time": "04:20 PM"}]]]
