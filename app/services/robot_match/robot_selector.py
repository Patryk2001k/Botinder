from geoalchemy2.shape import to_shape
from geopy.distance import geodesic

from app.services.database_operations.database_operations import (
    get_not_matched_robots_by_localization, get_user_criteria, session_scope)

MINIMUM_MATCHED_ROBOTS = MINIMUM_NOT_MATCHED_ROBOTS = 10


def filter_robots_by_criteria(robots, user_criteria):
    robots_matched_user_criteria = []
    robots_not_matched_user_criteria = []
    for robot in robots:
        if match_robot_type(user_criteria, robot) and match_employment_status(
            user_criteria, robot
        ):
            robots_matched_user_criteria.append(robot)
        else:
            robots_not_matched_user_criteria.append(robot)
    return {
        "matched_robots": robots_matched_user_criteria,
        "not_matched_robots": robots_not_matched_user_criteria,
    }


def match_robot_type(user_criteria, robot):
    return (
        user_criteria.type_of_robot == "all"
        or robot.profile_robot.type_of_robot == user_criteria.type_of_robot
    )


def match_employment_status(user_criteria, robot):
    return (
        user_criteria.employment_status == "all"
        or robot.profile_robot.employment_status == user_criteria.employment_status
    )


def wkt_to_tuple(point):
    return (point.y, point.x)


def calculate_distance(first_cords, second_cords):
    return int(geodesic(first_cords, second_cords).km)


def sort_robots_by_distance(robots_array, user):
    user_location = to_shape(user.location)
    return_array = []
    for robot in robots_array:
        dist = calculate_distance(
            wkt_to_tuple(user_location), wkt_to_tuple(to_shape(robot.location))
        )
        return_array.append([robot, {"distance_to_user": dist}])
    return sorted(return_array, key=lambda x: x[1]["distance_to_user"])


def rank_robots(no_ranked_robots, user_criteria, user):
    robots_by_criteria = filter_robots_by_criteria(no_ranked_robots, user_criteria)
    sorted_robots_matched = sort_robots_by_distance(
        robots_by_criteria["matched_robots"], user
    )
    if len(sorted_robots_matched) < MINIMUM_MATCHED_ROBOTS:
        sorted_robots_not_matched = sort_robots_by_distance(
            robots_by_criteria["not_matched_robots"], user
        )
        sorted_robots_matched.extend(sorted_robots_not_matched)
    return sorted_robots_matched


def get_robots_for_user(user, session):
    robots = get_not_matched_robots_by_localization(user, session)
    user_criteria = get_user_criteria(user, session)
    if len(robots) > 1:
        return rank_robots(robots, user_criteria, user)
    else:
        return False
