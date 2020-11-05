def filter_meishi(morphs):
    """名詞だけをフィルタにかける

        Args:
            morphs (list): Morphのリスト

        Returns:
            list: posが名詞であるMorphのリスト
    """

    return list(filter(lambda x:x.pos == "名詞", morphs))

def merge_meishi_ku(morphs):
    """連続する名詞を1つのMorphにまとめる

        Args:
            morphs (list): Morphのリスト

        Returns:
            list: morphs内で連続する名詞を1つの名詞にまとめた後のMorphのリスト
    """

    merged_morphs = []

    for morph in morphs:
        # 一番目のmorphはmerged_morphsに入れておく
        if len(merged_morphs) == 0:
            merged_morphs.append(morph)
            continue

        if merged_morphs[-1].pos == "名詞" and morph.pos == "名詞":
            # 名詞->名詞
            merged_morphs[-1].surface += morph.surface
            merged_morphs[-1].base += morph.base
        else:
            # 名詞->名詞以外 or 名詞以外->名詞 or 名詞以外->名詞以外
            merged_morphs.append(morph)
    return merged_morphs

def print_path(i, j=None, k=None):
    """パスを出力する

        Args:
            i (list): 文節iから始まるChunkのリスト
            j (list): 文節jから始まるChunkのリスト
            k (Chunk): 文節k
    """

    if j and k:
        # Case2
        i_output = path_text(i)
        j_output = path_text(j)
        k_output = path_text([k])[0]
        output = [
            " -> ".join(i_output),
            " -> ".join(j_output),
            k_output
        ]
        if len(output) > 1:
            print(" | ".join(output))
    else:
        # Case1
        output = path_text(i)
        if len(output) > 1:
            print(" -> ".join(output))


if __name__ == "__main__":
    from q40 import read_cabocha_xmlfile
    from q41 import read_child_elements
    from q48 import path_to_root, path_text

    path_to_root()
    document = read_cabocha_xmlfile("ai.ja.txt.parsed", read_child_elements, pos=["記号"])
    document = filter(lambda x:len(x) != 0, document)

    for sentence in document:
        # 文節内で連続して出現する名詞たちを、名詞句として1つの形態素にまとめる
        for chunk in sentence:
            chunk.morphs = merge_meishi_ku(chunk.morphs)

        # 最短係り受けパスを抽出する
        for i, i_chunk in enumerate(sentence):
            i_path = i_chunk.path_to_root(sentence)
            for j, j_chunk in enumerate(sentence[i+1:]):
                j_path = j_chunk.path_to_root(sentence)

                i_meishi_list = filter_meishi(i_chunk.morphs)
                j_meishi_list = filter_meishi(j_chunk.morphs)
                if not i_meishi_list or not j_meishi_list:
                    continue

                # 名詞句をXとYに置き換える
                i_meishi_tmp = i_meishi_list[0].surface
                j_meishi_tmp = j_meishi_list[0].surface
                i_meishi_list[0].surface = "X"
                j_meishi_list[0].surface = "Y"

                if j_chunk in i_path:
                    # Case1: 文節iから構文木の根に至る経路上に文節jが存在する場合
                    # - 文節iから文節jのパス

                    index = i_path.index(j_chunk)
                    print_path(i=i_path[:index+1])
                else:
                    # Case2: 文節iと文節jから構文木の根に至る経路上で共通の文節kで交わる場合
                    # - 文節iから文節kに至る直前のパス
                    # - 文節jから文節kに至る直前までのパス
                    # - 文節kの内容

                    # setでは順序が保証されないのでi_path準拠で並び替えている
                    k = sorted(set(i_path) & set(j_path), key=i_path.index)[0]
                    i_index = i_path.index(k)
                    j_index = j_path.index(k)
                    print_path(i=i_path[:i_index], j=j_path[:j_index], k=k)

                # 置き換えていたのを戻す
                i_meishi_list[0].surface = i_meishi_tmp
                j_meishi_list[0].surface = j_meishi_tmp
