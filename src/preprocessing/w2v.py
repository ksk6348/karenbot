# -*- coding: utf-8 -*-
from gensim.models import word2vec
import warnings

warnings.filterwarnings('ignore')

JANOME_WAKATI_PATH = '../../res/post_wakati.janome.txt'
JANOME_MODEL_PATH = '../../res/w2v_model.janome.model'

MECAB_WAKATI_PATH = '../../res/post_wakati.mecab.txt'
MECAB_MODEL_PATH = '../../res/w2v_model.mecab.model'


def generate_model(wakati_path, model_path):
    w2v_data = word2vec.LineSentence(wakati_path)
    model = word2vec.Word2Vec(w2v_data, size=100, window=3, hs=1, min_count=1, sg=1)
    model.save(model_path)

def test_model(model_path):
    model = word2vec.Word2Vec.load(model_path)
    words = [u'棒', u'人生', u'楽しい', '謎']
    for w in words:
        similar_words = model.most_similar(positive=[w])
        print(w, ':', [w[0] for w in similar_words])


if __name__ == '__main__':
    # generate_model(MECAB_WAKATI_PATH, MECAB_MODEL_PATH)
    test_model(MECAB_MODEL_PATH)
