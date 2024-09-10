import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import pos_tag
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger')


class TriggerDetection:
    @staticmethod
    def get_trigger_words(text, entities):

        # Initialize result list
        result = []
        sentences = sent_tokenize(text)
        current_position = 0
        sentence_starts = []
        for sentence in sentences:
            start_pos = text.index(sentence, current_position)
            sentence_starts.append(start_pos)
            current_position = start_pos + len(sentence)

        # Create a dictionary to store sentence -> associated entities
        sentence_entity_map = {i: [] for i in range(len(sentences))}

        # Map entities to the corresponding sentences by checking their positions
        for entity in entities:
            for i, sentence in enumerate(sentences):
                start_actual_sentence = sentence_starts[i]
                end_actual_sentence = start_actual_sentence + len(sentence)

                # If the entity lies within the sentence, add it to the map
                if (entity["start_char"] >= start_actual_sentence
                        and entity["end_char"] <= end_actual_sentence):
                    sentence_entity_map[i].append({"entity": entity})
                    break  # Move to the next entity once a match is found

        for i, sentence in enumerate(sentences):
            if sentence_entity_map[i]:  # If sentence has entities
                words = word_tokenize(sentence)
                pos_tags = pos_tag(words)
                triggers = []
                char_offset = sentence_starts[i]

                entity_positions = []
                for entity_wrapper in sentence_entity_map[i]:
                    entity = entity_wrapper['entity']
                    start_idx = entity["start_char"] - char_offset
                    end_idx = entity["end_char"] - char_offset
                    entity_positions.append((start_idx, end_idx))

                for pos in range(len(pos_tags)):
                    word, tag = pos_tags[pos]
                    if tag.startswith('VB') or tag.startswith('NN'):  # VB* tags are for verbs, NN* for nouns
                         #Check if the word is next to or within 2 words from an entity
                        #for (start_idx, end_idx) in entity_positions:
                            #f abs(pos - start_idx) <= 7 or abs(pos - end_idx) <= 7:
                        start_char = text.index(word, char_offset)
                        end_char = start_char + len(word)
                        triggers.append({
                            "tag": tag,
                            "text": word,
                            "start_char": start_char,
                            "end_char": end_char
                        })
                             #   break
                result.append({
                    "sentence": sentence,
                    "entities": sentence_entity_map[i],
                    "verbs": triggers
                })
        return result