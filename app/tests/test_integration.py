import unittest
from unittest.mock import patch

from app import app


class MockUserObject:
    def __init__(self, name):
        self.name = name


class TestRegistration(unittest.TestCase):
    def create_app(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        return app

    def test_register(self):
        with patch("app.routes.get_image") as mock_get_image, patch(
            "app.routes.insert_user_and_user_profile"
        ) as mock_insert, patch(
            "app.routes.UserObject", return_value=MockUserObject("test_user")
        ) as mock_user_object:
            mock_get_image.return_value = "test_image.jpg"
            mock_insert.return_value = None

            with app.test_client() as client:
                response = client.post(
                    "/register",
                    data={
                        "username": "testuser",
                        "password": "testpassword",
                        "confirm_password": "testpassword",
                        "email": "testowy@test.pl",
                        "type_of_robot": "humanoid",
                        "distance": 50,
                        "employment_status_criteria": "working_robot",
                        "age": 20,
                        "name": "testname",
                        "lastname": "testlastname",
                        "gender": "male",
                        "profile_description": "desc",
                        "domicile": "TCracow",
                        "education": "Tedx",
                        "employment_status_profile": "working",
                    },
                    follow_redirects=True,
                )

                self.assertEqual(response.status_code, 200)
                mock_get_image.assert_called_once()
                mock_insert.assert_called_once()
                mock_user_object.assert_called_once_with("testuser")
