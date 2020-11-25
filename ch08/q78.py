import torch


def check_device():
    """ GPUを使えるかどうかチェックする

    Returns:
        str: device
    """

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print("device:", device)
    return device


if __name__ == "__main__":
    from q71 import SingleLayerNN
    from q73 import load_dataloader
    from q75 import train_model

    device = check_device()
    #  batch_size_list = [2 ** i for i in range(20)]
    batch_size_list = [512]

    for batch_size in batch_size_list:
        dataloader_train = load_dataloader("train.data", batch_size=batch_size)
        dataloader_valid = load_dataloader("valid.data", batch_size=512)

        model = SingleLayerNN(300, 4)
        model, *_ = train_model(model, dataloader_train, dataloader_valid,
                lr=1e-1, epochs=100, device=device, save_plot=True, save_checkpoint=True)
