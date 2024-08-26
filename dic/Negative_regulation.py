from enum import Enum


class Negative_regulation(Enum):
    INHIBIT = ("inhibit", ["by", "through", "in"])
    SUPPRESS = ("suppress", ["by", "through", "in"])
    DECREASE = ("decrease", ["by", "in", "with"])
    DOWNREGULATE = ("downregulate", ["by", "in", "through"])
    BLOCK = ("block", ["by", "from", "through"])
    REPRESS = ("repress", ["by", "through", "in"])
    SILENCE = ("silence", ["by", "through", "in"])
    FEEDBACK = ("feedback", ["in", "by", "through"])