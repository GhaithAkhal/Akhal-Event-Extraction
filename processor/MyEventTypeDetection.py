
import Types as event_type
from typing import List, Tuple


class MyEventTypeDetection:
    def _event_classificaion(self, possible_trigger_words: List[str]) -> List[Tuple[str, str]]:
        # Simple NER using a dictionary-based approach
        entities = []
        # for word in possible_trigger_words:
        #     match word:
                # case event_type Binding:
                #     print()
                # case Gene_expression:
                #     print()
                # case Transcription :
                #     print()
                # case Protein_catabolism :
                #     print()
                # case Phosphorylation :
                #     print()
                # case Localization :
                #     print()
                # case Binding :
                #     print()
                # case Regulation :
                #     print()
                # case Positive_regulation :
                #     print()
                # case Negative_regulation :
                #     print()
                # case _:
                #     print("No match")
        return entities