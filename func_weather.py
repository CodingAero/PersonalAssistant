import requests
import json

import func_general as g

latitude = "40.029481"
longitude = "-105.060261"

def celsiusToFahrenheit(celsius):
    return ((celsius * (9./5.)) + 32.)

def getTemperature(verbose):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min&current_weather=true&timezone=auto"

    response = requests.get(url)
    data = response.json()

    temp_current = int(round(celsiusToFahrenheit(data['current_weather']['temperature']),0))
    temp_max = int(round(celsiusToFahrenheit(data['daily']['temperature_2m_max'][0]),0))
    temp_min = int(round(celsiusToFahrenheit(data['daily']['temperature_2m_min'][0]),0))

    # print(f"The temperature is currently {temp_current}°F, with a high of {temp_max}°F and a low of {temp_min}°F today.")

    return temp_current, temp_max, temp_min

def forecastMessage(msg,verbose):
    # National Weather Service (US only, no API key)
    points_url = f"https://api.weather.gov/points/{latitude},{longitude}"

    response = requests.get(points_url, headers={'User-Agent': 'MyWeatherApp'})
    data = response.json()

    forecast_url = data['properties']['forecast']
    forecast_response = requests.get(forecast_url, headers={'User-Agent': 'MyWeatherApp'})
    forecast_data = forecast_response.json()

    if forecast_data['properties']['periods'][0]['isDaytime']:
        today = forecast_data['properties']['periods'][0]
    else:
        today = forecast_data['properties']['periods'][1]

    # print(f"Forecast: {today['detailedForecast']}")

    msg = msg + '''
                    <h2>Forecast</h2>
                        <p>
                            ''' + today['detailedForecast'] + '''
                        </p>'''

    return msg

    return today['detailedForecast']