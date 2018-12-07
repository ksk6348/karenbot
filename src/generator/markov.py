from janome.tokenizer import Tokenizer
from src.common.my_mecab import MyMeCab
import emoji
import os, re, json, random
import numpy as np

MECAB_DICT_FILE = '../../res/markov.mecab.json'
POST = '../../res/post.txt'


def make_dic(words):
    tmp = ['@']
    dic = {}
    for w in words:
        if w in ['', ' ', '　', '「', '」', '\n']:
            continue
        tmp.append(w)
        if len(tmp) < 3:
            continue
        if len(tmp) > 3:
            tmp = tmp[1:]
        w1, w2, w3 = tmp
        if not w1 in dic:
            dic[w1] = {}
        if not w2 in dic[w1]:
            dic[w1][w2] = {}
        if not w3 in dic[w1][w2]:
            dic[w1][w2][w3] = 0
        dic[w1][w2][w3] += 1
        if w == '。':
            tmp = ['@']
            continue
    return dic


def make_sentence(dic):
    ret = []
    if not '@' in dic:
        return 'no dic'
    top = dic['@']
    w1 = word_choice(top)
    w2 = word_choice(top[w1])
    ret.append(w1)
    ret.append(w2)
    while True:
        w3 = word_choice(dic[w1][w2])
        ret.append(w3)
        if w3 == '。':
            break
        w1, w2 = w2, w3
    return ''.join(ret)


def word_choice(sel):
    keys = sel.keys()
    return random.choice(list(keys))


def mecab_tokenize(text):
    result = []
    lines = re.split('\n|\s', text)
    emoji_flag = False
    for line in lines:
        if not line:
            continue
        line = line.replace('#', '')
        morphemes = MyMeCab.parse(line)

        for m in morphemes:
            if m.infinitve in ['「', '」', '']:
                continue
            if m.surface in emoji.UNICODE_EMOJI:
                emoji_flag = True
            if emoji_flag and m.surface not in emoji.UNICODE_EMOJI:
                emoji_flag = False
                result.append('。')
            result.append(m.surface)
    return result


if __name__ == '__main__':
    if not os.path.exists(MECAB_DICT_FILE):
        with open(POST) as f:
            text = f.read()
            words = mecab_tokenize(text)
            dic = make_dic(words)
            json.dump(dic, open(MECAB_DICT_FILE, 'w'))
    else:
        dic = json.load(open(MECAB_DICT_FILE))

    for i in range(10):
        s = make_sentence(dic)
        print(s)
        print('-----')