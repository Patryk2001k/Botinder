from app.services.auth.auth import get_current_active_user, User
from app.main import app
from fastapi import Depends
from app.dependencies.geolocation.geolocation import get_coordinates_for_city, calculate_distance

#zapytanie: http://127.0.0.1:8000/ftest/?test_data1=123
@app.get("/ftest/")
def ftest(test_data1: int, current_user: User = Depends(get_current_active_user)):
    return {"test": test_data1}

@app.get("/get_coordinates/{city_name}")
def get_coordinates_endpoint(
    city_name: str, 
    coords: tuple = Depends(get_coordinates_for_city),
    current_user: User = Depends(get_current_active_user)):  # Dodanie zależności uwierzytelniającej
    if coords == (None, None):
        return {"error": "City not found"}
    return {"city_name": city_name, "latitude": coords[0], "longitude": coords[1]}


@app.get("/distance/")
def get_distance_endpoint(first_lat : float, first_lon : float, second_lat : float, second_lon : float, calculated_distance: int = Depends(calculate_distance), current_user: User = Depends(get_current_active_user)):
    return {"distance": calculated_distance}

