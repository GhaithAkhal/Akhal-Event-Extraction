
from typing import List, Tuple

class MyNER:
    def recognize_entities(self, tokens: List[str]) -> List[Tuple[str, str]]:
        # Simple NER using a dictionary-based approach
        entities = []
        for token in tokens:
            if token in {'John', 'Jane', 'New York'}:
                entities.append((token, 'PERSON' if token in {'John', 'Jane'} else 'LOCATION'))
            else:
                entities.append((token, 'O'))
        return entities