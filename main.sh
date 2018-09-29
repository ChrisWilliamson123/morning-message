weatherData="$(python weather.py)"
budgetingData="$(python budgeting.py)"
battery='{"battery": '$1'}'
echo $weatherData $budgetingData $battery | jq -s -c add


