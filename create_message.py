import json, sys, datetime

def suffix(d):
    return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')

def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))

# def create_bus_times_string(times):
#     less_times = times[0:3]
#     as_strings = ['%s, ' % t for t in less_times]
#     as_strings[-2] = as_strings[-2].replace(', ', ' and ')
#     as_strings[-1] = as_strings[-1].replace(', ', '')
#     return ''.join(as_strings)

if __name__ == "__main__":
    data = json.loads(sys.stdin.readline())
    weather_data = data['weather']
    budgeting_data = data['budgeting']

    today = custom_strftime('%A the {S} %B %Y', datetime.date.today())
    date_message = 'Good Morning Chris, Today is %s' % today

    weather_message = 'and the weather will provide %s. There will be a high of %s and a low of %s, with %s percent chance of rain.' % (
        weather_data['description'],
        weather_data['maxTemp'],
        weather_data['minTemp'],
        weather_data['precipitationProbability']
    )

    budgeting_message = 'Yesterday you saved %s therefore increasing your budgeting pot balance to %s.' % (
        budgeting_data['saved'],
        budgeting_data['pot_balance']
    )


    final_message = '%s %s %s' % (date_message, weather_message, budgeting_message)
    print(final_message)

