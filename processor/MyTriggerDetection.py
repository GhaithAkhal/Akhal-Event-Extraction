
from typing import List, Tuple
import Types
class MyTriggerDetection:
    def recognize_trriger(self, tokens: List[str]) -> List[Tuple[str, str]]:
        # Simple NER using a dictionary-based approach
        entities = []
        for token in tokens:
            if token in Types:
                entities.append((token, 1 if token in {'', ''}
                elsif  'LOCATION'))
            else:
                entities.append((token, 'O'))
        return entities