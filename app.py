import os
import requests

from pprint import PrettyPrinter
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Flask, render_template, request, send_file
from geopy.geocoders import Nominatim


################################################################################
## SETUP
################################################################################

app = Flask(__name__)

# Get the API key from the '.env' file
load_dotenv()

pp = PrettyPrinter(indent=4)

API_KEY = os.getenv('API_KEY')
API_URL = 'http://api.openweathermap.org/data/2.5/weather'
print(API_KEY)

################################################################################
## ROUTES
################################################################################

@app.route('/')
def home():
    """Displays the homepage with forms for current or historical data."""
    context = {
        'min_date': (datetime.now() - timedelta(days=5)),
        'max_date': datetime.now()
    }
    return render_template('home.html', **context)

def get_letter_for_units(units):
    """Returns a shorthand letter for the given units."""
    return '°F' if units == 'imperial' else '°C' if units == 'metric' else ' K'

@app.route('/weather')
def results():
    """Displays results for current weather conditions."""
    # TODO: Use 'request.args' to retrieve the city & units from the query
    # parameters.
    city = request.args.get('city')
    print(city)
    units = request.args.get('units')
    print(units)

    params = {
        # Add Units
        # TODO: Enter query parameters here for the 'appid' (your api key),
        # the city, and the units (metric or imperial).
        # See the documentation here: https://openweathermap.org/current
        'appid': API_KEY,
        'q': city,
        'units': units
    }

    result_json = requests.get(API_URL, params=params).json()
    print(result_json)
    print(result_json['name'])
    print(result_json['weather'][0]['description'])
    print(result_json['main']['temp'])
    print(result_json['main']['humidity'])
    print(result_json['wind']['speed'])
    print(datetime.fromtimestamp(result_json['sys']['sunrise']))
    print(datetime.fromtimestamp(result_json['sys']['sunset']))
    print(get_letter_for_units(units))
    # Uncomment the line below to see the results of the API call!
    # pp.pprint(result_json)

    # TODO: Replace the empty variables below with their appropriate values.
    # You'll need to retrieve these from the result_json object above.

    # For the sunrise & sunset variables, I would recommend to turn them into
    # datetime objects. You can do so using the `datetime.fromtimestamp()` 
    # function.
    
    date = datetime.now().strftime("%A, %B %d, %Y")
    sunrise = datetime.fromtimestamp(result_json['sys']['sunrise']).strftime("%I %p")
    sunset = datetime.fromtimestamp(result_json['sys']['sunset']).strftime("%I %p")


    context = {
        'date': date,
        'city': result_json['name'],
        'description': result_json['weather'][0]['description'],
        'temp': result_json['main']['temp'],
        'humidity': result_json['main']['humidity'],
        'wind_speed': result_json['wind']['speed'],
        'sunrise': sunrise,
        'sunset': sunset,
        'units_letter': get_letter_for_units(units)
        # Find all of it
    }
    # Fix template results.html
    return render_template('results.html', **context)


@app.route('/weather/comparison')
def comparison_results():
    """Displays the relative weather for 2 different cities."""
    # TODO: Use 'request.args' to retrieve the cities & units from the query
    # parameters.
    city1 = request.args.get('city1')
    city2 = request.args.get('city2')
    units = request.args.get('units')


    # TODO: Make 2 API calls, one for each city. HINT: You may want to write a 
    # helper function for this!
    params1 = {
        'appid': API_KEY,
        'q': city1,
        'units': units
    }
    params2 = {
        'appid': API_KEY,
        'q': city2,
        'units': units
    }

    result_json1 = requests.get(API_URL, params=params1).json()
    result_json2 = requests.get(API_URL, params=params2).json()

    # AMOUNT and GREATER THAN OR LESS THAN    
    # Need to get the number and expression(greaterthan/lessthan/same)

    # TODO: Pass the information for both cities in the context. Make sure to
    # pass info for the temperature, humidity, wind speed, and sunset time!
    # HINT: It may be useful to create 2 new dictionaries, `city1_info` and 
    # `city2_info`, to organize the data.
    
    # NEED TO CORRECTLY FIND KEYS
    city1_info = {
        'city': result_json1['name'],
        'temp': result_json1['main']['temp'],
        'humidity': result_json1['main']['humidity'],
        'wind_speed': result_json1['wind']['speed'],
        'sunset': datetime.fromtimestamp(result_json1['sys']['sunset'])
    }

    print('--------------------------------')
    print(city1_info['sunset'])

    city2_info = {
        'city': result_json2['name'],
        'temp': result_json2['main']['temp'],
        'humidity': result_json2['main']['humidity'],
        'wind_speed': result_json2['wind']['speed'],
        'sunset': datetime.fromtimestamp(result_json2['sys']['sunset'])
    }


    # WILL GET STUCK ON SUNSET, ALSO NEED TO CAP/ROUND DIFFERENCE
    context_key = ['temp', 'humidity', 'wind_speed']
    context = {
        'city1': city1_info['city'],
        'city2': city2_info['city'],
        'date': datetime.now(),
        'units_letter': get_letter_for_units(units)
    }

    for item in context_key:
        difference = city1_info[item] - city2_info[item]
        if difference < 0:
            if item == 'temp':
                expression = 'colder'
            elif item == 'sunset':
                expression = 'earlier'
            else:
                expression = 'less'
        elif difference > 0:
            if item == 'temp':
                expression = 'warmer'
            elif item == 'sunset':
                expression = 'later'
            else:
                expression = 'greater'
        else:
            expression = 'same'

        context[item] = {
            'difference': difference,
            'expression': expression,
        }

    print(context)
    
    return render_template('comparison_results.html', **context)


if __name__ == '__main__':
    app.config['ENV'] = 'development'
    app.run(debug=True)
