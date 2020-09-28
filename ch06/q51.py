def read_file(filename):
    labels = []
    corpus = []

    with open(filename) as f:
        for line in f:
            label, text = line.strip().split("\t")
            labels.append(label)
            corpus.append(text)
    return corpus, labels

def save_features(filename, features, labels):
    with open(filename, "w") as f:
        for label, feature in zip(labels, features):
            feature = "\t".join(map(str, feature))
            f.write(f"{label}\t{feature}\n")


if __name__ == "__main__":
    from sklearn.feature_extraction.text import CountVectorizer

    corpus_train, y_train = read_file("train.txt")
    corpus_valid, y_valid = read_file("valid.txt")
    corpus_test, y_test = read_file("test.txt")
    corpus = [*corpus_train, *corpus_valid, *corpus_test]

    vectorizer = CountVectorizer()
    features = vectorizer.fit_transform(corpus)

    X_train = features[:len(y_train)].toarray()
    X_valid = features[len(y_train):len(y_train)+len(y_valid)].toarray()
    X_test = features[-len(y_test):].toarray()

    save_features("train.feature.txt", X_train, y_train)
    save_features("valid.feature.txt", X_valid, y_valid)
    save_features("test.feature.txt", X_test, y_test)
