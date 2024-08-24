from enum import Enum


class Types(Enum):
    Gene_expression = "Gene_expression"
    Transcription = "Transcription"
    Protein_catabolism = "ProteinCatabolism"
    Phosphorylation = "Phosphorylation"
    Localization = "Localization"
    Binding = "Binding"
    Regulation = "Regulation"
    Positive_regulation = "PositiveRegulation"
    Negative_regulation = "NegativeRegulation"