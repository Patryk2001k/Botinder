import json
import logging  # IMPORT LOGGING
import country_converter as coco
from geopy.distance import geodesic
from ip2geotools.databases.noncommercial import DbIpCity
from flask import has_request_context, request, current_app
from pathlib import Path

from app.services.API_requests.requests import (
    get_botinderAPI_coordinates,
    get_botinderAPI_distance
)

logger = logging.getLogger(__name__)  # LOGGER INSTANCE

class GeolocalizationService:
    _cities_cache = None

    @classmethod
    def _load_cities(cls) -> dict:
        if cls._cities_cache is None:
            current_dir = Path(__file__).resolve().parent.parent
            cities_path = current_dir / "data" / "cities.json"
            try:
                with open(cities_path, "r", encoding="utf-8") as f:
                    cls._cities_cache = json.load(f)
            except Exception as e:
                logger.error(f"Failed to load cities.json from path {cities_path}: {e}", exc_info=True)  # POPRAWKA
                cls._cities_cache = {}
        return cls._cities_cache

    @classmethod
    def get_ip(cls) -> str:
        ip = current_app.config.get('STATIC_USER_IP', '')
        if not ip and has_request_context():
            ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        return ip

    @classmethod
    def get_location_info(cls) -> dict:
        ip_address = cls.get_ip()
        
        if (not ip_address or 
            ip_address in ["127.0.0.1", "::1", "localhost"] or 
            ip_address.startswith("172.") or 
            ip_address.startswith("10.") or 
            ip_address.startswith("192.168.")):
            ip_address = "89.64.0.1"
            
        try:
            response = DbIpCity.get(ip_address, api_key="free")
            return {
                "ip": ip_address,
                "city": response.city,
                "region": response.region,
                "country": response.country,
            }
        except Exception as e:
            logger.warning(f"DbIpCity lookup failed for IP {ip_address} (falling back to Warsaw, PL): {e}")  # POPRAWKA
            return {
                "ip": ip_address,
                "city": "Warszawa",
                "region": "Mazovia",
                "country": "PL",
            }

    @classmethod
    def get_cities(cls) -> list[str]:
        try:
            location = cls.get_location_info()
            country_code = location.get("country")
            
            cities_db = cls._load_cities()
            if not country_code or country_code not in cities_db:
                country_code = "PL"
                
            cities_with_country_code = cities_db.get(country_code, [])
            return [city["name"] for city in cities_with_country_code]
        except Exception as e:
            logger.error(f"Failed to generate cities list (falling back to defaults): {e}")  # POPRAWKA
            return ["Warszawa", "Kraków", "Wrocław", "Poznań", "Gdańsk", "Łódź"]

    @classmethod
    def get_coordinates(cls, city_name: str) -> list[float]:
        try:
            response = get_botinderAPI_coordinates(city_name)
            return [response["latitude"], response["longitude"]]
        except Exception as e:
            logger.warning(f"Failed to fetch coordinates for {city_name} from API (falling back to Warsaw): {e}")  # POPRAWKA
            return [52.2297, 21.0122]

    @classmethod
    def calculate_distance(cls, first_lat: float, first_lon: float, second_lat: float, second_lon: float) -> int:
        params = {
            "first_lat": first_lat,
            "first_lon": first_lon,
            "second_lat": second_lat,
            "second_lon": second_lon,
        }
        try:
            response = get_botinderAPI_distance(params)
            return response.get("distance")
        except Exception as e:
            logger.warning(f"Failed to fetch distance from API (falling back to local geodesic calculation): {e}")  # POPRAWKA
            first_cords = (first_lat, first_lon)
            second_cords = (second_lat, second_lon)
            return int(geodesic(first_cords, second_cords).km)

    @classmethod
    def country_name_to_code(cls) -> str:
        try:
            country_name = cls.get_location_info()
            return coco.convert(names=country_name["country"], to="ISO2")
        except Exception:
            return "PL"