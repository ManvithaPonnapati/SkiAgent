import os

import pandas as pd
import requests
from tqdm import tqdm

from powder.utils.google_maps_api import geocode_location, get_distance_between_locations


def find_best_hotel_by_price(hotels):
    for hotel in hotels:
        price_for_the_dates = hotel['price']
    return min(hotels, key=lambda x: x['price'])


def get_hotel_by_proximity_to_the_resort(hotels):
    return min(hotels, key=lambda x: x['distance'])


def search_hotels_by_location(latitude, longitude, checkin, checkout):
    user_location = f"""{latitude},{longitude}"""
    url = "https://tripadvisor16.p.rapidapi.com/api/v1/hotels/searchHotelsByLocation"
    querystring = {"latitude": latitude, "longitude": longitude,
                   "checkIn": checkin, "checkOut": checkout,
                   "currencyCode": "USD"}

    headers = {
        "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": "tripadvisor16.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code != 200:
        return {"success": False, "message": "Error in fetching data from the API"}
    else:
        hotels = response.json()['data']['data']
        hotel_details = []
        for hotel_info in tqdm(hotels):
            rating = hotel_info["bubbleRating"]['rating']
            rating_num = hotel_info["bubbleRating"]['count']
            price_per_night = hotel_info["priceForDisplay"]
            price_details = hotel_info["priceDetails"]
            title = hotel_info["title"]
            link_to_tripadvisor = hotel_info["commerceInfo"]["externalUrl"] if "externalUrl" in hotel_info[
                "commerceInfo"].keys() else None
            # TODO: Make geolocate the hotel and get the distance from the resort
            hotel_location = geocode_location(title)
            distance = get_distance_between_locations(user_location, hotel_location)

            hotel_details.append({
                "title": title,
                "rating": rating,
                "rating_num": rating_num,
                "price": price_per_night,
                "price_details": price_details,
                "distance": distance,
                "link": link_to_tripadvisor
            })
        hotel_df = pd.DataFrame(hotel_details,
                                columns=["title", "rating", "rating_num", "price", "price_details", "distance", "link"])
        return {"success": True, "hotels": hotel_df}
