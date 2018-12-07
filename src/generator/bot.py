from gensim.models import word2vec
import json, random
import sys
sys.path.append('..')
from common.my_mecab import MyMeCab
from generator.markov import word_choice
import warnings
import numpy as np
import os

class Bot:
    base = os.path.dirname(os.path.abspath(__file__))
    ROOT_PATH = os.path.normpath(os.path.join(base, '../../'))
    W2V_MODEL_PATH = ROOT_PATH + '/res/w2v_model.mecab.model'
    MARKOV_DIC_PATH = ROOT_PATH + '/res/markov.mecab.json'

    def __init__(self):
        self.w2v_model = word2vec.Word2Vec.load(self.W2V_MODEL_PATH)
        self.markov_dic = json.load(open(self.MARKOV_DIC_PATH))


    def tokenize(self, text):
        morphemes = MyMeCab.parse(text)
        for m in morphemes:
            if m.pos in ['名詞', '動詞', '形容詞']:
                try:
                    self.w2v_model.most_similar(positive=[m.infinitve])
                    return m.infinitve
                except:
                    continue
        return '@'

    def get_similar_word(self, word):
        try:
            similar_words = self.w2v_model.most_similar(positive=[word])
            return random.choice([w[0] for w in similar_words])
        except KeyError:
            return '@'

    def make_sentence(self, head):
        if head == '':
            return ''
        ret = []
        if head != '@':
            ret.append(head)
        try:
            top = self.markov_dic[head]
        except KeyError:
            top = self.markov_dic['@']
        w1 = word_choice(top)
        w2 = word_choice(top[w1])
        ret.append(w1)
        ret.append(w2)
        while True:
            if w1 in self.markov_dic and w2 in self.markov_dic[w1]:
                items = self.markov_dic[w1][w2].items()
                words, counts = zip(*items)
                weight = np.array(counts) / np.sum(counts)
                w3 = np.random.choice(words, p=weight)
            else:
                w3 = ""
            ret.append(w3)
            if w3 == '。' or w3 == '？' or w3 == '':
                break
            if len(ret) > 30:
                ret.append('。')
                break
            w1, w2 = w2, w3
        return ''.join(ret)

    def reply(self, text):
        t = self.tokenize(text)
        s_word = self.get_similar_word(t)
        return self.make_sentence(s_word)

if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    bot = Bot()
    while True:
        s = input('you  :')
        if s == 'quit':
            sys.exit()
        sentence = bot.reply(s)
        print('karen:' + sentence)