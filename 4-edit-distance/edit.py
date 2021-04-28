
LEFT = '\u2190'
UP = '\u2191'
DIAG = '\u2B09'


def print_2d(l): return print('\n'.join(map(''.join, list(map(str, l)))))


def levensheit(text_a, text_b):
    edit = [[None for _ in range(len(text_b) + 1)]
            for _ in range(len(text_a) + 1)]
    path = [[None for _ in range(len(text_b) + 1)]
            for _ in range(len(text_a) + 1)]

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

    i, j = len(text_a), len(text_b)
    changes = ""

    while i > 0 or j > 0:
        if path[i][j] == LEFT:
            changes += f'insert {text_b[j]} '
            j -= 1
        elif path[i][j] == UP:
            changes += f'delete {text_a[i]} '
            i -= 1
        else:
            if path[i][j] == DIAG and edit[i][j] != edit[i-1][j-1]:
                changes += f'replace {text_a[i]} with {text_b[j]} '
            i -= 1
            j -= 1

    print_2d(path)
    print_2d(edit)
    return edit[len(text_a)-1][len(text_b)-1], changes


if __name__ == '__main__':
    print(levensheit('los', 'kloc'))
