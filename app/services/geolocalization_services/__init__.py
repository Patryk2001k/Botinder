import json
import random

import country_converter as coco
import requests
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from ip2geotools.databases.noncommercial import DbIpCity

with open("app/services/geolocalization_services/cities.json", "r") as cities_data:
    cities = json.load(cities_data)
