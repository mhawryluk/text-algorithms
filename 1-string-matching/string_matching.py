# wyszukiwanie wzorca w tekście
# lab 1
import re


def naive(text, pattern):
    result = []

    pattern_length = len(pattern)
    text_length = len(text)

    for i in range(text_length - pattern_length + 1):
        if text[i:i + pattern_length] == pattern:
            result.append(i)

    return result


def finite_automaton(text, delta):
    result = []

    pattern_length = len(delta) - 1
    state = 0

    for i, char in enumerate(text):
        if char in delta[0]:
            state = delta[state][char]
            if state == pattern_length:
                result.append(i - pattern_length + 1)
        else:
            state = 0

    return result


def transition_table(pattern):
    result = []
    alphabet = set([c for c in pattern])

    for q in range(0, len(pattern) + 1):
        result.append({})
        for a in alphabet:
            k = min(len(pattern) + 1, q + 2)

            while True:
                k = k - 1
                if re.search(f"{pattern[:k]}$", pattern[:q] + a):
                    break

            result[q][a] = k

    return result


def kmp(text, pattern, prefix_function):
    result = []

    pi = prefix_function
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
    pass
