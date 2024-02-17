import requests, json, time, csv

def get_aqi_data(external_data, internal_data, time_log):
    aqi_combined_json = {"outside-aqi": external_data,
                        "inside-aqi": internal_data, 
                        "time": time_log}
    return aqi_combined_json

def average_data():
    data_log = open('log.csv', 'r')
    csv_reader = csv.reader(data_log)
    #TODO: Implement average data function for data older than 24 hours

def receive_aqi_data():
    try:
        external_data = requests.get("http://aqi.arthurktripp.com:5000/api/outside")
    except requests.exceptions.RequestException as e:
        print(e)
        return None
    try:    
        internal_data = requests.get("http://aqi.arthurktripp.com:5000/api/inside")
    except requests.exceptions.RequestException as e:
        print(e)
        return None
    time_log = time.asctime(time.localtime())
    aqi_to_log = get_aqi_data(external_data.json(), internal_data.json(), time_log)
    return aqi_to_log

def log_aqi_data(aqi_data):
    data_log = open('log.csv', 'a', newline='')
    csv_writer = csv.writer(data_log)
    if data_log.tell() == 0:
        csv_writer.writerow(aqi_data.keys())
    csv_writer.writerow(aqi_data.values())
    data_log.close()

test_data = {"outside-aqi": 20,
             "inside-aqi": 30,
             "time": "Wed Sep 1 10:45:13 2021"}
#aqi_to_log = receive_aqi_data()
log_aqi_data(test_data)
# while True:
#     aqi_data = receive_aqi_data()
#     log_aqi_data(aqi_data)
#     time.sleep(3600)