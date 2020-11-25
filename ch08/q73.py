import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm
from q71 import load_data, SingleLayerNN


class NewsDataset(Dataset):
  def __init__(self, X, y):
    self.X = X
    self.y = y

  def __len__(self):
    return len(self.y)

  def __getitem__(self, idx):
    return [self.X[idx], self.y[idx]]


def load_dataloader(filename, batch_size=-1, **kwargs):
    """ データを読んでDataLoaderをつくる

    Args:
        filename (str): データファイル名
        batch_size (int): バッチサイズ。デフォルトはバッチなし

    Returns:
        torch.utils.data.DataLoader: DataLoader
    """

    data = load_data(filename)
    dataset = NewsDataset(data["feature"], data["label"])

    if batch_size == -1:
        kwargs["batch_size"] = len(dataset)

    dataloader = DataLoader(dataset, **kwargs)
    return dataloader

def train_model(dataloader, lr=1e-2, epochs=100):
    """ モデルを訓練する

    Args:
        dataloader (torch.utils.data.DataLoader): 訓練データ
        lr (float): 学習率
        epochs (int): エポック数

    Returns:
        tuple: model, optimizer, loss_func
    """

    model = SingleLayerNN(300, 4)
    optimizer = optim.SGD(model.parameters(), lr=lr)
    loss_func = nn.CrossEntropyLoss()

    for epoch in range(epochs):
        # 訓練モード
        model.train()
        progressbar = tqdm(total=len(dataloader))
        progressbar.set_description("epoch {}".format(epoch+1))

        for i, (X, y) in enumerate(dataloader):
            # 勾配初期化
            optimizer.zero_grad()
            # 損失計算
            loss = loss_func(model(X), y)
            loss.backward()
            # 勾配更新
            optimizer.step()
            progressbar.update(1)

    return model, optimizer, loss_func


if __name__ == "__main__":
    dataloader_train = load_dataloader("train.data", batch_size=1)

    model, *_ = train_model(dataloader_train, lr=1e-2, epochs=100)
    print(model.linear.weight)
