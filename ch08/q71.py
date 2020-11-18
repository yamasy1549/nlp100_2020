import dill
import torch
import torch.nn as nn


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


class SingleLayerNN(nn.Module):
    """ 単層ニューラルネットワーク
    """

    def __init__(self, n_in, n_out):
        super().__init__()
        # Wは初期化
        self.W = nn.Parameter(torch.randn(300, 4))
        self.softmax = nn.Softmax(dim=-1)

    def forward(self, x):
        x = x @ self.W
        x = self.softmax(x)
        return x


if __name__ == "__main__":
    train = load_data("train.data")
    X_train = train["feature"]

    model = SingleLayerNN(300, 4)

    y_pred = model(X_train[0:1])
    print(y_pred)

    y_pred = model(X_train[0:4])
    print(y_pred)
