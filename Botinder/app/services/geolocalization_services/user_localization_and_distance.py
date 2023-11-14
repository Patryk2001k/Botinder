import json
import random
import requests
import country_converter as coco
from geopy.distance import geodesic
from ip2geotools.databases.noncommercial import DbIpCity
from app import BOTINDER_API_URL
with open("app/services/geolocalization_services/cities.json", "r") as cities_data:
    cities = json.load(cities_data)


def get_coordinates(city_name):  # Generates latitude and longtude from city name
    response = requests.get(BOTINDER_API_URL + f"/get_coordinates/{city_name}").json() #JSON format "city_name": , "latitude": , "longitude"
    return response.get("latitude"), response.get("longitude")


def get_cities():
    location = get_location()
    country_code = location["country"]
    cities_with_country_code = cities[country_code]

    country_cities = [i["name"] for i in cities_with_country_code]
    return country_cities


def generate_random_ip() -> str:  # Generates random IP address
    ip = ".".join(
        str(random.randint(0, 255)) for i in range(4)
    )  # generating random ip addresses is for tests
    """
    if we want to get real user ip address we need to put this code:
    ip = request.remote_addr
    """
    return ip


def get_location():  # Functions gets localization from IP address
    ip_address = generate_random_ip()
    response = DbIpCity.get(generate_random_ip(), api_key="free")
    location_data = {
        "ip": ip_address,
        "city": response.city,
        "region": response.region,
        "country": response.country,
    }
    if location_data["country"] == None or location_data["country"] == "ZZ":
        print("IP jest None")
        return get_location()
    else:
        print(location_data)
        return location_data

def distance(
    first_lat, first_lon, second_lat, second_lon
):  
    params = {
    'first_lat': first_lat,
    'first_lon': first_lon,
    'second_lat': second_lat,
    'second_lon': second_lon
    }
    return requests.get(BOTINDER_API_URL + f"/distance/", params=params).json().get("distance") #JSON format "distance": distance in km

def country_name_to_code():
    country_name = get_location()
    try:
        country_code = coco.convert(names=country_name["country"], to="ISO2")
        return country_code
    except:
        return None
