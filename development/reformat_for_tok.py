import sys
import re

index_counter = 1

for line in sys.stdin:
    cols = line.strip().split('\t')
    if len(cols) != 2:
        sys.stdout.write(line)
    else:
        t = re.sub(r'(\\|\|)(\d)(\S)', r'\1\2 \3', cols[1])
        t = re.sub(r'(\\|\|)(\d)', r'\1\2.', t)

        m = re.findall(r'\\([0-9]).', t)
        for original_index in m:
            if original_index == '0':
                continue
            t = t.replace(f'\\{original_index}.', f'\\{index_counter}').\
                    replace(f'|{original_index}.', f'|{index_counter}')
            index_counter += 1

        t = t.replace('\\0.','_p0')
        print(t.replace('\\', '_p').replace('|', '_v'))
