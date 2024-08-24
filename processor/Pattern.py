import re
from typing import List

class Pattern:
    # Function to generate regular expressions with every two entities
    def generate_regex_patterns(entities, verb_preposition_pairs):
        patterns = []
        for entity1 in entities:
            for entity2 in entities:
                if entity1 != entity2:
                    for verb, prep in verb_preposition_pairs:
                        pattern = rf"{entity1} {verb} {entity2} {prep} ({'|'.join(entities)})"
                        patterns.append(pattern)
        return patterns

# Function to extract all verbs and prepositions from an Enum class
    def extract_verbs_and_prepositions(enum_class):
        verb_preposition_pairs = []
        for member in enum_class:
            verb = member.value[0]
            prepositions = member.value[1]
            for prep in prepositions:
                verb_preposition_pairs.append((verb, prep))
        return verb_preposition_pairs

    def extract_entities(file_path):
        entities = []
        with open(file_path, 'r') as file:
            lines = file.readlines()
        for i in range(len(lines)):
            line = lines[i].strip()
            words = line.split()
            if words:
                last_word = words[-1]
                if re.match(r'^-?\d+$', last_word):  # Check if the last word is a number
                    number = last_word
                    for j in range(i - 1, -1, -1):  # Go back through previous lines
                        previous_line = lines[j].strip()
                        previous_word = previous_line.split()[-1]
                        if previous_word:
                            match = re.match(r"([a-zA-Z0-9-]+)(\d+)", previous_word)
                            if match:
                                replaced_word = f'{match.group(1)}{number}'
                                entities.append(replaced_word)
                                break
                else:
                    entities.append(last_word)
            else:
                entities.append('')
        return entities