from datetime import datetime, timedelta
from typing import Optional

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools import BaseTool

from powder.utils.google_maps_api import geocode_location
from powder.utils.hotels import search_hotels_by_location
from powder.utils.weather_unlocked_resorts import get_nearest_ski_resorts


class GetNearbySkiResorts(BaseTool):
    name = "GetNearbySkiResorts"
    description = ("This tool gets you a list of ski resorts near the current location. "
                   "Input the current address of the user it "
                   "will return description of the ski resorts near the user's location and the driving time and the current temperature at the resort")

    def _run(
            self, location: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        latlong = geocode_location(location)
        nearest_ski_resorts_with_distance_and_conditions = get_nearest_ski_resorts(latlong)
        response_to_agent = ""
        for idx, row in nearest_ski_resorts_with_distance_and_conditions.iterrows():
            response_to_agent += f"""{row['Name']} is {row['distance']} seconds away and the temperature is {row['current_conditions']}."""
        return response_to_agent

    async def _arun(
            self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("nearby does not support async")


class GetHotelsNearSkiResort(BaseTool):
    name = "GetHotelsNearSkiResort"
    description = ("This tool gives you information about hotels near a ski resort"
                   "Input the name of a resort and this tool will "
                   "will return a list of hotels near it along with distance, price per night, price details and ratings of a hotel")

    def _run(
            self, location: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        latlong = geocode_location(location)
        tomorrow_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        next_date = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
        hotels = search_hotels_by_location(latitude=latlong.split(",")[0], longitude=latlong.split(",")[1],
                                           checkin=str(tomorrow_date), checkout=str(next_date))
        response_to_agent = ""
        for idx, row in hotels['hotels'].iterrows():
            response_to_agent += f"""{row['title']} is {row['distance']} seconds away and the price per night is {row['price']} and the rating is {row['rating']}."""
        return response_to_agent

    async def _arun(
            self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("nearby does not support async")

#
