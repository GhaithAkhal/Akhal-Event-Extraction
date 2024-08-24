from enum import Enum


class PositiveRegulation(Enum):
    ACTIVATE = ("activate", ["by", "through", "in"])
    ENHANCE = ("enhance", ["by", "through", "in"])
    INCREASE = ("increase", ["by", "in", "with"])
    UPREGULATE = ("upregulate", ["by", "in", "through"])
    STIMULATE = ("stimulate", ["by", "through", "in"])
    PROMOTE = ("promote", ["by", "in", "through"])
    AMPLIFY = ("amplify", ["by", "in", "through"])