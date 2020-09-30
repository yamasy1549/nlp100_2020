import cloudpickle


def dump(filename, obj):
    """オブジェクトを保存する

    Args:
        filename (str): ファイル名
        obj (*): 保存したいオブジェクト
    """

    with open(filename, "wb") as f:
        f.write(cloudpickle.dumps(obj))

def load(filename):
    """オブジェクトを読み込む

    Args:
        filename (str): ファイル名

    Returns:
        *: 保存されていたオブジェクト
    """

    with open(filename, "rb") as f:
        return cloudpickle.loads(f.read())

def read_file(filename):
    """データファイルを読む

    Args:
        filename (str): ファイル名

    Returns:
        list: [データのリスト, ラベルのリスト]
    """

    labels = []
    corpus = []

    with open(filename) as f:
        for line in f:
            label, text = line.strip().split("\t")
            labels.append(label)
            corpus.append(text)
    return corpus, labels

def save_features(filename, features, labels):
    """素性とラベルを保存する

    Args:
        filename (str): ファイル名
        features (list): 素性のリスト
        labels (list): ラベルのリスト
    """

    with open(filename, "w") as f:
        for label, feature in zip(labels, features):
            feature = "\t".join(map(str, feature))
            f.write(f"{label}\t{feature}\n")


if __name__ == "__main__":
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.preprocessing import StandardScaler

    corpus_train, y_train = read_file("train.txt")
    corpus_valid, y_valid = read_file("valid.txt")
    corpus_test, y_test = read_file("test.txt")
    corpus = [*corpus_train, *corpus_valid, *corpus_test]

    # 素性を作る
    vectorizer = CountVectorizer()
    features = vectorizer.fit_transform(corpus)
    dump("vectorizer.dat", vectorizer)

    # 標準化する（中心化はしない）
    scaler = StandardScaler(with_mean=False)
    features = scaler.fit_transform(features)

    X_train = features[:len(y_train)].toarray()
    X_valid = features[len(y_train):len(y_train)+len(y_valid)].toarray()
    X_test = features[-len(y_test):].toarray()

    # 素性を保存する
    save_features("train.feature.txt", X_train, y_train)
    save_features("valid.feature.txt", X_valid, y_valid)
    save_features("test.feature.txt", X_test, y_test)
