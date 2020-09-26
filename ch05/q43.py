if __name__ == "__main__":
    from q40 import read_cabocha_xmlfile
    from q41 import Chunk, read_child_elements

    document = read_cabocha_xmlfile("ai.ja.txt.parsed", read_child_elements, pos=["記号"])

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
                print("{}{}\t{}{}".format(src_chunk.chunk_id, src_chunk.text(), chunk.chunk_id, chunk.text()))
