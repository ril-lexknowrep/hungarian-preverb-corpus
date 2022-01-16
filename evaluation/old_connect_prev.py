"""
Primitive way to connect perverbs to verbs.
Using advanced itertools techniques. :)
"""

import sys
import numpy as np

from itertools import chain
from more_itertools import split_at, windowed

EMPTYWORD = ''

CNT_FIELDS = 10
FORM, WSAFTER, TESTID, ANAS, LEMMA, XPOSTAG, PREV, PREVID, PREVOLD, PREVCLOSEST = list(range(CNT_FIELDS))


def stream_to_words(stream):
    """Process line: split by TAB + handle empty lines."""
    for line in stream:
        line = line.rstrip('\n')
        yield line.split('\t') + ['.', '.'] if line != EMPTYWORD else EMPTYWORD


def word_to_line(word):
    """Create a line from word."""
    return '\t'.join(word)


ENV = 2 # search for [/Prev] in a -env..env environment of the [/V]

PREV_POSITIONS = [-2, 1, 2] # ki sem vette, vette ki, vette most ki

VERB_POSTAG = '[/V]'
PREVERB_POSTAG = '[/Prev]'


def main():
    """Main."""
    header = next(sys.stdin).strip('\n')
    print(header + '\tprevold\tprevclosest')

    words = stream_to_words(sys.stdin)

    sentences = split_at(words, lambda x: x == EMPTYWORD)

    window_size = 2 * ENV + 1
    center = ENV # index of central element in window
    padding = [[''] * CNT_FIELDS] * ENV

    prevold_id = 0
    prevclosest_id = 0

    for sentence in sentences:

        # old connect_prev baseline
        padded_sentence = chain(padding, sentence, padding)

        for window in windowed(padded_sentence, window_size):

            central = window[center]

            #     csak olyanra tegyünk IK-t, amin még nincs
            if central[PREV] == 'pfx':
                continue

            if VERB_POSTAG in central[XPOSTAG]:
                for position in PREV_POSITIONS:
                    environmental = window[center+position]
                    if environmental[XPOSTAG] == PREVERB_POSTAG:
                        central[PREVOLD] = str(prevold_id)
                        environmental[PREVOLD] = str(prevold_id)
                        prevold_id += 1
                        break


        # Recski (2011) baseline, but without connecting to the
        # verb directly to the right
        for i, central in enumerate(sentence):
            if central[XPOSTAG] == PREVERB_POSTAG:
                left_closest, right_closest = None, None

                j = i - 1
                while j >= 0:
                    other_token = sentence[j]
                    if (VERB_POSTAG in other_token[XPOSTAG] and
                        other_token[PREV] != 'pfx'):
                            left_closest = j
                            break
                    j -= 1

                j = i + 2
                while j < len(sentence):
                    other_token = sentence[j]
                    if (VERB_POSTAG in other_token[XPOSTAG] and
                        other_token[PREV] != 'pfx'):
                            right_closest = j
                            break
                    j += 1

                if left_closest is None and right_closest is None:
                    continue

                if left_closest is None:
                    left_distance = np.inf
                else:
                    left_distance = i - left_closest

                if right_closest is None:
                    right_distance = np.inf
                else:
                    right_distance = right_closest - i

                if left_distance <= right_distance:
                    connected_index = left_closest
                else:
                    connected_index = right_closest

                other_token = sentence[connected_index]
                central[PREVCLOSEST] = str(prevclosest_id)
                other_token[PREVCLOSEST] = str(prevclosest_id)
                prevclosest_id += 1

        for tok in sentence:
            print(word_to_line(tok))

        print(EMPTYWORD)


if __name__ == '__main__':
    main()
