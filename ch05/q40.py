import xml.etree.ElementTree as ET

class Morph:
    def __init__(self, morph_id, surface, base, pos, pos1):
        """形態素を表すクラス

        Args:
            id (int): 形態素ID
            surface (str): 表層形
            base (str): 基本形
            pos (str): 品詞
            pos1 (str): 品詞細分類1
        """

        self.morph_id = morph_id
        self.surface = surface
        self.base = base
        self.pos = pos
        self.pos1 = pos1


if __name__ == "__main__":
    def read_child_elements(parent):
        """与えられたXML要素の子要素の<tok>をMorphオブジェクトで表現し、文と文節ごとにリストを作る

        Args:
            parent (xml.etree.ElementTree.Element): XMLの親要素

        Returns:
            list: parentの子要素を再帰的にMorphのリストにしたもの
        """

        document = []

        for child in parent:
            if child.tag == "tok":
                # tokならMorphにする
                feature = child.attrib["feature"].split(",")
                morph = Morph(morph_id=int(child.attrib["id"]), surface=child.text, base=feature[6], pos=feature[0], pos1=feature[1])
                document.append(morph)
            else:
                # 子要素を再帰的に見ていく
                child_document = read_child_elements(child)
                document.append(child_document)

        return document

    # cabocha -f3 ai.ja.txt > ai.ja.txt.parsed
    # CaboChaの出力には根となる要素がないので、無理矢理作ってElementTreeでパースできるようにする
    with open("ai.ja.txt.parsed") as f:
        root = ET.fromstringlist("<root>" + f.read() + "</root>")

    document = read_child_elements(root)
    for sentence in document:
        for chunk in sentence:
            for morph in chunk:
                print("surface:{}\tbase:{}\tpos:{}\tpos1:{}".format(morph.surface, morph.base, morph.pos, morph.pos1))
