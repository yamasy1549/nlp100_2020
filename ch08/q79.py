import os
import csv
import numpy as np
import pandas as pd
import torch.nn as nn
from torch.nn.utils.rnn import pad_sequence
from gensim.models import KeyedVectors
from sklearn.model_selection import train_test_split
from q70 import category_to_label
from q71 import save_data, load_data


if os.path.exists("w2v.data"):
    data = load_data("w2v.data")
    vocab_weights, vocab = data["vocab_weights"], data["vocab"]
else:
    w2v = KeyedVectors.load_word2vec_format("/home/resources/nlp100/GoogleNews-vectors-negative300.bin.gz", binary=True)
    vocab_weights = w2v.wv.syn0
    vocab = w2v.wv.index2word
    save_data("w2v.data", {"vocab_weights": vocab_weights, "vocab": vocab})

# <UNK> と <PAD> を追加する
ave_vec = sum(vocab_weights) / len(vocab_weights)
vocab_weights = np.append(vocab_weights, [ave_vec, ave_vec], axis=0)
vocab = np.append(vocab, ["<UNK>", "<PAD>"])
unk_id = np.where(vocab == "<UNK>")[0][0]
pad_id = np.where(vocab == "<PAD>")[0][0]


def word_to_index(word):
    if word in vocab:
        np.where(vocab == word)[0][0]
    else:
        unk_id

def load_corpus():
    """ CSVからデータを読んで保存する
    """

    columns = [
            "id",
            "title",
            "url",
            "publisher",
            "category",
            "story",
            "hostname",
            "timestamp",
            ]
    df = pd.read_table("../ch06/newsCorpora.csv", names=columns, quoting=csv.QUOTE_NONE)
    df = df.sample(frac=1)
    df = df[df["category"].isin(["b", "t", "e", "h"])]
    df = df[["title", "category"]]
    breakpoint()

    df["category"] = df["category"].map(lambda x: category_to_label(x))
    df["feature"] = df["title"].map(lambda x: [word_to_index(word) for word in x.split(" ")])

    breakpoint()
    train, valid = train_test_split(df, test_size=0.2, stratify=df["label"])
    valid, test = train_test_split(valid, test_size=0.5, stratify=valid["label"])
    train = train.reset_index(drop=True)
    valid = valid.reset_index(drop=True)
    test = test.reset_index(drop=True)
    train_feature, train_label = torch.Tensor(train["feature"]), torch.Tensor(train["label"])
    valid_feature, valid_label = torch.Tensor(valid["feature"]), torch.Tensor(valid["label"])
    test_feature, test_label = torch.Tensor(test["feature"]), torch.Tensor(test["label"])

    train_feature, valid_feature, test_feature = pad_sequence([train_feature, valid_feature, test_feature], padding_valid=pad_id)

    save_data("train2.data", {"feature": torch.Tensor(train["feature"]), "label": torch.Tensor(train["label"])})
    save_data("valid2.data", {"feature": torch.Tensor(valid["feature"]), "label": torch.Tensor(valid["label"])})
    save_data("test2.data", {"feature": torch.Tensor(test["feature"]), "label": torch.Tensor(test["label"])})


class BiLSTM(nn.Module):
    """ BiLSTM
        https://lionbridge.ai/ja/articles/deep-learning-multiclass-text-classification/
    """

    def __init__(self, out_features, hidden_size=64, dropout=0.1):
        super().__init__()
        self.hidden_size = hidden_size
        self.dropout = dropout

        # Embedding層の重みは単語ベクトル
        self.embedding = nn.Embedding.from_pretrained(vocab_weights)
        self.lstm = nn.LSTM(vocab_weights.shape[1], self.hidden_size, bidirectional=True, batch_first=True)
        self.linear = nn.Linear(self.hidden_size*4 , self.hidden_size)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(self.dropout)
        self.out = nn.Linear(self.hidden_size, out_features)

    def forward(self, x):
        h_embedding = self.embedding(x)
        h_lstm, _ = self.lstm(h_embedding)
        avg_pool = torch.mean(h_lstm, 1)
        max_pool, _ = torch.max(h_lstm, 1)
        conc = torch.cat((avg_pool, max_pool), 1)
        conc = self.relu(self.linear(conc))
        conc = self.dropout(conc)
        out = self.out(conc)
        return out


if __name__ == "__main__":
    import torch
    from torch import nn
    from q73 import load_dataloader
    from q75 import train_model

    n_epochs = 6
    batch_size = 512

    load_corpus()
    train_loader = load_dataloader("train2.data", batch_size=batch_size)
    valid_loader = load_dataloader("valid2.data", batch_size=batch_size)

    model = BiLSTM()
    loss_fn = nn.CrossEntropyLoss(reduction="sum")
    optimizer = torch.optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), lr=0.001)
    model.cuda()

    train_loss = []
    valid_loss = []
    for epoch in range(n_epochs):
        # 訓練モード
        model.train()
        avg_loss = 0.
        for i, (x_batch, y_batch) in enumerate(train_loader):
            y_pred = model(x_batch)
            loss = loss_fn(y_pred, y_batch)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            avg_loss += loss.item() / len(train_loader)

        # 評価モード
        model.eval()
        avg_val_loss = 0.
        val_preds = np.zeros((len(x_cv), 4))
        for i, (x_batch, y_batch) in enumerate(valid_loader):
            y_pred = model(x_batch).detach()
            avg_val_loss += loss_fn(y_pred, y_batch).item() / len(valid_loader)
            val_preds[i * batch_size:(i+1) * batch_size] = F.softmax(y_pred).cpu().numpy()

        val_accuracy = sum(val_preds.argmax(axis=1)==test_y)/len(test_y)
        train_loss.append(avg_loss)
        valid_loss.append(avg_val_loss)
        print('Epoch {}/{} \t loss={:.4f} \t val_loss={:.4f} \t val_acc={:.4f}'.format(
                epoch + 1, n_epochs, avg_loss, avg_val_loss, val_accuracy))
