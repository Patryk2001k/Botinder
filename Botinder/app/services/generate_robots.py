from json import load  # JAWNY IMPORT zamiast import json
from random import uniform, randint  # JAWNY IMPORT zamiast import random
from pathlib import Path
from logging import getLogger

from faker import Faker
from geopy.distance import great_circle
from geoalchemy2.elements import WKTElement

from app.models.robots import UserRobot, RobotProfile

logger = getLogger(__name__)

CURRENT_DIR = Path(__file__).resolve().parent.parent
DESCRIPTIONS_PATH = CURRENT_DIR / "data" / "descriptions.json"

try:
    with open(DESCRIPTIONS_PATH, "r", encoding="utf-8") as robots_descriptions:
        r_descriptions = load(robots_descriptions)
except Exception as e:
    logger.error(f"Failed to load descriptions.json from {DESCRIPTIONS_PATH}: {e}", exc_info=True)  # POPRAWKA
    r_descriptions = ["I am an advanced support android robot."]  # POPRAWKA: po angielsku


def generate_random_location_within_radius(user_location, radius_km=50):
    angle = uniform(0, 360)
    new_location = great_circle(kilometers=randint(0, radius_km)).destination(
        user_location, angle
    )
    return new_location.latitude, new_location.longitude


def generate_random_robots(
    start=0, number_of_robots=20, user_location=None, user=None, session=None
):
    logger.info(f"Generating {number_of_robots} random robots for matchmaking database...")  # POPRAWKA
    fake = Faker()
    for i in range(start, number_of_robots):
        if user_location is not None and user.user_criteria.distance is not None:
            latitude, longitude = generate_random_location_within_radius(
                user_location, user.user_criteria.distance
            )
        else:
            latitude = uniform(-90, 90)
            longitude = uniform(-180, 180)

        robot_location = WKTElement(f"POINT({longitude} {latitude})", srid=4326)
        name = fake.first_name()

        type_of_robot = ["humanoid", "non-humanoid"]
        robots_images = {
            "humanoid": ["T-1000_f.jpg", "T-1000_f_2.jpg", "T-1000_f_3.jpg"],
            "non-humanoid": ["Vacum_1.jpg", "Vacum_2.jpg"],
        }
        choosed_type_of_robot = type_of_robot[randint(0, 1)]

        robot = UserRobot(
            name=name,
            image_file=f"{choosed_type_of_robot}/{robots_images[choosed_type_of_robot][randint(0, len(robots_images[choosed_type_of_robot]) - 1)]}",
            location=robot_location,
            domicile_geolocation=robot_location,
        )

        session.add(robot)
        session.flush()

        employment_status = ["working robot", "disabled"]
        procesor_unit = ["i3", "i5", "i7", "i9"]
        procesor_value = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]

        robot_profile = RobotProfile(
            type_of_robot=choosed_type_of_robot,
            name=name,
            profile_description=f"{r_descriptions[randint(0, len(r_descriptions) - 1)]}",
            domicile=f"My-domicile{i}",
            procesor_unit=f"{procesor_unit[randint(0, 3)]}, {procesor_value[randint(0, 9)]}000",
            employment_status=employment_status[randint(0, 1)],
            user_id=robot.id,
        )

        session.add(robot_profile)
    logger.info("Successfully populated database with random robots.")  # POPRAWKA