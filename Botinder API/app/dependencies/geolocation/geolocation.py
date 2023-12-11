from geopy.distance import geodesic
from geopy.geocoders import Nominatim

def get_coordinates_for_city(city_name):  # Generates latitude and longtude from city name
    geolocator = Nominatim(user_agent="Botinder")
    location = geolocator.geocode(city_name)

    if location:
        latitude = location.latitude
        longitude = location.longitude
        return [latitude, longitude]
    else:
        return None, None

def calculate_distance(first_lat: float, first_lon: float, second_lat: float, second_lon: float) -> int:
    first_cords = (first_lat, first_lon)
    second_cords = (second_lat, second_lon)
    return int(geodesic(first_cords, second_cords).km)