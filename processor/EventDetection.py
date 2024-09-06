import nltk
from typing import List, Tuple
from nltk.stem import PorterStemmer
from processor.dic import enum_dict
from nltk.corpus import wordnet as wn
from processor.Pattern import Pattern
nltk.download('wordnet')
nltk.download('omw-1.4')

new_entities = []
new_events = []


def get_word_type(word):

    lemma = lemmatizer.stem(word.lower())
    # Überprüfe, ob das Lemma in einer der Kategorien in enum_dict ist
    for category, verbs in enum_dict.items():
        for verb in verbs:
            if lemma == lemmatizer.stem(verb):
                return category  # Gib die Kategorie zurück, falls gefunden
    return None
def simple_event_type(ext_verb):
    lemma = lemmatizer.stem(ext_verb.lower())
    for category, verbs in enum_dict.items():
        if (category == 'Gene_expression' or category == 'Transcription'
                or category == 'Protein_catabolism'):
            for verb in verbs:
                if lemma == lemmatizer.stem(verb):
                    return category
    return None


def check_if_entity_unique(newEntity, start_char, end_char):
    if len(new_entities) == 0:
        return True
    for entity in new_entities:
        parts = entity.split('\t')
        entity_start = int(parts[1].split()[1])
        entity_end = int(parts[1].split()[2])
        entity_text = parts[2]
        if (entity_text == newEntity
                and entity_start == start_char
                and entity_end == end_char):
            return False
    return True


lemmatizer = PorterStemmer()

def extract_binding_event(entities):
    my_entitis = []
    for entity_wrapper in entities:
        entity = entity_wrapper['entity']
        my_entitis.append(entity['text'])
    pattern = Pattern.generate_regex_patterns_binding(my_entitis, enum_dict['Binding'])
    return
def extract_phosphorylation_event():
    pass


def extract_localization_event():
    pass

def  extract_regulation_event(verb, sentence):
    site = []
    case = []
    return case, site

def create_new_entity( last_entity_id, entity_type, entity_start, entity_end, entity):
    if check_if_entity_unique(entity, entity_start, entity_end):
        new_entities.append(
            f"T{last_entity_id}\t{entity_type} {entity_start} {entity_end}\t{entity}")
        return True
    return False
def extract_simple_event(last_event_id, last_entity_id, entity_type, entity):
    new_events.append(
        f"E{last_event_id}\t{entity_type}:T{last_entity_id}\tTheme:{entity['id']}")

class EventDetection:
    # Simple Events are Gene_expression  Phosphorylation, Transcription, Protein_catabolism
    def _event_classificaion(triggers, last_entity_id, last_event_id):
        for detail in triggers:
            print(f"Sentence: {detail['sentence']}")
            for entity_wrapper in detail["entities"]:
                entity = entity_wrapper['entity']
                print(f"Entity: {entity['text']}\t{entity['start_char']}  {entity['end_char']}")
                for verb in detail["verbs"]:
                    print(f"{verb['tag']}:\t{verb['text']} {verb['start_char']} {verb['end_char']}")
                    extracted_entity_type = get_word_type(verb['text'])
                    if extracted_entity_type in ['Negative_regulation', 'Positive_regulation', 'Regulation']:
                        if create_new_entity(last_entity_id, extracted_entity_type, verb['start_char'], verb['end_char'], verb['text']):
                            last_entity_id += 1
                        # Example: theme and site extraction logic for regulation
                        case, site = extract_regulation_event(verb['text'], detail['sentence'])

                    elif extracted_entity_type == 'Localization':
                        if create_new_entity(last_entity_id, extracted_entity_type, verb['start_char'], verb['end_char'], verb['text']):
                            last_entity_id += 1
                        # Localization extraction logic
                        extract_localization_event()

                    elif extracted_entity_type == 'Phosphorylation':
                        if create_new_entity(last_entity_id, extracted_entity_type, verb['start_char'], verb['end_char'], verb['text']):
                            last_entity_id += 1
                        # Phosphorylation site extraction logic
                        extract_phosphorylation_event()

                    elif extracted_entity_type == 'Binding':
                        # Binding extraction logic
                        if create_new_entity(last_entity_id, extracted_entity_type, verb['start_char'], verb['end_char'],verb['text']):
                            last_entity_id += 1
                        extract_binding_event(detail["entities"], detail['sentence'])
                    else:
                        # Default case for handling unique entities
                        if create_new_entity(last_entity_id, extracted_entity_type, verb['start_char'], verb['end_char'], verb['text']):
                            last_entity_id += 1
                        # Create an event linking the verb and the entity
                        last_event_id += 1
                        extract_simple_event(last_event_id, extracted_entity_type, last_entity_id, entity['id'])
                    print("- " * 25)

        for n in new_entities:
            print(f"{n} ,")
        for n in new_events:
            print(f"{n} ,")