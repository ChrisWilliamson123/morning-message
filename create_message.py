import json, sys, datetime

def suffix(d):
    return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')

def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))

def pence_to_words(pence):
  pounds = str(int(pence/100))
  pence = str(pence)
  pence = pence[-2:] if pence[-2] is not '0' else pence[-1]
  return '%s pounds %s' % (pounds, (pence + ' pence') if int(pence) > 0 else '')

def create_budgeting_message(budgeting_data):
    saved = budgeting_data['saved']
    budget = budgeting_data['budget']
    spent = budgeting_data['spent']
    under_budget = spent < budget

    if under_budget:
        return 'Yesterday you saved %s therefore increasing your budgeting pot balance to %s.' % (pence_to_words(saved), pence_to_words(budgeting_data['pot_balance']))
    else:
        return 'Yesterday you were over budget by %s therefore decreasing your budgeting pot balance to %s.' % (pence_to_words(saved*-1), pence_to_words(budgeting_data['pot_balance']))

def create_weather_message(weather_data):
    rain_prob = weather_data['precipitationProbability']
    rain_message_prefix = 'a ' if rain_prob < 100 else ''
    return 'The weather will provide %s. There will be a high of %s and a low of %s, with %s%s percent chance of rain.' % (
        weather_data['description'],
        weather_data['maxTemp'],
        weather_data['minTemp'],
        rain_message_prefix,
        rain_prob
    )

if __name__ == "__main__":
    data = json.loads(sys.stdin.readline())
    weather_data = data['weather']
    budgeting_data = data['budgeting']

    today = custom_strftime('%A {S} %B', datetime.date.today())
    date_message = 'Good Morning Chris. Today is %s.' % today

    weather_message = 'The weather will provide %s. There will be a high of %s and a low of %s, with %s percent chance of rain.' % (
        weather_data['description'],
        weather_data['maxTemp'],
        weather_data['minTemp'],
        'a %s' % weather_data['precipitationProbability']
    )

    battery_message = 'You have %s percent battery remaining.' % data['battery']

    final_message = '%s %s %s %s' % (date_message, create_weather_message(weather_data), create_budgeting_message(budgeting_data), battery_message)
    print(final_message)
