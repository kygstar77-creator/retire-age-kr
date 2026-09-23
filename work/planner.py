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

def written_titles():
    """이미 쓴 묶음의 제목 — 같은 종목·같은 각도를 내일 또 배정하지 않기 위해(유사문서 회피)."""
    out = []
    for tp in glob.glob(os.path.join(R, '*', 'pkg', 'title.txt')):
        try: out.append(open(tp, encoding='utf-8').read().strip())
        except Exception: pass
    return out

def used(cand, titles):
    """후보 문자열의 핵심어(티커·상품명)가 이미 쓴 제목에 있으면 True."""
    key = re.split(r'[\s(]', str(cand).replace('(리얼티인컴)', ' 리얼티인컴'))[0].strip()
    if len(key) < 2: return False
    return any(key.lower() in t.lower() for t in titles)

def our_perf():
    """형식(form.txt)별 성과. form.txt가 있는 묶음만 센다 — 표기 없는 글을 '형식?'으로 묶어
    비율을 내면 측정하지 않은 것을 측정한 것처럼 보이므로(2026-09-23 수정) 개수만 따로 돌려준다."""
    perf = load(os.path.join(HERE, 'perf_log.json'), {}); byform = collections.defaultdict(list)
    forms = {}
    for pkg in glob.glob(os.path.join(R, '*', 'pkg')):
        tp, fp = os.path.join(pkg, 'title.txt'), os.path.join(pkg, 'form.txt')
        if os.path.exists(tp) and os.path.exists(fp): forms[open(tp, encoding='utf-8').read().strip()] = open(fp, encoding='utf-8').read().strip()
    unlabeled = 0
    for day, v in perf.items():
        for x in v.get('blog', []):
            f = forms.get(x.get('title', '').strip())
            if not f: unlabeled += 1; continue
            byform[f].append(1 if (x.get('self_rank') or 99) <= 10 else 0)
    return {f: (round(sum(a) / len(a) * 100), len(a)) for f, a in byform.items() if a}, unlabeled

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
    pats, ntitles = title_patterns(); perf, unlabeled = our_perf(); mkt = market_today(); idea = ideas()
    wtitles = written_titles()
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
    # 블로그 B2도 배당주·ETF·성장주 세 갈래를 번갈아 돈다(사장님 2026-09-23 밤).
    STOCKS = ['SOXL(ETF)', '리얼티인컴(O·배당주)', '엔비디아(NVDA·성장주)', 'TIGER 미국S&P500(ETF)',
              '코카콜라(KO·배당주)', '마이크로소프트(MSFT·성장주)', 'QQQ(ETF)', '존슨앤존슨(JNJ·배당주)',
              '애플(AAPL·성장주)', 'SCHD(ETF)', '알트리아(MO·배당주)', '브로드컴(AVGO·성장주)',
              'QLD(ETF)', '버라이즌(VZ·배당주)', '테슬라(TSLA·성장주)', 'JEPQ(ETF)',
              '펩시코(PEP·배당주)', 'KODEX 미국나스닥100(ETF)', 'VOO(ETF)', 'TQQQ(ETF)']
    CALC = [t['kw'] for t in sorted([x for x in topics if isinstance(x, dict) and '계산기' in x['kw']], key=lambda x: -(x.get('vol') or 0))][:24]
    CITIES = ['서울', '부산', '대구', '대전', '광주', '고양', '김해', '구미', '강릉', '경주', '목포', '춘천', '제주', '전주', '천안', '창원']
    AGES = ['30대', '40대', '50대', '60세 이상', '20대']
    VS = ['SCHD 직투 vs TIGER 미국배당다우존스', 'JEPI vs JEPQ', 'QQQ vs QQQM', 'VOO vs SPY', 'TQQQ vs QLD', '커버드콜 국내 3종(KODEX·TIGER·SOL)', 'ISA vs 연금저축', '달러예금 vs 미국 단기채 ETF']
    deadlines = [c for c in cands if c['src'] == '마감']
    seed = TOM.toordinal()
    def rot(lst, k):
        if not lst: return '(후보 없음)'
        fresh = [x for x in lst if not used(x, wtitles)]
        if fresh: return fresh[(seed + k) % len(fresh)]
        return lst[(seed + k) % len(lst)] + ' ※이미 쓴 주제 — 각도를 바꾸거나 교체할 것'
    # 2026-09-23 사장님: "시리즈로 올릴 부동산이랑 주식이랑 배당 등등 많은데 왜 그런 글은 아예 안 올라오지?"
    # 원인: series-plan.md에 적힌 B8·B9·B10·B11(부동산 4종)과 C8(배당 히트맵)이 이 표에 통째로 빠져 있었다.
    # 편성에 없으니 회차가 쓸 일이 없었다. 실제로 카페 48편 중 부동산은 1편뿐이었다.
    LIVE = ['치앙마이 님만해민', '리스본 캄포 데 오리케', '쿠알라룸푸르 몽키아라']                    # B9 (series-plan)
    DONG = ['공덕동', '옥수동', '상계동']                                                        # B11 (series-plan)
    UNDER = ['서울 25개 구 전세가율 순위', '고점 대비 20% 넘게 내린 단지 10', '오피스텔 월세 수익률 상위 10',
             '같은 구 평당가 편차 상위', '공시가격 대비 실거래 비율']                              # B10 지표(series-plan)
    HEAT = ['배당귀족 30종목 히트맵', '월배당 ETF 12종 히트맵', '국내 고배당 히트맵', '이번 주 배당 인상·삭감 발표 종목']  # C8·B12

    def heat_tool(topic):
        if '인상' in topic or '삭감' in topic:
            return 'divchange.py(나스닥 배당 캘린더의 이번 주 발표를 직전 회차와 대조해 인상·삭감·동결·주기변경으로 가른다)'
        return 'heatmap.py --list <종목들>'
    # 사장님 2026-09-23: "배당 히트맵은 카페뿐만 아니라 블로그도 올려야지" → B12
    # 사장님 2026-09-23: "주식 종목별로 조사하고 검증해서 종목 발굴하는 글은?" → B13
    DIG = ['내부자 매수가 몰린 종목(EDGAR Form 4 코드 P)', '배당 10년 이상 늘린 종목',
           '시총 상위 중 올해 낙폭 큰 종목', '배당률 높은데 배당성향 낮은 종목', '이번 주 실적 발표 예정 종목']  # B13
    # 사장님 2026-09-14: "파이어 후기 같은 거 좀 찾아서 올려봐 스토리텔링 잘된 걸로, 해외 사례도 많이 찾아오고,
    #   파이어 해서 어디에 거주하고 있고 거주비는 얼마인지" → B14. 지어내지 않고 실제 글·인터뷰를 찾아 링크한다.
    CASE = ['해외 파이어족 인터뷰(매체 보도 원문)', '레딧 r/financialindependence 올해 은퇴 후기',
            '레딧 r/leanfire 생활비 공개 글', '파이어 그만두고 복귀한 사람 이야기', '국내 파이어 후기(카페·블로그 공개글)']  # B14
    # 사장님 2026-09-22 20:01: "블로그 글을 미국 주식 종목, ETF 종목 분석하는 것도 한 종목에 하나씩 올리면 되지 않을까?
    #   대신 엄청 자료조사 잘해야겠지? **카페에도 배당주, ETF 한 종목씩 분석해서** 글 올리면 되지 않을까?"
    #   블로그는 B2로 돌고 있었는데 카페판이 없었다 → C9. C1(ETF 분배금 장부)과 달리 개별 배당주를 다룬다.
    # 사장님 2026-09-23 밤: "배당주 ETF 성장주 등등 종목 분석해서 올리고 하는 건 블로그랑 카페에 다 올려야지"
    #   → 카페 C9도 배당주만이 아니라 ETF·성장주를 함께 돈다. 블로그 B2의 목록에도 배당주를 넣어 세 갈래가 양쪽에 다 나간다.
    DIVSTOCK = ['리얼티인컴(O·배당주)', 'SCHD(ETF)', '엔비디아(NVDA·성장주)', '코카콜라(KO·배당주)',
                'JEPQ(ETF)', '마이크로소프트(MSFT·성장주)', '존슨앤존슨(JNJ·배당주)', 'TIGER 미국배당다우존스(ETF)',
                '애플(AAPL·성장주)', '알트리아(MO·배당주)', 'QQQ(ETF)', '브로드컴(AVGO·성장주)',
                '버라이즌(VZ·배당주)', 'KODEX 미국배당커버드콜액티브(ETF)', '테슬라(TSLA·성장주)',
                '펩시코(PEP·배당주)', 'VOO(ETF)', '맥도날드(MCD·배당주)']  # C9 — 배당주·ETF·성장주 번갈아
    forms = {'B1': '② 계산 사례', 'B2': '① 원문 정리', 'B3': '④ 통계·기록', 'B4': '① 비교', 'B5': '③ 일정', 'B6': '③ 일정', 'B7': '① 원문 정리',
             'B8': '③ 일정', 'B9': '① 비교', 'B10': '② 계산 사례', 'B11': '① 비교', 'B12': '④ 통계·기록', 'B13': '④ 통계·기록', 'B14': '① 원문 정리',
             'C1': '④ 기록', 'C3': '② 계산 사례', 'C4': '③ 일정', 'C5': '① 비교', 'C6': '① 원문 검증', 'C7': '④ 기록', 'C8': '④ 기록', 'C9': '① 원문 정리'}
    # 사장님 2026-09-20: "나이 월급 연봉 등도 관심 많고 남들이랑 비교하는 게 제일 관심 많지 않아?",
    #   "부동산도 상급지 중급지 하급지 얼마 벌면 어디 살고 이런 비교글을 한국인이 제일 좋아하지 않아?"
    #   → 비교 축(B3 나이대별·B4 도시별)을 하루 1칸에서 2칸씩으로 올린다.
    #              00    01    02     03     04     05    06    07    08     09    10     11    12    13     14    15    16     17     18    19     20     21    22    23
    blog_series = ['B2', 'B3', 'B10', 'B13', 'B14', 'B4', 'B6', 'B8', 'B12', 'B2', 'B10', 'B9', 'B8', 'B11', 'B3', 'B1', 'B13', 'B10', 'B5', 'B14', 'B12', 'B8', 'B4', 'B7']
    cafe_series = ['C1', 'C3', 'C5', 'C8', 'C9', 'C6', 'C3', 'C1', 'C5', 'C8', 'C7', 'C9', 'C3', 'C5', 'C6', 'C8', 'C1', 'C4', 'C3', 'C9', 'C8', 'C1', 'C5', 'C7']
    def topic(sid, k):
        if sid == 'B1': return f'{rot(CALC, k)} 숫자 vs 실제 낼 돈'
        if sid == 'B2': return f'{rot(STOCKS, k)} 한 편(사업·실적·배당·보수·세금)'
        if sid == 'B3': return f'{rot(AGES, k)} 순자산·소득·부채 중앙값과 상위 10%(가계금융복지조사)'
        if sid == 'B4': return f'순자산 {rot(["3억","5억","7억","10억"], k)}으로 살 수 있는 도시({rot(CITIES, k)} 등, firemap_realestate)'
        if sid == 'B5': return (deadlines[k % len(deadlines)]['kw'] + ' — 마감 ' + deadlines[k % len(deadlines)]['why']) if deadlines else '마감 후보 없음(calendar.json 확인)'
        # 수페TV 구조 그대로 여섯 코너. 2026-09-23 아침에 여섯 개로 정해 놓고 표에는 네 개만 적어 두었다.
        if sid == 'B6': return ('미국증시 한 장(수페TV 구조 6코너) — ① heatmap.py 히트맵 1장 + 4대 지수·미10년(apis.fred DGS10)·'
                                '원달러·WTI·VIX 한 줄 ② 오늘 이슈 5개(경제지표 실제/예상, 금리, 실적 결과) '
                                '③ 섹터·종목 등락(히트맵 요약) ④ 내부자 매수(insider.py)·실적 서프라이즈 '
                                '⑤ 내일 일정(실적·지표·배당락) ⑥ 한국 투자자 숫자(원달러, 국내 상장 미국 ETF 등락)')
        if sid == 'B7': return '30일 안에 시행되는 개정 법령(세법·연금·건보) — 법령 API 시행일'
        if sid == 'B8': return ('부동산 한 장 — heatmap_re.py로 구별 히트맵 1장(jeonse/yield/offi/price 중 어제와 다른 것) + 어제 실거래 신고 상위 + 코픽스·주담대(apis.finlife) + 오늘 정책·청약 일정')
        if sid == 'B9': return f'{rot(LIVE, k)} 실제 매물 5~8건(동네·단지명·월세·면적·방 수·부대시설·층·게시 링크) + 생활비·비자·환율'
        if sid == 'B10': return f'{rot(UNDER, k)} — 국토부 실거래로 계산(권유 문구 금지, 지표와 순위만)'
        if sid == 'B11': return f'{rot(DONG, k)} 자동 손품 — sonpum.py로 네이버 부동산 녹화 + 같은 재료로 단지별 표'
        if sid == 'B12':
            t = rot(HEAT, k)
            return f'{t}(블로그판: 종목별 배당률·배당락일 표를 같이) — {heat_tool(t)} + Nasdaq 배당 API'
        if sid == 'B13': return f'{rot(DIG, k)} — Nasdaq 스크리너(무키 7,100종목)·EDGAR Form 4(insider.py)·배당 이력으로 추린 목록. "사라·사지 마라"는 쓰지 않고 조건과 순위만'
        if sid == 'B14': return (f'{rot(CASE, k)} — 실제 글·인터뷰를 찾아 **원문 링크와 날짜를 달고** 나이·자산·생활비·거주지를 표로. '
                                 '사례를 지어내지 않는다. 못 찾으면 그 슬롯은 건너뛰고 note에 적는다')
        if sid == 'C8':
            t = rot(HEAT, k)
            return f'{t} — {heat_tool(t)} + 이번 주 배당 뉴스(한·영 WebSearch)'
        if sid == 'C9': return (f'{rot(DIVSTOCK, k)} 한 종목 분석(카페판) — 배당주는 배당 이력·배당률·배당성향, ETF는 분배금·보수·구성, 성장주는 실적·주가·배당 유무. 공통으로 '
                                '세후 월 얼마·같은 계열 대안 한 개. stockwants로 사람들이 치는 항목부터 채우고 '
                                'Nasdaq 배당 API·apis.av_quote·회사 IR로 확인한 숫자만 쓴다')
        if sid == 'C1': return f'{rot(ETFS, k)} 배당 캘린더·이력(배당락·지급일·1주당, 세후 월 100만원 환산)'
        if sid == 'C3': return f'{rot(["3억","5억","7억","10억","1억"], k)}이면 월 얼마(SCHD·JEPQ·커버드콜·예금 세후)'
        if sid == 'C4': return '이번 주 미국 실적·배당락·경제지표 캘린더(Nasdaq API)'
        if sid == 'C5': return rot(VS, k)
        if sid == 'C6': return '이번 주 상위 유튜브 영상이 말한 숫자 3개 원문 검증(lessons_*.md에서)'
        if sid == 'C7': return '이번 주 내부자 매수 공시 상위 10(EDGAR Form 4·Nasdaq insider)'
        return '?'
    lines = [f'# 내일 편성 {TOM} (planner.py, 생성 {time.strftime("%H:%M")})', '',
             '## 데이터가 말하는 것', '- 유튜브 제목 %d개 조회 가중 패턴: ' % ntitles + ' · '.join(f'{k} {v}%' for k, v in sorted(pats.items(), key=lambda kv: -kv[1])),
             '- 우리 블로그 형식별 제목검색 10위 안 비율: ' + (' · '.join(f'형식{f} {p}%({n}편)' for f, (p, n) in perf.items()) if perf else '측정 불가(form.txt 표기된 발행분 없음)') + f' / 형식 표기 없는 글 {unlabeled}편은 제외',
             '- 카페 축 실측 조회 중앙값: ' + ' · '.join(f'{k} {v}' for k, v in CAFE_AXIS_VIEWS.items()), *[f'- {m}' for m in mkt], '',
             '## 제목 규칙: **work/research/titlerule.md를 본다**(titlestudy.py가 네이버 상위 노출 제목을 긁어 잰 값). '
             '2026-09-23 측정 — 길이 38자 · 명사로 끝 80%/물음 15%/다 5% · 물음표 43%·쉼표 24%·구분자 없음 24% · 숫자 0~1개 71% · 반전 연결 26% · 독자 지칭 9%. '
             '손으로 정한 규칙(숫자 1개 이상 필수, 질문형 하루 3편 이하)은 측정과 어긋나 폐기했다. 자극어 금지는 유지(우리 규칙).', '']
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
