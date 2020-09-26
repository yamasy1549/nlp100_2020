if __name__ == "__main__":
    import os
    from q40 import read_cabocha_xmlfile
    from q41 import Chunk, read_child_elements
    from graphviz import Digraph

    document = read_cabocha_xmlfile("ai.ja.txt.parsed", read_child_elements, pos=["記号"])
    document = filter(lambda x:len(x) != 0, document)

    for i, sentence in enumerate(document):
        graph = Digraph(format="png")

        for chunk in sentence:
            graph.node(str(chunk.chunk_id), chunk.text())
            for src_id in chunk.srcs:
                src_chunk = sentence[src_id]
                graph.edge(str(src_chunk.chunk_id), str(chunk.chunk_id))

        graph.render("../output/sy44/{}".format(i))
        os.remove("../output/sy44/{}".format(i))
