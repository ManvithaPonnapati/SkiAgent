import os

import pandas as pd
import requests

from powder.utils.google_maps_api import geocode_location, get_distance_between_locations


OneWeatherKey = os.environ.get("ONEWEATHER_KEY")

def get_weather_conditions_for_resort(lat, lon, datestring="2024-04-30"):
    # date={datestring}&tz=-08:00
    request_url = f"""https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&units=metric&appid={OneWeatherKey}"""
    # TODO: In the future we can use snow and temp but for now just temp since this is off season
    response = requests.get(request_url)
    if response.status_code == 200:
        response_json = response.json()
        current_temp = response_json['current']['temp']
        return current_temp
    else:
        return None


def get_nearest_ski_resorts(user_location: str):
    df = pd.read_csv("/Users/manu/Documents/Projects/shredthepow/powder/utils/ski_resorts_annotated.csv")
    df_california = df[df['State'] == 'California']

    distance_to_user = []
    current_conditions = []
    for idx, row in df_california.iterrows():
        try:
            resort_location = geocode_location(row['Name'])
            current_conditions.append(
                get_weather_conditions_for_resort(resort_location.split(",")[0], resort_location.split(",")[1]))
            distance = get_distance_between_locations(user_location, resort_location)
            distance_to_user.append(distance['driving_time'])
        except:
            distance_to_user.append(1111111)
            current_conditions.append(None)

    df_california['current_conditions'] = current_conditions
    df_california['distance'] = distance_to_user
    sorted_df = df_california.sort_values(by=['distance', 'current_conditions'])
    return sorted_df
