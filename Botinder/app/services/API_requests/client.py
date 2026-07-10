import os
import time
import logging  # IMPORT LOGGING
from threading import Lock
import requests
from flask import current_app

logger = logging.getLogger(__name__)  # LOGGER INSTANCE

class BotinderApiClient:
    _instance = None
    _lock = Lock()

    _token = None
    _token_timestamp = 0
    _token_lifetime = 12 * 60 * 60  # Cache ważny przez 12 godzin

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = super(BotinderApiClient, cls).__new__(cls)
            return cls._instance

    def __init__(self):
        self.base_url = current_app.config.get("BOTINDER_API_URL")
        self.login_data = current_app.config.get("BOTINDER_API_LOGIN_DATA")

    def _is_token_expired(self) -> bool:
        if not self._token:
            return True
        return time.time() - self._token_timestamp > self._token_lifetime

    def get_token(self) -> str:
        if self._is_token_expired():
            with self._lock:
                if self._is_token_expired():
                    self._token = self._fetch_new_token()
                    self._token_timestamp = time.time()
        return self._token

    def _fetch_new_token(self) -> str:
        url = f"{self.base_url}/token"
        try:
            response = requests.post(url, data=self.login_data, timeout=5)
            if response.status_code == 200:
                token = response.json().get("access_token", "")
                logger.info("Successfully fetched and cached new Botinder-API access token.")  # POPRAWKA
                return token
            else:
                logger.error(f"Failed to authenticate with Botinder-API (Status: {response.status_code}): {response.text}")  # POPRAWKA
                return ""
        except requests.RequestException as e:
            logger.error(f"Network error during authorization with Botinder-API: {e}")  # POPRAWKA
            return ""

    def _get_headers(self) -> dict:
        token = self.get_token()
        return {"Authorization": f"Bearer {token}"}

    def get_coordinates(self, city_name: str) -> dict:
        url = f"{self.base_url}/get_coordinates/{city_name}"
        try:
            response = requests.get(url, headers=self._get_headers(), timeout=5)
            if response.status_code == 200:
                return response.json()
            logger.error(f"API get_coordinates returned error (Status: {response.status_code}): {response.text}")  # POPRAWKA
        except requests.RequestException as e:
            logger.error(f"Network connection failed in API get_coordinates: {e}")  # POPRAWKA
        return {}

    def get_distance(self, first_lat: float, first_lon: float, second_lat: float, second_lon: float) -> dict:
        url = f"{self.base_url}/distance/"
        params = {
            "first_lat": first_lat,
            "first_lon": first_lon,
            "second_lat": second_lat,
            "second_lon": second_lon,
        }
        try:
            response = requests.get(url, headers=self._get_headers(), params=params, timeout=5)
            if response.status_code == 200:
                return response.json()
            logger.error(f"API get_distance returned error (Status: {response.status_code}): {response.text}")  # POPRAWKA
        except requests.RequestException as e:
            logger.error(f"Network connection failed in API get_distance: {e}")  # POPRAWKA
        return {}