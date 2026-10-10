from dataclasses import dataclass


@dataclass
class Reading:
    psi: int
    pm25: int
    source: str
    region: str
    city: str


def build_query_params(readings: list[Reading], attr='pm25') -> str:
    query_string = "?"
    for reading in readings:
        query_string += f"{reading.region}={getattr(reading, attr)}&"
    if len(query_string) == 1:
        return ""
    return query_string[:-1]


def format_line(area, psi, pm25):
    area_str = f" {area}".ljust(9, " ")
    psi_str = f" {psi}".ljust(7, " ")
    pm25_str = f" {pm25}".ljust(7, " ")
    return f"|{area_str}|{psi_str}|{pm25_str}|"
