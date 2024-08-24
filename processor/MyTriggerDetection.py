from nltk.corpus import verbnet as vn
import re
from collections import defaultdict
import nltk

def MyTriggerDetection():
    categories = {
        "Gene expression": ["express", "transcribe", "translate", "synthesize", "produce", "encode"],
        "Transcription": ["transcribe", "copy", "replicate", "translate", "reverse", "read", "synthesize"],
        "Protein catabolism": ["catabolize", "degrade", "breakdown", "digest", "hydrolyze", "cleave"],
        "Phosphorylation": ["phosphorylate", "activate", "catalyze", "modify", "transfer"],
        "Localization": ["localize", "transport", "relocate", "target", "direct", "position", "move"],
        "Binding": ["bind", "attach", "interact", "associate", "complex", "adhere"],
        "Regulation": ["regulate", "control", "modulate", "adjust", "maintain", "balance"],
        "Positive regulation": ["activate", "enhance", "increase", "upregulate", "stimulate"],
        "Negative regulation": ["inhibit", "suppress", "decrease", "downregulate", "block", "repress"]
    }

    # Map categories to VerbNet classes
    category_to_verbnet_classes = {
        "Gene expression": ["create-26.4", "build-26.1"],
        "Transcription": ["copy-25.1", "write-25.2"],
        "Protein catabolism": ["destroy-44", "break-45.1"],
        "Phosphorylation": ["calibratable_cos-45.6", "prepare-26.3"],
        "Localization": ["carry-11.4", "send-11.1"],
        "Binding": ["attach-22.6", "amalgamate-22.1"],
        "Regulation": ["control-30.3", "manage-95"],
        "Positive regulation": ["help-72", "improve-45.4"],
        "Negative regulation": ["stop-55.4", "forbid-67.1"]
    }

    for category, vn_classes in category_to_verbnet_classes.items():
        for vn_class in vn_classes:
            verbs = vn.classids(vn_class)
            for verb in verbs:
                verb_list = vn.lemmas(verb)
                categories[category].extend(verb_list)

    # Ensure uniqueness
    for category in categories:
        categories[category] = list(set(categories[category]))

    return categories


expanded_keywords = MyTriggerDetection()
for category, verbs in expanded_keywords.items():
    print(f"{category}: {verbs}")