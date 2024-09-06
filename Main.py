from EventExtractor import EventExtractor
from processor.EventDetection import EventDetection
from processor.ExpandTriggerWords import ExpandTriggerWords
from processor.TriggerDetection import TriggerDetection
from processor.Entities import Entities
from processor.Pattern import Pattern
from processor.dic import enum_dict
from processor.dic import vn_class_mapping
from processor.dic import last_entity_id
from processor.dic import last_event_id

import re
from dic.Binding import Binding

def initialize():
    # Apply the function for all categories
    for category, vn_classes in vn_class_mapping.items():
        ExpandTriggerWords.add_verbs_from_verbnet(enum_dict, vn_classes, category)
        ExpandTriggerWords.add_words_from_wordnet(enum_dict, category)


    # Optionally remove duplicates and sort the lists
    for key in enum_dict:
        enum_dict[key] = sorted(set(enum_dict[key]))

def getLines(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

def getText(file_path):
    with open(file_path, 'r') as file:
        text = file.read().replace('\n', ' ')
    return text


new_entities = []
new_events = []
outPut = []
entities_text = []

initialize()
class Main:
    def __init__(self, file_path: str):
        self.file_path = file_path

    if __name__ == "__main__":

        # Print the updated dictionary
        for category, verbs in enum_dict.items():
            print(f"{category}: {verbs}")

        path_of_task = 'dataset/2009/'
        data_type = 'bionlp09_shared_task_training_data_rev2/'
        current_file = '1429562'
        entities_lines = getLines(path_of_task+data_type+current_file+".a1")
        last_entity_id = len(entities_lines)
        entities = Entities.parse_a1_file(entities_lines)
        text = getText(path_of_task+data_type+current_file+".txt")


        for entity in entities:
            entities_text.append(entity['text'])
        print("entities_text)")
        print(entities_text)

        #pattern = Pattern.generate_regex_patterns_binding(entities_text, enum_dict['Binding'])

        triggers = TriggerDetection.get_trigger_words(text, entities)
        EventDetection._event_classificaion(triggers,last_entity_id, last_event_id)