from sqlalchemy.orm import joinedload
from app.services.database_operations import (
    session_scope,
    get_chatroom_messages,
    add_match_unmatch,
    delete_chatroom,
    delete_matched_pair,
    add_message_to_chatroom,
)
from app.models.matches import UnMatches, UserMatches, RobotMatches
from app.models.chatroom import ChatRoom
from app.models.robots import UserRobot  # POPRAWKA (PEP 8): Importujemy model robota
from app.services.tasks import calL_GPT_API
from app.services.dtos import ChatroomContextDTO


class ChatService:
    @classmethod
    def get_chatroom_context(cls, user, chatroom_id: int) -> ChatroomContextDTO:
        """Pobiera i pakuje kontekst czatu do obiektu ChatroomContextDTO z bezpiecznym, głębokim eager loadingiem."""
        with session_scope() as session:
            # 1. Pobieramy mecze użytkownika z eager loadem relacji robot
            user_matches = (
                session.query(UserMatches)
                .options(joinedload(UserMatches.robot))
                .filter_by(user_id=user.id, user_name=user.name)
                .all()
            )
            robot_matches = (
                session.query(RobotMatches)
                .filter_by(user_id=user.id, user_name=user.name)
                .all()
            )

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
            chatroom_ids = {
                chatroom.robot_id: chatroom.id for chatroom in chatroom_query
            }

            matched_robots = []
            for match in user_matches:
                cid = chatroom_ids.get(match.robot_id)
                if cid and match.robot_id in common_matched_robot_ids:
                    matched_robots.append((match, cid))

            # 2. POPRAWKA: Pobieramy chatroom i łączymy zapytania (joinedload chain-ing)
            # tak, aby pobrać pokój czatu -> przypisanego robota -> oraz PROFIL tego robota w jednym zapytaniu!
            chatroom = (
                session.query(ChatRoom)
                .options(joinedload(ChatRoom.robot).joinedload(UserRobot.profile_robot))
                .filter_by(id=chatroom_id)
                .first()
            )
            robot_info = chatroom.robot if chatroom else None

            # 3. Pobieramy wiadomości czatu
            chat_messages = get_chatroom_messages(session, chatroom_id)

            return ChatroomContextDTO(
                matched_robots=matched_robots,
                robot_info=robot_info,
                messages=chat_messages,
            )

    @classmethod
    def unmatch_chatroom(
        cls, user, chatroom_id: int, robot_id: int, robot_name: str, user_name: str
    ) -> None:
        with session_scope() as session:
            add_match_unmatch(
                session,
                user.id,
                user.name,
                robot_id,
                robot_name,
                UnMatches,
            )
            delete_chatroom(session, chatroom_id)
            delete_matched_pair(session, user_name, robot_name)

    @classmethod
    def process_user_message(cls, chatroom_id: int, message_text: str) -> str:
        gpt_response = calL_GPT_API()

        with session_scope() as session:
            add_message_to_chatroom(
                session, message_text, chatroom_id, message_sender="user"
            )
            add_message_to_chatroom(
                session, gpt_response, chatroom_id, message_sender="robot"
            )
        return gpt_response
