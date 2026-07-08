from random import randint
from app.services.database_operations.database_operations import (
    session_scope, add_match_unmatch, add_chatroom,
    get_single_matched_robot, get_robot_info_by_chatroom_id,
    get_matched_robots
)
from app.models.matches import UnMatches, UserMatches, RobotMatches
from app.services.robot_match.robot_selector import get_robots_for_user
from app.services.helpers import generate_robots, robot_to_dict

class MatchmakingService:
    @classmethod
    def get_candidate_robots(cls, user) -> list[dict]:
        """Pobiera i formatuje listę robotów dopasowaną do geolokalizacji i kryteriów użytkownika."""
        with session_scope() as session:
            robots_list = get_robots_for_user(user, session)
            if not robots_list:
                # Automatyczne generowanie robotów w bazie, jeśli brak dopasowań
                generate_robots(
                    current_user=user, session=session, number_of_robots=5000
                )
                robots_list = get_robots_for_user(user, session)
            return robot_to_dict(robots_list) if robots_list else []

    @classmethod
    def get_matches(cls, user) -> list:
        """Pobiera listę pomyślnie zmatchowanych robotów wraz z ID ich pokojów rozmów."""
        with session_scope() as session:
            return get_matched_robots(
                session, user.id, user.name, include_chatroom_id="yes"
            )

    @classmethod
    def unmatch_robot(cls, user, robot_id: int, robot_name: str) -> None:
        """Zapisuje odrzucenie robota przez użytkownika."""
        with session_scope() as session:
            add_match_unmatch(
                session,
                user.id,
                user.name,
                robot_id,
                robot_name,
                UnMatches,
            )

    @classmethod
    def match_robot(cls, user, robot_id: int, robot_name: str) -> dict | None:
        """Obsługuje polubienie robota i symuluje losowe (1/3 szansy) odwzajemnienie polubienia."""
        with session_scope() as session:
            # Zapisujemy polubienie użytkownika
            add_match_unmatch(
                session,
                user.id,
                user.name,
                robot_id,
                robot_name,
                UserMatches,
            )

            # Robot odwzajemnia polubienie (losowo 1 na 3 próby)
            if randint(0, 2) == 1:
                add_match_unmatch(
                    session,
                    user.id,
                    user.name,
                    robot_id,
                    robot_name,
                    RobotMatches,
                )
                add_chatroom(session, user.id, robot_id)
                
                match_result = get_single_matched_robot(
                    user.id, user.name, robot_id, session
                )
                robot_info = get_robot_info_by_chatroom_id(session, match_result[1])
                
                return {
                    "robot_image": robot_info.image_file,
                    "chatroom_id": match_result[1],
                    "robot_name": robot_info.name,
                }
            return None