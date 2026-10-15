# script.md → test_input_vN.txt (이해 시험 심사관이 읽는 것: 장 제목·화면·말만, [자막]·출처 줄은 뺌)
import sys, re, os
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(H, 'script.md'), encoding='utf-8').read().split('\n---\n')[1]
out = []
for l in src.splitlines():
    s = l.strip()
    if s.startswith('## '): out += ['', s]
    elif s.startswith('(화면'): out.append('화면: ' + re.sub(r'^\(화면[^:]*:\s*', '', s).rstrip(')'))
    elif s.startswith('- '): out.append('말: ' + s[2:])
open(os.path.join(H, f'test_input_{sys.argv[1]}.txt'), 'w', encoding='utf-8').write('\n'.join(out).strip() + '\n')
sy = sum(len(re.findall(r'[가-힣]', s[2:])) + 1.5 * len(re.findall(r'\d+(?:,\d+)?', s)) for s in (x.strip() for x in src.splitlines()) if s.startswith('- '))
n = sum(1 for s in src.splitlines() if s.strip().startswith('- '))
print('말 줄', n, '· 음절 약', int(sy), '· 길이 약', round((sy / 5 + n * 0.5) / 60, 2), '분')
