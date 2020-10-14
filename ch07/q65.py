from itertools import chain


def flatten(nested_list):
    """1階層ネストしているリストをひらく

    Args:
        nested_list (list): ネストしているリスト

    Returns:
        list: 1階層ひらいたリスト
    """

    return list(chain.from_iterable(nested_list))


if __name__ == "__main__":
    from q64 import read_csv
    from sklearn.metrics import accuracy_score

    semantic_analogy = [
            "capital-common-countries",
            "capital-world",
            "currency",
            "city-in-state",
            "family",
            ]
    syntactic_analogy = [
            "gram1-adjective-to-adverb",
            "gram2-opposite",
            "gram3-comparative",
            "gram4-superlative",
            "gram5-present-participle",
            "gram6-nationality-adjective",
            "gram7-past-tense",
            "gram8-plural",
            "gram9-plural-verbs",
            ]

    data = read_csv("../output/sy64.txt")
    semantic = flatten([data[category] for category in semantic_analogy])
    syntactic = flatten([data[category] for category in syntactic_analogy])

    y_true = [words[3] for words in semantic]
    y_pred = [words[4] for words in semantic]
    print("semantic", accuracy_score(y_true=y_true, y_pred=y_pred))

    y_true = [words[3] for words in syntactic]
    y_pred = [words[4] for words in syntactic]
    print("syntactic", accuracy_score(y_true=y_true, y_pred=y_pred))
