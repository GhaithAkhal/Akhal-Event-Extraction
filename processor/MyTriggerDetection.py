import spacy
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import pos_tag
from typing import List, Dict



class MyTriggerDetection:

    def update_list(lst, new_string, new_int1, new_int2):
        # Iterate through the list
        for item in lst:
            # Check if the string and both integers match
            if item[0] == new_string and item[1] == new_int1 and item[2] == new_int2:
                # If match found, break the loop and return
                return

        # If no match is found, append the new tuple to the list
        lst.append((new_string, new_int1, new_int2))
    @staticmethod
    def get_trigger_words(text, entities, context_window=5) -> Dict[str, Dict[str, List[str]]]:
        nlp = spacy.load("en_core_web_sm")

        # Process the entire text
        doc = nlp(text)
        # Initialize result list
        result = []
        # Iterate over each sentence in the document
        for sent in doc.sents:
            sentence_tokens = [token.text for token in sent]

            # Iterate over each entity
            for entity in entities:
                # Check if the entity is present in the sentence
                if entity in sentence_tokens:
                    entity_indices = [i for i, token in enumerate(sentence_tokens) if token == entity]

                    for index in entity_indices:
                        entity_start_char = sent[index].idx
                        entity_end_char = entity_start_char + len(entity)

                        # Initialize trigger lists
                        contextual_triggers = []
                        syntactic_triggers = []
                        # Contextual Trigger Extraction
                        start = max(0, index - context_window)
                        end = min(len(sentence_tokens), index + context_window + 1)
                        context = sent[start:end]

                        # Extract verbs from context
                        for token in context:
                            if token.pos_ == 'VERB':
                                verb_start_char = token.idx
                                verb_end_char = verb_start_char + len(token.text)

                                MyTriggerDetection.update_list(contextual_triggers,token.lemma_, verb_start_char, verb_end_char)

                        # Syntactic Trigger Extraction
                        token = sent[index]
                        # Check if the head is a verb and not the token itself
                        if token.head != token and token.head.pos_ == 'VERB':
                            MyTriggerDetection.update_list(syntactic_triggers,token.head.lemma_, token.head.idx, token.head.idx + len(token.head.text))

                        # Check for verb children related to the entity
                        for child in token.children:
                            if child.pos_ == 'VERB':
                                MyTriggerDetection.update_list(syntactic_triggers, child.lemma_, child.idx, child.idx + len(child.text))

                        # Add entity and its triggers to result
                        entity_exists = False
                        for entry in result:
                            if entry['entity'] == entity and entry['start_char'] == entity_start_char and entry[
                                'end_char'] == entity_end_char:
                                # Append triggers to the existing entity entry
                                entry['contextual_triggers'].extend(contextual_triggers)
                                entry['syntactic_triggers'].extend(syntactic_triggers)
                                entity_exists = True
                                break

                        if not entity_exists:
                            # Add new entity and its triggers to result
                            result.append({
                                "entity": entity,
                                "start_char": entity_start_char,
                                "end_char": entity_end_char,
                                "contextual_triggers": contextual_triggers,
                                "syntactic_triggers": syntactic_triggers
                            })

        return result
