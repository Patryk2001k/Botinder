import os
import time
from threading import Lock
import requests
from flask import current_app

class BotinderApiClient:
    _instance = None
    _lock = Lock()

    # Zmienne klasowe służące jako cache dla tokenu
    _token = None
    _token_timestamp = 0
    _token_lifetime = 12 * 60 * 60  # Cache ważny przez 12 godzin

    def __new__(cls, *args, **kwargs):
        """Wzorzec Singleton gwarantujący jedną instancję klienta w całej aplikacji."""
        with cls._lock:
            if not cls._instance:
                cls._instance = super(BotinderApiClient, cls).__new__(cls)
            return cls._instance

    def __init__(self):
        # Pobieranie konfiguracji dynamicznie z kontekstu uruchomionej aplikacji Flaska
        self.base_url = current_app.config.get("BOTINDER_API_URL")
        self.login_data = current_app.config.get("BOTINDER_API_LOGIN_DATA")

    def _is_token_expired(self) -> bool:
        """Sprawdza, czy token wygasł lub nie został jeszcze pobrany."""
        if not self._token:
            return True
        return time.time() - self._token_timestamp > self._token_lifetime

    def get_token(self) -> str:
        """Pobiera token z cache procesu lub loguje się na nowo, jeśli wygasł (on-demand)."""
        if self._is_token_expired():
            with self._lock:
                # Blokada podwójnego sprawdzenia (Double-checked locking pattern)
                if self._is_token_expired():
                    self._token = self._fetch_new_token()
                    self._token_timestamp = time.time()
        return self._token

    def _fetch_new_token(self) -> str:
        """Wykonuje fizyczne żądanie POST /token do FastAPI."""
        url = f"{self.base_url}/token"
        try:
            response = requests.post(url, data=self.login_data, timeout=5)
            if response.status_code == 200:
                token = response.json().get("access_token", "")
                print("Pomyślnie wygenerowano i zapisano w cache nowy token Botinder-API.")
                return token
            else:
                print(f"Błąd logowania do API (Status: {response.status_code}): {response.text}")
                return ""
        except requests.RequestException as e:
            print(f"Wyjątek sieciowy podczas próby autoryzacji w Botinder-API: {e}")
            return ""

    def _get_headers(self) -> dict:
        """Generuje nagłówki autoryzacyjne."""
        token = self.get_token()
        return {"Authorization": f"Bearer {token}"}

    def get_coordinates(self, city_name: str) -> dict:
        """Pobiera współrzędne miasta z mikrousługi FastAPI."""
        url = f"{self.base_url}/get_coordinates/{city_name}"
        try:
            response = requests.get(url, headers=self._get_headers(), timeout=5)
            if response.status_code == 200:
                return response.json()
            print(f"Błąd API get_coordinates (Status: {response.status_code})")
        except requests.RequestException as e:
            print(f"Błąd sieciowy API get_coordinates: {e}")
        return {}

    def get_distance(self, first_lat: float, first_lon: float, second_lat: float, second_lon: float) -> dict:
        """Pobiera odległość między dwoma współrzędnymi z mikrousługi FastAPI."""
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
            print(f"Błąd API get_distance (Status: {response.status_code})")
        except requests.RequestException as e:
            print(f"Błąd sieciowy API get_distance: {e}")
        return {}