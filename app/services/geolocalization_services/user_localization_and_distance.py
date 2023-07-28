import random
import country_converter as coco
import requests
import json
from ip2geotools.databases.noncommercial import DbIpCity
from geopy.distance import geodesic
from geopy.geocoders import Nominatim


def get_coordinates(city_name):  # Generates latitude and longtude from city name
    geolocator = Nominatim(user_agent="Botinder")
    location = geolocator.geocode(city_name)

    if location:
        latitude = location.latitude
        longitude = location.longitude
        return latitude, longitude
    else:
        return None, None


def get_cities():
    location = get_location()
    country_code = location["country"]
    with open("app/geolocalization_services/cities.json", "r") as cities_data:
        cities = json.load(cities_data)
        cities_with_country_code = cities[country_code]

    country_cities = [
        i["name"] for i in cities_with_country_code
    ]

    #print(country_cities)

    # print(cities)
    # for i in cities:
    # if cities[i]["countrycode"] == country_code:
    # print(cities[i]["name"])
    # if cities[i]["name"] == "Warszawa" or "Warszawa" in cities[i]["alternatenames"]:
    # print("---------------")
    # print(cities[i]["name"])

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
    response = DbIpCity.get(generate_random_ip(), api_key='free')
    location_data = {
        "ip": ip_address,
        "city": response.city,
        "region": response.region,
        "country": response.country,
    }
    if location_data["country"] == None:
        print("IP jest None")
        return get_location()
    return location_data


def distance(
    first_cords, second_cords
):  # Calculate distance between coordinates in km.
    return int(geodesic(first_cords, second_cords).km)


def country_name_to_code():
    country_name = get_location()
    try:
        country_code = coco.convert(names=country_name["country"], to="ISO2")
        return country_code
    except:
        return None
