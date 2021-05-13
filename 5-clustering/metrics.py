from collections import Counter


def lcs(x, y):
    common = [[0 for _ in range(len(y)+1)] for _ in range(len(x)+1)]
    max_lcs = 0

    for i in range(1, len(x) + 1):
        for j in range(1, len(y)+1):
            common[i][j] = common[i-1][j-1] + 1 if x[i-1] == y[j-1] else 0
            max_lcs = max(max_lcs, common[i][j])

    return 1 - max_lcs/max(len(x), len(y))


def ngram(x, n):
    ngrams = [x[i:i+n] for i in range(len(x)-n+1)]
    return Counter(ngrams)


def dice(x, y, n=2):
    ngrams_x, ngrams_y = set(ngram(x, n).keys()), set(ngram(y, n).keys())
    return 1 - 2*len(ngrams_x & ngrams_y)/(len(ngrams_x)+len(ngrams_y))


def euclides(x, y):
    ngrams_x, ngrams_y = ngram(x, 2), ngram(y, 2)

    keys = set(ngrams_x.keys()) | set(ngrams_y.keys())
    dist = 0

    for key in keys:
        value_x = ngrams_x.get(key, 0)
        value_y = ngrams_y.get(key, 0)

        dist += (value_x - value_y)**2

    return dist**0.5


if __name__ == '__main__':
    x = 'BCDF'
    y = 'ABCDEF'
    print(lcs(x, y))
    print(dice(x, y))
    print(euclides(x, y))
