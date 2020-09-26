from q45 import is_joshi

def sort_by_kaku(kaku_kou_list):
    """格と項のリストを格で辞書順にソートする

        Args:
            kaku_kou_list (list): {"kaku: 格, "kou": 項}のリスト

        Returns:
            list: [格のリスト, 項のリスト]
    """

    # 格基準で辞書順に並べる
    kaku_kou_list = sorted(kaku_kou_list, key=lambda x:x["kaku"])
    kaku = [pairs["kaku"] for pairs in kaku_kou_list]
    kou = [pairs["kou"] for pairs in kaku_kou_list]
    return [kaku, kou]

def find_kaku_kou(chunk, sentence):
    """文節中の格と項をすべて見つけて返す

        Args:
            chunk (Chunk): 文節
            sentence (list): chunkを含む文節のリスト

        Returns:
            list: {"kaku: 格, "kou": 項, "chunk": 文節}のリスト
    """

    kaku_kou_list = []
    for src_id in chunk.srcs:
        src_chunk = sentence[src_id]
        for morph in src_chunk.morphs:
            # 述語(chunk)に係る助詞を格とする
            if is_joshi(morph):
                kaku_kou_list.append({"kaku": morph.surface, "kou": src_chunk.text(), "chunk": src_chunk})

    return kaku_kou_list


if __name__ == "__main__":
    from q40 import read_cabocha_xmlfile
    from q41 import Chunk, read_child_elements
    from q45 import find_jutsugo

    document = read_cabocha_xmlfile("ai.ja.txt.parsed", read_child_elements, pos=["記号"])
    document = filter(lambda x:len(x) != 0, document)

    for sentence in document:
        for chunk in sentence:
            jutsugo = find_jutsugo(chunk)
            if not jutsugo:
                continue
            # chunkが述語のときの処理
            kaku_kou_list = find_kaku_kou(chunk, sentence)
            kaku_list, kou_list = sort_by_kaku(kaku_kou_list)
            if len(kaku_list) != 0:
                kaku = " ".join(kaku_list)
                kou = " ".join(kou_list)
                print("{}\t{}\t{}".format(jutsugo, kaku, kou))
