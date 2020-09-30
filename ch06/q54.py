if __name__ == "__main__":
    from sklearn.metrics import accuracy_score
    from q51 import load
    from q52 import read_features

    X_train, y_train = read_features("train.feature.txt", num=True)
    X_test, y_test = read_features("test.feature.txt", num=True)
    model = load("model.dat")

    y_pred = model.predict(X_train)
    print("学習データ")
    print(accuracy_score(y_true=y_train, y_pred=y_pred))

    y_pred = model.predict(X_test)
    print("評価データ")
    print(accuracy_score(y_true=y_test, y_pred=y_pred))
