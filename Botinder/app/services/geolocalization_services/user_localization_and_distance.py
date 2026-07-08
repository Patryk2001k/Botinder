import json
import random
import country_converter as coco
from geopy.distance import geodesic
from ip2geotools.databases.noncommercial import DbIpCity
from flask import has_request_context, request, current_app # POPRAWKA: current_app
from app.services.API_requests.requests import (get_botinderAPI_coordinates,
                                                get_botinderAPI_distance)

# Bezpieczne ładowanie pliku JSON
try:
    with open("app/services/geolocalization_services/cities.JSON", "r") as cities_data:
        cities = json.load(cities_data)
except Exception as e:
    print("Nie udało się załadować pliku cities.JSON:", e)
    cities = {}


def get_coordinates(city_name):
    try:
        response = get_botinderAPI_coordinates(
            current_app.config.get("BOTINDER_API_HEADERS", {}), 
            city_name, 
            current_app.config.get("BOTINDER_API_URL")
        )
        return [response["latitude"], response["longitude"]]
    except Exception as e:
        print("Błąd pobierania współrzędnych z API (użyto fallback):", e)
        return [52.2297, 21.0122] # Współrzędne Warszawy


def get_cities():
    try:
        location = get_location()
        country_code = location.get("country")
        
        if not country_code or country_code not in cities:
            country_code = "PL"
            
        cities_with_country_code = cities.get(country_code, [])
        country_cities = [i["name"] for i in cities_with_country_code]
        return country_cities
    except Exception as e:
        print("Błąd podczas generowania listy miast (użyto fallback):", e)
        return ["Warszawa", "Kraków", "Wrocław", "Poznań", "Gdańsk", "Łódź"]


def get_ip() -> str:
    ip = current_app.config.get('STATIC_USER_IP', '')
    if not ip:
        if has_request_context():
            ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    return ip


def get_location():
    ip_address = get_ip()
    
    if (not ip_address or 
        ip_address in ["127.0.0.1", "::1", "localhost"] or 
        ip_address.startswith("172.") or 
        ip_address.startswith("10.") or 
        ip_address.startswith("192.168.")):
        ip_address = "89.64.0.1"
        
    try:
        response = DbIpCity.get(ip_address, api_key="free")
        location_data = {
            "ip": ip_address,
            "city": response.city,
            "region": response.region,
            "country": response.country,
        }
    except Exception as e:
        print(f"Błąd ip2geotools dla IP {ip_address} (zastosowano bezpieczny fallback): {e}")
        location_data = {
            "ip": ip_address,
            "city": "Warszawa",
            "region": "Mazovia",
            "country": "PL",
        }
    return location_data


def distance(first_lat, first_lon, second_lat, second_lon):
    params = {
        "first_lat": first_lat,
        "first_lon": first_lon,
        "second_lat": second_lat,
        "second_lon": second_lon,
    }
    try:
        response = get_botinderAPI_distance(
            current_app.config.get("BOTINDER_API_HEADERS", {}), 
            params, 
            current_app.config.get("BOTINDER_API_URL")
        )
        return response.get("distance")
    except Exception as e:
        print("Błąd pobierania dystansu z API (obliczono lokalnie):", e)
        first_cords = (first_lat, first_lon)
        second_cords = (second_lat, second_lon)
        return int(geodesic(first_cords, second_cords).km)


def country_name_to_code():
    try:
        country_name = get_location()
        country_code = coco.convert(names=country_name["country"], to="ISO2")
        return country_code
    except:
        return "PL"