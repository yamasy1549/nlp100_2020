def country_vec(w2v):
    """国名とベクトルのリストをつくる

    Args:
        w2v (Word2VecKeyedVectors): w2v

    Returns:
        list: [国名のリスト, ベクトルのリスト]
    """

    vocab = w2v.vocab.keys()

    # https://raw.githubusercontent.com/umpirsky/country-list/master/data/en/country.csv
    with open("country.txt") as f:
        all_country_list = [line.strip() for line in f]

    country_list = []
    vec_list = []

    for country in all_country_list:
        if country in vocab:
            country_list.append(country)
            vec_list.append(w2v.word_vec(country))

    return [country_list, vec_list]


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from gensim.models import KeyedVectors
    from sklearn.cluster import KMeans
    from sklearn.decomposition import PCA


    w2v = KeyedVectors.load_word2vec_format("/home/resources/nlp100/GoogleNews-vectors-negative300.bin.gz", binary=True)
    country_list, X = country_vec(w2v)

    # Kmeans
    kmeans = KMeans(n_clusters=5)
    cluster_numbers = kmeans.fit_predict(X)

    # PCA
    pca = PCA(n_components=2)
    features = pca.fit_transform(X)
    features = list(zip(*features))

    # 描画
    color_list = ["r", "g", "b", "c", "m"]
    color = [color_list[n] for n in cluster_numbers]
    plt.figure(figsize=(10, 10))
    for x, y, label in zip(*features, country_list):
        plt.text(x, y, label, size=10)
    plt.scatter(*features, alpha=0.8, color=color)
    plt.savefig("../output/sy67.svg")
