from requests import get, post


def get_botinderAPI_token(login_url: str, login_data: dict) -> str:
    response = post(f"{login_url}/token", data=login_data)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print("Nie udało się zalogować, status code:", response.status_code)
        return ""


def get_botinderAPI_coordinates(headers, city_name, botinderAPI_url):
    get_coords_url = f"{botinderAPI_url}/get_coordinates/{city_name}"
    coords_response = get(get_coords_url, headers=headers)
    print(coords_response.json())
    return coords_response.json()


def get_botinderAPI_distance(headers, distance_params: dict[float], botinderAPI_url):
    distance_url = f"{botinderAPI_url}/distance/"
    distance_response = get(distance_url, headers=headers, params=distance_params)
    print(distance_response.json())
    return distance_response.json()
