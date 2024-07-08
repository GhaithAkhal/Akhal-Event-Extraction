from EventExtractor import EventExtractor

from TextFileReader import TextFileReader

from processor.MyDependencyParser import MyDependencyParser
from processor.MyNER import MyNER
from processor.MyPOSTagger import MyPOSTagger
from processor.MyTokenizer import MyTokenizer


class Main:
    def __init__(self, file_path: str):
        self.file_path = file_path


if __name__ == "__main__":
    # Step 1: Read the text from the file and extract the sentences

    file_reader = TextFileReader('input.txt')
    text = file_reader.read_text()
    sentences = file_reader.segment(text)

    # Step 2: Process the text
    tokenizer = MyTokenizer()
    pos_tagger = MyPOSTagger()
    ner = MyNER()
    dep_parser = MyDependencyParser()

    # Step 3: Extract events
    event_extractor = EventExtractor(sentences, tokenizer, pos_tagger, ner, dep_parser)
    events = event_extractor.extract_events()

    # Print the extracted events
    for event in events:
        print(event)