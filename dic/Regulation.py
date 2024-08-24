from enum import Enum


class Regulation(Enum):
    REGULATE = ("regulate", ["by", "through", "in", "with"])
    CONTROL = ("control", ["by", "through", "over"])
    MODULATE = ("modulate", ["by", "through", "in"])
    ADJUST = ("adjust", ["to", "for"])
    MAINTAIN = ("maintain", ["in", "with"])
    BALANCE = ("balance", ["between", "with", "against"])
    FEEDBACK = ("feedback", ["in", "by", "through"])
    INDUCE = ("induce", ["by", "in", "through"])
