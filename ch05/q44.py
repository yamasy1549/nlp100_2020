if __name__ == "__main__":
    from q41 import Chunk, read_child_elements
    from q42 import exclude_marks
    from graphviz import Digraph
    import xml.etree.ElementTree as ET

    # CaboChaの出力には根となる要素がないので、無理矢理作ってElementTreeでパースできるようにする
    with open("ai.ja.txt.parsed") as f:
        root = ET.fromstringlist("<root>" + f.read() + "</root>")

    # 記号を除くように、インスタンスメソッドを書き換える
    Chunk.to_text = exclude_marks

    document = filter(lambda x:len(x) != 0, read_child_elements(root))
    for i, sentence in enumerate(document):
        if len(sentence) == 0:
            continue
        graph = Digraph(format="png")

        for chunk in sentence:
            graph.node(str(chunk.chunk_id), chunk.text)
            for src_id in chunk.srcs:
                src_chunk = sentence[src_id]
                graph.edge(str(src_chunk.chunk_id), str(chunk.chunk_id))

        graph.render("../output/{}".format(i))
