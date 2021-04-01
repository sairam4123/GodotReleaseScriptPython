from enum import Enum, auto


class ReleaseLevel(Enum):
    alpha = auto()
    beta = auto()
    release_candidate = auto()
    public = auto()

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_.values()


class ReleaseType(Enum):
    bugfix = auto()
    minor = auto()
    major = auto()
    hotfix = auto()

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_.values()


def value_from_key(dict_, value):
    for key in dict_:
        if dict_[key] == value:
            return key
    return None
