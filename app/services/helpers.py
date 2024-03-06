from app.services.database_operations.robots_generator.generate_robots import \
    generate_random_robots, update_user_location_domicile, session_scope
from app.services.geolocalization_services.user_localization_and_distance import \
    get_coordinates
from app.services.robot_match.robot_selector import to_shape, wkt_to_tuple

def robot_to_dict(table):
    return [
        {
            "id": table[i][0].id,
            "name": table[i][0].name,
            "distance_to_user": table[i][1]["distance_to_user"],
            "procesor_unit": table[i][0].profile_robot.procesor_unit,
            "type_of_robot": table[i][0].profile_robot.type_of_robot,
            "description": table[i][0].profile_robot.profile_description,
            "working_robot": table[i][0].profile_robot.employment_status,
            "image_file": table[i][0].image_file,
        }
        for i in range(len(table))
    ]


def generate_robots(current_user, session, number_of_robots=5000):
    if current_user.location is None:
        with session_scope() as session:
            update_user_location_domicile(session, current_user) #get_coordinates(current_user.profile.domicile)
        generate_random_robots(
            start=0,
            number_of_robots=number_of_robots,
            user_location=wkt_to_tuple(to_shape(current_user.domicile_geolocation)),
            user=current_user,
            session=session,
        )
    else:
        generate_random_robots(
            start=0,
            number_of_robots=number_of_robots,
            user_location=wkt_to_tuple(to_shape(current_user.location)),
            user=current_user,
            session=session,
        )
