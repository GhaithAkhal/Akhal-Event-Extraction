import re
from typing import List

class Pattern:
    # Function to generate regular expressions with every two entities
    def generate_regex_patterns_binding(entities, verbs):
        print(verbs)
        print(entities)
        patterns = []
        if len(entities) == 1:
            return None
        for entity1 in entities:
            for entity2 in entities:
                if entity1 != entity2:
                    for verb in verbs:
                        pattern = rf"{entity1} *{verb} *{entity2}*."
                        patterns.append(pattern)
        print(patterns)
        print("\n")
        return patterns