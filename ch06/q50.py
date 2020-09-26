import pandas as pd
from sklearn.model_selection import train_test_split

if __name__ == "__main__":
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
    df = pd.read_table("newsCorpora.csv", names=columns)
    df = df.sample(frac=1)
    df = df[df["publisher"].isin(["Reuters", "Huffington Post", "Businessweek", "Contactmusic.com", "Daily Mail"])]
    df = df[["category", "title"]]

    train, val = train_test_split(df, test_size=0.2)
    val, test = train_test_split(val, test_size=0.5)

    train.to_csv("train.txt", sep="\t", index=False, header=None)
    val.to_csv("val.txt", sep="\t", index=False, header=None)
    test.to_csv("test.txt", sep="\t", index=False, header=None)
