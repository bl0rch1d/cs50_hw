from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""

    a, b = a.splitlines(), b.splitlines()

    return compare_lists(a, b)


def sentences(a, b):
    """Return sentences in both a and b"""

    a, b = sent_tokenize(a), sent_tokenize(b)

    return compare_lists(a, b)


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    result_a = [a[i:i+n] for i in range(len(a))]
    result_b = [b[i:i+n] for i in range(len(b))]

    return compare_lists(result_a, result_b)


def compare_lists(list_1, list_2):
    return list(set(list_1) & set(list_2))
