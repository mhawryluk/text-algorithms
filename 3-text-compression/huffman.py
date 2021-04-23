from collections import defaultdict
from treelib import Tree
from heapq import heappush, heappop
from collections import Counter
from bitarray import bitarray, decodetree
from bitarray.util import *
from queue import Queue
import os


class Node:
    def __init__(self, *args, **kwargs):
        self.weight = args[-1]
        self.elements = args[:-1]

    def __str__(self):
        string = ""
        for element in self.elements:
            string += str(element)
        return string

    def __repr__(self):
        return str(self)

    def __lt__(self, other):
        return self.weight < other.weight


class AdaptiveNode:
    def __init__(self, char, weight=0, parent=None):
        self.char = char
        self.weight = weight
        self.parent = parent
        self.children = [None, None]
        self.index = -1

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
    count = defaultdict(int)
    nodes = {"#": AdaptiveNode("#", weight=0)}
    head = nodes["#"]

    bits = bitarray()

    for letter in text:
        if letter in nodes:
            node = nodes[letter]
            #print(node.code() + ' ' + node.letter)
            bits += node.code()
            #update_tree(node, head)
            node.increment()
        else:
            updated_node = nodes["#"]
            #print(updated_node.code() + ' ' + updated_node.letter)
            bits += updated_node.code()
            print("{0:b}".format(ord(letter)) + ' ' + letter)
            node = AdaptiveNode(letter, parent=updated_node)
            nodes[letter] = node
            del nodes["#"]
            zero_node = AdaptiveNode("#", parent=updated_node, weight=0)
            updated_node.add_child(0, zero_node)
            updated_node.add_child(1, node)
            nodes["#"] = zero_node
            #update_tree(updated_node, head)
            updated_node.increment()

    return head, bits


def decode_adaptive(bitarr):
    decoded = ""
    count = defaultdict(int)
    nodes = {"#": AdaptiveNode("#")}
    root = nodes["#"]
    current_node = root
    bits = len(bitarr)
    index = 0
    while index <= bits:
        if current_node.children[0] is None and current_node.children[1] is None:
            if current_node.char != "#":
                decoded += current_node.char
                current_node.increment()
            else:
                try:
                    letter = bitarr[index:index+8].tobytes().decode('utf-8')

                except UnicodeDecodeError:
                    print(bitarr[index:index+8])
                    print(f"Index: {index}, Bits: {bits}")
                    raise ArithmeticError

                decoded += letter
                index += 8
                node = AdaptiveNode(letter, weight=1)
                nodes[letter] = node
                zero_node = AdaptiveNode("#")
                current_node.add_child(0, zero_node)
                current_node.add_child(1, node)
                nodes["#"] = zero_node
                current_node.increment()
            current_node = root

        if index < bits:
            current_node = current_node.children[1] if bitarr[index] else current_node.children[0]
        index += 1

    return decoded


def huffman(letter_counts):
    nodes = []
    for a, weight in letter_counts.items():
        nodes.append(Node(a, weight))

    internal_nodes = []
    leafs = sorted(nodes, key=lambda n: n.weight)

    while(len(leafs) + len(internal_nodes) > 1):
        element_1 = get_lowest_weight_node(leafs, internal_nodes)
        element_2 = get_lowest_weight_node(leafs, internal_nodes)

        internal_nodes.append(
            Node(element_1, element_2, element_1.weight + element_2.weight))

    return internal_nodes[0]


def get_lowest_weight_node(leafs, internal):
    if not internal or (leafs and leafs[0].weight < internal[0].weight):
        return leafs.pop(0)
    return internal.pop(0)


def huffman_heap(letter_counts):
    heap = []
    for a, weight in letter_counts.items():
        heappush(heap, Node(a, weight))

    while(len(heap) > 1):
        element_1 = heappop(heap)
        element_2 = heappop(heap)

        heappush(heap, Node(element_1, element_2,
                 element_1.weight + element_2.weight))

    return heappop(heap)


def get_codes(head):
    codes = {}
    head.code = ''

    def walk_tree(node):
        for i, child in enumerate(node.elements):
            child.code = node.code + str(i)

            if len(child.elements) > 1:
                walk_tree(child)
            else:
                codes[child.elements[0]] = bitarray(child.code)

    walk_tree(head)
    return codes


def encode(text, file):
    node = huffman(Counter(text))
    codes = get_codes(node)
    encoded_text = bitarray()
    encoded_text.encode(codes, text)

    mapping = bitarray()

    for letter, code in codes.items():
        letter_utf = bitarray()
        letter_utf.frombytes(letter.encode('utf-32'))
        # print(letter, letter_utf)

        code_len = bitarray()
        code_len.frombytes(len(code).to_bytes(1, 'big'))
        mapping += letter_utf + code_len + code

    letters_count = bitarray()
    letters_count.frombytes(len(codes).to_bytes(4, 'big'))
    text_bit_size = bitarray()
    text_bit_size.frombytes(len(encoded_text).to_bytes(4, 'big'))

    bit_seq = bitarray()
    bit_seq = letters_count + mapping + text_bit_size + encoded_text

    with open(file, 'wb') as f:
        bit_seq.tofile(f)


def decode(file):
    with open(file, 'rb') as f:
        bit_seq = bitarray()
        bit_seq.fromfile(f)

    letters_count = ba2int(bit_seq[:32])
    decode_dict = {}
    i = 32

    for _ in range(letters_count):
        # print(bit_seq[i:i+64])
        letter = bit_seq[i:i+64].tobytes().decode('utf-32')
        # print(letter)
        i += 64
        code_len = ba2int(bit_seq[i:i+8])
        i += 8
        code = bit_seq[i:i+code_len]
        i += code_len

        decode_dict[letter] = code

    text_len = ba2int(bit_seq[i:i+32])
    i += 32

    decode_tree = decodetree(decode_dict)
    text = ''.join(bit_seq[i:i+text_len].decode(decode_tree))
    return text


def show_tree_adaptive(head):
    pass


def show_tree(head):
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
    print(decode_adaptive(bits))
