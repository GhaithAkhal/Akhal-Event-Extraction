from itertools import combinations

import nltk
from typing import List, Tuple
import re

from nltk import word_tokenize, pos_tag
from nltk.stem import PorterStemmer
from processor.dic import enum_dict
from nltk.corpus import wordnet as wn
from processor.dic import side_dic

nltk.download('wordnet')
nltk.download('omw-1.4')

new_entities = []
new_events = []

lemmatizer = PorterStemmer()


def get_trigger_of_entity(id):
    for line in new_entities:
        parts = line.split('\t')
        if id == parts[0]:
            return parts[2]
    return ''


def get_event_id(line):
    parts = line.split('\t')
    return parts[0]


def get_trigger_word_of_Event(line):
    parts = line.split('\t')
    data_1 = parts[1]
    data_2 = data_1.split(' ')
    trigger_entity_id = data_2[0]
    data_3 = trigger_entity_id.split(":")
    entity_id = data_3[1]
    data_4 = data_2[1]
    data_5 = data_4.split(':')
    theme_id = data_5[1]
    entity_word = get_trigger_of_entity(entity_id)
    theme = None
    if theme_id.startswith('T'):
        theme = get_trigger_of_entity(theme_id)
    return entity_word, theme


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


def check_if_event_unique(event_type_trigger, theme, theme2=None):
    if len(new_events)>0:
        for event in new_events:
            parts = event.split(' ')
            data = parts[0]
            new_parts = data.split('\t')
            new_event_type_trigger = new_parts[1]
            new_theme = parts[1]
            if theme2 is not None and len(parts) > 2:
                if parts[2] == theme2:
                    return False
                print(new_theme)
            elif new_event_type_trigger == event_type_trigger and theme == new_theme:
                return False
            else:
                return True
    return True
def create_new_entity(last_entity_id, entity_type, entity_start, entity_end, entity):
    if check_if_entity_unique(entity, entity_start, entity_end):
        new_entities.append(
            f"T{last_entity_id}\t{entity_type} {entity_start} {entity_end}\t{entity}")
        return True
    return False


# Extraction Functions
def extract_site(sentence, position, trigger):
    trigger = str(trigger)
    index_site = None
    site = None
    combined_words = '|'.join([re.escape(word) for key in side_dic for word in side_dic[key]])
    site_pattern_after = re.compile(rf"({re.escape(trigger)})\b\s+(to\s+)?.*?\b({combined_words})\s+(\w+)",
                                    re.IGNORECASE)
    site_pattern_before = re.compile(
        rf"({combined_words})\b\s+(to\s+)?.*?\b{re.escape(trigger)}\b\s+(\w+)",
        re.IGNORECASE
    )
    match_after = re.search(site_pattern_after, sentence)
    match_before = re.search(site_pattern_before, sentence)
    if match_after:
        site = match_after.group()
        index_site = match_after.start() + position
    if match_before:
        site = match_before.group()
        index_site = match_before.start() + position
    return site, index_site


def extract_localization_event(sentence, position, trigger):
    cellular_locations_to_pattern = re.compile(fr"{re.escape(trigger)}\b\s+(to\s+)?.*?(" + '|'.join(
        [re.escape(cl) for cl in side_dic['cellular_locations']]) + r")\s+(\w+)",
                                               re.IGNORECASE)
    cellular_locations_at_pattern = re.compile(fr"{re.escape(trigger)}\b\s+(to\s+)?.*?(" + '|'.join(
        [re.escape(cl) for cl in side_dic['cellular_locations']]) + r")\s+(\w+)",
                                               re.IGNORECASE)

    match = re.search(cellular_locations_to_pattern, sentence)
    if match:
        location = match.group()
        start_loc = match.start() + position
        return location, start_loc, 'To'
    match = re.search(cellular_locations_at_pattern, sentence)
    if match:
        location = match.group()
        start_loc = match.start() + position
        return location, start_loc, 'At'
    return None, None, None


def extract_binding_event(sentence, entities, verb):
    protein1_data = entities[0]
    verb = str(verb)
    if len(entities) < 2:
        entity_texts = [re.escape(entity['text']) for entity in entities]
        verb_pattern = re.escape(verb)
        one_entity_patterns = [rf"{verb_pattern}\b.*?\b({entity_texts[0]})?",
                               rf"?({entity_texts[0]})?\b.*?\b{verb_pattern}"]
        for pattern in one_entity_patterns:
            if re.search(pattern, sentence):
                return protein1_data['id'], None
    else:
        protein2_data = entities[1]
        patterns = generate_regex_patterns_binding(entities, verb)
        for pattern in patterns:
            if re.search(pattern, sentence):
                return protein1_data['id'], protein2_data['id']
    return None, None


def generate_regex_patterns_binding(entities, verb):
    entity_texts = [re.escape(entity['text']) for entity in entities]
    verb_pattern = re.escape(verb)
    patterns = [
        rf"({entity_texts[0]})\b.*?\b{verb_pattern}\b.*?\b({entity_texts[1]})",
        rf"({entity_texts[1]})\b.*?\b{verb_pattern}\b.*?\b({entity_texts[0]})"
    ]
    return patterns


def get_word_type(word):
    lemma = lemmatizer.stem(word.lower())
    # Überprüfe, ob das Lemma in einer der Kategorien in enum_dict ist
    for category, verbs in enum_dict.items():
        for verb in verbs:
            if lemma == lemmatizer.stem(verb):
                return category  # Gib die Kategorie zurück, falls gefunden
    return None


def extract_regulation_event(trigger_word, sentence, entities, position):
    """
       Extract entities involved in regulation events, along with side mentions and causal influences
       associated with a trigger word in a given sentence.

       Parameters:
       trigger_word (str): The word indicating regulation.
       sentence (str): The sentence in which to search for regulations.
       entities (list): List of entity data with 'id' and 'text'.
       position (int): The position of the sentence in a larger text (if applicable).
       new_events (list): List of events with 'trigger' and 'theme'.

       Returns:
       entity1_id, entity2_id, side_id, side_index if found, otherwise (None, None, None, None).
       """
    entity_texts = [re.escape(entity['text']) for entity in entities]

    if not entity_texts:
        return None, None, None, None, None

    entity_pattern = '|'.join(entity_texts)
    regulation_pattern1 = re.compile(
        rf"({entity_pattern})?.*?\b{re.escape(trigger_word)}\b.*?\b({entity_pattern})",
        re.IGNORECASE)
    regulation_pattern2 = re.compile(
        rf"({entity_pattern})\b.*?\b{re.escape(trigger_word)}\b.*?\b({entity_pattern})?",
        re.IGNORECASE)

    # Search for regulation matches
    regulation_match1 = regulation_pattern1.search(sentence)
    regulation_match2 = regulation_pattern2.search(sentence)

    if regulation_match1 or regulation_match2:
        regulation_match = regulation_match1 if regulation_match1 else regulation_match2

        entity1 = regulation_match.group(1) if regulation_match.group(1) else None
        entity2 = regulation_match.group(2) if regulation_match.group(2) else None
        type_entity2 = None
        # If no entities found in match, return None
        if not entity1 and not entity2:
            return None, None, None, None, None

        # Fetch entity IDs
        entity1_id = next((entity['id'] for entity in entities if entity1 and entity['text'] == entity1), None)
        entity2_id = next((entity['id'] for entity in entities if entity2 and entity['text'] == entity2), None)
        if entity2_id is None:
            type_entity2 = 'entity'
        # Check for side mentions
        side_trigger = trigger_word
        side, side_index = extract_site(sentence, position, side_trigger)
        side_id = next((entity['id'] for entity in entities if side and entity['text'] in side), None) if side else None

        # Cause patterns using prepositions
        cause_prepositions = ['by', 'due to', 'because of', 'from']
        cause_pattern_entity = re.compile(
            rf"{re.escape(trigger_word)}\b.*?\b({'|'.join([re.escape(prep) for prep in cause_prepositions])})?.*?\b({entity_pattern})",
            re.IGNORECASE
        )
        cause_match_entity = cause_pattern_entity.search(sentence)

        # Determine causal entity
        if cause_match_entity:
            cause_entity = cause_match_entity.group(2)
            entity2_id = next((entity['id'] for entity in entities if entity['text'] == cause_entity), None)
            if entity2_id is None:
                type_entity2 = 'cause'

        # Check causal relations with events
        for event in new_events:
            event_trigger, event_theme = get_trigger_word_of_Event(event)
            cause_pattern_event_1 = re.compile(
                rf"{re.escape(trigger_word)}\b.*?\b({'|'.join([re.escape(prep) for prep in cause_prepositions])})\b.*?({re.escape(event_theme)}) .*?\b({re.escape(event_trigger)})",
                re.IGNORECASE
            )
            cause_pattern_event_2 = re.compile(
                rf"{re.escape(trigger_word)}\b.*?\b({'|'.join([re.escape(prep) for prep in cause_prepositions])})\b.*?({re.escape(event_trigger)}).*?\b({re.escape(event_theme)})",
                re.IGNORECASE
            )
            cause_match_event = cause_pattern_event_1.search(sentence) or cause_pattern_event_2.search(sentence)
            if cause_match_event:
                entity2_id = get_event_id(event)
                type_entity2 = 'cause'
                return entity1_id, entity2_id, type_entity2, side_id, side_index

        return entity1_id, entity2_id, type_entity2, side_id, side_index
    # Return None if no matches found
    return None, None, None, None, None



class EventDetection:
    def _event_classification(triggers, last_entity_id, last_event_id):
        current_position = 0
        visited_entities = []
        visited_entities_binding = []
        trigger_id = last_entity_id
        for detail in triggers:
            current_position += len(detail['sentence'])
            last_site_id = 0

            for entity_wrapper in detail['entities']:
                sentence = detail['sentence']
                new_entity = entity_wrapper['entity']
                if new_entity not in visited_entities:
                    visited_entities.append(new_entity)

                    for verb in detail['verbs']:
                        extracted_trigger_type = get_word_type(verb['text'])

                        if extracted_trigger_type is not None:
                            theme_1, theme_2, theme_2_type, site, index_site = extract_regulation_event(
                                verb['text'], sentence, visited_entities, current_position)
                            if theme_1 is not None:
                                if create_new_entity(last_entity_id, extracted_trigger_type, verb['start_char'],
                                                     verb['end_char'], verb['text']):
                                    trigger_id = last_entity_id
                                    last_entity_id += 1
                                new_event_to_add = f"E{last_event_id}\t{extracted_trigger_type}:T{trigger_id} Theme:{theme_1}"
                                if theme_2 is not None:
                                    if theme_2_type == 'entity':
                                        new_event_to_add += f" Theme2:{theme_2}"
                                    if theme_2_type == 'cause':
                                        new_event_to_add += f" Cause:{theme_2}"
                                        if site is not None:
                                            if create_new_entity(last_entity_id, 'Entity',
                                                                 current_position + index_site,
                                                                 current_position + index_site + len(site),
                                                                 site):
                                                last_site_id = last_entity_id
                                                last_entity_id += 1
                                            new_event_to_add += f" CSite:T{last_site_id}"
                                else:
                                    if site is not None:
                                        if create_new_entity(last_entity_id, 'Entity',
                                                             current_position + index_site,
                                                             current_position + index_site + len(site), site):
                                            last_site_id = last_entity_id
                                            last_entity_id += 1
                                        new_event_to_add += f" Site:T{last_site_id}"

                                if check_if_event_unique(f'{extracted_trigger_type}:T{trigger_id}',
                                                         f'Theme:{new_entity["id"]}'):
                                    new_events.append(new_event_to_add)
                                    last_event_id += 1

                        elif extracted_trigger_type == 'Localization':
                            location, start_loc, prop = extract_localization_event(sentence,
                                                                                   current_position,
                                                                                   verb['text'])
                            if location is not None:
                                if create_new_entity(last_entity_id, extracted_trigger_type, verb['start_char'],
                                                     verb['end_char'], verb['text']):
                                    trigger_id = last_entity_id
                                    last_entity_id += 1
                                if create_new_entity(last_entity_id, 'Entity', current_position + start_loc,
                                                     current_position + start_loc + len(location), location):
                                    last_site_id = last_entity_id
                                    last_entity_id += 1
                                if check_if_event_unique(f'{extracted_trigger_type}:T{trigger_id}',
                                                         f'Theme:{new_entity["id"]}'):
                                    new_events.append(
                                        f"E{last_event_id}\t{extracted_trigger_type}:T{trigger_id} Theme:{new_entity['id']} {prop}Loc:T{last_site_id}")
                                    last_event_id += 1
                            else:
                                if check_if_event_unique(f'{extracted_trigger_type}:T{trigger_id}',
                                                         f'Theme:{new_entity["id"]}'):
                                    new_events.append(
                                        f"E{last_event_id}\t{extracted_trigger_type}:T{trigger_id} Theme:{new_entity['id']}")
                                    last_event_id += 1

                        elif extracted_trigger_type == 'Phosphorylation':
                            site, index_site = extract_site(sentence, current_position, verb)

                            if site is not None:
                                if create_new_entity(last_entity_id, extracted_trigger_type, verb['start_char'],
                                                     verb['end_char'], verb['text']):
                                    trigger_id = last_entity_id
                                    last_entity_id += 1
                                if create_new_entity(last_entity_id, 'Entity', current_position + index_site,
                                                     current_position + index_site + len(site), site):
                                    last_site_id = last_entity_id
                                    last_entity_id += 1
                                    if check_if_event_unique(f'{extracted_trigger_type}:T{trigger_id}',
                                                             f'Theme:{new_entity["id"]}'):
                                        new_events.append(
                                            f"E{last_event_id}\t{extracted_trigger_type}:T{trigger_id} Theme:{new_entity['id']} Site:T{last_site_id}")
                                        last_event_id += 1

                            else:
                                if create_new_entity(last_entity_id, extracted_trigger_type, verb['start_char'],
                                                     verb['end_char'], verb['text']):
                                    trigger_id = last_entity_id
                                    last_entity_id += 1
                                if check_if_event_unique(f'{extracted_trigger_type}:T{trigger_id}',
                                                         f'Theme:{new_entity["id"]}'):
                                    new_events.append(
                                        f"E{last_event_id}\t{extracted_trigger_type}:T{trigger_id} Theme:{new_entity['id']}")
                                    last_event_id += 1

                        elif extracted_trigger_type == 'Binding':

                            protein1_data_id, protein2_data_id = extract_binding_event(sentence,
                                                                                       visited_entities, verb)
                            if protein1_data_id or protein2_data_id is not None:
                                if create_new_entity(last_entity_id, extracted_trigger_type, verb['start_char'],
                                                     verb['end_char'], verb['text']):
                                    trigger_id = last_entity_id
                                    last_entity_id += 1
                            if protein1_data_id is not None and protein2_data_id is not None:
                                if check_if_event_unique(f'{extracted_trigger_type}:T{trigger_id}',
                                                         f'Theme:{protein1_data_id}',
                                                         f'Theme2:{protein2_data_id}'):
                                    new_events.append(
                                        f"E{last_event_id}\t{extracted_trigger_type}:T{trigger_id} Theme1:{protein1_data_id} Theme2:{protein2_data_id}")
                                    last_event_id += 1
                            elif protein1_data_id is not None:
                                if check_if_event_unique(f'{extracted_trigger_type}:T{trigger_id}',
                                                         f'Theme:{protein1_data_id}'):
                                    new_events.append(
                                        f"E{last_event_id}\t{extracted_trigger_type}:T{trigger_id} Theme:{protein1_data_id}")
                                    last_event_id += 1
                            elif protein2_data_id is not None:
                                if check_if_event_unique(f'{extracted_trigger_type}:T{trigger_id}',
                                                         f'Theme:{protein2_data_id}'):
                                    new_events.append(
                                        f"E{last_event_id}\t{extracted_trigger_type}:T{trigger_id} Theme:{protein2_data_id}")
                                    last_event_id += 1

                        elif extracted_trigger_type in ['Gene_expression', 'Protein_catabolism',
                                                        'Transcription']:
                            if create_new_entity(last_entity_id, extracted_trigger_type, verb['start_char'],
                                                 verb['end_char'], verb['text']):
                                trigger_id = last_entity_id
                                last_entity_id += 1
                            if check_if_event_unique(f'{extracted_trigger_type}:T{trigger_id}',
                                                     f'Theme:{new_entity["id"]}'):
                                new_events.append(
                                    f"E{last_event_id}\t{extracted_trigger_type}:T{trigger_id} Theme:{new_entity['id']}")
                                last_event_id += 1
                visited_entities.clear()

        return new_entities, new_events
