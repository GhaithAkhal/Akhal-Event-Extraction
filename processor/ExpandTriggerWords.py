from enum import Enum
from nltk.corpus import verbnet as vn
import nltk

# Assuming that the enums are correctly defined and imported
from dic.GeneExpression import GeneExpression
from dic.Transcription import Transcription
from dic.Phosphorylation import Phosphorylation
from dic.Localization import Localization
from dic.Regulation import Regulation
from dic.PositiveRegulation import PositiveRegulation
from dic.NegativeRegulation import NegativeRegulation
from dic.ProteinCatabolism import ProteinCatabolism
from dic.Binding import Binding




class ExpandTriggerWords:

    @staticmethod
    def get_verbnet_frames(verb):
        frames = []
        for vn_class in vn.classids(lemma=verb):
            for frame in vn.frames(vn_class):
                syntax = frame['syntax']
                frame_prepositions = []
                for element in syntax:
                    # Check if the element contains the 'value' key and if it's a preposition
                    if 'value' in element and 'Prep' in element['value']:

                        frame_prepositions.append(element['value'])
                if frame_prepositions:
                    frames.append((verb, frame_prepositions))

        print(f"Verb: {verb}, Frames: {frames}")
        return frames

    @staticmethod
    def expand_enum_with_verbnet(enum_class):
        new_enum_members = {}
        for member in enum_class:
            verb, existing_prepositions = member.value
            print(f"Expanding verb: {verb}")  # Debugging: Indicate the verb being expanded
            vn_frames = ExpandTriggerWords.get_verbnet_frames(verb)
            for _, prepositions in vn_frames:
                existing_prepositions.extend(prepositions)
            # Ensure uniqueness
            existing_prepositions = list(set(existing_prepositions))
            new_enum_members[member.name] = (verb, existing_prepositions)

        # Create a new Enum with the updated values
        NewEnum = Enum(enum_class.__name__, new_enum_members)
        return NewEnum


# Example of expanding the GeneExpression enum with VerbNet data
NewGeneExpression = ExpandTriggerWords.expand_enum_with_verbnet(GeneExpression)
ExpandTriggerWords.expand_enum_with_verbnet(GeneExpression)
ExpandTriggerWords.expand_enum_with_verbnet(Transcription)
ExpandTriggerWords.expand_enum_with_verbnet(ProteinCatabolism)
ExpandTriggerWords.expand_enum_with_verbnet(Phosphorylation)
ExpandTriggerWords.expand_enum_with_verbnet(Localization)
ExpandTriggerWords.expand_enum_with_verbnet(Binding)
ExpandTriggerWords.expand_enum_with_verbnet(Regulation)
ExpandTriggerWords.expand_enum_with_verbnet(PositiveRegulation)
ExpandTriggerWords.expand_enum_with_verbnet(NegativeRegulation)

for member in NewGeneExpression:
    print(f"{member.name}: Verbs = {member.value[0]}, Prepositions = {member.value[1]}")
