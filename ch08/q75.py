import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
from q71 import SingleLayerNN
from q73 import batch


class Trainer():
    def __init__(self):
        self.model = SingleLayerNN(300, 4)
        self.loss_func = nn.CrossEntropyLoss()
        self.plot_data = {
                "train_loss": [],
                "valid_loss": [],
                "train_acc": [],
                "valid_acc": [],
                }

    def train(self, X_train, y_train, X_valid, y_valid, lr=1e-2, epochs=100, batch_size=256):
        """ モデルを訓練する

        Args:
            X_train (iterable): 訓練データ
            y_train (iterable): 訓練データのラベル
            X_valid (iterable): 検証データ
            y_valid (iterable): 検証データのラベル
            lr (float): 学習率
            epochs (int): エポック数
            batch_size (int): バッチサイズ

        Returns:
            tuple: model, optimizer, loss_func
        """

        self.optimizer = optim.SGD(self.model.parameters(), lr=lr)

        for epoch in range(epochs):
            # 訓練モード
            self.model.train()
            for X, y in batch(X_train, y_train, batch_size):
                loss = self.loss_func(self.model(X), y)
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

            # 検証モード
            self.model.eval()
            with torch.no_grad():
                train_loss, train_acc = self.calc_scores(X_train, y_train, batch_size)
                valid_loss, valid_acc = self.calc_scores(X_valid, y_valid, batch_size)
                self.plot_data["train_loss"].append(train_loss)
                self.plot_data["valid_loss"].append(valid_loss)
                self.plot_data["train_acc"].append(train_acc)
                self.plot_data["valid_acc"].append(valid_acc)

        self.plot(epochs)

    def calc_scores(self, X_data, y_data, batch_size):
        loss = 0.0
        correct = 0
        total = 0
        batch_count = 0

        for X, y in batch(X_data, y_data, batch_size):
            loss += self.loss_func(self.model(X), y).item()
            correct += (self.model(X).argmax(dim=-1) == y).sum().item()
            total += len(X)
            batch_count += 1

        return loss / batch_count, correct / total


    def plot(self, epoch):
        epochs = list(range(epoch))

        for key, value in self.plot_data.items():
            plt.plot(epochs, value, label=key)
        plt.legend()
        plt.savefig("q75.png")



if __name__ == "__main__":
    from q71 import load_data

    train = load_data("train.data")
    valid = load_data("valid.data")
    X_train, y_train = train["feature"], train["label"]
    X_valid, y_valid = valid["feature"], valid["label"]

    trainer = Trainer()
    trainer.train(X_train, y_train, X_valid, y_valid, lr=1e-2, epochs=100, batch_size=256)
