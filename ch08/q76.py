if __name__ == "__main__":
    from q71 import load_data
    from q75 import Trainer

    train = load_data("train.data")
    valid = load_data("valid.data")
    X_train, y_train = train["feature"], train["label"]
    X_valid, y_valid = valid["feature"], valid["label"]

    Trainer().train(X_train, y_train, X_valid, y_valid,
            lr=1e-2, epochs=100, batch_size=256,
            checkpoint=True)
