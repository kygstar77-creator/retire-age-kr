# 범위 축소 기준값(11/19 이전 30일) — 축별 롱폼 첫 7일·쇼츠 첫 2일 조회, 카페 조회 중앙
#   py -3.12 work/research/growth/scope_baseline_1120.py
# 회의 11/19 21:5x 지시(레드팀 위험3). 축 나누기는 제목 낱말 규칙(아래 AXES) — 사람 판정 아님.
# 유튜브: Analytics API 일 단위라 '48시간'은 공개일+다음날(2일) 합으로 잰다.
import sys, os, json, re, statistics, datetime, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
W = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, W)
import ytanalytics as ya

S, E = datetime.date(2026, 10, 20), datetime.date(2026, 11, 18)
AXES = [('배당', r'배당|분배|SCHD|JEPI|JEPQ|커버드콜|리츠|월배당|DGRW|SPYD|VYM'),
        ('부동산', r'아파트|실거래|전세|월세|재건축|분양|시세|㎡|평당|단지|청약|오피스텔|집값|토지거래'),
        ('지수', r'S&P|나스닥|지수|KODEX|TIGER|코스피|KOSPI|ETF|적립|QQQ|VOO|SPY')]
OUT_RE = r'연금|주택연금|국민연금|세금|종부세|건보|건강보험|양도세|장특|예금|적금|금리|환율|연봉|정책'

def axis(t):
    if re.search(r'건보|건강보험|종부세|양도세', t): return '범위 밖'  # 배당 낱말이 있어도 주제가 세금·건보면 범위 밖
    if re.search(OUT_RE, t) and not re.search(r'배당|분배|S&P|나스닥|지수', t): return '범위 밖'
    for a, p in AXES:
        if re.search(p, t, re.I): return a
    return '범위 밖'

def med(xs): return round(statistics.median(xs)) if xs else None

def yt():
    vids = json.load(open(os.path.join(W, 'research/longform/loop/topic_stats_1119_ours.json'), encoding='utf-8'))
    rows = []; seen = set()
    for v in vids:
        if v.get('priv') != 'public' or v['id'] in seen: continue
        seen.add(v['id'])
        d = datetime.date.fromisoformat(v['d'][:10])
        if not (S <= d <= E): continue
        short = (v.get('sec') or 0) <= 180 or '#shorts' in v['t']
        n = 1 if short else 6
        r = ya.q('views', filters=f"video=={v['id']}", start=d.isoformat(), end=(d + datetime.timedelta(days=n)).isoformat())
        views = sum(x[0] for x in r.get('rows', [])) if r.get('rows') else 0
        rows.append(dict(id=v['id'], t=v['t'], d=v['d'][:10], kind='쇼츠' if short else '롱폼', axis=axis(v['t']), early=views, total=v.get('views')))
    return rows

def cafe():
    UA = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://cafe.naver.com/'}
    arts = []
    for pg in range(1, 5):
        u = ('https://apis.naver.com/cafe-web/cafe2/ArticleListV2dot1.json?search.clubid=31789001'
             f'&search.queryType=lastArticle&search.page={pg}&search.perPage=50')
        a = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=20))['message']['result']['articleList']
        arts += a
        if not a: break
    rows = []
    for a in arts:
        d = datetime.datetime.fromtimestamp(a['writeDateTimestamp'] / 1000).date()
        if S <= d <= E and a.get('writerNickname') and a.get('menuId') != 0:
            rows.append(dict(id=a['articleId'], t=a['subject'], d=d.isoformat(), axis=axis(a['subject']), reads=a.get('readCount', 0), writer=a.get('writerNickname')))
    return rows

if __name__ == '__main__':
    out = {'range': [S.isoformat(), E.isoformat()], 'at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}
    out['yt'] = yt(); out['cafe'] = cafe()
    json.dump(out, open(os.path.join(os.path.dirname(__file__), 'scope_baseline_1120.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('측정', out['at'], '기간', out['range'])
    for kind in ('롱폼', '쇼츠'):
        print(f'\n[{kind}] 첫 {"7일" if kind=="롱폼" else "2일"} 조회 중앙 (편수)')
        for a in ('배당', '지수', '부동산', '범위 밖'):
            # Analytics 늦게 쌓임: 첫 구간 0인데 누적이 50 넘으면 아직 안 들어온 것 → 뺀다
            xs = [r['early'] for r in out['yt'] if r['kind'] == kind and r['axis'] == a and not (r['early'] == 0 and (r['total'] or 0) > 50)]
            print(f'  {a}: {med(xs)} ({len(xs)}편)')
    print('\n[카페] 조회 중앙 (편수, 11/20 현재 누적)')
    for a in ('배당', '지수', '부동산', '범위 밖'):
        xs = [r['reads'] for r in out['cafe'] if r['axis'] == a]
        print(f'  {a}: {med(xs)} ({len(xs)}편)')
