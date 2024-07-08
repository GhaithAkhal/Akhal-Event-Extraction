
from typing import List
import processor
class EventExtractor:
    def __init__(self, sentences: List[str], tokenizer, pos_tagger, ner, dep_parser):
        self.sentences = sentences
        self.tokenizer = tokenizer
        self.pos_tagger = pos_tagger
        self.ner = ner
        self.dep_parser = dep_parser

    def extract_events(self) -> List[str]:
        events = []
        for sentence in self.sentences:
            tokens = self.tokenizer.tokenize(sentence)
            pos_tags = self.pos_tagger.pos_tag(tokens)
            entities = self.ner.recognize_entities(tokens)
            dependencies = self.dep_parser.parse(tokens)
            event = self._extract_event_from_tokens(tokens, pos_tags, entities, dependencies)
            if event:
                events.append(event)
        return events

    def _extract_event_from_tokens(self, tokens, pos_tags, entities, dependencies) -> str:
        # Simplified event extraction logic
        for token, pos in pos_tags:
            if pos == 'VERB':  # Check if the token is a verb
                return ' '.join(tokens)  # Return the sentence if it contains a verb
        return None


    @staticmethod
    def from_file(file_path: str) -> 'EventExtractor':
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return EventExtractor(text)
