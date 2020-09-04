def include_pos(self, target_pos):
    """指定したposを含むかどうか判定する

        Args:
            target_pos (str, list): 品詞名

        Returns:
            bool: 指定した品詞を含むならTrue
    """

    # 複数の品詞をORでチェックできるようにする
    if type(target_pos) is str:
        target_pos = [target_pos]

    pos_list = map(lambda x: x.pos, self.morphs)
    for pos in target_pos:
        if pos in pos_list:
            return True

    return False

if __name__ == "__main__":
    from q41 import Chunk, read_child_elements
    from q42 import exclude_marks
    import xml.etree.ElementTree as ET

    # CaboChaの出力には根となる要素がないので、無理矢理作ってElementTreeでパースできるようにする
    with open("ai.ja.txt.parsed") as f:
        root = ET.fromstringlist("<root>" + f.read() + "</root>")

    # 記号を除くように、インスタンスメソッドを書き換える
    Chunk.to_text = exclude_marks
    # インスタンスメソッドを追加する
    Chunk.include_pos = include_pos

    document = read_child_elements(root)
    for sentence in document:
        for chunk in sentence:
            # 係り先が動詞を含まないときは何もしない
            if not chunk.include_pos("動詞"):
                continue
            for src_id in chunk.srcs:
                src_chunk = sentence[src_id]
                # 係り元が名詞を含まないときは何もしない
                if not src_chunk.include_pos("名詞"):
                    continue
                print("{}{}\t{}{}".format(src_chunk.chunk_id, src_chunk.text, chunk.chunk_id, chunk.text))
