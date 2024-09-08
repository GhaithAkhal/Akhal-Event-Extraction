import nltk
from nltk.corpus import verbnet as vn
from nltk.corpus import wordnet as wn
# Ensure that the required VerbNet data is downloaded
nltk.download('verbnet')
nltk.download('wordnet')

# Print all available VerbNet class IDs
all_vn_classes = vn.classids()

class ExpandTriggerWords:

    def add_verbs_from_verbnet(enum_dict, vn_classes, category_name):
        """
        Adds verbs from specified VerbNet classes to a given category in the enum_dict.

        :param enum_dict: Dictionary to update.
        :param vn_classes: List of VerbNet classes to extract verbs from.
        :param category_name: The key in enum_dict to add the verbs under.
        """
        verbs = set(enum_dict[category_name])
        for vn_class in vn_classes:
            # Get the VerbNet class
            try:
                class_obj = vn.vnclass(vn_class)
            except ValueError:
                print(f"VerbNet class {vn_class} not found.")
                continue

            # Get the verbs associated with the VerbNet class
            if class_obj:
                members = class_obj.findall('MEMBERS/MEMBER')
                for member in members:
                    verb = member.attrib['name']
                    if ExpandTriggerWords.is_valid_for_category(verb, category_name):
                        verbs.add(verb)
        if category_name in enum_dict:
            enum_dict[category_name].extend(list(verbs))
        else:
            enum_dict[category_name] = list(verbs)

    def add_words_from_wordnet(enum_dict, category_name):
        """
        Adds related words from WordNet to a given category in the enum_dict.

        :param enum_dict: Dictionary to update.
        :param word: The word to find synonyms for.
        :param category_name: The key in enum_dict to add the words under.
        :param pos: Part of Speech (default is verb for WordNet)
        """

        words = enum_dict[category_name]
        related_words = set(words)
        for word in words:
            for synset in wn.synsets(word, wn.VERB):
                for lemma in synset.lemmas():
                    related_word = lemma.name()
                    if isinstance(related_word, str) and ExpandTriggerWords.is_valid_for_category(related_word, category_name):
                        related_words.add(related_word)
        enum_dict[category_name] = list(related_words)

    @staticmethod
    def is_valid_for_category(verb, category_name):
        """
        Manually filters the verbs to ensure they belong to the appropriate category.
        :param verb: The verb to check.
        :param category_name: The category name to match against.
        :return: Boolean indicating whether the verb fits the category.
        """
        # Normalize the verb to lowercase for consistent comparison
        verb = verb.lower()
        if category_name == "Localization":
            if verb == "return" :
                return False  # Explicitly exclude "return" from Localization
        if category_name == "Protein_catabolism":
            if verb == "use":
                return False

        if category_name == "Transcription":
            if verb == "type":
                return False
        if verb == "have":
            return False

        # Default case: return True if no specific filter exists for the category
        return True