def find_kaku_kou(chunk, sentence):
    """文節中の格と項をすべて見つけて返す

        Args:
            chunk (Chunk): 文節
            sentence (list): chunkを含む文節のリスト

        Returns:
            list: [格のリスト, 項のリスト] の形で、文節中の格と項を格の辞書順にソートしたもの
    """

    kaku_kou_list = []
    for src_id in chunk.srcs:
        src_chunk = sentence[src_id]
        for morph in src_chunk.morphs:
            # 述語(chunk)に係る助詞を格とする
            if morph.pos == "助詞":
                kaku_kou_list.append({"kaku": morph.surface, "kou": src_chunk.text})

    # 格基準で辞書順に並べる
    kaku_kou_list = sorted(kaku_kou_list, key=lambda x:x["kaku"])
    kaku = [pairs["kaku"] for pairs in kaku_kou_list]
    kou = [pairs["kou"] for pairs in kaku_kou_list]
    return [kaku, kou]


if __name__ == "__main__":
    from q41 import Chunk, read_child_elements
    from q45 import find_jutsugo
    import xml.etree.ElementTree as ET

    # CaboChaの出力には根となる要素がないので、無理矢理作ってElementTreeでパースできるようにする
    with open("ai.ja.txt.parsed") as f:
        root = ET.fromstringlist("<root>" + f.read() + "</root>")

    document = filter(lambda x:len(x) != 0, read_child_elements(root))
    for i, sentence in enumerate(document):
        for chunk in sentence:
            jutsugo = find_jutsugo(chunk)
            # 動詞を含む文節のときの処理
            if jutsugo:
                kaku_list, kou_list = find_kaku_kou(chunk, sentence)
                if len(kaku_list) != 0:
                    kaku = " ".join(kaku_list)
                    kou = " ".join(kou_list)
                    print("{}\t{}\t{}".format(jutsugo, kaku, kou))
