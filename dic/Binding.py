from enum import Enum


class Binding(Enum):
    BIND = ("bind", ["to", "with", "on"])
    ATTACH = ("attach", ["to", "with", "on"])
    INTERACT = ("interact", ["with", "between", "among"])
    ASSOCIATE = ("associate", ["with", "between"])
    FORM = ("form", ["with", "of"])
    ADHERE = ("adhere", ["to", "with", "on"])
    DOCK = ("dock", ["to", "at", "with"])
    AFFINATE = ("affinate", ["for", "with"])