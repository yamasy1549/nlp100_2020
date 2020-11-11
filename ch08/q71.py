import dill
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

    def __init__(self, n_in, n_mid):
        super().__init__()
        self.W = nn.Linear(n_in, n_mid)
        # 一様分布で初期化
        nn.init.normal_(self.W.weight, 0.0, 1.0)

    def forward(self, x):
        output = self.W(x)
        return output


if __name__ == "__main__":
    import torch

    train = load_data("train.data")
    X_train = train["feature"]

    model = SingleLayerNN(300, 4)

    _y = model(X_train[0:1])
    y = torch.softmax(_y, dim=-1)
    print(y)

    _y = model(X_train[0:4])
    y = torch.softmax(_y, dim=-1)
    print(y)
