import unittest

from flask import url_for
from flask_login import current_user

from app import app
from app.services.helper_functions import robot_to_dict


class RoutesTest(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["LOGIN_DISABLED"] = True
        self.client = app.test_client()

    def test_home_route(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        with app.test_request_context("/"):
            if current_user.is_authenticated:
                self.assertEqual(url_for("user_homepage"), response.location)

    def test_lore_route(self):
        response = self.client.get("/lore")
        self.assertEqual(response.status_code, 200)
        self.assertIn("lore.html", response.get_data(as_text=True))

    def test_FAQ_route(self):
        response = self.client.get("/FAQ")
        self.assertEqual(response.status_code, 200)
        self.assertIn("FAQ.html", response.get_data(as_text=True))


class TestUtils(unittest.TestCase):
    def test_robot_to_dict(self):
        mock_robots = [
            MockRobot(
                1, "Robot1", "CPU1", "Type1", "Desc1", "Working", "image1.jpg", 10
            ),
            MockRobot(
                2, "Robot2", "CPU2", "Type2", "Desc2", "Not Working", "image2.jpg", 20
            ),
        ]

        table = [
            (robot, {"distance_to_user": robot.distance_to_user})
            for robot in mock_robots
        ]

        result = robot_to_dict(table)

        self.assertEqual(len(result), 2)  # Sprawdzenie liczby robotów
        self.assertEqual(result[0]["id"], 1)
        self.assertEqual(result[0]["name"], "Robot1")
        self.assertEqual(result[0]["distance_to_user"], 10)


# Simulation of the robot object
class MockRobot:
    def __init__(
        self,
        id,
        name,
        procesor_unit,
        type_of_robot,
        profile_description,
        employment_status,
        image_file,
        distance_to_user,
    ):
        self.id = id
        self.name = name
        self.profile_robot = MockProfileRobot(
            procesor_unit, type_of_robot, profile_description, employment_status
        )
        self.image_file = image_file
        self.distance_to_user = distance_to_user


class MockProfileRobot:
    def __init__(
        self, procesor_unit, type_of_robot, profile_description, employment_status
    ):
        self.procesor_unit = procesor_unit
        self.type_of_robot = type_of_robot
        self.profile_description = profile_description
        self.employment_status = employment_status
