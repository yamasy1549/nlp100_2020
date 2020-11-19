if __name__ == "__main__":
    import torch.nn as nn
    from q71 import load_data, SingleLayerNN

    train = load_data("train.data")
    X_train, y_train = train["feature"], train["label"]

    loss_func = nn.CrossEntropyLoss()
    model = SingleLayerNN(300, 4)

    y_pred, y_true = model(X_train[0:1]), y_train[0:1]
    loss = loss_func(y_pred, y_true)
    model.zero_grad()
    loss.backward()
    print("クロスエントロピー損失", loss.item())
    print("行列Wに対する勾配", model.linear.weight.grad)

    y_pred, y_true = model(X_train[0:4]), y_train[0:4]
    loss = loss_func(y_pred, y_true)
    model.zero_grad()
    loss.backward()
    print("クロスエントロピー損失", loss.item())
    print("行列Wに対する勾配", model.linear.weight.grad)
