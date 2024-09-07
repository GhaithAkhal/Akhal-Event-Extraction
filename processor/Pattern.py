import re
from typing import List

class Pattern:
    # Function to generate regular expressions with every two entities
    def generate_regex_patterns_binding(entities, verb):
        print(verb)
        print(entities)
        entity_text = []
        for entity in entities:
            entity_text.append(entity['text'])
        entity_pattern = "\w+\s\w+"
        patterns = []
        for entity1 in entity_text:
            for entity2 in entity_text:
                if entity1 != entity2:
                    pattern = rf"\b{entity1}\b.*?\b{verb}\b.*?\b{entity2}\b"
                    patterns.append(pattern)
        return patterns