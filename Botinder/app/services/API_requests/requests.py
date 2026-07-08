from requests import get, post, packages
import time

def get_botinderAPI_token(login_url: str, login_data: dict) -> str:
    # Ponawiamy próbę połączenia maksymalnie 5 razy z 2-sekundowymi przerwami,
    # dając czas na uruchomienie bazy danych i serwera FastAPI.
    for attempt in range(5):
        try:
            response = post(f"{login_url}/token", data=login_data, timeout=5)
            if response.status_code == 200:
                return response.json().get("access_token")
            else:
                print(f"Błąd logowania do API (Próba {attempt+1}/5), status code: {response.status_code}")
        except Exception as e:
            print(f"API nie jest jeszcze gotowe na połączenie (Próba {attempt+1}/5): {e}")
        time.sleep(2)
    
    print("Nie udało się pobrać tokenu API po 5 próbach.")
    return ""

def get_botinderAPI_coordinates(headers, city_name, botinderAPI_url):
    get_coords_url = f"{botinderAPI_url}/get_coordinates/{city_name}"
    coords_response = get(get_coords_url, headers=headers)
    return coords_response.json()


def get_botinderAPI_distance(headers, distance_params: dict[float], botinderAPI_url):
    distance_url = f"{botinderAPI_url}/distance/"
    distance_response = get(distance_url, headers=headers, params=distance_params)
    print(distance_response.json())
    return distance_response.json()