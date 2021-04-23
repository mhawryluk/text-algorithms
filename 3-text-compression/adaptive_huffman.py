from collections import defaultdict
from treelib import Tree
from heapq import heappush, heappop
from collections import Counter
from bitarray import bitarray, decodetree
from bitarray.util import *
import os


class AdaptiveNode:
    def __init__(self, char, weight=0):
        self.char = char
        self.weight = weight
        self.parent = None
        self.children = [None, None]

    def get_code(self):
        if not self.parent:
            return bitarray()
        if self == self.parent.children[0]:
            return self.parent.get_code() + bitarray('0')
        else:
            return self.parent.get_code() + bitarray('1')

    def add_child(self, index, child):
        self.children[index] = child
        child.parent = self

    def get_char_repr(self):
        if not self.children[0]:
            return self.char

        return self.children[0].get_char_repr() + self.children[1].get_char_repr()

    def get_sibling(self):
        node = self
        levels_change = 0

        while node.parent:
            if node == node.parent.children[0]:
                sibling = node.parent.children[1].next_in_line(
                    0, levels_change)
                if sibling:
                    return sibling

            node = node.parent
            levels_change += 1

        return node.next_in_line(0, levels_change - 1)

    def next_in_line(self, current_level, end_level):
        if current_level == end_level:
            return self
        if not self.children[0]:
            return None
        return self.children[0].next_in_line(current_level + 1, end_level) or \
            self.children[1].next_in_line(current_level + 1, end_level)

    def increment(self):
        self.weight += 1

        if self.parent:
            sibling = self.get_sibling()
            if sibling:
                if self.weight > sibling.weight:
                    next_sibling = sibling.get_sibling()

                    while next_sibling and sibling.weight == next_sibling.weight:
                        sibling = next_sibling
                        next_sibling = sibling.get_sibling()

                    if sibling != self.parent:
                        swap_nodes(self, sibling)

            self.parent.increment()

    def __str__(self):
        return f'char(s): {"".join(sorted(self.get_char_repr()))}, weight: {self.weight}, code:{"".join(list(map(str, self.get_code())))}'

    def __repr__(self):
        return str(self)

    def __lt__(self, other):
        return self.weight < other.weight


def swap_nodes(node_1, node_2):
    node_1.parent, node_2.parent = node_2.parent, node_1.parent

    if node_2 == node_1.parent.children[0]:
        node_1.parent.children[0] = node_1
    else:
        node_1.parent.children[1] = node_1

    if node_1 == node_2.parent.children[0]:
        node_2.parent.children[0] = node_2
    else:
        node_2.parent.children[1] = node_2


def adaptive_huffman(text):
    nodes = {"#": AdaptiveNode("#", weight=0)}
    head = nodes["#"]
    bit_seq = bitarray()

    for letter in text:
        show_tree_adaptive(head)

        if letter in nodes:
            node = nodes[letter]
            bit_seq += node.get_code()
            node.increment()
        else:
            updated_node = nodes["#"]
            bit_seq += updated_node.get_code()

            letter_bits = bitarray()
            letter_bits.frombytes(letter.encode('utf-32'))
            bit_seq += letter_bits

            node = AdaptiveNode(letter, weight=1)
            nodes[letter] = node
            del nodes["#"]
            zero_node = AdaptiveNode("#", weight=0)
            updated_node.add_child(0, zero_node)
            updated_node.add_child(1, node)
            nodes["#"] = zero_node

            updated_node.increment()

    return head, bit_seq


def decode_adaptive(bit_seq):
    text = ""
    nodes = {"#": AdaptiveNode("#", weight=0)}
    head = nodes["#"]
    current_node = head
    i = 0

    while i <= len(bit_seq):
        if not current_node.children[0]:
            if current_node.char != "#":
                text += current_node.char
                current_node.increment()

            else:
                letter = bit_seq[i:i+64].tobytes().decode('utf-32')
                i += 64
                text += letter
                
                node = AdaptiveNode(letter, weight=1)
                nodes[letter] = node
                del nodes["#"]
                zero_node = AdaptiveNode("#")
                current_node.add_child(0, zero_node)
                current_node.add_child(1, node)
                nodes["#"] = zero_node
                current_node.increment()

            current_node = head

        if i < len(bit_seq):
            current_node = current_node.children[1] if bit_seq[i] == 1 else current_node.children[0]

        i += 1

    return text


def show_tree_adaptive(head):
    tree = Tree()
    tree.create_node(str(head), head, parent=None)

    def create_tree(node):
        for i, child in enumerate(node.children):
            tree.create_node(str(child),
                             child, parent=node)

            if child and child.children[0] and child.children[1]:
                create_tree(child)

    create_tree(head)
    tree.show()


if __name__ == '__main__':
    text = 'abracadabra'
    head, bits = adaptive_huffman(text)
    show_tree_adaptive(head)
    print(decode_adaptive(bits))
