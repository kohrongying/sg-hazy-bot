import requests
import os
from shared import Reading, format_line, build_query_params
import datetime
from zoneinfo import ZoneInfo

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


def get_time(response):
    if not response:
        return None
    iso = response.get("data", {}).get("time", {}).get("iso", None)
    dt_utc = datetime.datetime.fromisoformat(iso) if iso else None

    if not dt_utc:
        return None
    dt_sgt = dt_utc.astimezone(ZoneInfo("Asia/Singapore"))
    return f"{dt_sgt.strftime('%d %b %Y %H:%M:%S')} SGT"

def format_aqicn_response() -> str:
    readings = get_aqicn_readings()
    resp = make_request(urls[0])  # Get the first region's response to extract the time
    response = f"""
<b>Air Quality Index (AQI) Readings for {CITY.capitalize()}</b>
<em>Last updated on {get_time(resp)}:</em>
<pre>
| Area    | PSI   | PM2.5 | 
|---------|-------|-------|"""
    for reading in readings:
        response += f"\n{format_line(reading.region, reading.psi, reading.pm25)}"

    response += f"""
</pre>
See map of PM2.5 readings
<a href="{os.getenv("DYNAMIC_MAP_BASE_URL")}{build_query_params(readings)}">&#8205;</a>
    """
    return response
