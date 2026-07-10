from random import randint
from sqlalchemy.orm import joinedload  # POPRAWKA (PEP 8): Import joinedload na górze pliku
from app.services.database_operations import (
    session_scope, add_match_unmatch, add_chatroom,
    get_single_matched_robot, get_robot_info_by_chatroom_id,
    get_matched_robots
)
from app.models.matches import UnMatches, UserMatches, RobotMatches
from app.models.chatroom import ChatRoom  # POPRAWKA (PEP 8): Import modelu ChatRoom na górze
from app.services.robot_selector import get_robots_for_user
from app.services.generate_robots import generate_random_robots
from app.services.helpers import robot_to_dict
from app.services.dtos import MatchResultDTO

class MatchmakingService:
    @classmethod
    def get_candidate_robots(cls, user) -> list[dict]:
        with session_scope() as session:
            robots_list = get_robots_for_user(user, session)
            if not robots_list:
                generate_random_robots(
                    start=0, number_of_robots=5000, user_location=None, user=user, session=session
                )
                robots_list = get_robots_for_user(user, session)
            return robot_to_dict(robots_list) if robots_list else []

    @classmethod
    def get_matches(cls, user) -> list:
        """Pobiera dotychczasowe mecze użytkownika z bezpiecznym eager loadingiem powiązań robotów."""
        with session_scope() as session:
            # Eager loading powiązania robot w tabeli UserMatches, aby zapobiec DetachedInstanceError w szablonie
            user_matches = session.query(UserMatches).options(joinedload(UserMatches.robot)).filter_by(user_id=user.id, user_name=user.name).all()
            robot_matches = session.query(RobotMatches).filter_by(user_id=user.id, user_name=user.name).all()

            user_match_ids = [match.robot_id for match in user_matches]
            robot_match_ids = [match.robot_id for match in robot_matches]
            common_matched_robot_ids = list(set(user_match_ids) & set(robot_match_ids))

            chatroom_query = (
                session.query(ChatRoom)
                .filter(
                    ChatRoom.user_id == user.id,
                    ChatRoom.robot_id.in_(common_matched_robot_ids),
                )
                .all()
            )
            chatroom_ids = {chatroom.robot_id: chatroom.id for chatroom in chatroom_query}

            matched_with_chatroom = []
            for match in user_matches:
                chatroom_id = chatroom_ids.get(match.robot_id)
                if chatroom_id and match.robot_id in common_matched_robot_ids:
                    matched_with_chatroom.append((match, chatroom_id))
            return matched_with_chatroom

    @classmethod
    def unmatch_robot(cls, user, robot_id: int, robot_name: str) -> None:
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
    def match_robot(cls, user, robot_id: int, robot_name: str) -> MatchResultDTO | None:
        with session_scope() as session:
            add_match_unmatch(
                session,
                user.id,
                user.name,
                robot_id,
                robot_name,
                UserMatches,
            )

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
                
                return MatchResultDTO(
                    robot_image=robot_info.image_file,
                    chatroom_id=match_result[1],
                    robot_name=robot_info.name
                )
            return None