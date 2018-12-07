import MeCab
import unittest
import emoji

class MyMeCab:
    mecab = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')

    @classmethod
    def parse(cls, text):
        return [Morpheme(line) for line in cls.mecab.parse(text).split("\n") if not line == "EOS" and line]

class Morpheme:
    def __init__(self, morpheme_line):
        morphemes = morpheme_line.split("\t")
        feature = morphemes[1].split(",")
        self.surface = morphemes[0]
        self.pos = feature[0]
        self.pos_data = feature[1]
        if feature[6] == '*' or self.surface in emoji.UNICODE_EMOJI: # 絵文字処理
            self.infinitve = morphemes[0]
        else:
            self.infinitve = feature[6]

    def __str__(self):
        return '{} {} {} {}'.format(self.surface, self.infinitve, self.pos, self.pos_data)

class MeCabTest(unittest.TestCase):
    def test_mecab(self):
        m = MyMeCab.parse('BABY-G さんの撮影をした時のです⌚️💗')
        for _m in m:
            print(_m)

if __name__ == '__main__':
    unittest.main()