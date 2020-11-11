if __name__ == "__main__":
    import torch.nn as nn
    import torch.optim as optim
    from q71 import load_data, SingleLayerNN

    train = load_data("train.data")
    X_train, y_train = train["feature"], train["label"]

    loss_func = nn.CrossEntropyLoss()
    model = SingleLayerNN(300, 4)
    optimizer = optim.SGD(model.parameters(), lr=0.1)

    for epoch in range(100):
        optimizer.zero_grad()
        y_pred = model(X_train)
        loss = loss_func(y_pred, y_train)
        loss.backward()
        optimizer.step()
        print(loss.item())
