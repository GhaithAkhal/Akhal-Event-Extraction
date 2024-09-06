import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import pos_tag
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger')


def split_compound_words(word):
    # Split the word by hyphen and remove empty strings
    return [w for w in word.split('-') if w]
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
            print(sentence_entity_map[i])
            if sentence_entity_map[i]:  # If sentence has entities
                print(sentence_entity_map[i])
                words = word_tokenize(sentence)
                for word_ in words:
                    if '-' in word_:
                        split_words = split_compound_words(word_)
                        for split in split_words:
                            words.append(split)

                pos_tags = pos_tag(words)
                verbs = []
                char_offset = sentence_starts[i]
                for word, tag in pos_tags:
                    if tag.startswith('VB') or tag.startswith('N') or tag.startswith('RB'):  # VB* tags are for verbs
                        start_idx = sentence.index(word) + char_offset
                        end_idx = start_idx + len(word)
                        verbs.append({
                            "tag": tag,
                            "text": word,
                            "start_char": start_idx,
                            "end_char": end_idx
                        })
                result.append({
                    "sentence": sentence,
                    "entities": sentence_entity_map[i],
                    "verbs": verbs
                })
        return result