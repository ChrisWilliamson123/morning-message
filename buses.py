import datetime, json, pytz, requests

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Content-Type': 'application/json',
    'X-SC-securityMethod': 'API',
    'X-SC-apiKey': 'ukbusprodapi_7k8K536tNsPH#!',
}

data = {
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
               "stopPointLabel":"1800NF03991",
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

def get_arrival_time(bus):
    live_arrival_time_utc = datetime.datetime.strptime(bus['expectedArrivalTime'], '%Y-%m-%dT%H:%M:%SZ')
    british_time = pytz.timezone('Europe/London')
    arrival_time_british = live_arrival_time_utc.replace(tzinfo=pytz.utc).astimezone(british_time)
    return arrival_time_british

def main():
    response = requests.post('https://api.stagecoachbus.com/adc/stop-monitor', headers=headers, json=data)
    json_result = response.json()

    upcoming_buses = json_result['stopMonitors']['stopMonitor'][0]['monitoredCalls']['monitoredCall']
    arrival_times = [t.strftime("%H:%M") for t in sorted(list(map(get_arrival_time, upcoming_buses)))]

    print(json.dumps({'busTimes': arrival_times}))

if __name__ == '__main__':
    main()

