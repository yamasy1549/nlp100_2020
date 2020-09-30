if __name__ == "__main__":
    from q51 import load
    from q52 import read_features

    X_test, y_test = read_features("test.feature.txt")
    model = load("model.dat")

    # 予測カテゴリ
    y_pred = model.predict(X_test)
    # カテゴリごとの予測確率
    proba = model.predict_proba(X_test)

    print(f"正解\t予想\t{model.classes_}")
    for true, pred, p in zip(y_test, y_pred, proba):
        print(f"{true}\t{pred}\t{p}")
