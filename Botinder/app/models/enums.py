from enum import Enum


class RobotType(Enum):
    HUMANOID = "humanoid"
    NON_HUMANOID = "non-humanoid"
    ALL = "all"

    def __str__(self):
        return self.name.lower()


class Gender(Enum):
    MALE = "male"
    FEMALE = "female"
    CUSTOM = "custom"

    def __str__(self):
        return self.name.lower()


class EmploymentStatusCriteria(Enum):
    WORKING_ROBOT = "working robot"
    DISABLED = "disabled"
    ALL = "all"

    def __str__(self):
        return self.name.lower()


class EmploymentStatusProfile(Enum):
    HIRED = "hired"
    UNEMPLOYED = "unemployed"
    STUDENT = "student"

    def __str__(self):
        return self.name.lower()
