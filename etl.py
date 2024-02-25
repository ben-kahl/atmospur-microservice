import requests, json, time
from datetime import datetime, timedelta

datastore = []

def get_date(input_time):
    parsed_time = datetime.strptime(input_time, '%a %b %d %H:%M:%S %Y')
    formatted_time = parsed_time.strftime('%b %d')
    return formatted_time

def convert_to_12hr_time(input_time):
    # Parse the input time string
    parsed_time = datetime.strptime(input_time, '%a %b %d %H:%M:%S %Y')

    # Format the time in 12-hour time
    formatted_time = parsed_time.strftime('%I:%M %p')

    return formatted_time


def day_old(current_time, time_log):
    if time_log < current_time:
        return True
    else:
        return False

def average_data():
    pass
    #TODO: Implement average data function for data older than 24 hours


def receive_aqi_data():
    try:
        res = requests.get("http://aqi.arthurktripp.com:5000/api/data_tracking")
        aqi_to_log = res.json()
        return aqi_to_log
    except requests.exceptions.RequestException as e:
        print(e)

def send_avg_data(data):
    try:
        res = requests.post("http://aqi.arthurktripp.com:5000/api/data_tracking", json = data)
        return res
    except requests.exceptions.RequestException as e:
        print(e)


def log_aqi_data(aqi_data):
    try:
        with open('log.json', 'w') as data_log:
            json.dump(aqi_data, data_log, indent=2)
            data_log.close()
    except Exception as e:
        print(f"Error writing to JSON: {e}")

def add_data(data, datastore):
    current_date = datetime.now().strftime('%b %d')
    time = convert_to_12hr_time(data['aqi_time'])
    for entry in datastore:
        entry_date, entries = entry
        if entry_date == current_date:
            entries.append({
                    'Indoor AQI': data['inside-aqi'],
                    'Outdoor AQI': data['outside-aqi'],
                    'Time': time
                })
        return
    
    datastore.append((current_date, [{
        'Indoor AQI': data['inside-aqi'],
        'Outdoor AQI': data['outside-aqi'],
        'Time': time
    }]))
            
    

while True:
    aqi_data = receive_aqi_data()
    add_data(aqi_data, datastore)
    #If data is older than a day, average that day's data
    # if day_old(datastore[-1][aqi_data], prev_date):
    #     average_data(datastore)
    
    log_aqi_data(datastore)
    time.sleep(60)