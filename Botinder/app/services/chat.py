from app.services.database_operations.database_operations import (
    session_scope, get_matched_robots, get_robot_info_by_chatroom_id,
    get_chatroom_messages, add_match_unmatch, delete_chatroom, delete_matched_pair,
    add_message_to_chatroom
)
from app.models.matches import UnMatches
from app.services.tasks.tasks import calL_GPT_API

class ChatService:
    @classmethod
    def get_chatroom_context(cls, user, chatroom_id: int) -> dict:
        """Pobiera kompletny zestaw danych wymagany do wyrenderowania pokoju czatu."""
        with session_scope() as session:
            matched_robots = get_matched_robots(
                session, user.id, user.name, include_chatroom_id=True
            )
            robot_info = get_robot_info_by_chatroom_id(session, chatroom_id)
            chat_messages = get_chatroom_messages(session, chatroom_id)
            return {
                "matched_robots": matched_robots,
                "robot_info": robot_info,
                "messages": chat_messages,
            }

    @classmethod
    def unmatch_chatroom(cls, user, chatroom_id: int, robot_id: int, robot_name: str, user_name: str) -> None:
        """Trwale usuwa pokój rozmów, dotychczasowe dopasowania i zapisuje zdarzenie odrzucenia."""
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
        """Zapisuje wiadomość od użytkownika, odpytuje GPT API i zapisuje odpowiedź robota."""
        # Pobieranie odpowiedzi z silnika AI
        gpt_response = calL_GPT_API()

        with session_scope() as session:
            add_message_to_chatroom(
                session, message_text, chatroom_id, message_sender="user"
            )
            add_message_to_chatroom(
                session, gpt_response, chatroom_id, message_sender="robot"
            )
        return gpt_response