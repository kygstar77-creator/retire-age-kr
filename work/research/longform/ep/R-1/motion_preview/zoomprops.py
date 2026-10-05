# R-1 첫 장면 '점 하나 → 줌아웃' 미리보기 재료 — work/video/r1.json open 장면 + facts.txt 원문 대조 → open_zoom.json
#   py -3.12 work/research/longform/ep/R-1/motion_preview/zoomprops.py
# 글자는 r1.json(=facts.txt 문구) 그대로, 막대 길이용 값만 정수로 바꾼다. 갈래 시작 프레임은 말 2 안 단어 위치 비율로 어림(목소리 생기면 다시).
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); EP = os.path.dirname(HERE)
WORK = os.path.normpath(os.path.join(EP, '..', '..', '..', '..'))
FACTS = open(os.path.join(EP, 'facts.txt'), encoding='utf-8').read()


def build(s):
    """r1.json open 장면 → ZoomOutOpen props (r1props.py가 본편 r1.json에 넣을 때도 부른다, 10/5 PD)"""
    st = [0]
    for l in s['lines']: st.append(st[-1] + l['frames'])
    cap = s['lines'][3]['cap']
    m = re.search(r'^(.+?) · 세금 전 ([\d,]+원) → 세금 뒤 ([\d,]+원)$', cap); assert m, cap
    pre, post = m[2], m[3]
    for v in (pre, post): assert v.rstrip('원') in FACTS, v
    cutv = int(pre[:-1].replace(',', '')) - int(post[:-1].replace(',', ''))
    cut = f'{cutv:,}원'; assert cut[:-1] in FACTS and cut in s['data']['gapText'], cut
    d = re.search(r'(\d{4}\.\d{1,2}\.\d{1,2})에 넣고 (\d{4}\.\d{1,2}\.\d{1,2})에 뺐다면', s['sub']); assert d
    names = [b[0] for b in s['data']['bars']]
    l2 = s['lines'][1]['text']; n2 = len(l2)
    key = {'예금': '예금', 'S&P500': 'ETF', 'SCHD': 'ETF', '금': '금을'}
    nameAt = [st[1] + int(s['lines'][1]['frames'] * l2.index(key[n]) / n2) + (14 if n == 'SCHD' else 0) for n in names]
    zoom = dict(seed='R-1', dot='1억', names=names, nameAt=nameAt, **{'from': d[1]}, to=d[2], q=st[1], travel=st[2], gap=st[3],
                gapHead=m[1],   # 갈래가 빠진 뒤엔 막대 제목이 무엇의 간격인지 말해야 한다(심사 10/5) — 자막 칩 원문 그대로
                 pre=[pre, int(pre[:-1].replace(',', ''))], post=[post, int(post[:-1].replace(',', ''))], cut='줄어든 몫 ' + cut)
    assert '1억' in s['lines'][0]['text']
    return zoom


if __name__ == '__main__':
    r1 = json.load(open(os.path.join(WORK, 'video', 'r1.json'), encoding='utf-8'))
    s = next(x for x in r1['scenes'] if x['key'] == 'open')
    zoom = build(s)
    json.dump({'scene': s, 'zoom': zoom}, open(os.path.join(HERE, 'open_zoom.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(json.dumps(zoom, ensure_ascii=False))
