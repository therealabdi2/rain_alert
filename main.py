import requests
from twilio.rest import Client
import os

api_key = os.environ["OWM_API"]
OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/onecall"

account_sid = os.environ["twilio_acc_sid"]
auth_token = os.environ["twilio_auth_token"]

weather_params = {
    "lat": 33.673645,
    "lon": 72.993237,
    "appid": api_key,
    "exclude": "current,minutely,daily"
}

response = requests.get(OWM_ENDPOINT, params=weather_params)
response.raise_for_status()
weather_data = response.json()

twelve_hour_weather_list = weather_data["hourly"][:12]

will_rain = False
for hour_data in twelve_hour_weather_list:
    condition_code = int(hour_data["weather"][0]["id"])
    if condition_code < 700:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body="It's going to rain today. Remember to bring an umbrella ❤",
        from_="+16124007171",
        to="+92 334 5669021"
    )
    print(message.status)
