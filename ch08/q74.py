def accuracy_score(pred, true):
    """ accuracyを計算する

    Args:
        pred (list): 予測データ
        true (list): 正解データ

    Returns:
        float: accuracy
    """

    return len([p for p, t in zip(pred, true) if p == t]) / len(pred)


if __name__ == "__main__":
    from q71 import load_data
    from q73 import train_model

    train = load_data("train.data")
    valid = load_data("valid.data")
    X_train, y_train = train["feature"], train["label"]
    X_valid, y_valid = valid["feature"], valid["label"]

    model, *_ = train_model(X_train, y_train, lr=1e-2, epochs=100, batch_size=256)

    # 検証モード
    model.eval()
    print("train_acc:", accuracy_score(model(X_train).argmax(dim=-1), y_train))
    print("valid_acc:", accuracy_score(model(X_valid).argmax(dim=-1), y_valid))
