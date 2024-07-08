from typing import List, Tuple
class MyDependencyParser:
    def parse(self, tokens: List[str]) -> List[Tuple[str, str, str]]:
        # Simple rule-based dependency parsing
        dependencies = []
        for i, token in enumerate(tokens):
            if token.endswith('ing'):
                dependencies.append((token, 'ROOT', 'ROOT'))
            elif i > 0:
                dependencies.append((token, 'dep', tokens[i-1]))
            else:
                dependencies.append((token, 'ROOT', 'ROOT'))
        return dependencies