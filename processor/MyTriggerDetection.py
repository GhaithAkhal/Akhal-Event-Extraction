import spacy


class MyTriggerDetection:
    @staticmethod
    def get_trigger_words(text, entities):
        nlp = spacy.load("en_core_web_sm")

        # Process the entire text
        doc = nlp(text)
        # Initialize result list
        result = []
        # Iterate over each sentence in the document
        for entity in entities:
            # Extract the entity text using start and end positions from the text file
            extracted_text = text[entity["start_char"]:entity["end_char"]]

            # Find sentences containing the entity
            for sent in doc.sents:
                if entity["text"] in sent.text:
                    # Find all verbs in the sentence
                    verbs = [(token.text, token.idx, token.idx + len(token.text))
                             for token in sent if token.pos_ == "VERB"]
                    # Add the sentence, entity, and verbs to the list
                    result.append({
                        "sentence": sent.text,
                        "entity": {
                            "text": entity["text"],
                            "start_char": entity["start_char"],
                            "end_char": entity["end_char"]
                        },
                        "verbs": [
                            {
                                "text": verb[0],
                                "start_char": verb[1],
                                "end_char": verb[2]
                            } for verb in verbs
                        ]
                    })
        return result