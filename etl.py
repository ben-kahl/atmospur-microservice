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

def average_data(datastore):
    inside_avg = 0 
    outside_avg = 0
    entries = 0
    if len(datastore) < 2:
        print("No data to average")
        return
    
    today = datastore[-1]
    yesterday = datastore[-2] 
    
    if today[0] != yesterday[0]:
        for entry in yesterday[1]:
            try:
                inside_avg += entry['Indoor AQI']
                outside_avg += entry['Outdoor AQI']
                entries += 1
            except Exception as e:
                print(f"Date has already been averaged. {e}")
        if entries > 0:
            inside_avg = int((inside_avg/entries))
            outside_avg = int((outside_avg/entries))
            
            yesterday_avg_string = yesterday[0] + " Average"
            
            datastore[-2] = [yesterday_avg_string, 
                             [{
                                 "Indoor AQI": inside_avg,
                                 "Outdoor AQI": outside_avg
                             }]]
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
            
def load_log(datastore):
    try:
        with open('log.json', 'r') as data_log:
            data = json.load(data_log)
            datastore.extend(data)
            data_log.close
    except Exception as e:
        print(f"Error loading to list: {e}")


#Runs once on program start so that previous data isn't errased.     
load_log(datastore)

while True:
    aqi_data = receive_aqi_data()
    add_data(aqi_data, datastore)
    #average the data if needed
    average_data(datastore)
    log_aqi_data(datastore)
    time.sleep(60)