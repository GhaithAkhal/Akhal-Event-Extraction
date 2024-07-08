import re
from typing import List, Tuple

class MyPOSTagger:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def pos_tag(self, tokens: List[str]) -> List[Tuple[str, str]]:
        # Simple heuristic POS tagging
        pos_tags = []
        for token in tokens:
            if token.lower() in {'the', 'a', 'an'}:
                pos_tags.append((token, 'DET'))
            elif token.endswith('ing'):
                pos_tags.append((token, 'VERB'))
            elif token[0].isupper():
                pos_tags.append((token, 'NOUN'))
            else:
                pos_tags.append((token, 'OTHER'))
        return pos_tags