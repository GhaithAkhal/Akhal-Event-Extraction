import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import pos_tag

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
class TriggerDetection:
    @staticmethod
    def get_trigger_words(text, entities):

        # Initialize result list
        result = []
        sentences = sent_tokenize(text)

        for entity in entities:
            mylen = 0
            for sentence in sentences:
                mylen = mylen + 1 + len(sentence)
                if entity["text"] in sentence and entity["start_char"] < mylen:
                    words = word_tokenize(sentence)
                    pos_tags = pos_tag(words)

                    verbs = []
                    char_offset = text.index(sentence)
                    for word, tag in pos_tags:
                        if tag.startswith('VB'):  # VB* tags are for verbs
                            start_idx = sentence.index(word) + char_offset
                            end_idx = start_idx + len(word)
                            verbs.append({

                                "text": word,
                                "start_char": start_idx,
                                "end_char": end_idx
                            })
                    result.append({
                        "sentence": sentence,
                        "entity": {
                            "text": entity["text"],
                            "start_char": entity["start_char"],
                            "end_char": entity["end_char"]
                        },
                        "verbs": verbs
                    })
        return result