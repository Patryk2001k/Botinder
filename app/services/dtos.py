from dataclasses import dataclass

@dataclass(frozen=True)
class LocationInfoDTO:
    ip: str
    city: str
    region: str
    country: str


@dataclass(frozen=True)
class MatchResultDTO:
    robot_image: str
    chatroom_id: int
    robot_name: str


@dataclass(frozen=True)
class ChatroomContextDTO:
    matched_robots: list
    robot_info: object  # Model UserRobot
    messages: list