from EventExtractor import EventExtractor

from TextFileReader import TextFileReader

from processor.MyDependencyParser import MyDependencyParser
from processor.MyTriggerDetection import MyTriggerDetection
from processor.MyPOSTagger import MyPOSTagger
from processor.MyTokenizer import MyTokenizer


class Main:
    def __init__(self, file_path: str):
        self.file_path = file_path

    if __name__ == "__main__":

        path_of_task = 'dataset/2011/GE'
        data_type = '/BioNLP-ST_2011_genia_devel_data_rev1/'
        current_file = 'PMC-1134658-00-TIAB'
        # Step 1: Read the text from the file and extract the sentences
        file_reader = TextFileReader(path_of_task + data_type + current_file + '.txt')
        tmp_sentences = file_reader.read_text()
        sentences = file_reader.segment(tmp_sentences)
        # Step 2: Read Proteins
        file_reader = TextFileReader(path_of_task + data_type + current_file + '.a1')
        tmp_proteins = file_reader.read_text()
        proteins = file_reader.segment(tmp_proteins)

        # Step 3: Process the text
        tokenizer = MyTokenizer()
        pos_tagger = MyPOSTagger()
        ner = MyTriggerDetection()
        dep_parser = MyDependencyParser()

        # Step 3: Extract events
        event_extractor = EventExtractor(sentences, tokenizer, pos_tagger, ner, dep_parser)
        events = event_extractor.extract_events()

        # Print the extracted events
        for event in events:
            print(event)
