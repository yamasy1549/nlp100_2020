import csv
import numpy as np
from gensim.models import KeyedVectors


w2v = KeyedVectors.load_word2vec_format("/home/resources/nlp100/GoogleNews-vectors-negative300.bin.gz", binary=True)
vocab = w2v.vocab.keys()
word_to_vec = w2v.word_vec


def create_empty_vec():
    """ 0埋めされた単語ベクトルをつくる

    Returns:
        np.array: 単語ベクトル
    """

    return np.array([0.0] * 300)

def word_to_vector(word):
    """ 単語からベクトルをつくる

    Args:
        word (str): 単語

    Returns:
        np.array: 単語ベクトル
    """

    if word in vocab:
        return word_to_vec(word)
    return create_empty_vec()

def text_to_feature(text):
    """ テキストから素性をつくる

    Args:
        text (str): テキスト

    Returns:
        np.array: 素性
    """

    vec = create_empty_vec()
    words = text.split(" ")

    for word in words:
        vec += word_to_vector(word)
    return vec / len(words)

def category_to_label(category):
    """ カテゴリ名からラベルをつくる

    Args:
        category (str): カテゴリ名

    Returns:
        int: ラベル
    """

    if category == "b":
        return 0
    elif category == "t":
        return 1
    elif category == "e":
        return 2
    elif category == "h":
        return 3


if __name__ == "__main__":
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from q71 import save_data

    columns = [
            "id",
            "title",
            "url",
            "publisher",
            "category",
            "story",
            "hostname",
            "timestamp",
            ]
    df = pd.read_table("../ch06/newsCorpora.csv", names=columns, quoting=csv.QUOTE_NONE)
    df = df.sample(frac=1)
    df = df[df["category"].isin(["b", "t", "e", "h"])]
    df = df[["title", "category"]]

    feature = df["title"].apply(lambda title: text_to_feature(title))
    label = df["category"].apply(lambda category: category_to_label(category))
    df = pd.DataFrame.from_dict({"feature": feature, "label": label})

    train, valid = train_test_split(df, test_size=0.2)
    valid, test = train_test_split(valid, test_size=0.5)
    train = train.reset_index(drop=True)
    valid = valid.reset_index(drop=True)
    test = test.reset_index(drop=True)

    save_data("train.data", {"feature": train["feature"], "label": train["label"]})
    save_data("valid.data", {"feature": valid["feature"], "label": valid["label"]})
    save_data("test.data", {"feature": test["feature"], "label": test["label"]})
