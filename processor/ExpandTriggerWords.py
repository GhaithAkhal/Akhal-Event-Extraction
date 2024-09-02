import nltk
from nltk.corpus import verbnet as vn

# Ensure that the required VerbNet data is downloaded
nltk.download('verbnet')

# Print all available VerbNet class IDs
all_vn_classes = vn.classids()
print(all_vn_classes)

class ExpandTriggerWords:

    def add_verbs_from_verbnet(enum_dict, vn_classes, category_name):
        """
        Adds verbs from specified VerbNet classes to a given category in the enum_dict.

        :param enum_dict: Dictionary to update.
        :param vn_classes: List of VerbNet classes to extract verbs from.
        :param category_name: The key in enum_dict to add the verbs under.
        """
        verbs = set()
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
                    verbs.add(member.attrib['name'])
        if category_name in enum_dict:
            enum_dict[category_name].extend(list(verbs))
        else:
            enum_dict[category_name] = list(verbs)