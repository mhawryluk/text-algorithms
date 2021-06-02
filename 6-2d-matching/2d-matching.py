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

        current_node.pattern_end = i

    return head


def modofy_automaton(head):

    queue = [head]

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
            if edge not in queue:
                queue.append(edge)

    while queue:
        node = queue.pop(0)
        assign_fail_links(node)

    return head


def build_automaton(patterns):
    head = build_trie(patterns)

    queue = [head]

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
            if edge not in queue:
                queue.append(edge)

    while queue:
        node = queue.pop(0)
        assign_fail_links(node)

    return head


def pattern_match_2d(text, pattern):
    head = build_automaton(text, pattern)


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
            if node.fail_link in graph[node]:
                graph.add_edge(
                    node, node.fail_link, label=graph[node][node.fail_link].label + 'faillink')
            else:
                graph.add_edge(node, node.fail_link)

        node.visited = True

    pos = nx.spectral_layout(graph)
    nx.draw_networkx(
        graph, pos, connectionstyle='arc3, rad = 0.2', node_color='turquoise')
    labels = nx.get_edge_attributes(graph, 'label')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    plt.show()


if __name__ == '__main__':
    # head = build_trie(['abc', 'aab', 'cba'])
    head = build_automaton(['abc', 'aab', 'cba'])
    show_graph(head)
