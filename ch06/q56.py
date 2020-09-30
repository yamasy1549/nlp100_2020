def print_scores(y_true, y_pred, classes):
    print(classes)
    print("適合率: カテゴリごと", precision_score(y_true=y_true, y_pred=y_pred, average=None))
    print("適合率: マイクロ平均", precision_score(y_true=y_true, y_pred=y_pred, average="micro"))
    print("適合率: マクロ平均", precision_score(y_true=y_true, y_pred=y_pred, average="macro"))

    print(classes)
    print("再現率: カテゴリごと", recall_score(y_true=y_true, y_pred=y_pred, average=None))
    print("再現率: マイクロ平均", recall_score(y_true=y_true, y_pred=y_pred, average="micro"))
    print("再現率: マクロ平均", recall_score(y_true=y_true, y_pred=y_pred, average="macro"))

    print(classes)
    print("F1スコア: カテゴリごと", f1_score(y_true=y_true, y_pred=y_pred, average=None))
    print("F1スコア: マイクロ平均", f1_score(y_true=y_true, y_pred=y_pred, average="micro"))
    print("F1スコア: マクロ平均", f1_score(y_true=y_true, y_pred=y_pred, average="macro"))


if __name__ == "__main__":
    from sklearn.metrics import precision_score, recall_score, f1_score
    from q51 import load
    from q52 import read_features

    X_train, y_train = read_features("train.feature.txt")
    X_test, y_test = read_features("test.feature.txt")
    model = load("model.dat")
    classes = model.classes_

    y_pred = model.predict(X_train)
    print("学習データ")
    print_scores(y_train, y_pred, classes)

    y_pred = model.predict(X_test)
    print("評価データ")
    print_scores(y_test, y_pred, classes)
