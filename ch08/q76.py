if __name__ == "__main__":
    from q71 import SingleLayerNN
    from q73 import load_dataloader
    from q75 import train_model

    dataloader_train = load_dataloader("train.data", batch_size=1)
    dataloader_valid = load_dataloader("valid.data", batch_size=512)

    model = SingleLayerNN(300, 4)
    model, *_ = train_model(model, dataloader_train, dataloader_valid,
            lr=1e-2, epochs=100, save_checkpoint=True)
