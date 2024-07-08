import re
from typing import List


class TextFileReader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read_text(self) -> str:
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def segment(self, text: str) -> List[str]:
        # Segment text into sentences based on punctuation
        return re.split(r'(?<=[.!?]) +', text)