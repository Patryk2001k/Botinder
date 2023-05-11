import requests
import random
from geonamescache import GeonamesCache
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import country_converter as coco
from geocoder import 

def get_coordinates(city_name): #Generates latitude and longtude from city name
    geolocator = Nominatim(user_agent="Botinder") 
    location = geolocator.geocode(city_name) 

    if location:
        latitude = location.latitude
        longitude = location.longitude
        return latitude, longitude
    else:
        return None, None


def get_cities(country_code):
    gc = GeonamesCache()
    cities = gc.get_cities()
    #country_cities = [i for i in cities]
    #print(country_cities["countrycode"])
    #print(cities["1106542"])
    #for i in cities:
        #if cities[i]["countrycode"] == "PL":
            #print(cities[i]["name"])
            #if cities[i]["name"] == "Warszawa" or "Warszawa" in cities[i]["alternatenames"]:
                #print("---------------")
                #print(cities[i]["name"])


def generate_random_ip() -> str: #Generates random IP address
    ip = ".".join(str(random.randint(0, 255)) for i in range(4))
    return ip

def get_location(): #Functions gets localization from IP address
    ip_address = generate_random_ip()
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name")
    }
    return location_data

def distance(first_cords, second_cords): #Oblicza odległośc pomiędzy jednymi koordynatami a drugimi
    return int(geodesic(first_cords, second_cords).km)

def country_name_to_code(country_name):
    try:
        country_code = coco.convert(names=country_name, to='ISO3')
        return country_code
    except coco.CountryNotFoundError:
        return None
