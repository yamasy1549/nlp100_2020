if __name__ == "__main__":
    from q71 import SingleLayerNN
    from q73 import load_dataloader
    from q75 import train_model

    batch_size_list = [2 ** i for i in range(20)]

    for batch_size in batch_size_list:
        dataloader_train = load_dataloader("train.data", batch_size=batch_size)
        dataloader_valid = load_dataloader("valid.data", batch_size=512)

        model = SingleLayerNN(300, 4)
        model, *_ = train_model(model, dataloader_train, dataloader_valid,
                lr=1e-2, epochs=100, take_time=True)
