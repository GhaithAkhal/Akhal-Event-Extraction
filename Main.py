from EventExtractor import EventExtractor

from TextFileReader import TextFileReader
from processor.ExpandTriggerWords import ExpandTriggerWords
from processor.MyDependencyParser import MyDependencyParser
from processor.MyTriggerDetection import MyTriggerDetection
from processor.MyPOSTagger import MyPOSTagger
from processor.Pattern import Pattern
import re
from dic.Binding import Binding


from nltk.corpus import wordnet as wn


from nltk.corpus import wordnet as wn


class Main:
    def __init__(self, file_path: str):
        self.file_path = file_path

    if __name__ == "__main__":

        path_of_task = 'dataset/2011/GE'
        data_type = '/BioNLP-ST_2011_genia_devel_data_rev1/'
        current_file = 'PMC-1134658-00-TIAB'

        entities = Pattern.extract_entities("dataset/2011/GE/BioNLP-ST_2011_genia_devel_data_rev1/PMC-1134658-00-TIAB.a1")
        print(entities)
        verb_preposition_pairs = Pattern.extract_verbs_and_prepositions(Binding)
        print(verb_preposition_pairs)
        pattern = Pattern.generate_regex_patterns(entities, verb_preposition_pairs)
        print(pattern)
        # # Step 1: Read the text from the file and extract the sentences
        # file_reader = TextFileReader(path_of_task + data_type + current_file + '.txt')
        # tmp_sentences = file_reader.read_text()
        # sentences = file_reader.segment(tmp_sentences)
        #
        # # Step 2: Read Proteins
        # file_reader = TextFileReader(path_of_task + data_type + current_file + '.a1')
        # tmp_entities = file_reader.read_text()
        # entities = file_reader.segment(tmp_entities)
        #
        # # maximum the pattern with all synonyms
        # synonyms = set()
        # # using Set() to have unique pattern
        # myPattern = []
        #
        # for it in Binding:
        #     synonyms += get_synonyms(it.name)
        #
        # for sen in synonyms:
        #     myPattern += r"%s\s\w+\s %s\s %s\s\w+\n", entities, synonyms, entities
        #
        # for pattern in myPattern:
        #     matches = re.findall(pattern, tmp_sentences)
        #     if matches:
        #         print(f"Matches for {pattern}: {matches}")

        # Step 3: Process the text
        #tokenizer = MyTokenizer()
        #pos_tagger = MyPOSTagger()
        #ner = MyTriggerDetection()
        #dep_parser = MyDependencyParser()

        # Step 3: Extract events
        #event_extractor = EventExtractor(sentences, tokenizer, pos_tagger, ner, dep_parser)
       # events = event_extractor.extract_events()

        # Print the extracted events
        #for event in events:
        #    print(event)
