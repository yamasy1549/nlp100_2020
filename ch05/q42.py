def exclude_marks():
    def _exclude_marks(self):
        """morphsからsurfaceの連接（表示用）を作る際、記号を除外する

            Returns:
                str: 記号を除いて、morphs内のMorphのsurfaceを連接したもの
        """

        filtered_morphs = filter(lambda x: x.pos != "記号", self.morphs)
        return "".join(map(lambda x: x.surface, filtered_morphs))

    from q41 import Chunk
    # 記号を除くように、インスタンスメソッドを書き換える
    Chunk.to_text = _exclude_marks


if __name__ == "__main__":
    from q40 import read_cabocha_xmlfile
    from q41 import read_child_elements

    exclude_marks()
    document = read_cabocha_xmlfile("ai.ja.txt.parsed", read_child_elements)

    for sentence in document:
        for chunk in sentence:
            for src_id in chunk.srcs:
                src_chunk = sentence[src_id]
                print("{}{}\t{}{}".format(src_chunk.chunk_id, src_chunk.text(), chunk.chunk_id, chunk.text()))
