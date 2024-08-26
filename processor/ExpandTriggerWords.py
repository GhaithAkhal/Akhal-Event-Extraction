from enum import Enum
from nltk.corpus import verbnet as vn
import nltk

# Assuming that the enums are correctly defined and imported
from dic.Gene_expression import Gene_expression
from dic.Transcription import Transcription
from dic.Phosphorylation import Phosphorylation
from dic.Localization import Localization
from dic.Regulation import Regulation
from dic.Positive_regulation import Positive_regulation
from dic.Negative_regulation import Negative_regulation
from dic.Protein_catabolism import Protein_catabolism
from dic.Binding import Binding

class ExpandTriggerWords:
    @staticmethod
    def get_verbnet_frames(verb):
        frames = []
        for vn_class in vn.classids(lemma=verb):
            for frame in vn.frames(vn_class):
                syntax = frame['syntax']
                for element in syntax:
                    if 'value' in element :
                        frames.append(element['value'])
        print(f"Verb: {verb}, Frames: {frames}")
        return frames

    @staticmethod
    def expand_enum_with_verbnet(enum_class):
        vn_frames = []
        for member in enum_class:
            verb = member.name
            vn_frames.append(ExpandTriggerWords.get_verbnet_frames(verb))
        return vn_frames


# Example of expanding the GeneExpression enum with VerbNet data
NewGeneExpression = ExpandTriggerWords.expand_enum_with_verbnet(Gene_expression)
ExpandTriggerWords.expand_enum_with_verbnet(Gene_expression)
ExpandTriggerWords.expand_enum_with_verbnet(Transcription)
ExpandTriggerWords.expand_enum_with_verbnet(Protein_catabolism)
ExpandTriggerWords.expand_enum_with_verbnet(Phosphorylation)
ExpandTriggerWords.expand_enum_with_verbnet(Localization)
ExpandTriggerWords.expand_enum_with_verbnet(Binding)
ExpandTriggerWords.expand_enum_with_verbnet(Regulation)
ExpandTriggerWords.expand_enum_with_verbnet(Positive_regulation)
ExpandTriggerWords.expand_enum_with_verbnet(Negative_regulation)

for member in NewGeneExpression:
    print(f":{member} ")
