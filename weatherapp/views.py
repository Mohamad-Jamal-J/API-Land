from django.shortcuts import render
import requests
from datetime import datetime


def home_page(request):
    data = {}

    if request.method == 'POST':
        city = request.POST['city']
        key = "YOUR OWN API KEY"
        source = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={key}"
        response = requests.get(source)

        if response.status_code == 200:
            weather_data = response.json()

            data['city_name'] = weather_data['name']
            data['country_code'] = weather_data['sys']['country']
            data['coordinate'] = f"Latitude: {weather_data['coord']['lat']}, Longitude: {weather_data['coord']['lon']}"
            data['temperature'] = weather_data['main']['temp']
            data['humidity'] = weather_data['main']['humidity']
            data['description'] = weather_data['weather'][0]['description']
            data['feels_like'] = weather_data['main']['feels_like']
            data['pressure'] = weather_data['main']['pressure']
            data['wind_speed'] = weather_data['wind']['speed']

            sunrise_timestamp = weather_data['sys']['sunrise']
            sunset_timestamp = weather_data['sys']['sunset']
            data['sunrise'] = datetime.utcfromtimestamp(sunrise_timestamp).strftime('%I:%M %p')
            data['sunset'] = datetime.utcfromtimestamp(sunset_timestamp).strftime('%I:%M %p')
        else:
            data['error'] = f"Error {response.status_code}, City: '{city}' Not found"
        print(response.status_code)
    return render(request, 'weatherapp/weather.html', data)
