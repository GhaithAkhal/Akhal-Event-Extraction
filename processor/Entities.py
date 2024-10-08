import re
from typing import List, Tuple

from processor.dic import last_entity_id as last_entity

class Entities:

    def extract_number(id_string):
        # Use regular expression to find all numeric parts
        numbers = re.findall(r'\d+', id_string)
        # Join all found numbers into a single string and convert to integer
        return int(''.join(numbers))


    def parse_a1_file(lines):
        entities = []
        for line in lines:
            parts = line.strip().split('\t')
            if len(parts) == 3:
                entity_id = parts[0]
                entity_info = parts[1].split()
                entity_type = entity_info[0]
                start_char = int(entity_info[1])
                end_char = int(entity_info[2])
                entity_text = parts[2]

                entities.append({
                    "id": entity_id,
                    "type": entity_type,
                    "start_char": start_char,
                    "end_char": end_char,
                    "text": entity_text
                })
        return entities