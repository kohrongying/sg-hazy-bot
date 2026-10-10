import datetime
import os
import requests
from shared import Reading, format_line, build_query_params

BASE_URL = "https://api.data.gov.sg/v1/environment/psi"
regions = ["north", "south", "east", "west", "central"]


def make_request():
    response = requests.get(BASE_URL)
    if response.ok:
        return response.json()
    else:
        return None


def get_nea_readings(response: dict) -> list[Reading]:
    readings = []
    if not response:
        return readings
    data = response["items"][0]["readings"]
    for region in regions:
        psi = data["psi_twenty_four_hourly"].get(region, None)
        pm25 = data["pm25_twenty_four_hourly"].get(region, None)
        readings.append(
            Reading(psi=psi, pm25=pm25, source="NEA", region=region, city="singapore")
        )
    return readings


def get_last_updated_time(response) -> str:
    timestamp = response["items"][0]["update_timestamp"]
    datetime_obj = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S%z")
    return f"{datetime_obj.strftime('%d %b %Y %H:%M:%S')} SGT"


def format_nea_response() -> str:
    response = make_request()
    readings = get_nea_readings(response)
    last_updated_time = get_last_updated_time(response)

    response = f"""
<pre>
| Area    | PSI   | PM2.5 | 
|---------|-------|-------|"""
    for reading in readings:
        response += f"\n{format_line(reading.region, reading.psi, reading.pm25)}"

    response += f"""
</pre>
<em>Last updated on {last_updated_time}</em>
<a href="{os.getenv("DYNAMIC_MAP_BASE_URL")}{build_query_params(readings, 'psi')}">&#8205;</a>
    """
    return response