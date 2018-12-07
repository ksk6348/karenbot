import os
import numpy as np
import random, sys
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file

base = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.normpath(os.path.join(base, '../../'))
TEXT_PATH = ROOT_PATH + '/res/post.txt'

with open(TEXT_PATH) as f:
    text = f.read()
print('コーパスの長さ:{}'.format(len(text)))
chars = sorted(list(set(text)))
print('使われている文字の数:{}'.format(len(chars)))
char2id = dict((c, i) for i, c in enumerate(chars))
id2char = dict((i, c) for i, c in enumerate(chars))
maxlen = 20
step = 3
sentences = []
next_chars = []
for i in range(0, len(text) - maxlen, step):
    sentences.append(text[i: i + maxlen])
    next_chars.append(text[i + maxlen])
print('学習する文の数:{}'.format(len(sentences)))

print('テキストをIDベクトルにします...')
X = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        X[i, t, char2id[char]] = 1
    y[i, char2id[next_chars[i]]] = 1

print('モデルを構築します...')
model = Sequential()
model.add(LSTM(128, inpu_shape=(maxlen, len(chars))))
model.add(Dense(len(chars)))
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
    start_index = random.randint(0, len(text) - maxlen - 1)
    for diversity in [0.2, 0.5, 1.0, 1.2]:
        print('---多様性=', diversity)
        generated = ''
        sentence = text[start_index: start_index + maxlen]
        generated += sentence
        print('---シード="{}"'.format(sentence))
        print(sentence, end='')
        for i in range(400):
            x = np.zeros((1, maxlen, len(chars)))
            for t, char in enumerate(sentence):
                x[0, t, char2id[char]] = 1.
                preds = model.predict(x, verbose=0)[0]
                next_index = sample(preds, diversity)
                next_char = id2char[next_index]
                generated += next_char
                sentence = sentence[1:] + next_char
                print(next_char, end='')
        print()