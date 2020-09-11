def path_to_root():
    def _path_to_root(self, chunk_list):
        """文節から構文木の根に至るパスを抽出する

            Args:
                chunk_list (list): chunkを含む文節のリスト

            Returns:
                list: chunkから構文木の根までの文節のリスト
        """

        path = [self]
        dst = self.dst
        if dst == -1:
            return path
        else:
            path += chunk_list[dst].path_to_root(chunk_list)
            return path

    from q41 import Chunk
    # インスタンスメソッドを追加する
    Chunk.path_to_root = _path_to_root

def path_text(chunk_list):
    return [chunk.text() for chunk in chunk_list]


if __name__ == "__main__":
    from q40 import read_cabocha_xmlfile
    from q41 import read_child_elements
    from q42 import exclude_marks

    exclude_marks()
    path_to_root()

    document = read_cabocha_xmlfile("ai.ja.txt.parsed", read_child_elements)
    document = filter(lambda x:len(x) != 0, document)

    for sentence in document:
        for chunk in sentence:
            if not chunk.include_pos("名詞"):
                continue
            # 名詞を含む文節の場合
            path = chunk.path_to_root(sentence)
            if len(path) > 1:
                output = path_text(path)
                print(" -> ".join(output))
