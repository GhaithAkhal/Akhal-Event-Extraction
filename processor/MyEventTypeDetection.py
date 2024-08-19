
import Types as event_type
from typing import List, Tuple
from dic.Binding import Binding
from dic.Gene_expression import Gene_expression
from dic.Binding import Binding
from dic.Binding import Binding
from dic.Binding import Binding


class MyEventTypeDetection:
    def _event_classificaion(self, possible_trigger_words: List[str]) -> List[Tuple[str, str]]:
        # Simple NER using a dictionary-based approach
        entities = []
        for word in possible_trigger_words:
            match word:
                case Binding:
                    print()
                case Gene_expression:

                case Transcription :

                case Protein_catabolism :

                case Phosphorylation :

                case Localization :

                case Binding :

                case Regulation :

                case Positive_regulation :

                case Negative_regulation :

                case _: print("No match")
        return entities