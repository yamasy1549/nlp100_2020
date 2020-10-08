from gensim.models import KeyedVectors


w2v = KeyedVectors.load_word2vec_format("/home/resources/GoogleNews-vectors-negative300.bin.gz", binary=True)
top_scores = w2v.most_similar(positive=["Spain", "Athens"], negative=["Madrid"], topn=10)
for word, sim in top_scores:
    print(word, sim)
