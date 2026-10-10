import requests
import os
from shared import Reading, format_line, build_query_params


CITY = "singapore"
BASE_URL = f"https://api.waqi.info/feed/{CITY}"
AQICN_TOKEN = os.getenv("AQICN_TOKEN")

regions = ["north", "south", "east", "west", "central"]
urls = [f"{BASE_URL}/{region}/?token={AQICN_TOKEN}" for region in regions]


def make_request(url):
    response = requests.get(url)
    if response.ok:
        return response.json()
    else:
        return None


def get_aqicn_readings():
    readings = []
    for region, url in zip(regions, urls):
        response = make_request(url)
        if response and "data" in response:
            data = response["data"]
            pm25 = data["iaqi"]["pm25"]["v"] if "pm25" in data["iaqi"] else None
            readings.append(
                Reading(psi=None, pm25=pm25, source="AQICN", region=region, city=CITY)
            )
    return readings


def format_aqicn_response() -> str:
    readings = get_aqicn_readings()

    response = f"""
<pre>
| Area    | PSI   | PM2.5 | 
|---------|-------|-------|"""
    for reading in readings:
        response += f"\n{format_line(reading.region, reading.psi, reading.pm25)}"

    response += f"""
</pre>
<a href="{os.getenv("DYNAMIC_MAP_BASE_URL")}{build_query_params(readings)}">&#8205;</a>
    """
    return response
