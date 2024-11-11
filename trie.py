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


# Helper functions
def load_dictionary(trie, filename):
    try:
        with open(filename, 'r') as file:
            for word in file:
                word = word.strip()  # Remove newlines or extra spaces
                trie.add_word(word)
        return True
    except FileNotFoundError:
        print("Dictionary file not found.")
        return False


def main():
    trie = Trie()
    print("Loading dictionary...")
    load_dictionary(trie, 'words.txt')

    while True:
        print("\nInteractive mode:")
        print("1: Auto Complete Feature")
        print("2: Delete Word")
        print("3: Print all words in Trie")
        print("4: Quit")
        mode = int(input("Choose an option: "))

        if mode == 1:
            # Auto-complete functionality
            prefix = input("Enter prefix: ").lower()
            auto_complete_list = []
            if trie.auto_complete(prefix, auto_complete_list):
                
                    print("Autocomplete suggestions:")
                    for word in auto_complete_list:
                        print(f"\t{word}")
            else:
                print("Prefix not found in dictionary.")

        elif mode == 2:
            # Delete word functionality
            word_to_delete = input("Enter word to delete: ").lower()
            if trie.search_word(word_to_delete):
                trie.delete_word(word_to_delete)
                print(f"Word '{word_to_delete}' deleted.")
            else:
                print(f"Word '{word_to_delete}' not found in the dictionary.")

        elif mode == 3:
            # Print all words in Trie
            print("Words in Trie:")
            trie.print_trie()

        elif mode == 4:
            # Exit the program
            print("Exiting...")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
