import datetime, json, pytz, requests, sys, time

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Content-Type': 'application/json',
    'X-SC-securityMethod': 'API',
    'X-SC-apiKey': 'ukbusprodapi_7k8K536tNsPH#!',
}

data = lambda bus_stop: {
   "StopMonitorRequest":{
      "header":{
         "retailOperation":"",
         "channel":"",
         "ipAddress":""
      },
      "lookAheadMinutes":60,
      "stopMonitorQueries":{
         "stopMonitorQuery":[
            {
               "stopPointLabel": bus_stop,
               "servicesFilters":{
                  "servicesFilter":[
                     {
                        "filter":"50"
                     }
                  ]
               }
            }
         ]
      }
   }
}

british_time = pytz.timezone('Europe/London')

get_live_buses = lambda all_buses: [b for b in all_buses['stopMonitors']['stopMonitor'][0]['monitoredCalls']['monitoredCall'] if 'expectedArrivalTime' in b]

def json_print(to_print):
    print(json.dumps(to_print, indent=4))


def get_arrival_time(bus):
    live_arrival_time_utc = datetime.datetime.strptime(bus['expectedArrivalTime'], '%Y-%m-%dT%H:%M:%SZ')
    arrival_time_british = live_arrival_time_utc.replace(tzinfo=pytz.utc).astimezone(british_time)
    return arrival_time_british

def get_difference_in_minutes_between(time_a, time_b):
    difference = time_a - time_b
    in_minutes_and_seconds = divmod(difference.days * 86400 + difference.seconds, 60)
    print(in_minutes_and_seconds)
    return in_minutes_and_seconds[0]

def parse_multiple_times(bus_times):
    return '%s minutes and %s minutes' % (
        ' minutes, '.join(bus_times[:-1]),
        bus_times[-1]
    )

def create_message(bus_times):
    count = len(bus_times)
    time_strings = [str(time) for time in bus_times]
    if count == 1:
        return 'The next Media City UK bus is in %d minutes.' % time_strings[0]
    else:
        return 'The next Media City UK buses leave in %s.' % parse_multiple_times(time_strings)

def main():
    response = requests.post('https://api.stagecoachbus.com/adc/stop-monitor', headers=headers, json=data("1800NF03991"))
    json_result = response.json()
    upcoming_live_buses = get_live_buses(json_result)
    current_time = datetime.datetime.now().astimezone(british_time)
    arrival_times = sorted(list(map(get_arrival_time, upcoming_live_buses)))
    minutes_away = [get_difference_in_minutes_between(arrival_time, current_time) for arrival_time in arrival_times]
    filtered = [m for m in minutes_away if m >= 2][:3]
    print(create_message(filtered))

if __name__ == '__main__':
    main()

