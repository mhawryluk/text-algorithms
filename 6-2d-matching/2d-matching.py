class Node:
    def __init__(self, is_head=False, parent=None, char=None):
        self.is_head = is_head
        self.edges = {}
        self.fail_link = None
        self.parent = parent
        self.char = char


def build_trie(patterns):
    head = Node(is_head=True)

    for pattern in patterns:
        current_node = head
        for char in pattern:
            if char in current_node.edges:
                current_node = current_node.edges[char]
            else:
                current_node.edges[char] = Node(char=char, parent=current_node)

    return head


def build_automaton(text):
    head = build_trie(text)

    queue = [head]

    def assign_fail_links(node):
        current_node = node.parent.fail_link

        while current_node:
            if node.char in current_node.edges:
                node.fail_link = current_node.edge[node.char]
                break
            current_node = current_node.fail_link
        else:
            node.fail_link = head

        for edge in node.edges.items():
            if edge not in queue:
                queue.append(assign_fail_links(edge))

    while queue:
        node = queue.pop(0)
        assign_fail_links(node)


if __name__ == '__main__':
    pass
