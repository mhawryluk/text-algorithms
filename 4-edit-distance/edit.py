import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
from spacy.lang.pl import Polish

LEFT = '\u2190'
UP = '\u2191'
DIAG = '\u2B09'

NEXT = 0
INSERT = 1
DELETE = 2
REPLACE = 3


def print_2d(l): return print(
    '\n'.join(map(''.join, list(map(lambda x: str(x).replace("'", ""), l)))))


def levensheit(text_a, text_b, delta=None):
    edit = [[None for _ in range(len(text_b) + 1)]
            for _ in range(len(text_a) + 1)]
    path = [[None for _ in range(len(text_b) + 1)]
            for _ in range(len(text_a) + 1)]

    if delta is None:
        def delta(char_a, char_b): return 0 if char_a == char_b else 1

    for i in range(len(text_a) + 1):
        edit[i][0] = i
        path[i][0] = UP

    for j in range(1, len(text_b) + 1):
        edit[0][j] = j
        path[0][j] = LEFT

    for i in range(1, len(text_a)+1):
        for j in range(1, len(text_b)+1):
            options = [edit[i-1][j] + 1, edit[i][j-1] + 1,
                       edit[i-1][j-1] + delta(text_a[i-1], text_b[j-1])]
            edit[i][j] = min(options)

            if edit[i][j] == options[0]:
                path[i][j] = UP
            elif edit[i][j] == options[1]:
                path[i][j] = LEFT
            else:
                path[i][j] = DIAG

    return edit[len(text_a)][len(text_b)], edit, path


def get_changes(text_a, text_b, edit, path):
    i, j = len(text_a), len(text_b)
    changes = []

    while i > 0 or j > 0:
        if path[i][j] == LEFT:
            changes.append([INSERT, text_b[j-1]])
            j -= 1
        elif path[i][j] == UP:
            changes.append([DELETE, text_a[i-1]])
            i -= 1
        else:
            if path[i][j] == DIAG and edit[i][j] != edit[i-1][j-1]:
                changes.append([REPLACE, text_a[i-1], text_b[j-1]])
            else:
                changes.append([NEXT])

            i -= 1
            j -= 1
    return changes


def transform(text_a, text_b, changes):
    i = 0
    current = text_a
    states = [current]

    for change in reversed(changes):
        if change[0] == INSERT:
            current = current[:i] + change[1] + current[i:]
            states.append(current[:i] + '*' + current[i] + '*' + current[i+1:])
        elif change[0] == REPLACE:
            current = current[:i] + change[2] + current[i+1:]
            states.append(current[:i] + '*' + current[i] + '*' + current[i+1:])
        elif change[0] == DELETE:
            current = current[:i] + current[i+1:] if i + \
                1 < len(current) else current[:i]
            states.append(current[:i]+'**'+current[i:])
            i -= 1

        i += 1

    return states


def get_lcs(text_a, text_b):
    def delta(x, y): return 0 if str(x) == str(y) else 2
    dist, edit, path = levensheit(text_a, text_b, delta)

    lcs_len = (len(text_a) + len(text_b) - dist)//2

    i, j = len(text_a), len(text_b)
    common = []

    while i > 0 or j > 0:
        if path[i][j] == LEFT:
            j -= 1
        elif path[i][j] == UP:
            i -= 1
        else:
            if path[i][j] == DIAG:
                common.append((i-1, j-1, text_a[i-1]))
            i -= 1
            j -= 1

    lcs = ''.join(str(x[2]) for x in reversed(common))
    return lcs_len, lcs, common


def print_diff(line_a, line_b, num):
    dist, lcs, common = get_lcs(line_a, line_b)
    print(lcs)
    print(common)
    i = 0

    if dist == len(line_a) and dist == len(line_b):
        return

    common_a = set(x[0] for x in common)
    common_b = set(x[1] for x in common)

    print(
        f"< {num} | {''.join(str(c) for i, c in enumerate(line_a) if i not in common_a)}")
    print(
        f"> {num} | {''.join(str(c) for i, c in enumerate(line_b) if i not in common_b)}")


def diff(file_a, file_b):
    nlp = Polish()
    tokenizer = nlp.tokenizer
    f_a = open(file_a, "r")
    f_b = open(file_b, "r")
    for i, lines in enumerate(zip(f_a, f_b)):
        print_diff(tokenizer(lines[0]), tokenizer(lines[1]), i)


def animate(states):
    fig, ax = plt.subplots()
    time_text = ax.text(0, 1, '', fontsize=30)
    plt.axis('off')

    def updatefig(num):
        time_text.set_text(states[num])
        return time_text,

    return animation.FuncAnimation(fig, updatefig, interval=500, frames=len(states))


if __name__ == '__main__':
    text_a, text_b = "kwintesencja", "quintessence"
    # value, edit, path = levensheit(text_a, text_b)
    # changes = get_changes(text_a, text_b, edit, path)
    # print(value)
    # # print_2d(changes)
    # # print_2d(edit)
    # # print_2d(path)
    # states = transform(text_a, text_b, changes)
    # print(states)
    # animation = animate(states)
    # # plt.draw()
    # plt.show()


    print(get_lcs('los', 'kloc'))
    # nlp = Polish()
    # tokenizer = nlp.tokenizer

    # with open('romeo-i-julia-700.txt', 'r') as f:
    #     text = ''.join(f)

    # diff('a.txt', 'b.txt')
