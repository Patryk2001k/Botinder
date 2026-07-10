from app.services.API_requests.client import BotinderApiClient


def get_botinderAPI_token(login_url: str, login_data: dict) -> str:
    """Metoda pomocnicza zachowana dla kompatybilności (zwraca token bezpośrednio)."""
    client = BotinderApiClient()
    return client.get_token()


def get_botinderAPI_coordinates(city_name: str) -> dict:
    """Fasada kierująca żądanie do zunifikowanego klienta API."""
    client = BotinderApiClient()
    return client.get_coordinates(city_name)


def get_botinderAPI_distance(distance_params: dict) -> dict:
    """Fasada kierująca żądanie do zunifikowanego klienta API."""
    client = BotinderApiClient()
    return client.get_distance(
        first_lat=distance_params.get("first_lat"),
        first_lon=distance_params.get("first_lon"),
        second_lat=distance_params.get("second_lat"),
        second_lon=distance_params.get("second_lon"),
    )
