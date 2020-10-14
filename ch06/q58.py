import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score


def predict_accuracy(model, X, y):
    y_pred = model.predict(X)
    score = accuracy_score(y_true=y, y_pred=y_pred)
    print(score)
    return score


if __name__ == "__main__":
    from q52 import read_features
    from sklearn.linear_model import LogisticRegression

    X_train, y_train = read_features("train.feature.txt")
    X_test, y_test = read_features("test.feature.txt")
    X_valid, y_valid = read_features("valid.feature.txt")

    acc_train = []
    acc_test = []
    acc_valid = []

    C = [0.001, 0.01, 0.1, 1, 10, 100]
    for c in C:
        model = LogisticRegression(max_iter=10000, C=c)
        model.fit(X_train, y_train)

        acc_train.append(predict_accuracy(model, X_train, y_train))
        acc_test.append(predict_accuracy(model, X_test, y_test))
        acc_valid.append(predict_accuracy(model, X_valid, y_valid))

    plt.plot(C, acc_train, label="train")
    plt.plot(C, acc_test, label="test")
    plt.plot(C, acc_valid, label="valid")
    plt.legend()
    plt.xlabel("C")
    plt.ylabel("accuracy")
    plt.savefig("../output/sy58.png")
