from janome.tokenizer import Tokenizer
from src.common.my_mecab import MyMeCab
import re
import emoji

TEXT_PATH = '../../res/post.txt'
JANOME_WAKATI_PATH = '../../res/post_wakati.janome.txt'
MECAB_WAKATI_PATH = '../../res/post_wakati.mecab.txt'

def janome_tokenize(text):
    t = Tokenizer()
    result = []
    emoji_flag = False
    lines = re.split('\n|\s', text)
    for line in lines:
        if not line:
            continue
        line = line.replace('#', '')
        print('解析行:', line)
        tokens = t.tokenize(line)

        for token in tokens:
            base_form = token.base_form
            if base_form in ['「', '」', '']:
                continue
            pos = token.part_of_speech
            pos = pos.split(',')[0]
            if pos in ['名詞', '動詞', '形容詞', '記号']:
                if base_form in emoji.UNICODE_EMOJI:
                    emoji_flag = True
                if emoji_flag and base_form not in emoji.UNICODE_EMOJI:
                    emoji_flag = False
                    result.append('。')
                result.append(base_form)
    return result

def mecab_tokenize(text):
    result = []
    lines = re.split('\n|\s', text)
    emoji_flag = False
    for line in lines:
        if not line:
            continue
        line = line.replace('#', '')
        print('解析行:', line)
        morphemes = MyMeCab.parse(line)

        for m in morphemes:
            if m.infinitve in ['「', '」', '']:
                continue
            if m.pos in ['名詞', '動詞', '形容詞', '記号']:
                if m.infinitve in emoji.UNICODE_EMOJI:
                    emoji_flag = True
                if emoji_flag and m.infinitve not in emoji.UNICODE_EMOJI:
                    emoji_flag = False
                    result.append('。')
                result.append(m.infinitve)
    return result


if __name__ == '__main__':
    # with open(TEXT_PATH) as f:
    #     text = f.read()
    # result = janome_tokenize(text)
    # with open(JANOME_WAKATI_PATH, 'w') as f:
    #     f.write(' '.join(result))
    with open(TEXT_PATH) as f:
        text = f.read()
    result = mecab_tokenize(text)
    with open(MECAB_WAKATI_PATH, 'w') as f:
        f.write(' '.join(result))