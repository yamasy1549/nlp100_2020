from q40 import Morph
import xml.etree.ElementTree as ET

class Chunk:
    def __init__(self, chunk_id, morphs, dst, srcs):
        """文節を表すクラス

        Args:
            chunk_id (int): 文節ID
            morphs (list): 形態素のリスト
            dst (int): 係り先文節インデックス番号
            srcs (list): 係り元文節インデックス番号
        """

        self.chunk_id = chunk_id
        self.morphs = morphs
        self.dst = dst
        self.srcs = srcs
        self.text = self.to_text

    def to_text(self):
        """morphsからsurfaceの連接（表示用）を作る

        Returns:
            str: morphs内のMorphのsurfaceを連接したもの
        """

        return "".join(map(lambda x: x.surface, self.morphs))

    def include_pos(self, target_pos):
        """指定したposを含むかどうか判定する

            Args:
                target_pos (str, list): 品詞名

            Returns:
                bool: 指定した品詞を含むならTrue
        """

        # 複数の品詞をORでチェックできるようにする
        if type(target_pos) is str:
            target_pos = [target_pos]

        pos_list = map(lambda x: x.pos, self.morphs)
        for pos in target_pos:
            if pos in pos_list:
                return True

        return False


def read_child_elements(parent):
    """与えられたXML要素の子要素の<tok>をMorphオブジェクトで、<chunk>をChunkオブジェクトで表現し、文ごとにリストを作る

    Args:
        parent (xml.etree.ElementTree.Element): XMLの親要素

    Returns:
        list: parentの子要素を再帰的にChunkのリストにしたもの
    """

    document = []

    for child in parent:
        if child.tag == "tok":
            # tokならMorphにする
            feature = child.attrib["feature"].split(",")
            morph = Morph(morph_id=int(child.attrib["id"]), surface=child.text, base=feature[6], pos=feature[0], pos1=feature[1])
            document.append(morph)

        elif child.tag == "chunk":
            # 子要素を再帰的に見ていく
            child_document = read_child_elements(child)
            # chunkならChunkにする
            chunk = Chunk(chunk_id=int(child.attrib["id"]),
                          morphs=child_document,
                          dst=int(child.attrib["link"]),
                          srcs=[])
            document.append(chunk)

        elif child.tag == "sentence":
            # 子要素を再帰的に見ていく
            child_document = read_child_elements(child)
            # srcsを埋める
            for chunk in child_document:
                if chunk.dst != -1:
                    child_document[chunk.dst].srcs.append(chunk.chunk_id)
            document.append(child_document)

    return document


if __name__ == "__main__":
    from q40 import read_cabocha_xmlfile

    document = read_cabocha_xmlfile("ai.ja.txt.parsed", read_child_elements)

    for sentence in document:
        for chunk in sentence:
            print("{}{}\tdst:{}\tsrcs:{}".format(chunk.chunk_id, chunk.text(), chunk.dst, chunk.srcs))
