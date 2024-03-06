import json
import random
from random import uniform

from faker import Faker
from geopy.distance import great_circle

from app.models import Session
from app.services.database_operations.database_operations import *
from app.services.database_operations.database_operations import session_scope

with open(
    "app/services/database_operations/robots_generator/descriptions.json",
    "r",
    encoding="utf-8",
) as robots_descriptions:
    r_descriptions = json.load(robots_descriptions)


def generate_random_location_within_radius(user_location, radius_km=50):
    angle = uniform(0, 360)
    new_location = great_circle(kilometers=random.randint(0, radius_km)).destination(
        user_location, angle
    )
    return new_location.latitude, new_location.longitude


# I need this function to generate robots and simulate search in database full of robots like 5000 robots
def generate_random_robots(
    start=0, number_of_robots=20, user_location=None, user=None, session=None
):
    fake = Faker()
    for i in range(start, number_of_robots):
        if user_location is not None and user.user_criteria.distance is not None:
            latitude, longitude = generate_random_location_within_radius(
                user_location, user.user_criteria.distance
            )
        else:
            latitude = random.uniform(-90, 90)
            longitude = random.uniform(-180, 180)

        robot_location = WKTElement(f"POINT({longitude} {latitude})", srid=4326)

        name = fake.first_name()

        type_of_robot = ["humanoid", "non-humanoid"]
        robots_images = {
            "humanoid": ["T-1000_f.jpg", "T-1000_f_2.jpg", "T-1000_f_3.jpg"],
            "non-humanoid": ["Vacum_1.jpg", "Vacum_2.jpg"],
        }
        choosed_type_of_robot = type_of_robot[random.randint(0, 1)]

        robot = UserRobot(
            name=name,
            image_file=f"{choosed_type_of_robot}/{robots_images[choosed_type_of_robot][random.randint(0, len(robots_images[choosed_type_of_robot]) - 1)]}",
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
            profile_description=f"{r_descriptions[random.randint(0, len(r_descriptions) - 1)]}",
            domicile=f"My-domicile{i}",
            procesor_unit=f"{procesor_unit[random.randint(0, 3)]}, {procesor_value[random.randint(0, 9)]}000",
            employment_status=employment_status[random.randint(0, 1)],
            user_id=robot.id,
        )

        session.add(robot_profile)
