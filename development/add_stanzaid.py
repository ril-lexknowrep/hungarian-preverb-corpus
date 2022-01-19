import sys
sys.path.append('../preverb')

from more_itertools import split_at
from word import Word

header = next(sys.stdin)
Word.features = header.strip().split('\t') + ['stanzaid']
print(Word.header())

lines = sys.stdin.read().split('\n')
sentences = list(split_at(lines, lambda x: x == ''))
for s in sentences:
    words = [Word(token.split('\t') + ['.']) for token in s]
    for w in words:
        if w.deprel == 'compound:preverb':
            w.stanzaid = w.head
            words[int(w.head) - 1].stanzaid = w.head
    for w in words:
        print(w)
    print()