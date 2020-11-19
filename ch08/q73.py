import torch.nn as nn
import torch.optim as optim
from q71 import SingleLayerNN


def batch(X, y, batch_size=1):
    """ ミニバッチをつくる

    Args:
        X (iterable): X
        y (iterable): y
        batch_size (int): バッチサイズ
    """

    X_size = len(X)
    for begin in range(0, X_size, batch_size):
        end = min(begin + batch_size, X_size)
        yield X[begin:end], y[begin:end]

def train_model(X_train, y_train, lr=1e-2, epochs=100, batch_size=256):
    """ モデルを訓練する

    Args:
        X_train (iterable): 訓練データ
        y_train (iterable): 訓練データのラベル
        lr (float): 学習率
        epochs (int): エポック数
        batch_size (int): バッチサイズ

    Returns:
        tuple: model, optimizer, loss_func
    """

    model = SingleLayerNN(300, 4)
    optimizer = optim.SGD(model.parameters(), lr=lr)
    loss_func = nn.CrossEntropyLoss()

    for epoch in range(epochs):
        # 訓練モード
        model.train()
        for X, y in batch(X_train, y_train, batch_size):
            loss = loss_func(model(X), y)
            # 勾配初期化
            optimizer.zero_grad()
            # 勾配計算
            loss.backward()
            # 勾配更新
            optimizer.step()

    return model, optimizer, loss_func


if __name__ == "__main__":
    from q71 import load_data

    train = load_data("train.data")
    X_train, y_train = train["feature"], train["label"]

    model, *_ = train_model(X_train, y_train, lr=1e-2, epochs=100, batch_size=256)
    print(model.linear.weight)
