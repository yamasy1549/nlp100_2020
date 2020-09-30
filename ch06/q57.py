if __name__ == "__main__":
    from q51 import load

    model = load("model.dat")
    # 素性の一覧を得る
    vectorizer = load("vectorizer.dat")
    features = vectorizer.get_feature_names()

    # カテゴリx素性のぶんだけcoef_があるが、すべてひっくるめてソートする
    all_coef = []
    for category_coef, category in zip(model.coef_, model.classes_):
        for coef, feature in zip(category_coef, features):
            all_coef.append((coef, feature, category))

    sorted_coef = sorted(all_coef)
    n = 10

    print("重みの高い特徴量")
    for coef in sorted_coef[::-1][:n]:
        print(coef)

    print("重みの低い特徴量")
    for coef in sorted_coef[:n]:
        print(coef)
