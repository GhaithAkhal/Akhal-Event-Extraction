import spacy
from typing import List

# Load the spaCy model
# This object provides various functionalities, including:
#
#     Tokenization:
#         Splitting the text into individual tokens (words, punctuation, etc.).
#
#     Part-of-Speech Tagging:
#         Assigning part-of-speech tags (such as nouns, verbs, adjectives, etc.) to each token.
#
#     Named Entity Recognition (NER):
#         Identifying named entities (such as people, organizations, locations, dates, etc.) in the text.
#
#     Dependency Parsing:
#         Analyzing the syntactic structure of the text to understand the relationship between tokens.
#
#     Sentence Segmentation:
#         Dividing the text into sentences.


class TextProcessor:
    def __init__(self, text: str):
        self.text = text

    def get_sentences(self) -> (List)[spacy.tokens.Span]:
        return list(self.doc.sents)
