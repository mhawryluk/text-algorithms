from treelib import Tree
from random import shuffle


def unique_last_character(text):
    is_unique = text[-1] not in text[:-1]

    if is_unique:
        return text

    for i in range(36, 1000):
        if chr(i) not in text:
            return text + chr(i)


class TrieNode:
    def __init__(self, char):
        self.char = char
        self.children = {}

    def __str__(self):
        return self.char

    def __lt__(self, other):
        return self.char < other.char


class TreeNode:
    def __init__(self, range):
        self.range = range
        self.children = []

    def __str__(self):
        str = ""
        for i in range(self.range[0], self.range[1]+1):
            str += TreeNode.text[i]
        return str

    def __repr__(self):
        str = ""
        for i in range(self.range[0], self.range[1]+1):
            str += TreeNode.text[i]
        return str

    def __lt__(self, other):
        return str(self) < str(other)


def build_trie(text):
    text = unique_last_character(text)
    head = TrieNode("")

    for i in range(len(text)):
        current_node = head
        for j, char in enumerate(text[i:]):
            if char in current_node.children:
                current_node = current_node.children[char]
            else:
                for k, char in enumerate(text[i+j:]):
                    new_node = TrieNode(char)
                    current_node.children[char] = new_node
                    current_node = new_node
                break

    return head


def build_tree(text):
    text = unique_last_character(text)
    head = TreeNode(range=(0, -1))

    for suffix_index in range(len(text)):
        show_tree(text, head)
        current_node = head
        current_index = suffix_index
        found = 0
        while current_index < len(text) and not found:
            skip = 0
            shuffle(current_node.children)
            print(current_node.children)
            for child in current_node.children:
                common = 0

                for k in range(child.range[0], child.range[1]+1):
                    if text[current_index+common] == text[k]:
                        common += 1
                    else:
                        break

                if common == child.range[1] - child.range[0] + 1:
                    current_node = child
                    current_index += common
                    skip = 1
                    break

                elif common > 0:
                    new_child_1 = TreeNode(
                        range=(child.range[0]+common, child.range[1]))
                    new_child_2 = TreeNode(
                        range=(current_index+common, len(text)-1))

                    new_child_1.children = child.children

                    child.range = (
                        child.range[0], child.range[0]+common-1)
                    child.children = [new_child_1, new_child_2]
                    found = 1
                    break

            if not found and not skip:
                new_child = TreeNode(range=(current_index, len(text)-1))
                current_node.children.append(new_child)
                break

    return head


def show_trie(text):
    tree = Tree()
    head = build_trie(text)
    tree.create_node(head, head, parent=None)

    def create_tree(node):
        for child in node.children.values():
            tree.create_node(child, child, parent=node)
            create_tree(child)

    create_tree(head)
    tree.show()


def show_tree(text, head):
    TreeNode.text = unique_last_character(text)
    tree = Tree()
    tree.create_node(head, head, parent=None)

    def create_tree(node):
        for child in node.children:
            tree.create_node(child, child, parent=node)
            create_tree(child)

    create_tree(head)
    tree.show()


if __name__ == "__main__":
    text = "aabbabd"
    head = build_tree(text)
    show_tree(text, head)
