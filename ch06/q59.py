def labelize(label, *data):
    encoder = LabelEncoder()
    encoder.fit(label)
    result = [encoder.transform(_data) for _data in data]
    return [encoder, *result]


if __name__ == "__main__":
    from q52 import read_features
    from sklearn.metrics import accuracy_score
    from sklearn.model_selection import GridSearchCV
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import LabelEncoder, StandardScaler
    from sklearn.svm import SVC

    X_train, y_train = read_features("train.feature.txt")
    X_test, y_test = read_features("test.feature.txt")
    X_valid, y_valid = read_features("valid.feature.txt")
    encoder, y_train, y_test, y_valid = labelize(["b", "e", "m", "t"], y_train, y_test, y_valid)

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("svc", SVC()),
        ])

    parameter = {
            "svc__C": [0.1, 1, 10],
            "svc__kernel": ["linear", "poly", "rbf", "sigmoid"],
            "svc__gamma": ["scale", "auto"],
            }

    model = GridSearchCV(pipeline, parameter, n_jobs=-1)
    model.fit(X_train, y_train)
    import pdb; pdb.set_trace()
