import json, requests

salford_weather_url = 'https://weather-broker-cdn.api.bbci.co.uk/en/forecast/aggregated/2638671'

def main():
    response = requests.get(salford_weather_url)
    response_json = response.json()
    full_summary = response_json['forecasts'][0]['summary']['report']
    short_summary = {'weather': 
        {
            'description': full_summary['enhancedWeatherDescription'],
            'maxTemp': full_summary['maxTempC'],
            'minTemp': full_summary['minTempC'],
            'precipitationProbability': full_summary['precipitationProbabilityInPercent']
        }
    }

    print(json.dumps(short_summary))

if __name__ == '__main__':
    main()
