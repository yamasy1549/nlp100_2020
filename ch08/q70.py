import csv
import torch
import numpy as np
from gensim.models import KeyedVectors


w2v = KeyedVectors.load_word2vec_format("/home/resources/nlp100/GoogleNews-vectors-negative300.bin.gz", binary=True)
vocab = w2v.vocab.keys()
word_to_vec = w2v.word_vec


def text_to_feature(text):
    """ テキストから素性をつくる

    Args:
        text (str): テキスト

    Returns:
        np.array: 素性
    """

    words = text.split(" ")
    words = [word.strip("(),!?:;'\"") for word in words]

    vec = [word_to_vec(word) for word in words if word in vocab]
    return sum(vec) / len(vec)

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

def select_features(df):
    """ dfから特徴量を取り出す

    Args:
        pd.DataFrame (df): df

    Returns:
        torch.Tensor: 読みだしたデータ
    """

    data = df.loc[:, df.columns.str.startswith("vec")]
    return torch.Tensor(data.values)

def select_labels(df):
    """ dfからラベルを取り出す

    Args:
        pd.DataFrame (df): df

    Returns:
        torch.Tensor: 読みだしたデータ
    """

    data = df["label"]
    return torch.Tensor(data.values).long()


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

    # 特徴ベクトルをつくる
    features = []
    for i, row in df.iterrows():
        try:
            feature = text_to_feature(row["title"])
            feature = { "vec{}".format(i): feature[i] for i in range(len(feature)) }
        except:
            print(row["title"], "was ignored.")
            continue
        feature = dict(**feature, label=category_to_label(row["category"]))
        features.append(feature)
    df = pd.DataFrame.from_dict(features)

    train, valid = train_test_split(df, test_size=0.2, stratify=df["label"])
    valid, test = train_test_split(valid, test_size=0.5, stratify=valid["label"])
    train = train.reset_index(drop=True)
    valid = valid.reset_index(drop=True)
    test = test.reset_index(drop=True)

    save_data("train.data", {"feature": select_features(train), "label": select_labels(train)})
    save_data("valid.data", {"feature": select_features(valid), "label": select_labels(valid)})
    save_data("test.data", {"feature": select_features(test), "label": select_labels(test)})
