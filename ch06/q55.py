def print_scores(y_true, y_pred, classes):
    print(classes)
    print(confusion_matrix(y_true=y_true, y_pred=y_pred))


if __name__ == "__main__":
    from sklearn.metrics import confusion_matrix
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
