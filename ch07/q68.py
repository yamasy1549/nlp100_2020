import numpy as np
from scipy.cluster.hierarchy import dendrogram


def plot_dendrogram(model, labels, **kwargs):
    """デンドログラムを描く
       https://scikit-learn.org/stable/auto_examples/cluster/plot_agglomerative_dendrogram.html

    Args:
        model (sklearn.cluster.AgglomerativeClustering): モデル
    """

    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)

    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack([model.children_, model.distances_, counts]).astype(float)

    dendrogram(linkage_matrix, labels=labels, **kwargs)


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from gensim.models import KeyedVectors
    from sklearn.cluster import AgglomerativeClustering
    from q67 import country_vec


    w2v = KeyedVectors.load_word2vec_format("/home/resources/nlp100/GoogleNews-vectors-negative300.bin.gz", binary=True)
    country_list, X = country_vec(w2v)

    # Ward
    model = AgglomerativeClustering(affinity="euclidean", linkage="ward", distance_threshold=0, n_clusters=None)
    model = model.fit(X)

    # 描画
    plt.figure(figsize=(20, 10))
    plot_dendrogram(model, labels=country_list)
    plt.savefig("../output/sy68.png")
