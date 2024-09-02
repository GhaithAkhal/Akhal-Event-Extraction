from EventExtractor import EventExtractor

from TextFileReader import TextFileReader
from processor.ExpandTriggerWords import ExpandTriggerWords
from processor.TriggerDetection import TriggerDetection
from processor.Entities import Entities
from processor.Pattern import Pattern
import re
from dic.Binding import Binding




def getLines(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines
def getText(file_path):
    with open(file_path, 'r') as file:
        text = file.read().replace('\n', ' ')
    return text
class Main:
    def __init__(self, file_path: str):
        self.file_path = file_path

    if __name__ == "__main__":
        enum_dict = {
            # prepare step, expand the data set
            'Binding': ['bind', 'attach', 'interact', 'associate', 'form', 'adhere', 'dock', 'affiliate'],
            'Gene_expression': ['express', 'transcribe', 'synthesize', 'produce', 'encode', 'regulate', 'activate',
                                'modify'],
            'Localization': ['localize', 'transport', 'relocate', 'target', 'direct', 'position', 'move', 'secrete',
                             'export'],
            'Negative_regulation': ['inhibit', 'suppress', 'decrease', 'downregulate', 'block', 'repress', 'silence',
                                    'feedback'],
            'Phosphorylation': ['phosphorylate', 'activate', 'catalyze', 'modify', 'transfer', 'dephosphorylate',
                                'signal'],
            'Positive_regulation': ['activate', 'enhance', 'increase', 'upregulate', 'stimulate', 'promote', 'amplify'],
            'Protein_catabolism': ['catabolite', 'degrade', 'BREAK', 'digest', 'hydrolyze', 'cleave', 'autophagize',
                                   'ubiquitinate'],
            'Regulation': ['regulate', 'control', 'modulate', 'adjust', 'maintain', 'balance', 'feedback', 'induce'],
            'Transcription': ['transcribe', 'copy', 'replicate', 'translate', 'reverse', 'read', 'synthesize',
                              'initiate',
                              'terminate']
        }
        # Define the mapping of categories to VerbNet classes
        vn_class_mapping = {
                'Binding': ['amalgamate-22.2', 'shake-22.3', 'tape-22.4', 'cooking-45.3', 'mix-22.1', 'funnel-9.3'],
                'Gene_expression': ['declare-29.4', 'illustrate-25.3', 'indicate-78'],
                'Localization': ['put-9.1', 'carry-11.4', 'send-11.1'],
                'Negative_regulation': ['forbid-67', 'stop-55.4', 'neglect-75', 'avoid-52', 'banish-10.2'],
                'Phosphorylation': ['change_bodily_state-40.8.4'],
                'Positive_regulation': ['urge-58', 'force-59', 'enforce-63', 'advise-37.9', 'allow-64', 'approve-77'],
                'Protein_catabolism': ['consume-66', 'remove-10.1', 'destroy-44'],
                'Regulation': ['enforce-63', 'care-88', 'order-60'],
                'Transcription': ['transcribe-25.4', 'transcribe-25.4']
        }

        # Apply the function for all categories
        for category, vn_classes in vn_class_mapping.items():
            ExpandTriggerWords.add_verbs_from_verbnet(enum_dict, vn_classes, category)

        # Optionally remove duplicates and sort the lists
        for key in enum_dict:
            enum_dict[key] = sorted(set(enum_dict[key]))

        # Print the updated dictionary
        for category, verbs in enum_dict.items():
            print(f"{category}: {verbs}")


        path_of_task = 'dataset/2009/'
        data_type = 'bionlp09_shared_task_training_data_rev2/'
        current_file = '1386962'
        entities_lines = getLines(path_of_task+data_type+current_file+".a1")
        entities = Entities.parse_a1_file(entities_lines)

        text = getText(path_of_task+data_type+current_file+".txt")
        triggers= TriggerDetection.get_trigger_words(text, entities)
        for detail in triggers:
            print(f"Sentence: {detail['sentence']}")
            print(f"Entity: {detail['entity']['text']} (Start: {detail['entity']['start_char']}, End: {detail['entity']['end_char']})")
            for verb in detail["verbs"]:
                print(f"Verb: {verb['text']} (Start: {verb['start_char']}, End: {verb['end_char']})")
            print("-" * 50)

        entities_text = []
        for entity in entities:
            entities_text.append(entity['text'])
        print("entities_text)")
        print(entities_text)

        #print(verb_preposition_pairs)
        pattern = Pattern.generate_regex_patterns_binding(entities_text, enum_dict['Binding'])
        #print(pattern)
