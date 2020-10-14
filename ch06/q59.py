from sklearn.metrics import accuracy_score, make_scorer


def acc_test(clf, X, y_true):
    y_pred = clf.predict(X_test)
    return accuracy_score(y_true, y_pred)

def acc_test_scorer():
    return make_scorer(acc_test)


if __name__ == "__main__":
    from q52 import read_features
    from sklearn.metrics import accuracy_score
    from sklearn.model_selection import GridSearchCV
    from sklearn.preprocessing import LabelEncoder
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.svm import SVR

    X_train, y_train = read_features("train.feature.txt")
    X_test, y_test = read_features("test.feature.txt")
    X_valid, y_valid = read_features("valid.feature.txt")

    le = LabelEncoder()
    le.fit(["b", "e", "m", "t"])
    y_train = le.transform(y_train)
    y_test = le.transform(y_test)
    y_valid = le.transform(y_valid)

    pipeline = make_pipeline(
            StandardScaler(),
            SVR()
            )
    parameters = {
            "svr__C": [0.001, 0.01, 0.1, 1, 10, 100],
            "svr__epsilon": [0.1 * n for n in range(10)],
            }
    model = GridSearchCV(pipeline, parameters, scoring=acc_test_scorer(), n_jobs=-1)
    model.fit(X_train, y_train)

    import pdb; pdb.set_trace()
