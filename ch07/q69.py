import numpy as np
from scipy.cluster.hierarchy import dendrogram


def plot_dendrogram(model, **kwargs):
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

    dendrogram(linkage_matrix, **kwargs)


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from gensim.models import KeyedVectors
    from sklearn.manifold import TSNE
    from q67 import country_vec


    w2v = KeyedVectors.load_word2vec_format("/home/resources/nlp100/GoogleNews-vectors-negative300.bin.gz", binary=True)
    country_list, X = country_vec(w2v)

    # t-SNE
    model = TSNE(n_components=2)
    features = model.fit_transform(X)
    features = list(zip(*features))

    # 描画
    plt.figure(figsize=(10, 10))
    for x, y, label in zip(*features, country_list):
        plt.text(x, y, label, size=10)
    plt.scatter(*features, alpha=0.8)
    plt.savefig("../output/sy69.png")
