from enum import Enum


class Transcription(Enum):
    TRANSCRIBE = ("transcribe", ["from", "into", "on"])
    COPY = ("copy", ["from", "into", "to"])
    REPLICATE = ("replicate", ["from", "into"])
    TRANSLATE = ("translate", ["into", "from"])
    REVERSE = ("reverse", ["from", "to"])
    READ = ("read", ["from", "into"])
    SYNTHESIZE = ("synthesize", ["in", "from"])
    INITIATE = ("initiate", ["at", "from"])
    TERMINATE = ("terminate", ["at", "from", "in"])

