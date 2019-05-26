import requests


def get_forecast_for_today(city):
    forecast_json = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city},ua&mode=json&units=metric&lang=ru&APPID=8d8d31da4d4c6285183aa59a66fa3893").json()
    msg = "Temperature: " + str(forecast_json['main']['temp'])
    msg += "\n⛅️" + str(forecast_json['weather'][0]['main'])
    msg += '\n💨Pressure: ' + str(forecast_json["main"]["pressure"]) + ' hPa'
    return msg

