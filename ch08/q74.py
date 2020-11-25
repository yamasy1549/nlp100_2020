import torch


def accuracy_score(model, dataloader):
    """ accuracyを計算する

    Args:
        model (nn.Module): モデル
        dataloader (torch.utils.data.DataLoader): データ

    Returns:
        float: accuracy
    """

    total = 0
    correct = 0

    # 検証モード
    model.eval()

    with torch.no_grad():
        for X, y in dataloader:
            y_pred = torch.argmax(model(X), dim=-1)
            total += len(y)
            correct += (y_pred == y).sum().item()

    return correct / total


if __name__ == "__main__":
    from q71 import SingleLayerNN
    from q73 import load_dataloader, train_model

    dataloader_train = load_dataloader("train.data", batch_size=1)
    dataloader_valid = load_dataloader("valid.data", batch_size=512)

        model = SingleLayerNN(300, 4)
    model, *_ = train_model(model, dataloader_train, dataloader_valid,
            lr=1e-2, epochs=100)

    print("train_acc:", accuracy_score(model, dataloader_train))
    print("valid_acc:", accuracy_score(model, dataloader_valid))
