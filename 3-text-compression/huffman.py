from collections import defaultdict
from treelib import Tree
from heapq import heappush, heappop
from collections import Counter


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


def get_codes(head):
    codes = {}
    head.code = ''

    def walk_tree(node):
        for i, child in enumerate(node.elements):
            child.code = node.code + str(i)

            if len(child.elements) > 1:
                walk_tree(child)
            else:
                codes[child.elements[0]] = child.code

    walk_tree(head)
    return codes


# def adaptive_huffman(text):
#     Node.nodes = []
#     count = defaultdict(int)
#     nodes = {"#": Node("#", weight=0)}
#     root = nodes["#"]

#     for letter in list(text):
#         if letter in nodes:
#             node = nodes[letter]
#             print(node.code() + ' ' + node.letter)
#             node.increment()
#         else:
#             updated_node = nodes["#"]
#             print(updated_node.code() + ' ' + updated_node.letter)
#             print("{0:b}".format(ord(letter)) + ' ' + letter)
#             node = Node(letter, parent=updated_node)
#             nodes[letter] = node
#             del nodes["#"]
#             zero_node = Node("#", parent=updated_node, weight=0)
#             updated_node.add_child(0, zero_node)
#             updated_node.add_child(1, node)
#             nodes["#"] = zero_node
#             updated_node.increment()


if __name__ == '__main__':
    print(get_codes(huffman_heap(Counter('abracadabra'))))
