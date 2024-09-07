import nltk
from typing import List, Tuple
import re

from nltk import word_tokenize, pos_tag
from nltk.stem import PorterStemmer
from processor.dic import enum_dict
from nltk.corpus import wordnet as wn
from processor.Pattern import Pattern
from processor.dic import side_dic
nltk.download('wordnet')
nltk.download('omw-1.4')

new_entities = []
new_events = []
output = []
output_directory = 'dataset/result'
def extract_site(sentence, position):
    words = word_tokenize(sentence)
    pos_tags = pos_tag(words)
    index_site = None
    site = None
    i = 0
    while i < len(words):
        word = words[i].lower()
        # Check for single-word amino acids or other entities
        if (word in side_dic['amino_acids']
                or word in side_dic['protein_domains']
                or word in side_dic['chemical_modifications']
                or word in side_dic['cellular_locations']
                or word in side_dic['molecular_interactions']):
            site = words[i]
            index_site = sentence.index(site) + position
            break

        # Check for multi-word terms (amino acids, protein domains, etc.)
        if i + 1 < len(words):
            two_word_phrase = f"{words[i].lower()} {words[i+1].lower()}"
            if (two_word_phrase in side_dic['amino_acids']
                    or two_word_phrase in side_dic['protein_domains']
                    or two_word_phrase in side_dic['chemical_modifications']
                    or two_word_phrase in side_dic['cellular_locations']
                    or two_word_phrase in side_dic['molecular_interactions']):
                site = f"{words[i]} {words[i+1]}"
                index_site = sentence.index(site) + position
                break
        i += 1
    return site, index_site

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

def extract_binding_event(sentence, entities, verb, last_event_id):
    entity_data = []
    protein1_data = {}
    protein2_data = {}
    i = 0;
    for entity in entities:
        entity_id = entity['id']
        entity_type = entity['type']
        entity_positions = (entity['start_char'], entity['end_char'])
        entity_text = entity['text']
        if i == 0:
            protein1_data = {
                'id': entity_id,
                'type': entity_type,
                'positions': entity_positions,
                'text': entity_text}
        if i == 1:
            protein2_data = {
                'id': entity_id,
                'type': entity_type,
                'positions': entity_positions,
                'text': entity_text}
        i += 1
    # Generate regex patterns
    patterns = Pattern.generate_regex_patterns_binding(entities, verb)
    print(entity_data)
    # Find matches in text
    events = []
    for pattern in patterns:
        matches = re.finditer(pattern, sentence)
        for match in matches:
            if match:
                binding_event = f"E{last_event_id} Binding:{protein1_data['id']} Theme:{protein1_data['id']} Theme2:{protein2_data['id']}"
                new_events.append(binding_event)

    return events



def extract_localization_event(sentence, position):
    cellular_locations = side_dic['cellular_locations']

    words = word_tokenize(sentence)
    pos_tags = pos_tag(words)
    start_loc = None
    location = None
    for word, tag in pos_tags:
        # Check if the word is a cellular location
        if word.lower() in cellular_locations:
            location = word
            start_loc = position + sentence.index(location)
            break
    return location, start_loc

def  extract_regulation_event(trigger_word, sentence,entities, position):
    cause = None
    site = None
    index_site = None
    words = word_tokenize(sentence)
    pos_tags = pos_tag(words)

    # Prepositions that indicate the site and cause
    site_prepositions = ['at', 'on', 'in']
    cause_prepositions = ['by', 'due to', 'because of', 'from']

    # Iterate through the sentence to find the trigger word and its context
    for i, (word, tag) in enumerate(pos_tags):
        if word == trigger_word:
            # Check for cause after the trigger
            for j in range(i + 1, len(words)):
                if words[j] in cause_prepositions:
                    if j + 1 < len(words) and pos_tags[j + 1][1].startswith('NN'):
                        cause_candidate = words[j + 1]
                        # Check if the cause is a known entity
                        for entity in entities:
                            if cause_candidate in entity['text']:
                                cause = entity
                                break
                        if cause is None:
                            cause = cause_candidate
                        break

            # Check for site near the trigger
            for j in range(i + 1, len(words)):
                if words[j] in site_prepositions:
                    if j + 1 < len(words) and pos_tags[j + 1][1].startswith('NN'):
                        site_candidate = words[j + 1]
                        # Check if the site is a known entity
                        for entity_wrapper in entities:
                            entity = entity_wrapper['entity']
                            if site_candidate in entity['text']:
                                site = entity['text']
                                index_site = sentence.index(site) + position
                                break
                        if site is None:
                            site = site_candidate
                            index_site = sentence.index(site) + position
                        break
            break
    return site, index_site, cause

def create_new_entity( last_entity_id, entity_type, entity_start, entity_end, entity):
    if check_if_entity_unique(entity, entity_start, entity_end):
        new_entities.append(
            f"T{last_entity_id}\t{entity_type} {entity_start} {entity_end}\t{entity}")
        return True
    return False


class EventDetection:
    # Simple Events are Gene_expression  Phosphorylation, Transcription, Protein_catabolism
    def _event_classificaion(triggers, last_entity_id, last_event_id):
        current_position = 0
        local_entities = []
        for detail in triggers:
            current_position += len(detail['sentence'])
            print(f"Sentence: {detail['sentence']}")
            for entity_wrapper in detail["entities"]:
                entity = entity_wrapper['entity']
                local_entities.append(entity)
                print(f"Entity: {entity['text']}\t{entity['start_char']}  {entity['end_char']}")
                for verb in detail["verbs"]:
                    print(f"{verb['tag']}:\t{verb['text']} {verb['start_char']} {verb['end_char']}")
                    extracted_entity_type = get_word_type(verb['text'])
                    if extracted_entity_type is not None:
                        last_event_id += 1
                        if extracted_entity_type in ['Negative_regulation', 'Positive_regulation', 'Regulation']:
                            if create_new_entity(last_entity_id, extracted_entity_type, verb['start_char'], verb['end_char'], verb['text']):
                                last_entity_id += 1
                            # Example: theme and site extraction logic for regulation
                            site, index_site, cause = extract_regulation_event(
                                verb['text'], detail['sentence'], local_entities, current_position)
                            if cause is not None:
                                if site is not None:
                                    if create_new_entity(last_entity_id, 'Entity', current_position+index_site,
                                                      current_position + index_site + len(site), site):
                                        last_entity_id += 1
                                    new_events.append(f"E{last_event_id}\t{extracted_entity_type}:T{last_entity_id}\tTheme:{last_entity_id - 1}\tCause:{cause['id']}\tCSide:{last_entity_id}")
                                else:
                                    new_events.append(
                                        f"E{last_event_id}\t{extracted_entity_type}:T{last_entity_id}\tTheme:{last_entity_id - 1}\tCause:{cause['id']}")
                            else:
                                if site is not None:
                                    if create_new_entity(last_entity_id, 'Entity', current_position+index_site,
                                                      current_position + index_site + len(site), site):
                                        last_entity_id += 1
                                    new_events.append(f"E{last_event_id}\t{extracted_entity_type}:T{last_entity_id}\tTheme:{entity['id']} Side:T{last_entity_id-1}")
                                else:
                                    new_events.append(f"E{last_event_id}\t{extracted_entity_type}:T{last_entity_id}\tTheme:{entity['id']}")

                        elif extracted_entity_type == 'Localization':
                            if create_new_entity(last_entity_id, extracted_entity_type, verb['start_char'], verb['end_char'], verb['text']):
                                last_entity_id += 1
                            # Localization extraction logic
                            location, start_loc = extract_localization_event(detail['sentence'], current_position)
                            if location is not None:
                                if create_new_entity(last_entity_id, 'Entity', current_position+start_loc,
                                                  current_position + start_loc + len(location), location):
                                    last_entity_id += 1
                                f"E{last_event_id}\t{entity['type']}:T{last_entity_id}\tTheme:{entity['id']} AtLoc:{last_entity_id}"

                            new_events.append(
                                f"E{last_event_id}\t{extracted_entity_type}:T{last_entity_id}\tTheme:{entity['id']}")
                        elif extracted_entity_type == 'Phosphorylation':
                            if create_new_entity(last_entity_id, extracted_entity_type, verb['start_char'], verb['end_char'], verb['text']):
                                last_entity_id += 1
                            # Phosphorylation site extraction logic
                            site, index_site = extract_site(detail['sentence'], current_position)
                            if site is not None:
                                if create_new_entity(last_entity_id, 'Entity', current_position + index_site,
                                                  current_position + index_site + len(site), site):
                                    last_entity_id += 1
                                new_events.append(
                                    f"E{last_event_id}\t{extracted_entity_type}:T{last_entity_id}\tTheme:{entity['id']} Side:T{last_entity_id - 1}")
                            else:
                                new_events.append(
                                    f"E{last_event_id}\t{extracted_entity_type}:T{last_entity_id}\tTheme:{entity['id']}")

                        elif extracted_entity_type == 'Binding':
                            # Binding extraction logic
                            if create_new_entity(last_entity_id, extracted_entity_type, verb['start_char'], verb['end_char'],verb['text']):
                                last_entity_id += 1
                            if len(local_entities) ==1:
                                new_events.append(f"E{last_event_id}\t{extracted_entity_type}:T{last_entity_id}\tTheme:{entity['id']}")
                            else:
                                extract_binding_event(detail['sentence'], local_entities, verb['text'], last_entity_id)
                        else:
                            # Default case for handling unique entities
                            if create_new_entity(last_entity_id, extracted_entity_type, verb['start_char'], verb['end_char'], verb['text']):
                                last_entity_id += 1
                            # Create an event linking the verb and the entity
                            new_events.append(
                                f"E{last_event_id}\t{extracted_entity_type}:T{last_entity_id}\tTheme:{entity['id']}")
            local_entities = []

        return new_entities,new_entities