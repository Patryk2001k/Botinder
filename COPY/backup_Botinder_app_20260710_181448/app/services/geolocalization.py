from logging import getLogger  # JAWNY IMPORT
from os import environ  # JAWNY IMPORT
import country_converter as coco
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from ip2geotools.databases.noncommercial import DbIpCity
from flask import has_request_context, request, current_app

from app.services.dtos import LocationInfoDTO

logger = getLogger(__name__)


class GeolocalizationService:

    @classmethod
    def get_ip(cls) -> str:
        ip = current_app.config.get("STATIC_USER_IP", "")
        if not ip and has_request_context():
            ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        return ip

    @classmethod
    def get_location_info(cls) -> LocationInfoDTO:
        ip_address = cls.get_ip()

        if (
            not ip_address
            or ip_address in ["127.0.0.1", "::1", "localhost"]
            or ip_address.startswith("172.")
            or ip_address.startswith("10.")
            or ip_address.startswith("192.168.")
        ):
            ip_address = "89.64.0.1"

        try:
            response = DbIpCity.get(ip_address, api_key="free")
            return LocationInfoDTO(
                ip=ip_address,
                city=response.city,
                region=response.region,
                country=response.country,
            )
        except Exception as e:
            logger.warning(
                f"DbIpCity lookup failed for IP {ip_address} (falling back to Warsaw, PL): {e}"
            )
            return LocationInfoDTO(
                ip=ip_address, city="Warszawa", region="Mazovia", country="PL"
            )

    @classmethod
    def get_coordinates(cls, city_name: str) -> list[float]:
        """Konwertuje nazwę miasta na współrzędne geograficzne NATYWNIE przy użyciu geopy."""
        geolocator = Nominatim(user_agent="Botinder_App_Decoupled_Monolith_Client_2026")
        try:
            location = geolocator.geocode(city_name, timeout=10)
            if location:
                logger.info(
                    f"Successfully geocoded '{city_name}' to [{location.latitude}, {location.longitude}] natively."
                )
                return [location.latitude, location.longitude]
            logger.warning(
                f"City '{city_name}' not found by native geocoder. Using default Warsaw coordinates."
            )
        except Exception as e:
            logger.error(
                f"Error during native geocoding of city '{city_name}': {e}",
                exc_info=True,
            )
        return [52.2297, 21.0122]  # Fallback: Warszawa

    @classmethod
    def calculate_distance(
        cls, first_lat: float, first_lon: float, second_lat: float, second_lon: float
    ) -> int:
        """Oblicza odległość geodezyjną w kilometrach NATYWNIE przy użyciu geopy."""
        try:
            first_cords = (first_lat, first_lon)
            second_cords = (second_lat, second_lon)
            dist = int(geodesic(first_cords, second_cords).km)
            return dist
        except Exception as e:
            logger.error(
                f"Error during native distance calculation: {e}", exc_info=True
            )
            return 0

    @classmethod
    def country_name_to_code(cls) -> str:
        try:
            country_name = cls.get_location_info()
            return coco.convert(names=country_name.country, to="ISO2")
        except Exception:
            return "PL"
