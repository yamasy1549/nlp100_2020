if __name__ == "__main__":
    import pandas as pd
    from gensim.models import KeyedVectors


    w2v = KeyedVectors.load_word2vec_format("/home/resources/nlp100/GoogleNews-vectors-negative300.bin.gz", binary=True)

    df = pd.read_csv("wordsim353/combined.csv")
    df["word_vec"] = 0.0

    for i, row in df.iterrows():
        vec1 = w2v.word_vec(row["Word 1"])
        vec2 = w2v.word_vec(row["Word 2"])
        df.loc[i, "word_vec"] = w2v.cosine_similarities(vec1, vectors_all=[vec2])[0]

    spearman_r = df[["word_vec", "Human (mean)"]].corr(method="spearman")
    print(spearman_r)
