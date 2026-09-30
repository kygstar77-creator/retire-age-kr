# A-1 화면 재료 — voice.json(장·문장·길이) + 사실표 숫자 → work/video/a1.json (Remotion A1 컴포지션이 읽는다)
#   py -3.12 work/research/longform/ep/A-1/a1props.py
# 숫자는 전부 facts.txt와 ccvideo/ 원자료(extra.json·raw/*_10y.json)에서 온다. 목소리가 아직 없는 문장은 초당 6음절로 길이를 어림해
# 화면만 맞춰 보고(preview), 업로드는 missing=0일 때만 한다(PD 규칙).
import json, os, re, sys, datetime
sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.dirname(os.path.abspath(__file__))
CC = os.path.normpath(os.path.join(EP, '..', '..', '..', 'ccvideo'))
VID = os.path.normpath(os.path.join(EP, '..', '..', '..', '..', 'video'))
v = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
extra = json.load(open(os.path.join(CC, 'extra.json'), encoding='utf-8'))
FPS = 30

def series(tk, start, adj=False, step=5):
    r = json.load(open(os.path.join(CC, 'raw', f'{tk}_10y.json')))['chart']['result'][0]
    ts, q = r['timestamp'], (r['indicators']['adjclose'][0]['adjclose'] if adj else r['indicators']['quote'][0]['close'])
    pts = [(datetime.datetime.fromtimestamp(t, datetime.UTC).strftime('%Y-%m-%d'), c) for t, c in zip(ts, q) if c is not None]
    pts = [p for p in pts if start <= p[0] <= '2026-09-28']
    base = pts[0][1]; out = [(d, round((c / base - 1) * 100, 2)) for d, c in pts]
    return out[::step] + ([out[-1]] if (len(out) - 1) % step else [])

def pair(a, b, start, adj):
    A, B = series(a, start, adj), series(b, start, adj)
    return {'a': a, 'b': b, 'start': start, 'A': [p[1] for p in A], 'B': [p[1] for p in B], 'd0': A[0][0], 'd1': A[-1][0]}

PRICE = 'Yahoo Finance chart API(2025-09-26→2026-09-28 종가, 분배금 단순 합산)'
DATA = {
    0: dict(kind='open', data={'q': '커버드콜 ETF, 원금 깎이나요?', 'big': [['JEPQ', '1억 1,679만원', 11679], ['SCHD', '1억 2,462만원', 12462]],
            'dist': [['JEPQ', '분배금 12%'], ['SCHD', '분배금 4%']], 'note': '1억 · 1년(2025-09-26→2026-09-28) · 미국 세금 15% 뗌 · 환율 변동 제외'},
            source='Yahoo Finance chart API · 파이어맵 계산'),
    1: dict(kind='logo', data={'sub': '은퇴 나이, 숫자로'}),
    2: dict(kind='agenda', title='오늘 확인할 다섯 가지', data={'items': ['1년 뒤 남은 돈', '원금이 깎이나', '떨어진 해에는', '세금과 건보료', '월 100만원에 필요한 원금'],
            'extra': '+ 은퇴 나이가 몇 년 바뀌나'}),
    3: dict(kind='structure', title='커버드콜은 어디서 돈을 만들까', sub='JEPQ·JEPI 보유 구성 · 2026-09-28 기준',
            source='JPMorgan 일일 보유 종목 · SEC EDGAR JEPQ 497K(2025-11-01)',
            data={'flow': ['주식을 들고', '콜옵션을 팔고', '받은 프리미엄', '분배금'],
                  'quote1': 'through equity-linked notes (ELNs), selling call options', 'quote1ko': 'ELN(주가연계채권)을 통해 콜옵션을 판다',
                  'donut': [{'name': 'JEPQ', 'parts': [['주식 89종', 80.71], ['ELN 15개', 15.63]]}, {'name': 'JEPI', 'parts': [['주식 116종', 82.08], ['ELN 15개', 13.74]]}],
                  'quote2': 'it receives a premium but limits its opportunity to profit from an increase in the market value',
                  'quote2ko': '프리미엄을 받는 대신, 주가가 크게 올라도 정해진 가격 위 이익은 못 가져간다',
                  'quote3': 'the Fund may underperform the Benchmark, particularly in rising markets', 'quote3ko': '특히 오르는 장에서는 기준 지수보다 덜 벌 수 있다',
                  'steps': [0, 3, 4, 6]}),
    4: dict(kind='pairs', title='같은 코스피200, 커버드콜을 붙이면', sub='KODEX 200 vs KODEX 200타겟위클리커버드콜 · 2026-09-28 기준 공시',
            source='삼성자산운용 KODEX 공시(2026-09-28 기준)',
            data={'names': ['KODEX 200', 'KODEX 200타겟위클리커버드콜'], 'rows': [['최근 1년', 135.38, 109.58, '26%p 덜 벌었다'], ['최근 3개월', -20.20, -19.95, '0.25%p 차이']],
                  'steps': [1, 4]}),
    5: dict(kind='stack', rail=1, title='1년 들고 있었다면', sub='분배금 + 주가 변화 · 2025-09-26 → 2026-09-28', source=PRICE + ' · 삼성자산운용 KODEX 공시',
            data={'items': [['JEPI', 8.05, -0.76, 'cc'], ['SPY', 1.15, 15.68, 'idx'], ['SPYI', 12.17, 2.38, 'cc'], ['JEPQ', 11.82, 6.74, 'cc'],
                             ['QQQI', 14.17, 2.73, 'cc'], ['QQQ', 0.52, 23.59, 'idx'], ['SCHD', 3.88, 21.32, 'div']],
                  'total': {'JEPI': 7.29, 'SPY': 16.83, 'SPYI': 14.55, 'JEPQ': 18.56, 'QQQI': 16.9, 'QQQ': 24.1, 'SCHD': 25.19},
                  'show': [2, 3, 4, 5, 5, 6, 7], 'kodex': ['KODEX 미국배당커버드콜액티브', 10.86, 13.31], 'kodexAt': 9}),
    6: dict(kind='lines', rail=2, title='원금은 깎이나', source='Yahoo Finance chart API(종가·수정종가, 2026-09-28까지)',
            data={'panels': [dict(pair('JEPI', 'SPY', '2020-05-22', False), sub='주가만(분배금 제외) · 2020-05-22 → 2026-09-28', endA=12.81, endB=159.14),
                             dict(pair('JEPQ', 'QQQ', '2022-05-04', False), sub='주가만(분배금 제외) · 2022-05-04 → 2026-09-28', endA=19.60, endB=123.46),
                             dict(pair('JEPI', 'SPY', '2020-05-22', True), sub='분배금 재투자 · 2020-05-22 → 2026-09-28', endA=93.06, endB=183.34),
                             dict(pair('JEPQ', 'QQQ', '2022-05-04', True), sub='분배금 재투자 · 2022-05-04 → 2026-09-28', endA=94.45, endB=129.66)],
                  'at': [0, 3, 5, 6]}),
    7: dict(kind='neg', rail=3, title='2022년, 떨어진 해', sub='분배금 포함 1년 수익률 · 2021-12-31 → 2022-12-30', source='Yahoo Finance chart API(분배금 단순 합산)',
            data={'items': [['QQQ', -32.53, 'idx'], ['SPY', -18.15, 'idx'], ['JEPI', -3.70, 'cc'], ['SCHD', -3.37, 'div']], 'jepi': [-13.77, 10.07]}),
    8: dict(kind='won', title='1억을 넣었다면, 1년 뒤', sub='세후 분배금 + 평가금액 · 미국 세금 15% · 환율 변동 제외', source=PRICE + ' · 파이어맵 계산',
            data={'rows': [['SCHD', 330, 12132, 12462], ['JEPQ', 1005, 10674, 11679], ['SPY', 98, 11568, 11666], ['JEPI', 684, 9924, 10608]]}),
    9: dict(kind='holdings', title='안에 뭐가 들었나', sub='상위 10종목 비중(%) · 2026-09-28 기준', source='JPMorgan 일일 보유 종목 · Schwab Asset Management 전체 보유',
            data={'cols': [{'name': 'JEPI', 'top10': 18.34, 'note': '주식 116종', 'rows': [['MSFT', 1.99], ['AAPL', 1.93], ['NVDA', 1.92], ['META', 1.84], ['JNJ', 1.82], ['AMZN', 1.81], ['TT', 1.79], ['MA', 1.78], ['MMM', 1.73], ['GOOGL', 1.73]]},
                           {'name': 'JEPQ', 'top10': 43.04, 'note': '정보기술 48.6%', 'rows': [['NVDA', 7.35], ['AAPL', 6.49], ['MSFT', 5.14], ['MU', 4.88], ['GOOG', 4.68], ['AMD', 3.90], ['AMZN', 3.66], ['META', 2.92], ['TSLA', 2.01], ['LRCX', 2.01]]},
                           {'name': 'SCHD', 'top10': 41.55, 'note': '100종목', 'rows': [['QCOM', 4.64], ['TXN', 4.59], ['PG', 4.24], ['KO', 4.15], ['MRK', 4.12], ['CVX', 4.10], ['UNH', 3.97], ['AMGN', 3.97], ['VZ', 3.91], ['COP', 3.86]]}],
                  'at': [1, 2, 3]}),
    10: dict(kind='tax', rail=4, title='분배금 세금', sub='일반 증권 계좌 기준', source='소득세법 제129조 · 지방세법 제103조의13 · 삼성자산운용 KODEX 분배금 공시(최근 12회)',
             data={'cards': [['미국 상장 ETF 직접', '15%', '미국이 먼저 뗌 → 한국 추가 0원', '소득세법 제129조④ · 지방세법 제103조의13'],
                             ['국내 상장 ETF', '15.4%', '과세표준에만 뗌', '소득세법 제129조 · 지방소득세 1.4% 포함']],
                   'split': [{'name': 'KODEX 200타겟위클리커버드콜', 'total': 3126, 'taxed': 120}, {'name': 'KODEX 미국배당커버드콜액티브', 'total': 1184, 'taxed': 1184}],
                   'at': [0, 3, 4, 7]}),
    11: dict(kind='taxbars', title='국내 커버드콜 11종, 세금 붙는 몫', sub='과세표준 합 ÷ 분배금 합 · 최근 분배(최대 12회)', source='삼성자산운용 KODEX 분배금 공시(2026-09-30 조회)',
             data={'items': [['KODEX 200커버드콜액티브', 0.0, '국내주식', '분배 3회'], ['KODEX 미국30년국채타겟커버드콜(합성 H)', 0.0, '채권', ''],
                             ['KODEX 200타겟위클리커버드콜', 3.8, '국내주식', ''], ['KODEX 금융고배당TOP10타겟위클리커버드콜', 20.0, '국내주식', ''],
                             ['KODEX 미국성장커버드콜액티브', 47.4, '해외주식', '분배 9회'], ['KODEX 테슬라커버드콜채권혼합액티브', 49.4, '혼합자산', ''],
                             ['KODEX 미국나스닥100데일리커버드콜OTM', 78.4, '해외주식', ''], ['KODEX 미국S&P500데일리커버드콜OTM', 92.1, '해외주식', ''],
                             ['KODEX 미국배당다우존스타겟커버드콜', 92.7, '해외주식', ''], ['KODEX 미국AI테크TOP10타겟커버드콜', 100.0, '해외주식', ''],
                             ['KODEX 미국배당커버드콜액티브', 100.0, '해외주식', '']]}),
    12: dict(kind='line2k', title='금융소득 2천만원 선', sub='이자·배당 합계 연 2천만원 초과 → 종합과세', source='소득세법 제14조·제62조 · 국민건강보험법 제71조·시행령 제41조',
             data={'bars': [['미국 상장 ETF', '세후 월 141만 7천원', 1700, '세전 연 2,000만원'], ['KODEX 200타겟위클리커버드콜', '분배금 연 5억 2천만원', 52632, '과세표준 3.8%']],
                   'law': ['직장가입자: 보수 외 소득 연 2천만원 초과분에 보험료', '지역가입자: 연간 소득 ÷ 12', '시행령 제41조: 소득세법상 비과세 소득은 뺀다'],
                   'at': [1, 3, 4]}),
    13: dict(kind='monthly', title='분배금은 매달 같지 않다', sub='한 주당 분배금(달러) · 최근 12회', source='Yahoo Finance chart API(배당락일 기준)',
             data={'JEPQ': extra['monthly_JEPQ'], 'JEPI': extra['monthly_JEPI'], 'at': [1, 3]}),
    14: dict(kind='need', rail=5, title='세후 월 100만원, 원금은 얼마', sub='최근 12개월 분배금 유지 · 환율 변동 제외 · 일반 증권 계좌', source='파이어맵 계산(Yahoo Finance · 삼성자산운용 KODEX 공시)',
             data={'items': [['SCHD', 44118], ['JEPI', 17408], ['KODEX 미국배당커버드콜액티브', 14729], ['JEPQ', 12753], ['QQQI', 10230], ['KODEX 200타겟위클리커버드콜', 7869]],
                   'labels': {'SCHD': '4억 4천만원', 'JEPI': '1억 7,400만원', 'JEPQ': '1억 2,800만원', 'QQQI': '1억 200만원', 'KODEX 미국배당커버드콜액티브': '1억 4,700만원', 'KODEX 200타겟위클리커버드콜': '7,900만원'}}),
    15: dict(kind='summary', title='한 장 정리', source='이 영상의 모든 숫자 — 설명란 출처 목록',
             data={'cells': [['오른 1년', '지수 > 커버드콜', 'QQQ 24.10% · JEPQ 18.56%'], ['떨어진 2022년', '커버드콜·배당 덜 잃음', 'QQQ −32.53% · JEPI −3.70%'],
                             ['원금(주가만)', '깎이진 않았지만 덜 올랐다', 'JEPI +13% · SPY +159%'], ['세금 붙는 몫', '담은 자산 따라 0~100%', 'KODEX 커버드콜 11종']]}),
    16: dict(kind='age', title='은퇴 나이로 바꾸면', sub='파이어맵 계산기 · 연 수익률만 바꿔서', source='파이어맵 은퇴 계산기(retirementSimulator.js)',
             data={'inputs': [['현재 나이', '35세'], ['모아 둔 돈', '1억'], ['매달 저축', '300만원'], ['생활비', '월 300만원'], ['물가', '연 3%'], ['국민연금', '65세부터 월 100만원']],
                   'ages': [[3, 61], [4, 57], [5, 54], [6, 51], [7, 48], [8, 46]], 'at': [1, 2, 4]}),
    17: dict(kind='close', data={'quote': 'does not guarantee that distributions will always be paid or will be paid at a relatively stable level',
                                 'ko': '분배금이 항상, 또 안정된 수준으로 지급된다고 보장하지 않는다', 'src': 'JPMorgan JEPQ 설명서(SEC 497K, 2025-11-01)',
                                 'cta': ['ETF별 전체 표 → 파이어맵 카페', '내 은퇴 나이 → 파이어맵 계산기']}),
}

scenes = []
for i, sc in enumerate(v['sections']):
    d = DATA[i]; lines = []
    for l in sc['lines']:
        if l.get('audio'): lines.append({'text': l['text'], 'audio': l['audio'], 'frames': l['frames']})
        else:
            sec = len(re.findall('[가-힣0-9]', l['say'])) / 6.0
            lines.append({'text': l['text'], 'audio': None, 'frames': int(sec * FPS) + 12})
    frames = sum(x['frames'] for x in lines) + 24 if lines else 72
    title = d.get('title') or re.sub(r'^[\d\-\. \[]+|\s*·.*$|\]$', '', sc['title'])
    scenes.append({'kind': d['kind'], 'title': title, 'sub': d.get('sub'), 'source': d.get('source'), 'rail': d.get('rail', 0),
                   'data': d['data'], 'lines': lines, 'frames': frames})
missing = sum(1 for s in scenes for l in s['lines'] if not l['audio'])
out = {'fps': FPS, 'scenes': scenes, 'missing': missing}
json.dump(out, open(os.path.join(VID, 'a1.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print(f'장 {len(scenes)} · 길이 {sum(s["frames"] for s in scenes)/FPS/60:.1f}분 · 목소리 없는 문장 {missing}')

# ── 업로드 메타(meta.json) — 챕터 시각은 장 길이에서 계산(목소리가 다 차면 다시 돌려 맞춘다), 챕터 제목은 그 장의 결론 문장(RULES 관찰 2026-09-30)
CHAP = {0: 'JEPQ 1억 1,679만원 vs SCHD 1억 2,462만원', 3: '커버드콜은 ELN으로 콜옵션을 판다(JEPQ ELN 15.63%)', 4: '코스피200 커버드콜, 오른 1년 26%p 덜 벌었다',
        5: '1년 합계 SCHD 25.19%, JEPQ 18.56%, JEPI 7.29%', 6: '주가만 보면 원금은 안 깎였지만 지수만큼 오르지 못했다', 7: '2022년 JEPI −3.70%, QQQ −32.53%',
        8: '1억 넣었다면 SCHD가 가장 많이 남았다', 9: 'JEPQ 상위 10종목 43%, 엔비디아 7.35%', 10: '미국 상장 15%, 국내 상장은 과세표준에만 15.4%',
        11: '국내 커버드콜 11종, 세금 붙는 몫 0~100%', 12: '금융소득 2천만원·건보료는 과세표준으로 따진다', 13: 'JEPQ 분배금 가장 많은 달이 가장 적은 달의 1.58배',
        14: '세후 월 100만원: JEPQ 1억 2,800만원, SCHD 4억 4천만원', 15: '한 장 정리', 16: '수익률 2%포인트 차이 = 은퇴 나이 6년'}
t, chap = 0, []
for i, s in enumerate(scenes):
    if i in CHAP: chap.append(f'{t // FPS // 60}:{t // FPS % 60:02d} {CHAP[i]}')
    t += s['frames']
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
pub = now.replace(hour=19, minute=30, second=0, microsecond=0)
if pub < now + datetime.timedelta(hours=1): pub += datetime.timedelta(days=1)
desc = '\n'.join([
    'JEPQ와 SCHD에 1억씩 넣고 1년(2025.9.26→2026.9.28) 지나니, 세금 떼고 남은 돈은 JEPQ 1억 1,679만원, SCHD 1억 2,462만원이었습니다(환율 변동 제외).',
    '커버드콜 ETF(JEPQ·JEPI·QQQI·SPYI·KODEX 200타겟위클리커버드콜)의 원금, 2022년 하락, 세금·건보료, 세후 월 100만원에 필요한 원금을 운용사 공시와 법령 원문으로 비교했습니다.',
    '내 은퇴 나이 계산(영상 끝 장면 계산기): https://firemap.kr/?utm_source=youtube&utm_medium=longform&utm_campaign=A-1',   # 9/30 회의 배정
    '', *chap, '',
    '출처',
    '· 1년 가격·분배금(미국 상장): Yahoo Finance chart API, 2025-09-26 종가 → 2026-09-28 종가(분배금 단순 합산)',
    '· 2022년·설정 이후·월 분배금·주가만 수익·재투자 수익: Yahoo Finance chart API(종가·수정종가)',
    '· KODEX 수익률·분배금·과세표준: 삼성자산운용 KODEX 공시(2026-09-28 기준, 분배금 최근 12회)',
    '· 보유 종목: JPMorgan 일일 보유(JEPI·JEPQ, 2026-09-28) · Schwab Asset Management 전체 보유(SCHD, 2026-09-28)',
    '· JEPQ 설명서: SEC EDGAR 497K(2025-11-01)',
    '· 세법·건보: 소득세법 제14조·제62조·제129조, 지방세법 제103조의13, 국민건강보험법 제71조·시행령 제41조(국가법령정보센터)',
    '· 은퇴 나이: 파이어맵 은퇴 계산기(35세·1억·월 300만원 저축·생활비 월 300만원·물가 3%·국민연금 65세 월 100만원 가정)',
    '',
    'ETF별 전체 표(카페): https://cafe.naver.com/firemap',
    '',
    '계산은 일반 증권 계좌 기준이며 ISA·연금계좌는 방식이 다릅니다. 특정 상품을 사거나 팔라는 뜻이 아니고, 지난 숫자가 앞으로를 보장하지 않습니다.',
    '이 영상의 내레이션은 AI 음성(Google Gemini TTS)입니다. 숫자와 대본은 파이어맵이 1차 출처로 확인했습니다.'])
meta = {'video': os.path.join(VID, 'out', 'a1.mp4'), 'thumb': os.path.join(EP, 'thumb.png'),
        'title': 'JEPQ와 SCHD, 1억 넣고 1년 뒤 실제로 남은 돈은? 커버드콜 ETF 원금·세금 비교',
        'desc': desc, 'tags': ['JEPQ', 'SCHD', '커버드콜ETF', 'KODEX200타겟위클리커버드콜', '배당ETF'],
        'publishAt': pub.isoformat(timespec='seconds'), 'synthetic': True, 'veo': False, 'missing': missing,
        'synthetic_why': '공식 도움말 14328491 공개 대상 3가지엔 해당하지 않는다고 읽히나 일반 TTS 해설은 목록에 이름이 없어 애매 → RULES 4장(애매하면 켠다)·공개해도 노출·수익 불이익 없음(같은 도움말)에 따라 켠다.',
        'answers': json.load(open(os.path.join(EP, 'answers.json'), encoding='utf-8')) if os.path.exists(os.path.join(EP, 'answers.json')) else {}}
json.dump(meta, open(os.path.join(EP, 'meta.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('meta.json 예약', meta['publishAt'], '· 챕터', len(chap))
