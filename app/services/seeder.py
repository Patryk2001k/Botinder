from logging import getLogger
from geoalchemy2.elements import WKTElement

from app.extensions import bcrypt
from app.database import db_session
from app.models.user import User, Profile, UserCriteria
from app.services.generate_robots import generate_random_robots

logger = getLogger(__name__)


def seed_data() -> None:
    with db_session() as db_scope:

        warszawa_user = db_scope.query(User).filter_by(username="user_warszawa").first()
        if not warszawa_user:
            logger.info("Seeding test user for Warszawa (user_warszawa)...")
            hashed_pw = bcrypt.generate_password_hash("password123").decode("utf-8")

            geo_warszawa = WKTElement("POINT(21.0122 52.2297)", srid=4326)

            u_warszawa = User(
                username="user_warszawa",
                name="Jan",
                lastname="Kowalski",
                email="warszawa@botinder.pl",
                password=hashed_pw,
                image_file="default.jpg",
                location=geo_warszawa,
                domicile_geolocation=geo_warszawa,
            )
            db_scope.add(u_warszawa)
            db_scope.flush()

            p_warszawa = Profile(
                age=25,
                gender="male",
                profile_description="Hi! I am Jan from Warsaw. Looking for cool nearby robots to hang out!",
                domicile="Warszawa",
                education="Higher Education",
                employment_status="hired",
                user=u_warszawa,
            )
            c_warszawa = UserCriteria(
                type_of_robot="all",
                distance=10,
                employment_status="all",
                user=u_warszawa,
            )
            db_scope.add(p_warszawa)
            db_scope.add(c_warszawa)
            db_scope.flush()

            generate_random_robots(
                start=0,
                number_of_robots=250,
                user_location=(52.2297, 21.0122),
                user=u_warszawa,
                session=db_scope,
            )
            db_scope.commit()
            logger.info(
                "Successfully seeded Warszawa user and 250 surrounding robots within 10km."
            )

        krakow_user = db_scope.query(User).filter_by(username="user_krakow").first()
        if not krakow_user:
            logger.info("Seeding test user for Kraków (user_krakow)...")
            hashed_pw = bcrypt.generate_password_hash("password123").decode("utf-8")

            geo_krakow = WKTElement("POINT(19.9450 50.0647)", srid=4326)

            u_krakow = User(
                username="user_krakow",
                name="Anna",
                lastname="Nowak",
                email="krakow@botinder.pl",
                password=hashed_pw,
                image_file="default.jpg",
                location=geo_krakow,
                domicile_geolocation=geo_krakow,
            )
            db_scope.add(u_krakow)
            db_scope.flush()

            p_krakow = Profile(
                age=22,
                gender="female",
                profile_description="Hello! I am Anna from Kraków. Excited to meet some local artificial intelligence!",
                domicile="Kraków",
                education="Higher Education",
                employment_status="student",
                user=u_krakow,
            )
            c_krakow = UserCriteria(
                type_of_robot="all",
                distance=10,
                employment_status="all",
                user=u_krakow,
            )
            db_scope.add(p_krakow)
            db_scope.add(c_krakow)
            db_scope.flush()

            generate_random_robots(
                start=0,
                number_of_robots=250,
                user_location=(50.0647, 19.9450),
                user=u_krakow,
                session=db_scope,
            )
            db_scope.commit()
            logger.info(
                "Successfully seeded Kraków user and 250 surrounding robots within 10km."
            )
