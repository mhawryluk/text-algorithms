from treelib import Tree


class Node:
    def __init__(self, char):
        self.char = char
        self.children = {}

    def __str__(self):
        return self.char

    def __lt__(self, other):
        return self.char < other.char


def build_trie(text):
    text += '\0'
    head = Node("")

    for i in range(len(text)):
        current_node = head
        for j, char in enumerate(text[i:]):
            if char in current_node.children:
                current_node = current_node.children[char]
            else:
                for k, char in enumerate(text[i+j:]):
                    new_node = Node(char)
                    current_node.children[char] = new_node
                    current_node = new_node
                break

    return head


def show_trie(text):
    tree = Tree()
    head = build_trie(text)
    tree.create_node(head, head, parent=None)
    tree.show()

    def create_tree(node):
        for child in node.children.values():
            tree.create_node(child, child, parent=node)
            create_tree(child)

    create_tree(head)
    tree.show()


def build_suffix_tree(text):
    pass


if __name__ == "__main__":
    show_trie("aabbabbc")
