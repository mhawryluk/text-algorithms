from collections import defaultdict
from treelib import Tree
from heapq import heappush, heappop
from collections import Counter
from bitarray import bitarray, decodetree
from bitarray.util import *
from queue import Queue
import os


class AdaptiveNode:
    def __init__(self, char, weight=0, parent=None):
        self.char = char
        self.weight = weight
        self.parent = parent
        self.children = [None, None]
        self.index = -1

    def __str__(self):
        return self.char

    def __repr__(self):
        return str(self)

    def code(self):
        if self.parent is None:
            return bitarray()
        if self == self.parent.children[0]:
            return self.parent.code() + bitarray('0')
        else:
            return self.parent.code() + bitarray('1')

    def add_child(self, index, child):
        self.children[index] = child
        child.parent = self

    def find_next_at_level(self, level):
        if level == 0:
            return self

        if self.children[0] is not None:
            found = self.children[0].find_next_at_level(level+1)
            if found is not None:
                return found

            found = self.children[1].find_next_at_level(level+1)

            if found is not None:
                return found

        return None

    def right_sibling(self):
        current_node = self
        level = 0

        while current_node.parent is not None:
            if current_node == current_node.parent.children[0]:
                found = current_node.parent.children[1].find_next_at_level(
                    level)
                if found is not None:
                    return found

            current_node = current_node.parent
            level -= 1

        current_node = self
        depth = 0

        while current_node.parent is not None:
            current_node = current_node.parent
            depth += 1

        found = current_node.find_next_at_level(-depth + 1)

        if found is not None:
            return found

        return None

    def increment(self):
        self.weight += 1

        if self.parent:
            right_sib = self.right_sibling()

            if right_sib.weight < self.weight:
                while True:
                    next_sib = right_sib.right_sibling()
                    if next_sib is None or right_sib.weight != next_sib.weight:
                        break
                    else:
                        right_sib = next_sib

                if right_sib != self.parent:
                    swap(self, right_sib)

            self.parent.increment()


def swap(node1, node2):
    node1.parent, node2.parent = node2.parent, node1.parent
    if node1.parent.children[0] == node2:
        node1.parent.children[0] = node1
    else:
        node1.parent.children[1] = node1

    if node2.parent.children[0] == node1:
        node2.parent.children[0] = node2
    else:
        node2.parent.children[1] = node2


def adaptive_huffman(text):
    AdaptiveNode.nodes = []
    nodes = {"#": AdaptiveNode("#", weight=0)}
    head = nodes["#"]

    bits = bitarray()

    for letter in text:
        if letter in nodes:
            node = nodes[letter]
            print(node.code(), end=' <--')
            print(node.char)
            bits += node.code()
            #update_tree(node, head)
            node.increment()
        else:
            updated_node = nodes["#"]
            print("{0:b}".format(ord(letter)) + ' ' + letter)
            print(updated_node.code(), end=' <- ')
            print(updated_node.char)
            bits += updated_node.code()
            node = AdaptiveNode(letter, parent=updated_node)
            nodes[letter] = node
            del nodes["#"]
            zero_node = AdaptiveNode("#", parent=updated_node, weight=0)
            updated_node.add_child(0, zero_node)
            updated_node.add_child(1, node)
            nodes["#"] = zero_node
            #update_tree(updated_node, head)
            updated_node.increment()

    print(bits)
    return head, bits


def decode_adaptive(bits):
    decoded = ""
    nodes = {"#": AdaptiveNode("#")}
    head = nodes["#"]
    current_node = head
    index = 0

    while index <= len(bits):
        if current_node.children[0] is None and current_node.children[1] is None:
            if current_node.char != "#":
                decoded += current_node.char
                print(current_node.char)
                current_node.increment()

            else:
                print(bits[index:index+8], end='letter: ')
                letter = chr(ba2int(bits[index:index+8]))
                print(letter)

                decoded += letter
                index += 8

                node = AdaptiveNode(letter, weight=1)
                nodes[letter] = node

                zero_node = AdaptiveNode("#")
                current_node.add_child(0, zero_node)
                current_node.add_child(1, node)
                nodes["#"] = zero_node
                current_node.increment()

            current_node = head

        if index < len(bits):
            current_node = current_node.children[1] if bits[index] else current_node.children[0]

        index += 1

    return decoded


def show_tree_adaptive(head):
    tree = Tree()
    tree.create_node(str(head) + ' weight: ' +
                     str(head.weight), head, parent=None)
    head.code = ''

    def create_tree(node):
        for i, child in enumerate(node.elements):
            child.code = node.code + str(i)
            tree.create_node(str(child) + ' weight: ' + str(child.weight) + ' code: ' + str(child.code),
                             child, parent=node)
            if len(child.elements) > 1:
                create_tree(child)

    create_tree(head)
    tree.show()


if __name__ == '__main__':
    text = 'abracadabra'
    head, bits = adaptive_huffman(text)
    show_tree_adaptive(head)
    print(decode_adaptive(bits))
