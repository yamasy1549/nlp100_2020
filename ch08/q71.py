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

    def __init__(self, in_features, out_features):
        super().__init__()
        # Wは初期化
        self.linear = nn.Linear(in_features, out_features, bias=False)
        nn.init.normal_(self.linear.weight, 0.0, 1.0)

    def forward(self, x):
        x = self.linear(x)
        return x


if __name__ == "__main__":
    import torch

    train = load_data("train.data")
    X_train = train["feature"]

    model = SingleLayerNN(300, 4)

    y_pred = model(X_train[0:1])
    y_proba = torch.softmax(y_pred, dim=-1)
    print(y_proba)

    y_pred = model(X_train[0:4])
    y_proba = torch.softmax(y_pred, dim=-1)
    print(y_proba)
