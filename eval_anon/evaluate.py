import sys

sys.path.append('../preverb')
from word import Word

PREVERB_COUNT, TRUE_POS, FALSE_POS, TRUE_NEG, FALSE_NEG = 0, 1, 2, 3, 4

ALGORITHM_COLUMN = {
    'emPreverb': 'previd',
    'max2': 'prevmax2',
    'nearest verb': 'prevnearest',
    'emStanza': 'stanzaid',
}

def main():
    input_stream = sys.stdin

    header = next(input_stream)
    Word.features = header.strip().split('\t')

    input_lines = input_stream.read().split('\n')

    for algorithm, column in ALGORITHM_COLUMN.items():
        if column in Word.features:
            results = evaluate_target_column(input_lines, column)
            calculate_metrics(algorithm, results)

def evaluate_target_column(input_lines, target_col_name):
    preverb_count, true_pos, false_pos, true_neg, false_neg = 0, 0, 0, 0, 0

    p_testids = {}
    v_testids = {}
    irrelevant_previds = []

    for n, token in enumerate(input_lines):
        if token.strip() == '':
            for p_testid, p_target_id in p_testids.items():
                if (p_target_id in irrelevant_previds or  # \i is connected to a non-annotated verb
                    p_testid not in v_testids or          # \i is not connected to any annotated verbs
                    v_testids[p_testid] != p_target_id):  # \i is not connected to |i, but some other |j
                    false_pos += 1
                else:
                    true_pos += 1
            p_testids = {}
            v_testids = {}
            irrelevant_previds = []
            continue

        token = Word(token.strip('\n').split('\t'))
        target_id = getattr(token, target_col_name)

        if token.testid == '.':
            if target_id not in ('.', ''):
                irrelevant_previds.append(target_id)
            continue

        if token.testid == 'p0':
            preverb_count += 1
            if target_id in ('.', ''):
                true_neg += 1    # not connected, OK
            else:
                false_pos += 1   # preverb annotated as \0 connected to anything
            continue

        if token.testid[0] == 'p':
            preverb_count += 1
            if target_id in ('.', ''):
                false_neg += 1   # preverb annotated as \1 etc. should have been connected
            elif token.testid[1:] in p_testids and p_testids[token.testid[1:]] != target_id:
                false_pos += 1   # previd does not match preverb with the same annotation
            else:
                p_testids[token.testid[1:]] = target_id
            continue

        if token.testid[0] == 'v' and target_id not in ('.', ''):
            v_testids[token.testid[1:]] = target_id

    return (preverb_count, true_pos, false_pos, true_neg, false_neg)

def calculate_metrics(algorithm, results):
    print("Results for", algorithm)
    print(results)

    precision = results[TRUE_POS] / (results[TRUE_POS] + results[FALSE_POS])
    print("Precision: %.4f" % precision)

    recall = results[TRUE_POS] / (results[TRUE_POS] + results[FALSE_NEG])
    print("Recall: %.4f" % recall)

    # F1
    print("F1: %.4f"%(2 * precision * recall / (precision + recall)))

    # accuracy:
    print("Accuracy: %.4f"%((results[TRUE_POS] + results[TRUE_NEG]) / results[PREVERB_COUNT]))

    print()

if __name__ == '__main__':
    main()
