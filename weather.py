import datetime as datetime
import logger as log
import message
import pprint
import requests

def getTemperatures(config):
    '''
    Determines the current, high, and low temperatures of the day
    for the message header.

    Input:
        config (dict): Configuration key value pairs
    Output:
        n/a
    '''

    log.note(config,f"Function call: getTemperatures")
    current_temp = '---'
    high_temp = '---'
    low_temp = '---'

    try:
        # National Weather Service (US only, no API key)
        points_url = f"https://api.weather.gov/points/{config['latitude']},{config['longitude']}"

        response = requests.get(points_url, headers={'User-Agent': 'MyWeatherApp'})
        data = response.json()

        forecast_url = data['properties']['forecastHourly']
        forecast_response = requests.get(forecast_url, headers={'User-Agent': 'MyWeatherApp'})
        forecast_data = forecast_response.json()

        for hour in forecast_data['properties']['periods']:
            if str(datetime.datetime.now().strftime("%Y-%m-%d")) in hour['endTime']:
                if current_temp == '---':
                    current_temp = hour['temperature']
                    high_temp = hour['temperature']
                    low_temp = hour['temperature']
                if hour['temperature'] > high_temp:
                    high_temp = hour['temperature']
                if hour['temperature'] < low_temp:
                    low_temp = hour['temperature']

    except Exception as e:
        log.note(config,f"getTemperatures: FAILED TO GET TEMPERATURES\n    Error: {e}")

    return current_temp,high_temp,low_temp

def forecastMessage(config):
    '''
    Appends weather forecast information to the correspondence message

    Input:
        config (dict): Configuration key value pairs
    Output:
        n/a
    '''

    log.note(config,f"Function call: forecastMessage")

    msg = []

    try:
        # National Weather Service (US only, no API key)
        points_url = f"https://api.weather.gov/points/{config['latitude']},{config['longitude']}"

        response = requests.get(points_url, headers={'User-Agent': 'MyWeatherApp'})
        data = response.json()

        forecast_url = data['properties']['forecast']
        forecast_response = requests.get(forecast_url, headers={'User-Agent': 'MyWeatherApp'})
        forecast_data = forecast_response.json()

        if forecast_data['properties']['periods'][0]['isDaytime']:
            msg.append(forecast_data['properties']['periods'][0]['detailedForecast'])
            log.note(config,f"forecastMessage: Adding weather forecast information")
        else:
            msg.append(forecast_data['properties']['periods'][1]['detailedForecast'])
            log.note(config,f"forecastMessage: Adding weather forecast information")

        message.appendMessage(config, 'Forecast', msg)
    except Exception as e:
        log.note(config,f"forecastMessage: FAILED TO GET FORECAST\n    Error: {e}")

    return