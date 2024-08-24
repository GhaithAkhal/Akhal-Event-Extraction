from enum import Enum


class Phosphorylation(Enum):
    PHOSPHORYLATE = ("phosphorylate", ["in", "on", "by"])
    ACTIVATE = ("activate", ["by", "through"])
    CATALYZE = ("catalyze", ["by", "with"])
    MODIFY = ("modify", ["by", "in"])
    TRANSFER = ("transfer", ["to", "from", "through"])
    DEPHOSPHORYLATE = ("dephosphorylate", ["in", "by"])
    SIGNAL = ("signal", ["in", "through"])
