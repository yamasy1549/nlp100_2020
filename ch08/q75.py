import time
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
from tqdm import tqdm


def plot_scores(epochs, plot_data):
    """ スコアをグラフに描画する

    Args:
        epochs (int): 総エポック数
        plot_data (dict): 描画データ
    """

    for key, value in plot_data.items():
        plt.plot(epochs, value, label=key)
    plt.legend()
    plt.savefig("sy75.png")

def save_params(model, optimizer, epoch):
    """ チェックポイントでセーブする

    Args:
        model (nn.Module): モデル
        epoch (int): 現在のエポック数
    """

    path = "sy76model:{}.pt".format(epoch)
    torch.save({
        'epoch': epoch,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        }, path)

def calc_scores(model, loss_func, dataloader, device="cpu"):
    """ 損失と正解率を計算する

    Args:
        model (nn.Module): モデル
        loss_func (torch.nn.modules.loss.*): 損失関数
        dataloader (torch.utils.data.DataLoader): データ
        device (str): GPUを使うかどうか

    Returns:
        tuple: loss, accuracy
    """

    loss = 0.0
    total = 0
    batch_count = len(dataloader)
    correct = 0

    # 検証モード
    model.eval()

    with torch.no_grad():
        for i, (X, y) in enumerate(dataloader):
            X = X.to(device)
            y = y.to(device)

            loss += loss_func(model(X), y).item()
            y_pred = torch.argmax(model(X), dim=-1)
            total += len(y)
            correct += (y_pred == y).sum().item()

    return loss / batch_count, correct / total

def train_model(model, dataloader_train, dataloader_valid, lr=1e-2, epochs=100, device="cpu",
        show_progress=True, save_plot=False, save_checkpoint=False, take_time=False):
    """ モデルを訓練する

    Args:
        dataloader_train (torch.utils.data.DataLoader): 訓練データ
        dataloader_valid (torch.utils.data.DataLoader): 検証データ
        lr (float): 学習率
        epochs (int): エポック数
        device (str): GPUを使うかどうか
        show_progress (bool): 進行度を表示するかどうか
        save_plot (bool): スコアをプロットして保存するかどうか
        save_checkpoint (bool): チェックポイントでセーブするかどうか
        take_time (bool): 1エポックごとの所要時間を測るかどうか

    Returns:
        tuple: model, optimizer, loss_func
    """

    # グラフ描画用
    plot_data = {
            "train_loss": [],
            "valid_loss": [],
            "train_acc": [],
            "valid_acc": [],
            }

    model = model.to(device)
    optimizer = optim.SGD(model.parameters(), lr=lr)
    loss_func = nn.CrossEntropyLoss()

    for epoch in range(epochs):
        if show_progress:
            progressbar = tqdm(total=len(dataloader_train))
            progressbar.set_description("epoch {}".format(epoch+1))

        # 訓練モード
        model.train()

        # 時間計測
        start_time = time.time()

        for i, (X, y) in enumerate(dataloader_train):
            X = X.to(device)
            y = y.to(device)

            # 勾配初期化
            optimizer.zero_grad()
            # 損失計算
            loss = loss_func(model(X), y)
            loss.backward()
            # 勾配更新
            optimizer.step()

            if show_progress:
                progressbar.update(1)

        # 時間計測
        if take_time:
            end_time = time.time()
            print("time:", end_time - start_time)

        # スコア計算
        train_loss, train_acc = calc_scores(model, loss_func, dataloader_train, device=device)
        valid_loss, valid_acc = calc_scores(model, loss_func, dataloader_valid, device=device)
        plot_data["train_loss"].append(train_loss)
        plot_data["valid_loss"].append(valid_loss)
        plot_data["train_acc"].append(train_acc)
        plot_data["valid_acc"].append(valid_acc)
        print("epoch:", epoch, {key:value[-1] for key, value in plot_data.items()})

        # チェックポイントでセーブ
        if save_checkpoint:
            save_params(model, optimizer, epoch)

    # スコアをプロットして保存
    if save_plot:
        plot_scores(epochs, plot_data)

    return model, optimizer, loss_func


if __name__ == "__main__":
    from q71 import SingleLayerNN
    from q73 import load_dataloader

    dataloader_train = load_dataloader("train.data", batch_size=1)
    dataloader_valid = load_dataloader("valid.data", batch_size=512)

    model = SingleLayerNN(300, 4)
    model, *_ = train_model(model, dataloader_train, dataloader_valid,
            lr=1e-2, epochs=100, save_plot=True)
