from enum import Enum


class Localization(Enum):
    LOCALIZE = ("localize", ["in", "at", "on", "to", "into"])
    TRANSPORT = ("transport", ["to", "from", "into", "through"])
    RELOCATE = ("relocate", ["to", "from", "into"])
    TARGET = ("target", ["to", "at", "for"])
    DIRECT = ("direct", ["to", "at", "towards"])
    POSITION = ("position", ["in", "at", "on", "between"])
    MOVE = ("move", ["to", "from", "into", "across", "through"])
    SECRETE = ("secrete", ["in", "by"])
    EXPORT = ("export", ["to", "from", "through"])
