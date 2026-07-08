from app.services.auth.auth import (
    get_current_active_user, 
    User, 
    Token, 
    OAuth2PasswordRequestForm,
    authenticate_user,
    timedelta,
    ACCES_TOKEN_EXPIRE_DAYS, 
    create_access_token
    )
from app.main import app
from fastapi import Depends
from app.dependencies.geolocation.geolocation import get_coordinates_for_city, calculate_distance


@app.get("/get_coordinates/{city_name}")
def get_coordinates(
    city_name: str, 
    coords: tuple = Depends(get_coordinates_for_city),
    current_user: User = Depends(get_current_active_user)):
    if coords == (None, None):
        return {"error": "City not found"}
    return {"city_name": city_name, "latitude": coords[0], "longitude": coords[1]}


@app.get("/distance/")
def get_distance(first_lat : float, first_lon : float, second_lat : float, second_lon : float, calculated_distance: int = Depends(calculate_distance), current_user: User = Depends(get_current_active_user)):
    if(first_lat == None and first_lon == None and second_lat == None and second_lon == None):
        return {"error": "No latitude or longitude given"}
    return {"distance": calculated_distance}

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    access_token_expires = timedelta(days=ACCES_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/users/me/items")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": 1, "owner": current_user}]