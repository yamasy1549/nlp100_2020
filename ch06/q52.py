def read_features(filename):
    """ファイルから素性を読み出す

    Args:
        filename (str): ファイル名（中身は ラベル\t素性... の形式。行内の素性は\tで区切られている）

    Returns:
        list: [素性のリスト, ラベルのリスト]
    """

    labels = []
    features = []

    with open(filename) as f:
        for line in f:
            label, *feature = line.strip().split("\t")
            # 素性をfloatとして読む
            feature = [float(elem) for elem in feature]
            features.append(feature)
            labels.append(label)

    return features, labels


if __name__ == "__main__":
    from q51 import dump
    from sklearn.linear_model import LogisticRegression

    X_train, y_train = read_features("train.feature.txt")

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    dump("model.dat", model)
