from app.main import app
from fastapi import Depends
from app.dependencies.geolocation.geolocation import get_coordinates_for_city, calculate_distance

@app.get("/test")
def test():
    return {"test": "test"}

@app.get("/get_coordinates/{city_name}")
def get_coordinates_endpoint(city_name: str, coords: tuple = Depends(get_coordinates_for_city)):
    if coords == (None, None):
        return {"error": "City not found"}
    return {"city_name": city_name, "latitude": coords[0], "longitude": coords[1]}

@app.get("/distance/")
def get_distance_endpoint(first_lat: float, first_lon: float, second_lat: float, second_lon: float, calculated_distance: int = Depends(calculate_distance)):
    return {"distance": calculated_distance}