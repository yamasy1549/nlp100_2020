if __name__ == "__main__":
    from q40 import read_cabocha_xmlfile
    from q41 import read_child_elements

    document = read_cabocha_xmlfile("ai.ja.txt.parsed", read_child_elements, pos=["記号"])

    for sentence in document:
        for chunk in sentence:
            for src_id in chunk.srcs:
                src_chunk = sentence[src_id]
                print("{}{}\t{}{}".format(src_chunk.chunk_id, src_chunk.text(), chunk.chunk_id, chunk.text()))
