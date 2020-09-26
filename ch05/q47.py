def is_sahen(morph):
    return morph.pos == "名詞" and morph.pos1 == "サ変接続"

def is_wo(morph):
    return morph.surface == "を" and morph.pos == "助詞"

def is_sahen_wo(kaku_kou):
    morphs = kaku_kou["chunk"].morphs
    if len(morphs) < 2:
        return False
    # サ変接続名詞+をで構成されるかどうかチェックする
    morph1, morph2 = morphs[0:2]
    return is_sahen(morph1) and is_wo(morph2)


if __name__ == "__main__":
    from q40 import read_cabocha_xmlfile
    from q41 import read_child_elements
    from q45 import find_jutsugo
    from q46 import find_kaku_kou, sort_by_kaku

    document = read_cabocha_xmlfile("ai.ja.txt.parsed", read_child_elements, pos=["記号"])
    document = filter(lambda x:len(x) != 0, document)

    for sentence in document:
        for chunk in sentence:
            jutsugo_suffix = find_jutsugo(chunk)
            kaku_kou_result = find_kaku_kou(chunk, sentence)
            if not jutsugo_suffix or not kaku_kou_result:
                continue
            # 動詞に最も近い位置で係っている項がjutsugo_prefix
            *kaku_kou_list, jutsugo_prefix = kaku_kou_result
            if not kaku_kou_list or not is_sahen_wo(jutsugo_prefix):
                continue
            kaku_list, kou_list = sort_by_kaku(kaku_kou_list)
            if len(kaku_list) != 0:
                jutsugo = jutsugo_prefix["kou"] + jutsugo_suffix
                kaku = " ".join(kaku_list)
                kou = " ".join(kou_list)
                print("{}\t{}\t{}".format(jutsugo, kaku, kou))
