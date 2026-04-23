from enum import Enum

class MenuSpecialType(str, Enum):
    NONE = "NONE"
    TODAYS_SPECIAL = "TODAYS_SPECIAL"
    DEAL_OF_THE_DAY = "DEAL_OF_THE_DAY"