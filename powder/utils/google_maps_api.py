import os
from datetime import datetime

import googlemaps

GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
gmaps = googlemaps.Client(key=GOOGLE_API_KEY)


def get_distance_between_locations(location_1, location_2):
    """ This function is for geting the driving distance from home
    to a particular resort
    [right now this just works with coords]
    TODO: make this take the resort as an input and look up the resort coords
    """

    now = datetime.now()
    directions_result = gmaps.directions(location_1,
                                         location_2,
                                         mode="driving",
                                         departure_time=now)
    try:
        return {"driving_time": directions_result[0]["legs"][0]["duration"]["value"]}
    except:
        return {"driving_time": None}


def geocode_location(location_name='Heavenly Mountain — South Lake Tahoe'):
    """
    returns the lattitude and longitute of a ski resort
    expects a simple name of a ski resort
    """
    geocode_result = gmaps.geocode(location_name.split(". ")[-1])
    try:
        geocode_result_location = geocode_result[0]['geometry']["location"]
        return f"""{geocode_result_location['lat']},{geocode_result_location['lng']}"""
    except:
        return f"""{0},{0}"""
