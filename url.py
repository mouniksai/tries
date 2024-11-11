class Node:
    def __init__(self, content=''):
        self.content = content  # Character at this node
        self.marker = False      # Marker to check if this is the end of a word
        self.children = {}       # Dictionary to store children nodes by character

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
                current.marker = True  # Mark end of the word

    def search_word(self, word):
        current = self.root
        for char in word:
            current = current.find_child(char)
            if current is None:
                return False
        return current.marker

    def auto_complete(self, prefix, res):
        current = self.root
        for char in prefix:
            current = current.find_child(char)
            if current is None:
                return False  # Prefix not found in Trie

        self.parse_tree(current, prefix, res)
        return True

    def print_trie(self):
        # Helper method to initiate recursive DFS from the root
        self._dfs_print(self.root, "")

    def _dfs_print(self, node, word):
        if node.marker:
            print(word)  # Print the word when we reach the end of a valid word

        for char, child in sorted(node.children.items()):
            self._dfs_print(child, word + char)

    def parse_tree(self, current, s, res, limit=15):
        if current:
            if current.marker:
                res.append(s)
                if len(res) >= limit:
                    return  # Stop when reaching the limit

            for char, child in current.children.items():
                self.parse_tree(child, s + char, res, limit)

    def delete_word(self, word):
        def _delete(current, word, index):
            if index == len(word):
                if not current.marker:
                    return False  # Word not found
                current.marker = False
                return len(current.children) == 0  # Check if node has no children

            char = word[index]
            child = current.find_child(char)
            if child is None:
                return False  # Word not found

            should_delete_child = _delete(child, word, index + 1)

            if should_delete_child:
                current.remove_child(char)  # Remove the child node
                return len(current.children) == 0 and not current.marker

            return False

        _delete(self.root, word, 0)

    # Pre-order DFS Traversal
    def dfs_traversal(self):
        words = []
        self._dfs(self.root, "", words)
        return words

    def _dfs(self, node, path, words):
        if node.marker:
            words.append(path)
        
        for char, child in sorted(node.children.items()):
            self._dfs(child, path + char, words)

    # BFS Traversal
    def bfs_traversal(self):
        from collections import deque
        queue = deque([(self.root, "")])
        words = []

        while queue:
            node, path = queue.popleft()
            if node.marker:
                words.append(path)
            
            for char, child in sorted(node.children.items()):
                queue.append((child, path + char))

        return words

    def add_url(self, url):
        parts = url.split('/')  # Split URL by slashes to handle segments
        current = self.root
        for part in parts:
            if part not in current.children:
                current.children[part] = Node(part)
            current = current.children[part]
        current.marker = True  # Mark end of a URL path

    def search_url(self, url):
        parts = url.split('/')
        current = self.root
        for part in parts:
            current = current.find_child(part)
            if current is None:
                return False
        return current.marker

    def match_urls(self, prefix):
        # Auto-complete URLs based on prefix
        parts = prefix.split('/')
        current = self.root
        for part in parts:
            current = current.find_child(part)
            if current is None:
                return []  # Prefix not found
        
        matched_urls = []
        self.parse_tree(current, '/'.join(parts), matched_urls)
        return matched_urls

 


def main():
    trie = Trie()
    print("Starting predefined tests for URL and IP management.\n")

    # URL Management Test Cases
    print("--- URL Management Tests ---")
    urls_to_add = [
        "https://example.com/home",
        "https://example.com/about",
        "https://example.com/contact",
        "https://sample.com/shop",
        "https://sample.com/blog"
    ]
    for url in urls_to_add:
        trie.add_url(url)
        print(f"Added URL: {url}")

    # Test URL search
    test_url = "https://example.com/about"
    print(f"\nSearching for URL '{test_url}'...")
    if trie.search_url(test_url):
        print(f"URL '{test_url}' found in Trie.")
    else:
        print(f"URL '{test_url}' not found in Trie.")

    # Test URL auto-complete
    prefix = "https://example.com"
    print(f"\nFinding URL matches for prefix '{prefix}'...")
    url_matches = trie.match_urls(prefix)
    print("URL matches for prefix:")
    for match in url_matches:
        print(f"\t{match}")


if __name__ == "__main__":
    main()
