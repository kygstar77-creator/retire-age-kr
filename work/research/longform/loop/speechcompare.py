# 사람 말투 실측 — 경쟁 롱폼 자막(사람이 실제로 말한 것) vs 우리 롱폼 대본(10/4 사장님 "그냥 니 생각 아니야?")
import json, glob, re, sys, os
sys.stdout.reconfigure(encoding='utf-8')
def subs(f):
    d = json.load(open(f, encoding='utf-8'))
    return ' '.join(''.join(s.get('utf8', '') for s in e.get('segs', [])) for e in d.get('events', []) if e.get('segs')).replace('\n', ' ')
def ours(ep):
    v = json.load(open(f'ep/{ep}/voice.json', encoding='utf-8'))
    return ' '.join(l['say'] for s in v['sections'] for l in s['lines'])
def m(t):
    sents = [x.strip() for x in re.split(r'(?<=[.?!])\s+', t) if len(x.strip()) > 3]
    words = t.split(); W = max(1, len(words))
    ends = [s.rstrip('.?! ') for s in sents]
    hap = sum(bool(re.search(r'(니다|니까)$', e)) for e in ends); yo = sum(e.endswith('요') for e in ends)
    k = lambda pat: len(re.findall(pat, t)) * 1000 / W
    return {'문장수': len(sents), '평균 문장 글자': round(sum(map(len, sents)) / max(1, len(sents)), 1),
            '-니다 끝 %': round(100 * hap / max(1, len(ends))), '-요 끝 %': round(100 * yo / max(1, len(ends))),
            '숫자/1000단어': round(k(r'\d[\d,.]*'), 1), '숫자 2개 이상 문장 %': round(100 * sum(len(re.findall(r'\d[\d,.]*', s)) >= 2 for s in sents) / max(1, len(sents))),
            '추임새(자,·네,·근데·사실·그쵸·이제)/1000': round(k(r'(?:^|\s)(?:자,|네,|근데|사실|그쵸|그죠|이제)\s'), 1),
            '질문 문장 %': round(100 * sum(s.endswith('?') for s in sents) / max(1, len(sents)))}
rows = []
for f in sorted(glob.glob('loop/subs/*.ko-orig.json3')):
    rows.append(('경쟁 ' + os.path.basename(f)[:11], m(subs(f))))
for ep in ['E-1', 'D-1', 'E-2', 'N-1']:
    if os.path.exists(f'ep/{ep}/voice.json'): rows.append(('우리 ' + ep, m(ours(ep))))
keys = list(rows[0][1])
print('| 영상 | ' + ' | '.join(keys) + ' |'); print('|' + '---|' * (len(keys) + 1))
for n, r in rows: print(f'| {n} | ' + ' | '.join(str(r[k]) for k in keys) + ' |')
import statistics as st
for grp in ['경쟁', '우리']:
    g = [r for n, r in rows if n.startswith(grp)]
    print(f'| **{grp} 중앙값** | ' + ' | '.join(str(st.median([x[k] for x in g])) for k in keys) + ' |')
