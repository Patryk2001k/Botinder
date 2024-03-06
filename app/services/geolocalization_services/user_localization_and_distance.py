import json
import random
import country_converter as coco
from geopy.distance import geodesic
from ip2geotools.databases.noncommercial import DbIpCity
from flask import request
from app import BOTINDER_API_HEADERS, BOTINDER_API_URL, app
from app.services.API_requests.requests import (get_botinderAPI_coordinates,
                                                get_botinderAPI_distance)

with open("app/services/geolocalization_services/cities.JSON", "r") as cities_data:
    cities = json.load(cities_data)


def get_coordinates(city_name):  # Generates latitude and longtude from city name
    response = get_botinderAPI_coordinates(
        BOTINDER_API_HEADERS, city_name, BOTINDER_API_URL
    )  # JSON format "city_name": , "latitude": , "longitude"
    print(response)
    return [response["latitude"], response["longitude"]]


def get_cities():
    location = get_location()
    country_code = location["country"]
    cities_with_country_code = cities[country_code]

    country_cities = [i["name"] for i in cities_with_country_code]
    return country_cities


def get_ip() -> str:
    ip = app.config['STATIC_USER_IP']
    return ip


def get_location():  # Functions gets localization from IP address
    ip_address = get_ip()
    response = DbIpCity.get(get_ip(), api_key="free")
    location_data = {
        "ip": ip_address,
        "city": response.city,
        "region": response.region,
        "country": response.country,
    }
    return location_data


def distance(first_lat, first_lon, second_lat, second_lon):
    params = {
        "first_lat": first_lat,
        "first_lon": first_lon,
        "second_lat": second_lat,
        "second_lon": second_lon,
    }
    response = get_botinderAPI_distance(BOTINDER_API_HEADERS, params, BOTINDER_API_URL)
    return response.get("distance")  # JSON format "distance": distance in km


def country_name_to_code():
    country_name = get_location()
    try:
        country_code = coco.convert(names=country_name["country"], to="ISO2")
        return country_code
    except:
        return None
