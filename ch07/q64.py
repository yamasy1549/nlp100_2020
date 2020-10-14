import csv
from gensim.models import KeyedVectors


def read_csv(filename):
    """CSVを読み込む

    Args:
        filename (str): ファイル名

    Returns:
        dict: カテゴリごとに単語のリストをまとめたもの
    """

    data = {}

    with open(filename) as f:
        for line in f:
            if line[0] == ":":
                category = line.strip(": \n")
                data[category] = []
            else:
                words = line.strip().split(" ")
                data[category].append(words)

    return data


if __name__ == "__main__":
    w2v = KeyedVectors.load_word2vec_format("/home/resources/nlp100/GoogleNews-vectors-negative300.bin.gz", binary=True)
    data = read_csv("/home/resources/nlp100/questions-words.txt")

    for category, entries in data.items():
        print(f": {category}")
        for words in entries:
            positive = [words[1], words[2]]
            negative = [words[0]]
            word, score = w2v.most_similar(positive=positive, negative=negative, topn=1)[0]
            output = [
                    *words,
                    word,
                    str(score),
                    ]
            print(" ".join(output))
