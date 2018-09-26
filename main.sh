weatherData="$(python weather.py)"
busData="$(python buses.py)"
budgetingData="$(python budgeting.py)"
echo $weatherData $busData $budgetingData | jq -s -c add


