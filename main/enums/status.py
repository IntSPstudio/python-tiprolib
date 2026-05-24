#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#GLOBAL DATA STATUS
from enum import IntEnum

class Status(IntEnum):
    PASSIVE = 0
    ACTIVE = 1
    DELETED = 4

    @classmethod
    def is_valid(cls, value):
        return value in cls._value2member_map_