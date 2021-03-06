def is_doushi(morph):
    return morph.pos == "動詞"

def is_joshi(morph):
    return morph.pos == "助詞"

def find_jutsugo(chunk):
    """文節中の述語を見つけて返す

        Args:
            chunk (Chunk): 文節

        Returns:
            str: 文節の述語、なければ空文字
    """

    # 動詞を含むかどうかチェックする
    jutsugo_list = list(filter(lambda x: is_doushi(x), chunk.morphs))
    if len(jutsugo_list) == 0:
        return ""
    # 文節の最左の動詞の基本形を述語とする
    return jutsugo_list[0].base

def find_kaku(chunk, sentence):
    """文節中の格をすべて見つけて返す

        Args:
            chunk (Chunk): 文節
            sentence (list): chunkを含む文節のリスト

        Returns:
            list: 文節中の格を辞書順にソートしたもの
    """

    kaku_list = []
    for src_id in chunk.srcs:
        src_chunk = sentence[src_id]
        for morph in src_chunk.morphs:
            # 述語(chunk)に係る助詞を格とする
            if is_joshi(morph):
                kaku_list.append(morph.surface)

    # 辞書順に並べる
    return sorted(kaku_list)


if __name__ == "__main__":
    from q40 import read_cabocha_xmlfile
    from q41 import read_child_elements

    document = read_cabocha_xmlfile("ai.ja.txt.parsed", read_child_elements, pos=["記号"])
    document = filter(lambda x:len(x) != 0, document)

    for i, sentence in enumerate(document):
        for chunk in sentence:
            jutsugo = find_jutsugo(chunk)
            if not jutsugo:
                continue
            # chunkが述語のときの処理
            kaku_list = find_kaku(chunk, sentence)
            if len(kaku_list) != 0:
                kaku = " ".join(kaku_list)
                print("{}\t{}".format(jutsugo, kaku))
