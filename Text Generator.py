from itertools import count
from re import match
import typing
from collections import Counter, defaultdict
from random import choice, choices

file_name = input()
tokens = []
with open(file_name, encoding='utf-8') as file:
    for line in file:
        mid = line.split()
        for n, token in enumerate(mid):
            if '.' == token:
                mid.remove(token)
                mid[n - 1] += token
        tokens.extend(mid)

heads: typing.List[str] = []
for first, second in zip(tokens[:-2], tokens[1:-1]):
    heads.append(' '.join((first, second)))
tails = tokens[2:]
row_bigram = defaultdict(list)
trigrams = {}
for head, tail in zip(heads, tails):
    row_bigram[head].append(tail)
for head, tails_list in row_bigram.items():
    trigrams[head] = Counter(tails_list)


def create_sentence(least_word=5):
    first_word = choice(heads)
    while not match(r'[A-Z].*[^!?.]$', first_word.split()[0]):
        first_word = choice(heads)
    sentence: typing.List[str] = first_word.split()
    for n_word in count(3):
        key = ' '.join(sentence[-2:])
        word = choices(list(trigrams[key]), list(trigrams[key].values()))[0]
        sentence.append(word)
        if n_word >= least_word and match(r'.+[!?.]$', word):
            break
    sentence[0] = sentence[0].capitalize()
    return ' '.join(sentence)


for _ in range(10):
    print(create_sentence())
