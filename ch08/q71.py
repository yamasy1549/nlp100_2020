import dill
import numpy as np


def save_data(filename, data):
    """ シリアライズ

    Args:
        filename (str): 保存先ファイル名
        data (*): 保存するデータ
    """

    with open(filename, "wb") as f:
        dill.dump(data, f)
    print("{}: saved".format(filename))

def load_data(filename):
    """ デシリアライズ

    Args:
        filename (str): 読み出しファイル名

    Returns:
        *: 読みだしたデータ
    """

    with open(filename, "rb") as f:
        return dill.load(f)

def to_nparray(series):
    """ np.arrayのSeriesを行列にする

    Args:
        series (pd.Series): np.arrayのSeries

    Returns:
        np.array: 行列にしたもの
    """

    return np.array([*series])


if __name__ == "__main__":
    import numpy as np
    from scipy.special import softmax

    train = load_data("train.data")
    X_train, y_train = train["feature"], train["label"]

    W = np.random.rand(300, 4)

    y = X_train[0]
    print(softmax(y.dot(W)))
    y = to_nparray(X_train[0:4])
    print(softmax(y.dot(W)))
