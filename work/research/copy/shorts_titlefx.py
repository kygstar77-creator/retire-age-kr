# 쇼츠 전편: 첫날 조회(분석 day) · 지금 공개 조회(Data API) · 평균 본 비율 × 제목 틀(질문/단정 · 숫자 위치 · 길이)
#   py -3.12 work/research/copy/shorts_titlefx.py   → research/copy/shorts_titlefx.md
import sys, os, json, re, datetime
sys.stdout.reconfigure(encoding='utf-8')
W = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, W)
import ytanalytics as ya
from googleapiclient.discovery import build
rows = [json.loads(l) for l in open(os.path.join(W, 'research/cardshorts/log.jsonl'), encoding='utf-8')]
ids = [r['id'] for r in rows]
yt = build('youtube', 'v3', credentials=ya.creds())
pub = {}
for it in yt.videos().list(part='statistics,snippet', id=','.join(ids)).execute()['items']:
    pub[it['id']] = (int(it['statistics'].get('viewCount', 0)), it['snippet']['publishedAt'])
def frame(t):
    t = t.replace('#shorts', '').strip()
    q = '질문' if '?' in t else '단정'
    m = re.search(r'\d', t); pos = (m.start() / len(t)) if m else None
    npos = '숫자없음' if pos is None else ('앞' if pos < 0.34 else '가운데' if pos < 0.67 else '뒤')
    return t, q, npos, len(t)
def first_frame(spec):  # 첫 프레임 큰 글씨: cover(표지) > cards[0].q > title 순 — 피드 유입 93~98%가 처음 보는 글자
    try:
        sp = spec if os.path.isabs(spec) else os.path.join(os.path.dirname(W), spec if spec.startswith('work/') else 'work/' + spec)
        d = json.load(open(sp, encoding='utf-8'))
    except Exception:
        return None
    lines = d.get('cover') or (d.get('cards') or [{}])[0].get('q') or d.get('title') or []
    return ' / '.join(re.sub(r'[{}]', '', x) for x in lines) or None
def ff_kind(f):
    if not f: return '없음'
    q = '질문' if ('?' in f or '몇' in f or '얼마' in f) else '단정'
    return q + ('·숫자' if re.search(r'\d', f) else '·숫자없음')
out = ['# 쇼츠 제목 틀 × 첫 2일 조회 (생성 %s)' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), '',
       '| 공개 | id | 틀 | 숫자 위치 | 글자 | 첫 2일(분석) | 지금 공개 조회 | 평균 본 비율 | 넘기지 않은 비율(engaged/조회) | 첫 프레임 틀 | 첫 프레임 글자 | 제목 |', '|---|---|---|---|---|---|---|---|---|---|---|---|']
data = []
for r in rows:
    vid = r['id']; t, qf, npos, n = frame(r['title'])
    d0 = (datetime.date.fromisoformat(r['at'][:10]) - datetime.timedelta(days=1)).isoformat()  # 분석 날짜는 태평양 시각 — 한국 낮 공개분은 전날로 잡힌다
    try:
        rd = ya.q('views,averageViewPercentage', dims='day', filters='video==' + vid, start=d0)
        days = sorted(rd.get('rows') or [])
    except Exception as e:
        days = []
    first = sum(x[1] for x in days[:2]) if days else None  # 공개일+다음날(분석 날짜는 태평양 시각)
    avp = None; eng = None
    try:
        rv = ya.q('views,averageViewPercentage,engagedViews', filters='video==' + vid, start=d0).get('rows')
        avp = round(rv[0][1]) if rv else None
        eng = round(100 * rv[0][2] / rv[0][0], 1) if rv and rv[0][0] else None
    except Exception: pass
    pv = pub.get(vid, (None,))[0]
    ff = first_frame(r.get('spec') or ''); fk = ff_kind(ff)
    data.append(dict(id=vid, at=r['at'], frame=qf, npos=npos, n=n, first=first, pub=pv, avp=avp, eng=eng, layout=r.get('layout'), title=t, days=days[:3], ff=ff, ffk=fk, ffn=len(ff.replace(' / ', '')) if ff else None))
    out.append('| %s | %s | %s | %s | %d | %s | %s | %s%% | %s%% | %s | %s | %s |' % (r['at'][5:16], vid, qf, npos, n, first, pv, avp, eng, fk, ff, t))
def med(v):
    v = sorted(x for x in v if x is not None); return v[len(v)//2] if v else None
out += ['', '## 묶음 중앙값(지금 공개 조회)']
for key in ('frame', 'npos', 'layout', 'ffk'):
    g = {}
    for d in data: g.setdefault(d[key], []).append(d)
    out.append('- %s: ' % key + ' · '.join('%s %s편 조회 %s·넘기지 않음 %s%%' % (k, len(v), med([x['pub'] for x in v]), med([x['eng'] for x in v])) for k, v in g.items()))
g = {'짧음(≤30자)': [d['pub'] for d in data if d['n'] <= 30], '긺(>30자)': [d['pub'] for d in data if d['n'] > 30]}
g2 = {'첫 프레임 ≤20자': [d for d in data if d['ffn'] and d['ffn'] <= 20], '첫 프레임 >20자': [d for d in data if d['ffn'] and d['ffn'] > 20]}
out.append('- 첫 프레임 길이: ' + ' · '.join('%s %s편 조회 %s·넘기지 않음 %s%%' % (k, len(v), med([x['pub'] for x in v]), med([x['eng'] for x in v])) for k, v in g2.items()))
out.append('- 길이: ' + ' · '.join('%s %s편 %s' % (k, len(v), med(v)) for k, v in g.items()))
open(os.path.join(W, 'research/copy/shorts_titlefx.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
json.dump(data, open(os.path.join(W, 'research/copy/shorts_titlefx.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('\n'.join(out))
