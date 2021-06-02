from treelib import Tree
import networkx as nx
import matplotlib.pyplot as plt


class Node:
    index = 0

    def __init__(self, parent=None, char=None):
        self.edges = {}
        self.fail_link = None
        self.parent = parent
        self.char = char
        self.visited = False
        self.id = Node.index
        Node.index += 1
        self.pattern_end = None

    def __lt__(self, other):
        return self.char < other.char

    def __str__(self):
        return str(self.id)


def build_trie(patterns):
    head = Node()

    for i, pattern in enumerate(patterns):
        current_node = head
        for char in pattern:
            if char in current_node.edges:
                current_node = current_node.edges[char]
            else:
                current_node.edges[char] = Node(char=char, parent=current_node)
                current_node = current_node.edges[char]

        current_node.pattern_end = i+1

    return head


def build_automaton(patterns):
    head = build_trie(patterns)
    # show_graph(head)

    queue = [head]
    visited = []

    def assign_fail_links(node):
        if node is not head:
            current_node = node.parent.fail_link
            while current_node:
                if node.char in current_node.edges:
                    node.fail_link = current_node.edges[node.char]
                    break
                current_node = current_node.fail_link
            else:
                node.fail_link = head

        for edge in node.edges.values():
            if edge not in visited:
                queue.append(edge)

        visited.append(node)

    while queue:
        node = queue.pop(0)
        assign_fail_links(node)

    return head


def modify_automaton(head):

    queue = [head]
    visited = []

    def copy_edges(node):
        if node is not head:
            for key, node_edge in node.fail_link.edges.items():
                if key not in node.edges:
                    node.edges[key] = node_edge

        for edge in node.edges.values():
            if edge not in visited and edge not in queue:
                queue.append(edge)
                visited.append(edge)

        visited.append(node)
        node.fail_link = None

    while queue:
        node = queue.pop(0)
        copy_edges(node)

    return head


def pattern_match_2d(text, pattern):
    head = build_automaton(pattern)
    # show_graph(head)
    head = modify_automaton(head)
    # show_graph(head)

    patterns_matrix = [[0 for _ in range(len(text[0]))]
                       for _ in range(len(text))]

    for i, line in enumerate(text):
        current_node = head
        for j, char in enumerate(line):
            if char in current_node.edges:
                current_node = current_node.edges[char]
            else:
                current_node = head

            if current_node.pattern_end:
                patterns_matrix[i][j] = current_node.pattern_end

    print(patterns_matrix)

    col_pattern = [i+1 for i in range(len(pattern[0]))]

    result = []

    for i in range(len(text[0])):
        line = [patterns_matrix[j][i] for j in range(len(text))]
        print(line, col_pattern)
        for j in kmp(line, col_pattern):
            result.append((j, i-len(pattern[0])+1))

    print(result)
    return result


def show_trie(patterns=None, head=None):
    tree = Tree()
    if head is None:
        head = build_trie(patterns)
    tree.create_node(head, head, parent=None)

    def create_tree(node):
        for child in node.edges.values():
            tree.create_node(child, child, parent=node)
            create_tree(child)

    create_tree(head)
    tree.show()


def show_graph(head):
    graph = nx.DiGraph()
    stack = [head]

    while stack:
        node = stack.pop()
        for key, edge_node in node.edges.items():
            graph.add_edge(node, edge_node, label=key)

            if not edge_node.visited:
                stack.append(edge_node)

        if node.fail_link:
            graph.add_edge(node, node.fail_link)

        node.visited = True

    pos = nx.spectral_layout(graph)
    nx.draw_networkx(
        graph, pos, connectionstyle='arc3, rad = 0.2', node_color='turquoise')
    labels = nx.get_edge_attributes(graph, 'label')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    plt.show()


def kmp(text, pattern):
    result = []

    pi = prefix_function(pattern)
    q = 0

    for i in range(0, len(text)):
        while q > 0 and pattern[q] != text[i]:
            q = pi[q-1]

        if pattern[q] == text[i]:
            q = q + 1

        if q == len(pattern):
            result.append(i + 1 - q)
            q = pi[q-1]

    return result


def prefix_function(pattern):
    pi = [0]
    k = 0

    for q in range(1, len(pattern)):
        while(k > 0 and pattern[k] != pattern[q]):
            k = pi[k-1]

        if(pattern[k] == pattern[q]):
            k = k + 1

        pi.append(k)

    return pi


if __name__ == '__main__':
    # # head = build_trie(['abc', 'aab', 'cba'])
    # head = build_automaton(['abc', 'aab', 'cba'])
    # # show_graph(head)
    # head = modify_automaton(head)
    # show_graph(head)

    text = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 9, 9]]
    pattern = [[1, 2], [4, 5]]

    pattern_match_2d(text, pattern)
