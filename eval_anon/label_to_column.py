import sys
import re

header = next(sys.stdin)
print(header.strip('\n') + "\ttestid")

for line in sys.stdin:
    if line.strip() == '':
        sys.stdout.write(line)
        continue
    testid = '.'
    m = re.findall('_([pv]\d+)', line)
    if m:
        testid = m[0]
        line = re.sub('_[pv]\d+', '', line)
    print(line.strip() + '\t' + testid)
