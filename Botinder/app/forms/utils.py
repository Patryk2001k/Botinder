from app.models.enums import *


def enum_to_choices(enum, replace):
    if replace == True:
        return [(str(i).replace("_", " "), str(i.value)) for i in enum]
    else:
        return [(str(j), str(j.value)) for j in enum]
