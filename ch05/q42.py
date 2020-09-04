def exclude_marks(self):
    """morphsからsurfaceの連接（表示用）を作る際、記号を除外する

        Returns:
            str: 記号を除いて、morphs内のMorphのsurfaceを連接したもの
    """

    filtered_morphs = filter(lambda x: x.pos != "記号", self.morphs)
    return "".join(map(lambda x: x.surface, filtered_morphs))


if __name__ == "__main__":
    from q41 import Chunk, read_child_elements
    import xml.etree.ElementTree as ET

    # CaboChaの出力には根となる要素がないので、無理矢理作ってElementTreeでパースできるようにする
    with open("ai.ja.txt.parsed") as f:
        root = ET.fromstringlist("<root>" + f.read() + "</root>")

    # 記号を除くように、インスタンスメソッドを書き換える
    Chunk.to_text = exclude_marks

    document = read_child_elements(root)
    for sentence in document:
        for chunk in sentence:
            for src_id in chunk.srcs:
                src_chunk = sentence[src_id]
                print("{}{}\t{}{}".format(src_chunk.chunk_id, src_chunk.text, chunk.chunk_id, chunk.text))
