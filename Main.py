import glob
import os

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


outPut = []
entities_text = []

initialize()
class Main:
    def __init__(self, file_path: str):
        self.file_path = file_path

    if __name__ == "__main__":

        source_directory = r'dataset\2009\bionlp09_shared_task_training_data_rev2'  # Source directory
        destination_directory = r'dataset\result'
        source_files = glob.glob(os.path.join(source_directory, '*.a1'))
        for file_path in source_files:

            filename_without_extension = os.path.splitext(os.path.basename(file_path))[0]
            if filename_without_extension.startswith('R' or 'L'):
                pass
            else:
                destination_file_path = os.path.join(destination_directory, filename_without_extension + '.a2')
                try:
                    text_path = os.path.join(source_directory, filename_without_extension +'.txt')
                    text = getText(text_path)
                    entities_lines = getLines(file_path)
                    last_entity_id = len(entities_lines)
                    entities = Entities.parse_a1_file(entities_lines)
                    for entity in entities:
                        entities_text.append(entity['text'])

                    triggers = TriggerDetection.get_trigger_words(text, entities)
                    newEntities,newEvents = EventDetection._event_classificaion(triggers,last_entity_id, last_event_id)
                    with open(destination_file_path, 'w') as destination_file:
                        for line in newEntities:
                            destination_file.write(line + "\n")
                        for line in newEvents:
                            destination_file.write(line + "\n")
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")
        print("Completed processing all files.")