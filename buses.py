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

stops = {
    'work': {
        'id': '1800NF09811',
        'destination_name': 'Salford Central'
    },
    'home': {
        'id': '1800NF03991',
        'destination_name': 'Media City UK'
    }
}

british_time = pytz.timezone('Europe/London')

get_live_buses = lambda all_buses: [b for b in all_buses['stopMonitors']['stopMonitor'][0]['monitoredCalls']['monitoredCall'] if ('expectedArrivalTime' in b or 'expectedDepartureTime' in b)]

def json_print(to_print):
    print(json.dumps(to_print, indent=4))


def get_arrival_time(bus):
    if 'expectedArrivalTime' in bus:
        live_arrival_time_utc = datetime.datetime.strptime(bus['expectedArrivalTime'], '%Y-%m-%dT%H:%M:%SZ')
    else:
        live_arrival_time_utc = datetime.datetime.strptime(bus['expectedDepartureTime'], '%Y-%m-%dT%H:%M:%SZ')
    arrival_time_british = live_arrival_time_utc.replace(tzinfo=pytz.utc).astimezone(british_time)
    return arrival_time_british

def get_difference_in_minutes_between(time_a, time_b):
    difference = time_a - time_b
    in_minutes_and_seconds = divmod(difference.days * 86400 + difference.seconds, 60)
    return in_minutes_and_seconds[0]

def parse_multiple_times(bus_times):
    return '%s minutes and %s minutes' % (
        ' minutes, '.join(bus_times[:-1]),
        bus_times[-1]
    )

def create_message(bus_times, destination_name):
    count = len(bus_times)
    time_strings = [str(time) for time in bus_times]
    if count == 1:
        return 'The next bus to %s is in %d minutes.' % (destination_name, time_strings[0])
    else:
        return 'The upcoming buses to %s leave in %s.' % (destination_name, parse_multiple_times(time_strings))

def get_origin(arguments):
    if len(arguments) < 2:
        print('Must provide start location as an argument')
        sys.exit(1)
    origin_name = sys.argv[1]
    allowed_values = list(stops.keys())
    if origin_name not in allowed_values:
        print('Origin must be one of %s' % allowed_values)
        sys.exit(1)
    return stops[origin_name]

def main():
    origin = get_origin(sys.argv)

    response = requests.post('https://api.stagecoachbus.com/adc/stop-monitor', headers=headers, json=data(origin['id']))
    json_result = response.json()

    upcoming_live_buses = get_live_buses(json_result)

    arrival_times = sorted(list(map(get_arrival_time, upcoming_live_buses)))

    current_time = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=pytz.utc).astimezone(british_time)
    print(current_time, arrival_times[0])
    minutes_away = [get_difference_in_minutes_between(arrival_time, current_time) for arrival_time in arrival_times]
    print(minutes_away)
    filtered = [m for m in minutes_away if m >= 2][:3]
    print(create_message(filtered, origin['destination_name']))

if __name__ == '__main__':
    main()

