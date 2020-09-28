from sklearn.linear_model import LogisticRegression

def read_features(filename, num=True):
    """ファイルから素性を読み出す

    Args:
        filename (str): ファイル名（中身は ラベル\t素性... の形式。行内の素性は\tで区切られている）
        num (bool): 素性を数値とする

    Returns:
        list: [素性のリスト, ラベルのリスト]
    """

    labels = []
    features = []

    with open(filename) as f:
        for line in f:
            label, *feature = line.strip().split("\t")
            if num:
                feature = [int(elem) for elem in feature]
            features.append(feature)
            labels.append(label)

    return features, labels


if __name__ == "__main__":
    X_train, y_train = read_features("train.feature.txt", num=True)
    X_test, y_test = read_features("test.feature.txt", num=True)

    lr = LogisticRegression()
    lr.fit(X_train, y_train)
