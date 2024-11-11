from collections import deque, defaultdict

class Node:
    def __init__(self, content=''):
        self.content = content
        self.marker = False
        self.children = {}
        self.failure_link = None  # Failure link for Aho-Corasick
        self.output = []  # Stores patterns that end at this node

    def find_child(self, c):
        return self.children.get(c, None)

    def append_child(self, child):
        self.children[child.content] = child

    def remove_child(self, c):
        if c in self.children:
            del self.children[c]


class Trie:
    def __init__(self):
        self.root = Node()

    def add_word(self, word):
        current = self.root
        for i, char in enumerate(word):
            if char not in current.children:
                current.children[char] = Node(char)
            current = current.children[char]
            if i == len(word) - 1:
                current.marker = True
                current.output.append(word)  # Store pattern at this node for matching

    def build_failure_links(self):
        queue = deque()
        for child in self.root.children.values():
            child.failure_link = self.root
            queue.append(child)

        while queue:
            current = queue.popleft()
            for char, child in current.children.items():
                queue.append(child)

                failure = current.failure_link
                while failure is not None and char not in failure.children:
                    failure = failure.failure_link

                child.failure_link = failure.children[char] if failure else self.root
                if child.failure_link:
                    child.output.extend(child.failure_link.output)

    def dna_pattern_match(self, text):
        current = self.root
        matches = defaultdict(list)  # {pattern: [positions]}

        for i, char in enumerate(text):
            while current is not None and char not in current.children:
                current = current.failure_link

            if current is None:
                current = self.root
                continue

            current = current.children[char]

            for pattern in current.output:
                matches[pattern].append(i - len(pattern) + 1)

        return matches

    # Additional methods for autocomplete, add, delete, etc., remain the same

# Example of how to use dna_pattern_match with patterns loaded into Trie
def main():
    trie = Trie()

    # Sample DNA patterns
    dna_patterns = ["AGCT", "CGT", "TTG", "GCTA"]
    for pattern in dna_patterns:
        trie.add_word(pattern)

    # Build failure links for Aho-Corasick
    trie.build_failure_links()

    # DNA sequence to match against
    dna_sequence = "AGCTGCTATCGTAGCTAGTTTGCGT"

    # Find pattern matches
    matches = trie.dna_pattern_match(dna_sequence)
    print("Pattern matches in the DNA sequence:")
    for pattern, positions in matches.items():
        print(f"Pattern '{pattern}' found at positions: {positions}")

if __name__ == "__main__":
    main()
