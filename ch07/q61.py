from gensim.models import KeyedVectors


w2v = KeyedVectors.load_word2vec_format("/home/resources/GoogleNews-vectors-negative300.bin.gz", binary=True)
vec1 = w2v.word_vec("United_States")
vec2 = w2v.word_vec("U.S.")
sim = w2v.cosine_similarities(vec1, vectors_all=[vec2])
print(sim)
