def filter_meishi(morphs):
    return list(filter(lambda x:x.pos == "名詞", morphs))

def path_text(chunk_list):
    return [chunk.text() for chunk in chunk_list]

if __name__ == "__main__":
    from q40 import read_cabocha_xmlfile
    from q41 import read_child_elements
    from q48 import path_to_root

    path_to_root()
    document = read_cabocha_xmlfile("ai.ja.txt.parsed", read_child_elements, pos=["記号"])
    document = filter(lambda x:len(x) != 0, document)

    for sentence in document:
        for i, i_chunk in enumerate(sentence):
            i_path = i_chunk.path_to_root(sentence)
            for j, j_chunk in enumerate(sentence[i+1:]):
                j_path = j_chunk.path_to_root(sentence)

                i_meishi_list = filter_meishi(i_chunk.morphs)
                j_meishi_list = filter_meishi(j_chunk.morphs)
                if not i_meishi_list or not j_meishi_list:
                    continue

                # XとYに置き換える
                # TODO: 名詞"句"を置き換える
                i_meishi_tmp = i_meishi_list[0].surface
                j_meishi_tmp = j_meishi_list[0].surface
                i_meishi_list[0].surface = "X"
                j_meishi_list[0].surface = "Y"

                if j_chunk in i_path:
                    # 文節iから構文木の根に至る経路上に文節jが存在する場合
                    # - 文節iから文節jのパス

                    index = i_path.index(j_chunk)
                    output = path_text(i_path[:index+1])
                    if len(output) > 1:
                        print(" -> ".join(output))
                else:
                    # 文節iと文節jから構文木の根に至る経路上で共通の文節kで交わる場合
                    # - 文節iから文節kに至る直前のパス
                    # - 文節jから文節kに至る直前までのパス
                    # - 文節kの内容

                    # setでは順序が保証されないのでi_path準拠で並び替えている
                    k = sorted(set(i_path) & set(j_path), key=i_path.index)[0]
                    i_index = i_path.index(k)
                    j_index = j_path.index(k)
                    i_output = path_text(i_path[:i_index])
                    j_output = path_text(j_path[:j_index])
                    k_output = path_text([k])[0]
                    output = [
                        " -> ".join(i_output),
                        " -> ".join(j_output),
                        k_output
                    ]
                    if len(output) > 1:
                        print(" | ".join(output))

                # 置き換えていたのを戻す
                i_meishi_list[0].surface = i_meishi_tmp
                j_meishi_list[0].surface = j_meishi_tmp
