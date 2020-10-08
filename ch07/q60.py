from gensim.models import KeyedVectors


w2v = KeyedVectors.load_word2vec_format("/home/resources/GoogleNews-vectors-negative300.bin.gz", binary=True)
vec = w2v.word_vec("United_States")
print(vec)
