import os
import numpy as np
import random
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.layers import LSTM
from keras.optimizers import RMSprop
import MeCab
import warnings
warnings.filterwarnings('ignore')

base = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.normpath(os.path.join(base, '../../'))
TEXT_PATH = ROOT_PATH + '/res/post.txt'

with open(TEXT_PATH) as f:
    text = f.read()
tagger = MeCab.Tagger('-Owakati -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
words = []
for line in text.split('\n'):
    words.extend(tagger.parse(line)[:-1].split(' '))
print('コーパスの長さ:{}'.format(len(text)))
words_set = sorted(list(set(words)))
print('使われている単語の数:{}'.format(len(words_set)))

with open(ROOT_PATH + '/res/post_wakati.all.txt', 'w') as f:
    f.write(' '.join(words))
word2id = dict((c, i) for i, c in enumerate(words_set))
id2word = dict((i, c) for i, c in enumerate(words_set))
maxlen = 20
step = 3
sentences = []
next_words = []
for i in range(0, len(words) - maxlen, step):
    sentences.append(words[i: i + maxlen])
    next_words.append(words[i + maxlen])
print('学習する文の数:{}'.format(len(sentences)))

if not os.path.exists(ROOT_PATH + '/res/x.npy'):
    print('テキストをIDベクトルにします...')
    X = np.zeros((len(sentences), maxlen, len(words_set)), dtype=np.bool)
    y = np.zeros((len(sentences), len(words_set)), dtype=np.bool)
    for i, sentence in enumerate(sentences):
        for t, word in enumerate(sentence):
            X[i, t, word2id[word]] = 1
        y[i, word2id[next_words[i]]] = 1
    np.save(ROOT_PATH + '/res/x.npy', X)
    np.save(ROOT_PATH + '/res/y.npy', y)
else:
    X = np.load(ROOT_PATH + '/res/x.npy')
    y = np.load(ROOT_PATH + '/res/y.npy')

print('モデルを構築します...')
model = Sequential()
model.add(LSTM(128, input_shape=(maxlen, len(words_set))))
model.add(Dense(len(words_set)))
model.add(Activation('softmax'))
optimizer = RMSprop(lr=0.01)
model.compile(loss='categorical_crossentropy', optimizer=optimizer)


def sample(preds, temperature=1.0):
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

for iteration in range(1, 60):
    print()
    print('-' * 50)
    print('繰り返し=', iteration)
    model.fit(X, y, batch_size=128, nb_epoch=1)
    start_index = random.randint(0, len(words) - maxlen - 1)
    for diversity in [0.2, 0.5, 1.0, 1.2]:
        print('---多様性=', diversity)
        generated = ''
        sentence = words[start_index: start_index + maxlen]
        generated += ''.join(sentence)
        print('---シード="{}"'.format(''.join(sentence)))
        print(''.join(sentence), end='')
        for i in range(400):
            x = np.zeros((1, maxlen, len(words_set)))
            for t, char in enumerate(sentence):
                x[0, t, word2id[char]] = 1.
                preds = model.predict(x, verbose=0)[0]
                next_index = sample(preds, diversity)
                next_word = id2word[next_index]
                generated += next_word
                sentence = sentence[1:] + next_word
                print(next_word, end='')
        print()