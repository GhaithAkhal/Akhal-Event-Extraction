from enum import Enum



class Protein_catabolism(Enum):
    CATABOLIZE = ("catabolize", ["in", "by", "through"])
    DEGRADE = ("degrade", ["by", "through", "into"])
    BREAK = ("break", ["into", "by"])
    DIGEST = ("digest", ["in", "by", "through"])
    HYDROLYZE = ("hydrolyze", ["in", "by", "with"])
    CLEAVE = ("cleave", ["into", "by", "with"])
    AUTOPHAGIZE = ("autophagize", ["in", "by"])
    UBIQUITINATE = ("ubiquitinate", ["of", "in", "by"])