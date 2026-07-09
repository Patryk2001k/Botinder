import json
import country_converter as coco
from geopy.distance import geodesic
from ip2geotools.databases.noncommercial import DbIpCity
from flask import has_request_context, request, current_app
from pathlib import Path

from app.services.API_requests.requests import (
    get_botinderAPI_coordinates,
    get_botinderAPI_distance
)

class GeolocalizationService:
    _cities_cache = None

    @classmethod
    def _load_cities(cls) -> dict:
        """Ładuje bazę miast z pliku JSON w sposób leniwy (lazy load)."""
        if cls._cities_cache is None:
            current_dir = Path(__file__).resolve().parent
            # Scieżka do pliku cities.JSON w oryginalnej lokalizacji
            cities_path = current_dir / "geolocalization_services" / "cities.JSON"
            try:
                with open(cities_path, "r", encoding="utf-8") as f:
                    cls._cities_cache = json.load(f)
            except Exception as e:
                print(f"Błąd ładowania pliku cities.JSON pod ścieżką {cities_path}: {e}")
                cls._cities_cache = {}
        return cls._cities_cache

    @classmethod
    def get_ip(cls) -> str:
        """Pobiera bezpiecznie adres IP klienta z kontekstu zapytania Flaska."""
        ip = current_app.config.get('STATIC_USER_IP', '')
        if not ip and has_request_context():
            ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        return ip

    @classmethod
    def get_location_info(cls) -> dict:
        """Pobiera informacje o lokalizacji na podstawie adresu IP z bezpiecznym fallbackiem."""
        ip_address = cls.get_ip()
        
        # Zapobieganie błędom geolokalizacji dla lokalnych adresów IP w Dockerze
        if (not ip_address or 
            ip_address in ["127.0.0.1", "::1", "localhost"] or 
            ip_address.startswith("172.") or 
            ip_address.startswith("10.") or 
            ip_address.startswith("192.168.")):
            ip_address = "89.64.0.1"  # Przykładowe publiczne IP z Warszawy
            
        try:
            response = DbIpCity.get(ip_address, api_key="free")
            return {
                "ip": ip_address,
                "city": response.city,
                "region": response.region,
                "country": response.country,
            }
        except Exception as e:
            print(f"Błąd DbIpCity dla IP {ip_address} (zastosowano bezpieczny fallback): {e}")
            return {
                "ip": ip_address,
                "city": "Warszawa",
                "region": "Mazovia",
                "country": "PL",
            }

    @classmethod
    def get_cities(cls) -> list[str]:
        """Zwraca listę miast dla kraju, w którym aktualnie znajduje się użytkownik."""
        try:
            location = cls.get_location_info()
            country_code = location.get("country")
            
            cities_db = cls._load_cities()
            if not country_code or country_code not in cities_db:
                country_code = "PL"
                
            cities_with_country_code = cities_db.get(country_code, [])
            return [city["name"] for city in cities_with_country_code]
        except Exception as e:
            print(f"Błąd pobierania listy miast (wykorzystano fallback): {e}")
            return ["Warszawa", "Kraków", "Wrocław", "Poznań", "Gdańsk", "Łódź"]

    @classmethod
    def get_coordinates(cls, city_name: str) -> list[float]:
        """Zamienia nazwę miasta na współrzędne geograficzne."""
        try:
            response = get_botinderAPI_coordinates(city_name)
            return [response["latitude"], response["longitude"]]
        except Exception as e:
            print(f"Błąd pobierania współrzędnych dla {city_name} z API (użyto fallback): {e}")
            return [52.2297, 21.0122]  # Współrzędne Warszawy jako fallback

    @classmethod
    def calculate_distance(cls, first_lat: float, first_lon: float, second_lat: float, second_lon: float) -> int:
        """Oblicza odległość w km między dwoma punktami geograficznymi."""
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
            print(f"Błąd pobierania odległości z API (obliczono lokalnie): {e}")
            first_cords = (first_lat, first_lon)
            second_cords = (second_lat, second_lon)
            return int(geodesic(first_cords, second_cords).km)

    @classmethod
    def country_name_to_code(cls) -> str:
        """Konwertuje nazwę kraju na kod ISO2."""
        try:
            country_name = cls.get_location_info()
            return coco.convert(names=country_name["country"], to="ISO2")
        except Exception:
            return "PL"