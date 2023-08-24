import random

from faker import Faker

from services.database_operations.database_operations import *


def generate_random_robots(n=20):
    fake = Faker()

    for _ in range(n):
        # Tworzenie losowej lokalizacji na świecie
        latitude = random.uniform(-90, 90)
        longitude = random.uniform(-180, 180)

        # Ustalanie lokalizacji dla robota
        robot_location = WKTElement(f"POINT({longitude} {latitude})", srid=4326)

        # Generowanie losowej nazwy
        name = fake.first_name()

        robot = UserRobot(
            name=name,
            image_file=f"image_{i}.jpg",
            location=robot_location,
            domicile_location=robot_location,
        )

        session.add(robot)
        session.flush()

        type_of_robot = ["humanoid", "non-humanoid"]
        employment_status = ["working robot", "disabled"]

        robot_profile = RobotProfile(
            type_of_robot=type_of_robot[random.randint(0, 1)],
            name=name,
            profile_description=f"description{i}",
            domicile=f"domicile{i}",
            procesor_unit=f"i5{i}",
            employment_status=employment_status[random.randint(0, 1)],
            user_id=robot.id,
        )

        session.add(robot_profile)
    session.commit()
