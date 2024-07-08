import re
from typing import List

class MyTokenizer:
    def tokenize(self, text: str) -> List[str]:
        # Split text into tokens based on whitespace and punctuation
        return re.findall(r'\w+|\S', text)
