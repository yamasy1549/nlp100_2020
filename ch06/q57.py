if __name__ == "__main__":
    from q51 import load

    model = load("model.dat")
    vectorizer = load("vectorizer.dat")
    model.coef_
    import pdb; pdb.set_trace()
