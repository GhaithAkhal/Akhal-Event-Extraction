from enum import Enum


class Gene_expression(Enum):
    EXPRESS = ("express", ["in", "on", "by", "through"])
    TRANSCRIBE = ("transcribe", ["from", "into"])
    TRANSLATE = ("translate", ["into", "from"])
    SYNTHESIZE = ("synthesize", ["in", "from"])
    PRODUCE = ("produce", ["by", "in", "from"])
    ENCODE = ("encode", ["in", "by", "for"])
    REGULATE = ("regulate", ["in", "by", "through"])
    ACTIVATE = ("activate", ["of", "in"])
    MODIFY = ("modify", ["in", "by", "through"])