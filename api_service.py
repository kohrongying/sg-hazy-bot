import requests
import datetime

BASE_URL = "https://api.data.gov.sg/v1/environment/psi"


def make_request():
    response = requests.get(BASE_URL)
    if response.ok:
        return response.json()
    else:
        return None


def get_psi_twenty_four_hourly(response):
    return response['items'][0]['readings']['psi_twenty_four_hourly']


def get_pm25_twenty_four_hourly(response):
    return response['items'][0]['readings']['pm25_twenty_four_hourly']


def get_last_updated_time(response):
    timestamp = response['items'][0]['update_timestamp']
    datetime_obj = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S%z')
    return f"{datetime_obj.strftime('%d %b %Y %H:%M:%S')} SGT"


def format_response(psi, pm25, updated_time):
    response = f"""
<pre>
| Area    | PSI   | PM2.5 | 
|---------|-------|-------|"""
    for area in psi:
        if area != "national":
            psi_reading = psi[area]
            pm25_reading = pm25[area]
            response += f'\n{format_line(area, psi_reading, pm25_reading)}'

    response += f"""
</pre>
<em>Last updated on {updated_time}</em>
    """
    return response


def format_line(area, psi, pm25):
    area_str = f' {area}'.ljust(9, ' ')
    psi_str = f' {psi}'.ljust(7, ' ')
    pm25_str = f' {pm25}'.ljust(7, ' ')
    return f'|{area_str}|{psi_str}|{pm25_str}|'


def main():
    response = make_request()
    psi = get_psi_twenty_four_hourly(response)
    pm25 = get_pm25_twenty_four_hourly(response)
    last_updated_time = get_last_updated_time(response)
    return format_response(psi, pm25, last_updated_time)
