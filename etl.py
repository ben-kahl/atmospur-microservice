import requests, json, time, csv, random
from bokeh.models import DatetimeTickFormatter
from bokeh.plotting import figure, show
from datetime import datetime, timedelta

def get_aqi_data(external_data, internal_data, time_log):
    aqi_combined_json = {"outside-aqi": external_data,
                        "inside-aqi": internal_data, 
                        "time": time_log}
    return aqi_combined_json

def day_old(current_time, time_log):
    time_difference = current_time - time_log
    if time_difference > timedelta(days=1):
        return True
    else:
        return False

def average_data():
    data_log = open('log.csv', 'r')
    csv_reader = csv.reader(data_log)
    current_time = datetime.now()
    aqi_data = list(csv_reader)
    time = []
    for row in aqi_data[1:]:
        time.append(datetime.strptime(row[2], '%a %b %d %H:%M:%S %Y'))
        if day_old(current_time, time[-1]):
            print("Data older than 24 hours")
            #Now collect all data of the same data and the aqi values
            #Then average the aqi values and log the new data
        else:
            print("Data not older than 24 hours")
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

def plot_aqi_data():
    data_log = open('log.csv', 'r')
    csv_reader = csv.reader(data_log)
    aqi_data = list(csv_reader)
    time = []
    outside_aqi = []
    inside_aqi = []
    for row in aqi_data[1:]:
        time.append(datetime.strptime(row[2], '%a %b %d %H:%M:%S %Y'))
        outside_aqi.append(int(row[0]))
        inside_aqi.append(int(row[1]))
    plot = figure(title="AQI Data",
                   x_axis_type="datetime", 
                   x_axis_label='Time', 
                   y_axis_label='AQI', 
                   x_range=(time[0], time[-1]), 
                   background_fill_color="#232627")
    plot.line(time, outside_aqi, legend_label="Outside AQI", line_width=2)
    plot.line(time, inside_aqi, legend_label="Inside AQI", line_width=2, line_color="red")
    plot.xaxis.formatter = DatetimeTickFormatter(hours=["%H:%M"], days=["%m/%d"], months=["%m/%d"])
    show(plot)


# for x in range(10):
#     test_data = {"outside-aqi": random.randint(15, 50),
#              "inside-aqi": random.randint(15, 50),
#              "time": time.asctime(time.localtime())}
#     log_aqi_data(test_data)
#     time.sleep(1)

# plot_aqi_data()
# while True:
#     aqi_data = receive_aqi_data()
#     log_aqi_data(aqi_data)
#     time.sleep(3600)