"""
For more theoretical information, please refer to:
https://www.dcc.uchile.cl/~gnavarro/ps/spire03.4.pdf
https://pdfs.semanticscholar.org/62de/373af61cc71854f86028554a988f8a4dbe36.pdf

Roman Kotenko, 2017
"""

from collections import defaultdict
from hashlib import md5
from os import makedirs
from os.path import isdir, isfile, join
from re import findall
from timeit import default_timer


PATTERN = '[\w\'"-]+|[ \n.,!?:;]'

CODE_FILE = '%d.txt'
DECODE_DIR = 'decode'
ENCODE_DIR = 'encode'
VOCAB_FILE = 'vocab.txt'
TEXT_FILE = 'text.txt'

text = None
split = None
vocab = None


def scdc_encode(s):
    """
    SCDC encode text.
    :param s: s parameter for scdc
    :return: wall execution time in seconds, encoded bytes size
    """
    start = default_timer()

    c = 256 - s
    out = b''
    global text, split, vocab

    for item in split:
        if item == ' ':
            i = vocab.index('%space%')
        elif item == '\n':
            i = vocab.index('%newline%')
        else:
            i = vocab.index(item)
        cur = (i % s + c).to_bytes(1, 'big')
        x = i // s
        while x > 0:
            x -= 1
            cur += (x % c).to_bytes(1, 'big')
            x //= c
        out += cur[::-1]

    with open(join(ENCODE_DIR, CODE_FILE % s), 'wb') as file_out:
        file_out.write(out)

    return default_timer() - start, len(out)


def scdc_decode(s):
    """
    Decode SCDC encoded text.
    :param s: s parameter for scdc
    :return: wall execution time in seconds
    """

    def generate_base():
        """
        Generate base values for decoding.
        base[0] = 0, base[1] = s, base[2] = s + sc, base[3] = s + sc + sc^2 ...
        Please refer to http://vios.dc.fi.udc.es/codes/semistatic.html
        :return: base values - list
        """
        yield 0
        yield s
        cc = 256 - s
        prev = s
        while True:
            prev = prev + s * cc
            yield prev
            cc *= cc

    def write_decode(text):
        """
        Write decode result to corresponding file.
        :param text: decoded text
        :return: None
        """
        with open(join(DECODE_DIR, CODE_FILE % s), 'w', encoding='utf-8') as file_out:
            for item in text:
                if item == '%space%':
                    file_out.write(' ')
                elif item == '%newline%':
                    file_out.write('\n')
                else:
                    file_out.write(item)

    start = default_timer()

    filename = join(ENCODE_DIR, CODE_FILE % s)
    if not isfile(filename):
        print("file '%s' not found for decoding" % filename)
        return None
    with open(filename, 'rb') as file_in:
        code = file_in.read()

    c = 256 - s
    global vocab
    out = []  # decoded text

    cur = 0  # index in vocabulary of item represented by current byte sequence
    base = generate_base()
    for x in code:
        if x < c:  # non-stopping byte
            cur = cur * c + x
            next(base)  # with each non-stopping byte just move on to next base value
            # so that we have the value we need when the stopping byte is hit
        else:  # we hit stopping byte in the sequence
            cur = cur * s + x - c + next(base)
            out.append(vocab[cur])
            # reset these before moving to next byte sequence
            cur = 0
            base = generate_base()

    write_decode(out)
    return default_timer() - start


def scdc_prepare():
    """
    Create required directories, read text from file, split the text, and get vocabulary (unique words) for it.
    :return: None
    """

    def md5calc(filename):
        """
        Calculate file's MD5 hashsum.
        :param filename: you know
        :return: MD5 sum
        """
        hashsum = md5()
        with open(filename, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hashsum.update(chunk)
        return hashsum.hexdigest()

    def generate_vocab():
        """
        Generate vocabulary from input text and write it to file.
        First line will be MD5 hash of original text file, following lines -- one vocabulary item each.
        :return: None
        """
        vocab_dict = defaultdict(int)
        global text, split, vocab
        for item in split:
            if item == ' ':
                vocab_dict['%space%'] += 1
            elif item == '\n':
                vocab_dict['%newline%'] += 1
            else:
                vocab_dict[item] += 1
        vocab = [item[0] for item in sorted(vocab_dict.items(), key=lambda a: a[1], reverse=True)]
        with open(VOCAB_FILE, 'w', encoding='utf-8') as file_out:
            file_out.write(md5hash + '\n')
            for item in vocab:
                file_out.write(item + '\n')

    global text, split
    with open(TEXT_FILE, 'r', encoding='utf-8') as file_in:
        text = file_in.read()
    split = findall(PATTERN, text)

    md5hash = md5calc(TEXT_FILE)
    if isfile(VOCAB_FILE):
        with open(VOCAB_FILE, 'r', encoding='utf-8') as file_in:
            global vocab
            vocab = []
            for line in file_in:
                vocab.append(line.rstrip())
            # compare md5 of TEXT_FILE and the file vocab was compiled for
            if vocab[0] == md5hash:
                del vocab[0]
            else:
                generate_vocab()
    else:
        generate_vocab()

    for dir in (ENCODE_DIR, DECODE_DIR):
        if not isdir(dir):
            makedirs(dir)


def main():
    scdc_prepare()
    for f in (scdc_encode, scdc_decode):
        for s in range(1, 256):
            print(f(s))


if __name__ == '__main__':
    main()
