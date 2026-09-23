# 기획 자동화 — "무엇을 쓰면 클릭·조회·완독이 많을지"를 데이터로 정해 내일 24회차 편성표를 만든다(사장님 2026-09-23).
#   python work/planner.py            → work/research/plan_<내일>.md (블로그 24·카페 24 슬롯: 시리즈·주제·제목 초안·훅·담을 항목·출처)
# 신호(전부 지금 있는 파일·API): ① 검색수(topics.json) ② 마감(calendar.json) ③ 유튜브 상위 채널 제목·조회(research/yt/lessons_*.md, full/*/index.json)
#   ④ 우리 글 성과(perf_log.json·visitors_log.json·pkg/form.txt·axis.txt) ⑤ 카페 실측 조회 축 ⑥ 오늘 시장(Nasdaq 캘린더·히트맵 상위 등락) ⑦ 오늘 찾은 글감(topic-ideas.md)
import sys, os, re, json, glob, time, datetime, collections, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, 'research')
H = {'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'}
TOM = (datetime.date.today() + datetime.timedelta(days=1))
AXIS = {'tax': '세금연금', 'fire': '세금연금', 'us': '종목', 'kr': '종목', 'realestate': '부동산', 'macro': '종목', 'div': '배당현금흐름'}
CAFE_AXIS_VIEWS = {'커버드콜': 1169, '부업': 1111, '미국주식': 912, '배당': 857, 'ISA': 430, '파이어': 359}   # 파이어족 카페 600편 실측(2026-09-21)

def load(p, default):
    try: return json.load(open(p, encoding='utf-8'))
    except Exception: return default

def title_patterns():
    """유튜브 상위 채널 제목에서 조회수 가중으로 '먹히는 제목 모양'을 센다."""
    titles = []
    for f in glob.glob(os.path.join(R, 'yt', 'full', '*', 'index.json')):
        for v in load(f, {}).values(): titles.append((v.get('title', ''), v.get('views') or 0))
    for f in glob.glob(os.path.join(R, 'yt', 'lessons_*.md')):
        for line in open(f, encoding='utf-8'):
            m = re.match(r'- \*\*(.+?)\*\* \(([\d,]+)회', line)
            if m: titles.append((m.group(1), int(m.group(2).replace(',', ''))))
    if not titles: return {}, 0
    pats = {'숫자': r'\d', '질문': r'\?', '따옴표': r'["“”\']', '이유·방법': r'이유|방법|정리|총정리|법$', '자극어': r'수혜|기회|위기|폭락|급등|역대|충격|긴급', '나이·금액': r'\d+대|\d+억|\d+만원|\d+세', '비교': r'vs|차이|비교'}
    tot = sum(v for _, v in titles) or 1
    score = {k: round(sum(v for t, v in titles if re.search(p, t)) / tot * 100) for k, p in pats.items()}
    return score, len(titles)

def our_perf():
    perf = load(os.path.join(HERE, 'perf_log.json'), {}); byform = collections.defaultdict(list)
    forms = {}
    for pkg in glob.glob(os.path.join(R, '*', 'pkg')):
        tp, fp = os.path.join(pkg, 'title.txt'), os.path.join(pkg, 'form.txt')
        if os.path.exists(tp) and os.path.exists(fp): forms[open(tp, encoding='utf-8').read().strip()] = open(fp, encoding='utf-8').read().strip()
    for day, v in perf.items():
        for x in v.get('blog', []):
            f = forms.get(x.get('title', ''), '?'); byform[f].append(1 if (x.get('self_rank') or 99) <= 10 else 0)
    return {f: (round(sum(a) / len(a) * 100), len(a)) for f, a in byform.items() if a}

def market_today():
    out = []
    try:
        d = json.load(urllib.request.urlopen(urllib.request.Request(f'https://api.nasdaq.com/api/calendar/earnings?date={TOM.isoformat()}', headers=H), timeout=20))
        rows = d.get('data', {}).get('rows') or []
        big = sorted(rows, key=lambda r: -float(re.sub(r'[^\d.]', '', r.get('marketCap') or '0') or 0))[:6]
        if big: out.append('내일 실적: ' + ', '.join(f"{r['symbol']}({r.get('time','')})" for r in big))
    except Exception as e: out.append('실적 캘린더 실패 ' + str(e)[:40])
    try:
        d = json.load(urllib.request.urlopen(urllib.request.Request(f'https://api.nasdaq.com/api/calendar/economicevents?date={TOM.isoformat()}', headers=H), timeout=20))
        rows = [r for r in (d.get('data', {}).get('rows') or []) if r.get('country') in ('US', 'United States')][:6]
        if rows: out.append('내일 지표: ' + ', '.join(f"{r['eventName']}({r.get('gmt','')})" for r in rows))
    except Exception: pass
    return out

def ideas():
    p = os.path.join(R, 'topic-ideas.md')
    return [l.strip('- ').strip() for l in open(p, encoding='utf-8') if l.startswith('- ')][-12:] if os.path.exists(p) else []

def main():
    topics = load(os.path.join(HERE, 'topics.json'), []); topics = topics if isinstance(topics, list) else topics.get('topics', [])
    cal = load(os.path.join(HERE, 'calendar.json'), {}); events = cal.get('events', cal if isinstance(cal, list) else [])
    pats, ntitles = title_patterns(); perf = our_perf(); mkt = market_today(); idea = ideas()
    # 후보 점수: 검색수 × 마감 가중 × 축 로테이션
    cands = []
    for ev in events if isinstance(events, list) else []:
        try:   # calendar.json의 date는 'MM-DD' 또는 'MM-DD~MM-DD'(연도 없음)
            ds = str(ev.get('date') or ev.get('start') or '')[:5]; d0 = datetime.date(TOM.year, int(ds[:2]), int(ds[3:5]))
            if d0 < TOM - datetime.timedelta(days=60): d0 = d0.replace(year=TOM.year + 1)
            dd = (d0 - TOM).days
        except Exception: continue
        if not (-3 <= dd <= 30): continue
        kw = ev.get('name') or ev.get('title') or ev.get('kw'); kw = kw[0] if isinstance(kw, list) else str(kw)
        cands.append({'src': '마감', 'kw': kw, 'axis': AXIS.get(ev.get('axis'), '세금연금'), 'score': (ev.get('vol') or 1000) * (3 if dd <= 7 else 1.5), 'why': f'D{dd:+d}'})
    for t in sorted([x for x in topics if isinstance(x, dict) and not x.get('quote')], key=lambda x: -(x.get('vol') or 0))[:80]:
        cands.append({'src': '검색', 'kw': t['kw'], 'axis': AXIS.get(t.get('axis'), '종목'), 'score': (t.get('vol') or 0) * (0.5 if t.get('adcomp') == '높음' else 1), 'why': f"검색 {t.get('vol'):,}"})
    for i in idea: cands.append({'src': '오늘 글감', 'kw': i[:60], 'axis': '종목', 'score': 200000, 'why': '유튜브·카페에서 오늘 나온 것'})
    cands.sort(key=lambda c: -c['score'])
    # 시리즈 편성(series-plan.md)에 맞춰 슬롯을 채운다 — 각 시리즈의 후보를 데이터에서 뽑는다
    ETFS = ['SCHD', 'JEPQ', 'JEPI', 'QYLD', 'TIGER 미국배당다우존스', 'KODEX 미국배당커버드콜액티브', 'SOL 미국배당다우존스', 'ACE 미국배당다우존스', 'TIGER 미국나스닥100커버드콜', 'XYLD', 'DIVO', 'O(리얼티인컴)', 'VYM', 'HDV', 'DGRO', 'SPYD']
    STOCKS = ['SOXL', 'TIGER 미국S&P500', 'QQQ', 'QLD', 'SCHD', 'QQQM', 'KODEX 미국나스닥100', 'JEPQ', 'VOO', 'TIGER 미국배당다우존스', 'TQQQ', 'SPY', 'JEPI', 'NVDA 엔비디아', 'O 리얼티인컴', 'TSLA', 'MSFT', 'AAPL', 'AVGO', 'KO 코카콜라']
    CALC = [t['kw'] for t in sorted([x for x in topics if isinstance(x, dict) and '계산기' in x['kw']], key=lambda x: -(x.get('vol') or 0))][:24]
    CITIES = ['서울', '부산', '대구', '대전', '광주', '고양', '김해', '구미', '강릉', '경주', '목포', '춘천', '제주', '전주', '천안', '창원']
    AGES = ['30대', '40대', '50대', '60세 이상', '20대']
    VS = ['SCHD 직투 vs TIGER 미국배당다우존스', 'JEPI vs JEPQ', 'QQQ vs QQQM', 'VOO vs SPY', 'TQQQ vs QLD', '커버드콜 국내 3종(KODEX·TIGER·SOL)', 'ISA vs 연금저축', '달러예금 vs 미국 단기채 ETF']
    deadlines = [c for c in cands if c['src'] == '마감']
    seed = TOM.toordinal()
    def rot(lst, k): return lst[(seed + k) % len(lst)] if lst else '(후보 없음)'
    forms = {'B1': '② 계산 사례', 'B2': '① 원문 정리', 'B3': '④ 통계·기록', 'B4': '① 비교', 'B5': '③ 일정', 'B6': '③ 일정', 'B7': '① 원문 정리',
             'C1': '④ 기록', 'C3': '② 계산 사례', 'C4': '③ 일정', 'C5': '① 비교', 'C6': '① 원문 검증', 'C7': '④ 기록'}
    blog_series = ['B6', 'B1', 'B2', 'B3', 'B1', 'B2', 'B4', 'B5', 'B1', 'B2', 'B3', 'B7', 'B1', 'B2', 'B4', 'B1', 'B2', 'B5', 'B1', 'B2', 'B3', 'B4', 'B1', 'B2']
    cafe_series = ['C1', 'C3', 'C5', 'C1', 'C6', 'C4', 'C1', 'C3', 'C7', 'C1', 'C5', 'C1', 'C3', 'C6', 'C1', 'C5', 'C1', 'C3', 'C7', 'C1', 'C5', 'C6', 'C1', 'C3']
    def topic(sid, k):
        if sid == 'B1': return f'{rot(CALC, k)} 숫자 vs 실제 낼 돈'
        if sid == 'B2': return f'{rot(STOCKS, k)} 한 편(사업·실적·배당·보수·세금)'
        if sid == 'B3': return f'{rot(AGES, k)} 순자산·소득·부채 중앙값과 상위 10%(가계금융복지조사)'
        if sid == 'B4': return f'순자산 {rot(["3억","5억","7억","10억"], k)}으로 살 수 있는 도시({rot(CITIES, k)} 등, firemap_realestate)'
        if sid == 'B5': return (deadlines[k % len(deadlines)]['kw'] + ' — 마감 ' + deadlines[k % len(deadlines)]['why']) if deadlines else '마감 후보 없음(calendar.json 확인)'
        if sid == 'B6': return '미국증시 한 장(히트맵+4대 지수·환율·WTI·VIX, 이슈 5, 내일 일정) — heatmap.py'
        if sid == 'B7': return '30일 안에 시행되는 개정 법령(세법·연금·건보) — 법령 API 시행일'
        if sid == 'C1': return f'{rot(ETFS, k)} 배당 캘린더·이력(배당락·지급일·1주당, 세후 월 100만원 환산)'
        if sid == 'C3': return f'{rot(["3억","5억","7억","10억","1억"], k)}이면 월 얼마(SCHD·JEPQ·커버드콜·예금 세후)'
        if sid == 'C4': return '이번 주 미국 실적·배당락·경제지표 캘린더(Nasdaq API)'
        if sid == 'C5': return rot(VS, k)
        if sid == 'C6': return '이번 주 상위 유튜브 영상이 말한 숫자 3개 원문 검증(lessons_*.md에서)'
        if sid == 'C7': return '이번 주 내부자 매수 공시 상위 10(EDGAR Form 4·Nasdaq insider)'
        return '?'
    lines = [f'# 내일 편성 {TOM} (planner.py, 생성 {time.strftime("%H:%M")})', '',
             '## 데이터가 말하는 것', '- 유튜브 제목 %d개 조회 가중 패턴: ' % ntitles + ' · '.join(f'{k} {v}%' for k, v in sorted(pats.items(), key=lambda kv: -kv[1])),
             '- 우리 블로그 형식별 제목검색 10위 안 비율: ' + (' · '.join(f'형식{f} {p}%({n}편)' for f, (p, n) in perf.items()) if perf else '측정치 없음'),
             '- 카페 축 실측 조회 중앙값: ' + ' · '.join(f'{k} {v}' for k, v in CAFE_AXIS_VIEWS.items()), *[f'- {m}' for m in mkt], '',
             '## 제목 규칙(위 패턴에서): 숫자 1개 이상 필수, 나이·금액이 있으면 앞에, 질문형은 하루 3편 이하, 자극어 금지(우리 규칙), 비교형은 카페에.', '']
    lines += ['## 오늘 글감(유튜브·카페에서 자가발전 루틴이 모은 것 — 있으면 같은 축 슬롯을 대체)', *([f'- {i}' for i in idea] or ['- 없음']), '']
    for name, series in (('블로그', blog_series), ('카페', cafe_series)):
        lines.append(f'## {name} 24슬롯'); lines.append('| 시 | 시리즈 | 형식 | 주제 | 먼저 할 일 |'); lines.append('|---|---|---|---|---|')
        cnt = collections.Counter()
        for h, sid in enumerate(series):
            k = cnt[sid]; cnt[sid] += 1
            todo = 'stockwants' if sid in ('B2', 'C1', 'C3', 'C5') else 'toprank'
            lines.append(f"| {h:02d} | {sid} | {forms[sid]} | {topic(sid, k)} | {todo} → WebSearch 5건(한·영) → 1차 출처 → 초안 → 교차검증 |")
        lines.append('')
    p = os.path.join(R, f'plan_{TOM}.md'); open(p, 'w', encoding='utf-8').write('\n'.join(lines)); print('저장', p); print('\n'.join(lines[:12]))

if __name__ == '__main__': main()
