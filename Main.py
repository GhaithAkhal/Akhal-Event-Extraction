import glob
import os
import time

from EventExtractor import EventExtractor
from processor.EventDetection import EventDetection
from processor.ExpandTriggerWords import ExpandTriggerWords
from processor.TriggerDetection import TriggerDetection
from processor.Entities import Entities
from processor.dic import enum_dict
from processor.dic import vn_class_mapping
from processor.dic import last_entity_id
from processor.dic import last_event_id


import re

def classify_lines(file_content):
    # Initialize dictionary with empty lists for different classifications
    classified_lines = []

    for line in file_content.split("\n"):
        if line.startswith("T"):
            parts = line.split()
            entity_type = parts[1]
            term = parts[-1]
            classified_lines.append(f'{entity_type} {term}')
    return classified_lines


def read_a2_files(directory_path):
    all_classified_lines = []
    files = glob.glob(os.path.join(directory_path, '*.a2'))
    print(f'Files found: {files}')

    for filename in files:
        print(f'Reading file: {filename}')

        with open(filename, 'r') as file:
            file_content = file.read()

        classified_lines = classify_lines(file_content)
        all_classified_lines.extend(classified_lines)

    all_classified_lines = sorted(set(all_classified_lines))
    return all_classified_lines


def initialize():
    # Apply the function for all categories
    # for category, vn_classes in vn_class_mapping.items():
    #     ExpandTriggerWords.add_verbs_from_verbnet(enum_dict, vn_classes, category)
    #     ExpandTriggerWords.add_words_from_wordnet(enum_dict, category)


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


entities_text = []

initialize()


class Main:
    def __init__(self, file_path: str):
        self.file_path = file_path

    if __name__ == "__main__":

        # classified_data = read_a2_files(r'dataset\2009\bionlp09_shared_task_training_data_rev2')
        # outPut =[]
        # # You can display classified data or process it further as needed
        # for line in classified_data:
        #     parts = line.split(' ')
        #     if parts[0] == 'Transcription':
        #         outPut.append(parts[1])
        #
        # print(outPut)
        #     # if parts[0] == 'Gene_expression':
        #     # if parts[0] == 'Localization':
        #     # if parts[0] == 'Negative_regulation':
        #     # if parts[0] == 'Phosphorylation':
        #     # if parts[0] == 'Positive_regulation':
        #     # if parts[0] == 'Protein_catabolism':
        #     # if parts[0] == 'Regulation':
        #     # if parts[0] == 'Transcription':




        start_time = time.time()
        source_directory = r'dataset\2009\bionlp09_shared_task_development_data_rev1'  # Source directory
        destination_directory = r'dataset\new5'
        source_files = glob.glob(os.path.join(source_directory, '*.a1'))
        for file_path in source_files:

            filename_without_extension = os.path.splitext(os.path.basename(file_path))[0]
            if filename_without_extension.startswith('R' or 'L'):
                pass
            else:
                #try:
                destination_file_path = os.path.join(destination_directory, filename_without_extension + '.a2')
                text_path = os.path.join(source_directory, filename_without_extension + '.txt')
                text = getText(text_path)
                entities_lines = getLines(file_path)

                last_entity_id = len(entities_lines)
                last_event_id = 1
                entities = Entities.parse_a1_file(entities_lines)
                for entity in entities:
                    entities_text.append(entity['text'])

                if last_entity_id > 0:
                    triggers = TriggerDetection.get_trigger_words(text, entities)
                    newEntities, newEvents = EventDetection._event_classification(triggers, last_entity_id+1,
                                                                                 last_event_id)
                    with open(destination_file_path, 'w') as destination_file:
                        for newEntity in newEntities:
                            destination_file.write(newEntity + "\n")

                        for event in newEvents:
                            destination_file.write(event + "\n")

                        newEvents.clear()
                        newEntities.clear()
                        entities.clear()
                        entities_lines.clear()
                        text = ''
                    print(f"End processing file {filename_without_extension}")
                #except Exception as e:
                #    print(f"Error processing file {file_path}: {e}")
        print("Completed processing all files.")
        print("--- %s seconds ---" % (time.time() - start_time))
