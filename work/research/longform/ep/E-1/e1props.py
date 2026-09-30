# E-1 화면 재료 — script.md(장·문장) + voice.json(있으면 길이) + 원자료 → work/video/e1.json (Remotion E1 컴포지션이 읽는다)
#   py -3.12 work/research/longform/ep/E-1/e1props.py
# 숫자는 전부 원자료(quarters.json·raw/nasdaq_MU.json·raw/naver_*.txt·form4.json·fireage.json·facts.txt [6])에서 계산한다.
# 분기는 quarters.json의 마지막 8개를 쓰므로 루프가 마이크론 4분기를 build_facts로 넣으면 다시 돌리기만 하면 된다.
# 목소리가 없는 문장은 초당 5.5음절(RULES 목소리 규칙 2 목표)로 길이를 어림해 화면만 본다(preview). 업로드는 missing=0일 때만.
# 장면은 제목 열쇠말로 찾고, 문장 시점은 '그 문장에 든 말'로 찾는다 — 루프가 문장·장을 더해도 어긋나지 않게.
import json, os, re, sys, datetime
sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(EP, '..', '..', '..', '..'))
VID = os.path.join(WORK, 'video')
sys.path.insert(0, WORK)
import lfvoice
FPS = 30

# ── 원자료 ──
def mu_prices():
    rows = json.load(open(os.path.join(EP, 'raw', 'nasdaq_MU.json'), encoding='utf-8'))['data']['tradesTable']['rows']
    out = []
    for r in rows:
        m, d, y = r['date'].split('/'); out.append((f'{y}{m}{d}', float(r['close'].replace('$', '').replace(',', ''))))
    return sorted(out)
def kr_prices(code):
    txt = open(os.path.join(EP, 'raw', f'naver_{code}.txt'), encoding='utf-8').read()
    return sorted((d, float(c)) for d, c in re.findall(r'\["(\d{8})",\s*[\d.]+,\s*[\d.]+,\s*[\d.]+,\s*([\d.]+)', txt))
def window(pts, a='20250929', b='20260929'):
    return [p for p in pts if a <= p[0] <= b]
def mdd(pts):
    best, pk, out = 0, pts[0], None
    for p in pts:
        if p[1] > pk[1]: pk = p
        dd = p[1] / pk[1] - 1
        if dd < best: best, out = dd, (pk[0], p[0])
    return round(best * 100, 1), out
PR = {'마이크론': window(mu_prices()), 'SK하이닉스': window(kr_prices('000660')), '삼성전자': window(kr_prices('005930'))}
PRICE = {}
for k, pts in PR.items():
    dd, (pk, tr) = mdd(pts); r1 = round((pts[-1][1] / pts[0][1] - 1) * 100, 1)
    step = max(1, len(pts) // 90); thin = pts[::step] + ([pts[-1]] if (len(pts) - 1) % step else [])
    PRICE[k] = {'d': [p[0] for p in thin], 'v': [round(p[1] / pts[0][1] * 100, 1) for p in thin], 'ret': r1, 'dd': dd, 'peak': pk, 'trough': tr,
                'first': pts[0], 'last': pts[-1]}
# 사실표 [4]와 기계 대조 — 어긋나면 화면을 만들지 않는다
FACT4 = {'마이크론': (549.8, -39.1, '20260625', '20260729'), 'SK하이닉스': (412.9, -54.7, '20260622', '20260730'), '삼성전자': (226.6, -42.9, '20260618', '20260730')}
for k, (r, d, pk, tr) in FACT4.items():
    p = PRICE[k]; assert (p['ret'], p['dd'], p['peak'], p['trough']) == (r, d, pk, tr), (k, p['ret'], p['dd'], p['peak'], p['trough'])

Q = json.load(open(os.path.join(EP, 'quarters.json'), encoding='utf-8'))
FACTS = open(os.path.join(EP, 'facts.txt'), encoding='utf-8').read()
# 마이크론 회계 4분기(2026-09-03 끝) — SEC companyfacts엔 10-K 제출 전이라 없다 → 8-K 보도자료(facts [12]) 숫자를 넣고, 사실표 원문 줄과 기계 대조
MU_Q4 = {'k': '2026-09-03', 'rev': 54229, 'op': 43751}
assert f"매출 {MU_Q4['rev']:,} · 영업이익 {MU_Q4['op']:,}" in FACTS, 'facts [12] 마이크론 4분기 숫자 불일치'
if MU_Q4['k'] not in Q['마이크론']['매출']:
    Q['마이크론']['매출'][MU_Q4['k']] = {'v': MU_Q4['rev'] * 1e6, 'calc': False, 'src': '8-K'}
    Q['마이크론']['영업이익'][MU_Q4['k']] = {'v': MU_Q4['op'] * 1e6, 'calc': False, 'src': '8-K'}
SEG = [['데이터센터', 1577, 18002], ['클라우드 메모리', 4543, 16283], ['모바일·PC', 3760, 13114], ['자동차·임베디드', 1434, 6824]]
assert 'Cloud Memory 16,283 / 4,543 · Core Data Center 18,002 / 1,577 · Mobile and Client 13,114 / 3,760 · Automotive and Embedded 6,824 / 1,434' in FACTS
GUIDE = {'lo': 490, 'hi': 510, 'act': 542.29, 'next': 615, 'pm': 15}
assert '매출 $50.0B ± $1.0B(= 490억~510억 달러)' in FACTS and '매출 $61.5B ± $1.5B' in FACTS
DS = {'rev': [1301282, 2092317], 'op': [248581, 1428593], 'dx_op': [128527, 21489], 'share': 97.4, 'dx_share': 1.5}
assert '영업이익 1,428,593(142조 8,593억원, 전사 영업이익 중 비중 97.4%)' in FACTS and '연간 DS 매출 1,301,282' in FACTS and '영업이익 21,489(2조 1,489억원' in FACTS
HY = [['2024년', 661930], ['2025년', 971467], ['2026년 상반기', 1318950]]      # 억원
assert '131,895,033(131조 8,950억원)' in FACTS and '97,146,675(97조 1,467억원)' in FACTS and '66,192,960(66조 1,930억원)' in FACTS
def daysb(a, b): return (datetime.date.fromisoformat(b) - datetime.date.fromisoformat(a)).days
def qlabel(co, k):
    if co == '마이크론': y, m, _ = k.split('-'); return f"{y[2:]}.{m}"      # 분기 끝 달(회계 분기와 달력 분기가 달라 끝 달로 적는다)
    return f"{k[2:4]}.{k[-1]}Q"
QS = {}
for co in ('마이크론', 'SK하이닉스', '삼성전자'):
    ks = sorted(Q[co]['매출'])[-8:]; unit = 1e8 if co == '마이크론' else 1e12      # 억 달러 / 조원
    rev = [round(Q[co]['매출'][k]['v'] / unit, 1) for k in ks]
    op = [Q[co]['영업이익'][k]['v'] for k in ks]
    QS[co] = {'q': [qlabel(co, k) for k in ks], 'keys': ks, 'rev': rev, 'unit': '억 달러' if co == '마이크론' else '조원',
              'margin': [round(o / Q[co]['매출'][k]['v'] * 100, 1) for o, k in zip(op, ks)],
              'opx': round(op[-1] / op[-5], 2), 'revx': round(Q[co]['매출'][ks[-1]]['v'] / Q[co]['매출'][ks[-5]]['v'], 2),
              'calc': [Q[co]['매출'][k]['calc'] for k in ks]}
k9 = sorted(Q['마이크론']['매출'])[-9:]
QS['마이크론']['margin9'] = [round(Q['마이크론']['영업이익'][k]['v'] / Q['마이크론']['매출'][k]['v'] * 100, 1) for k in k9]
QS['마이크론']['q9'] = [qlabel('마이크론', k) for k in k9]
MK = sorted(Q['마이크론']['매출'])
WEEKS = [round(daysb(MK[-2], MK[-1]) / 7), round(daysb(MK[-6], MK[-5]) / 7)]      # 이번 분기 / 1년 전 같은 분기(주)
assert WEEKS == [14, 13], WEEKS
assert (QS['마이크론']['opx'], QS['마이크론']['revx'], QS['마이크론']['margin'][-1], QS['마이크론']['margin'][-5], QS['마이크론']['margin9'][0]) == (11.97, 4.79, 80.7, 32.3, 19.6), QS['마이크론']
F4 = json.load(open(os.path.join(EP, 'form4.json'), encoding='utf-8'))
sells = [r for r in F4 if r['code'] == 'S']; buys = [r for r in F4 if r['code'] == 'P']
who = {}
for r in sells:
    w = who.setdefault(r['who'], {'title': r['title'], 'sh': 0, 'usd': 0}); w['sh'] += r['shares']; w['usd'] += r['shares'] * r['price']
top = sorted(who.items(), key=lambda x: -x[1]['usd'])[:4]
FORM4 = {'n': len(sells), 'buys': len(buys), 'sh': round(sum(r['shares'] for r in sells)), 'usd': round(sum(r['shares'] * r['price'] for r in sells) / 1e6, 1),
         'rows': [[n.title(), w['title'], round(w['sh']), round(w['usd'] / 1e6, 2)] for n, w in top]}
AGE = json.load(open(os.path.join(EP, 'fireage.json'), encoding='utf-8'))

# ── 장면 지정(제목 열쇠말 → 종류·재료). 목록에 없는 장은 'bullets'(문장 카드)로 나온다 ──
PSRC = '나스닥 공식 과거 시세(MU) · 네이버 금융 일별 시세(000660·005930) · 2025-09-29 → 2026-09-29 종가'
QSRC = 'SEC XBRL companyfacts(마이크론 CIK 723125) · Micron 8-K(2026-09-30, 4분기) · OpenDART 단일회사 주요계정(연결)'
CO3 = ['마이크론', 'SK하이닉스', '삼성전자']
SPEC = [
    ('여는', lambda L: dict(kind='open', source=PSRC, data={'p': PRICE['SK하이닉스'], 'name': 'SK하이닉스', 'at': [0, L('54.7'), L('다섯 배 올랐어도'), L('회계 4분기'), L('공시 원문')],
                                                                         'q4': f"마이크론 4분기 매출 {GUIDE['act']:.0f}억$ · 영업이익률 {QS['마이크론']['margin'][-1]}%"})),
    ('로고', lambda L: dict(kind='logo', data={'sub': '은퇴 나이, 숫자로'})),
    ('다섯 가지', lambda L: dict(kind='agenda', title='오늘 볼 다섯 가지', data={'items': ['1년 주가와 최대 낙폭', '여덟 분기 매출', '이익률', '주가 vs 이익', '회사가 적은 위험'],
                                 'extra': '+ 내 은퇴 나이는 몇 년 바뀌나', 'at': [L('다섯 가지를'), L('1년 주가와'), L('은퇴 계획')]})),
    ('최대 낙폭', lambda L: dict(kind='price', rail=1, title='1년 주가와 최대 낙폭', sub='같은 출발점 100 · 2025-09-29 → 2026-09-29 종가', source=PSRC,
                                 data={'cos': [dict(PRICE[c], name=c) for c in CO3], 'at': [L('마이크론은 163'), L('SK하이닉스는 34만'), L('삼성전자는 8만'),
                                       L('가장 크게 빠진'), L('마이크론은 6월'), L('삼성전자는 6월'), L('SK하이닉스는 6월'), L('같은 여름')]})),
    ('매출:mu', lambda L: dict(kind='mu8', rail=2, title='마이크론 여덟 분기 매출', sub='분기 매출(억 달러) · 분기 끝 달 · 1년 전 같은 분기는 테두리', source=QSRC.split(' · ')[0] + ' · Micron 8-K(2026-09-30, 4분기)',
                          data=dict(QS['마이크론'], weeks=WEEKS, at=[0, L('결산 시점'), L('542억'), L('14주')]))),
    ('매출:guide', lambda L: dict(kind='guide', rail=2, title='회사 전망 vs 실제 — 마이크론 4분기 매출', sub='억 달러 · 전망은 2026-06-24 회사 발표(GAAP)', source='Micron 8-K(2026-06-24 3분기·2026-09-30 4분기 보도자료) · SEC EDGAR',
                          data=dict(GUIDE, at=[0]))),
    ('매출:seg', lambda L: dict(kind='seg', rail=2, title='마이크론 사업부별 매출', sub='백만 달러 · 1년 전 같은 분기(2025-08) vs 이번 분기(2026-09)', source='Micron 8-K(2026-09-30) 보도자료 사업부 매출 · SEC EDGAR',
                          data={'rows': SEG, 'at': [0]})),
    ('매출:kr', lambda L: dict(kind='revenue', rail=2, title='세 회사 여덟 분기 매출', sub='분기 매출 · 1년 전 같은 분기는 테두리 · 마이크론은 분기 끝 달', source=QSRC,
                          data={'cos': [dict(QS[c], name=c) for c in CO3], 'at': [0, 0, L('SK하이닉스는 올해'), L('삼성전자는 171'), L('스마트폰')]})),
    ('매출:ds', lambda L: dict(kind='dsdx', rail=2, title='삼성전자 반도체(DS) 부문만', sub='억원 · 2025년 12개월 vs 2026년 상반기 6개월 · 부문 간 내부거래 포함', source='삼성전자 2026 반기보고서(2026-08-14) 사업부문별 요약 재무 현황 · DART',
                          data=dict(DS, at=[0, L('209조'), L('130조'), L('142조'), L('97.4%')]))),
    ('매출:hy', lambda L: dict(kind='stairs', rail=2, title='SK하이닉스 매출, 해마다', sub='억원 · 2026년은 상반기 6개월만', source='SK하이닉스 사업보고서(2024·2025)·2026 반기보고서 매출실적 · DART',
                          data={'rows': HY, 'x': round(HY[2][1] / HY[1][1], 2), 'at': [0]})),
    ('같은 가격표:q', lambda L: dict(kind='quotes2', title='같은 가격표, 다른 표정', sub='회사가 반기보고서에 직접 적은 가격 변화', source='삼성전자·SK하이닉스 2026 반기보고서(2026-08-14) · DART',
                          data={'cards': [['삼성전자 · 주요 제품 가격 변동 현황', '메모리 평균 판매가격은 전년 연간 평균 대비', '약 220% 상승'],
                                          ['SK하이닉스 · 가격변동추이(2분기, 전분기 대비)', 'D램 평균 가격 30% 중반 상승 · 낸드 평균 가격', '50% 중반 상승']],
                                'at': [0, L('삼성전자 반기'), L('SK하이닉스도 2분기')]})),
    ('같은 가격표:s', lambda L: dict(kind='scale', title='같은 가격표, 다른 표정 — 삼성전자 안에서', sub='2026년 상반기 영업이익(억원) · 파는 쪽 DS vs 사는 쪽 DX', source='삼성전자 2026 반기보고서(2026-08-14) 사업부문별 요약·주요 원재료 가격 변동 추이 · DART',
                          data=dict(DS, at=[0, L('211%'), L('2조 1,489'), L('웃고'), L('나눌 수 없')]))),
    ('이익률', lambda L: dict(kind='margin', rail=3, title='이익률 — 100원 팔아 얼마 남기나', sub='분기 영업이익 ÷ 매출(%) · 마이크론은 9분기(분기 끝 달), 한국 2사는 8분기(아래 줄)', source=QSRC,
                           data={'cos': [dict(QS[c], name=c) for c in CO3], 'at': [L('마이크론은 1년 전'), L('100원어치'), L('SK하이닉스는 41'), L('삼성전자는 회사'), L('2년 전으로')]})),
    ('나란히', lambda L: dict(kind='twin', rail=4, title='이익은 몇 배, 주가는 몇 배', sub='영업이익: 최근 분기 ÷ 1년 전 같은 분기 · 주가: 1년', source=QSRC + ' · ' + PSRC.split(' · 2025')[0],
                           data={'rows': [[c, QS[c]['opx'], round(PRICE[c]['last'][1] / PRICE[c]['first'][1], 2)] for c in CO3],
                                 'at': [L('마이크론은 36억'), L('SK하이닉스는 9조'), L('삼성전자는 4조'), L('같은 1년 동안'), L('특히 삼성'), L('기간도')]})),
    ('누가 팔았나', lambda L: dict(kind='form4', title='마이크론 임원·이사 거래', sub='Form 4 · 2026-04-01 ~ 2026-08-28 제출분 · 공개시장 거래만',
                                source='SEC EDGAR Form 4(마이크론 임원·이사)', data=dict(FORM4, at=[L('Form 4라는'), L('237건'), L('0건'), L('메로트라'), L('10b5-1'), L('짐작')]))),
    ('위험', lambda L: dict(kind='risk', rail=5, title='회사가 스스로 적은 위험', sub='Micron FY2025 Form 10-K(2025-10-03 제출) 위험 요인', source='Micron FY2025 Form 10-K · SEC EDGAR',
                         data={'quotes': [['In the past five years, annual percentage changes in DRAM average selling prices have ranged from plus low 40% to a minus high 40% range.',
                                           '지난 5년, D램 평균 판매 가격의 연간 변화율은 +40% 초반 ~ −40% 후반'],
                                          ['In some prior periods, average selling prices for our products have been below our manufacturing costs',
                                           '어떤 시기에는 판매 가격이 제조 원가보다 낮았다'],
                                          ['we face the threat of increasing competition and DRAM and NAND oversupply due to significant investment in the semiconductor industry, including by the Chinese government',
                                           '중국 정부를 포함한 대규모 투자로 경쟁·공급 과잉 위협이 커진다']],
                               'at': [L('10-K에'), L('지난 5년'), L('어떤 시기'), L('중국'), L('40% 넘게'), L('80% 이익률')]})),
    ('일정:o', lambda L: dict(kind='outlook', title='마이크론 다음 분기 — 회사 전망', sub='분기 매출(억 달러) · 점선은 회사 추정치, 맞는다는 보장 없음', source='Micron 8-K(2026-09-30) 보도자료 · SEC EDGAR',
                         data=dict(QS['마이크론'], next=GUIDE['next'], pm=GUIDE['pm'], at=[0, L('발표 날짜')]))),
    ('일정', lambda L: dict(kind='calendar', title='다음 일정', sub='회사가 공지한 날짜만', source='Micron IR 보도자료 · DART(확인되는 대로)',
                         data={'items': [['마이크론 회계 4분기 실적', '발표함 — 2026-10-01 새벽(한국)', True], ['마이크론 다음 실적', '보도자료에 날짜 없음', False],
                                         ['삼성전자·SK하이닉스 3분기 실적', '공시 전 — 확인되면 고정 댓글', False]], 'at': [0, 0]})),
    ('은퇴', lambda L: dict(kind='age', title='이 흔들림을 내 은퇴 계획에 넣으면', sub='파이어맵 은퇴 계산기 · 연 5%·물가 3%·국민연금 65세 월 100만원 가정',
                         source='파이어맵 은퇴 계산기(retirementSimulator)',
                         data={'inputs': [['나이', '35세'], ['모은 돈', '1억원'], ['매달 저축', '300만원'], ['생활비', '월 300만원'], ['수익률', '연 5%']],
                               'bars': [['그대로', 0, AGE['out']['none']['asset'] // 10000, AGE['out']['none']['age']], ['마이크론 낙폭', 39.1, AGE['out']['mu']['asset'] // 10000, AGE['out']['mu']['age']],
                                        ['삼성전자 낙폭', 42.9, AGE['out']['samsung']['asset'] // 10000, AGE['out']['samsung']['age']], ['SK하이닉스 낙폭', 54.7, AGE['out']['hynix']['asset'] // 10000, AGE['out']['hynix']['age']]],
                               'at': [L('35세에'), L('54세에'), L('4,530'), L('마이크론 낙폭'), L('300만원이')]})),
    ('정리', lambda L: dict(kind='summary', title='한 장 정리', sub='1년 전 같은 분기 대비 · 주가는 2025-09-29 → 2026-09-29', source=' · '.join(QSRC.split(' · ')[:2]) + ' · OpenDART · ' + PSRC.split(' · 2025')[0],
                         data={'head': ['', '주가 1년', '최대 낙폭', '매출', '영업이익률', '영업이익'],
                               'rows': [[c, f"+{PRICE[c]['ret']}%", f"−{abs(PRICE[c]['dd'])}%", f"{QS[c]['revx']:.2f}배", f"{QS[c]['margin'][-5]}% → {QS[c]['margin'][-1]}%", f"{QS[c]['opx']:.2f}배"] for c in CO3],
                               'at': [0, L('39%에서'), L('40% 넘게'), L('앞으로 오를지')]})),
]

v = None
vj = os.path.join(EP, 'voice.json')
if os.path.exists(vj):
    v = json.load(open(vj, encoding='utf-8'))
secs = v['sections'] if v else [{'title': s['title'], 'lines': [{'text': t, 'say': lfvoice.speak(EP, t), 'audio': None} for t in s['lines']]} for s in lfvoice.sections(EP)]

SPLIT = {'여덟 분기 매출': [('매출:mu', None), ('매출:guide', '6월에 내놓은'), ('매출:seg', '사업부로'), ('매출:kr', 'SK하이닉스는 올해'), ('매출:ds', '그래서 8월에'), ('매출:hy', 'SK하이닉스도 비슷')],
         '같은 가격표': [('같은 가격표:q', None), ('같은 가격표:s', '반대편 숫자')],
         '다음 일정': [('일정:o', None), ('일정', '삼성전자와 SK하이닉스 3분기')]}
def chunks(sc):
    rule = next((v for k, v in SPLIT.items() if k in sc['title']), None)
    if not rule: return [dict(sc, key=None)]
    cut = []
    for key, word in rule:
        i = 0 if word is None else next(j for j, l in enumerate(sc['lines']) if word in l['text'])
        cut.append((i, key))
    return [dict(sc, key=key, lines=sc['lines'][i:(cut[n + 1][0] if n + 1 < len(cut) else None)]) for n, (i, key) in enumerate(cut)]
secs = [c for sc in secs for c in chunks(sc)]

def clean(t):   # 빈자리 표시는 화면 자막에서 뺀다(미리보기용 — 빈자리가 있으면 업로드 안 됨)
    return re.sub(r'\{\{Q4:\s*|\}\}', '', t)
scenes = []
for sc in secs:
    lines = []
    for l in sc['lines']:
        if l.get('audio'): lines.append({'text': clean(l['text']), 'audio': l['audio'], 'frames': l['frames']})
        else: lines.append({'text': clean(l['text']), 'audio': None, 'frames': int(lfvoice.syl(l['say']) / 5.5 * FPS) + 8})
    texts = [l['text'] for l in sc['lines']]
    def L(word, _t=texts):
        for i, t in enumerate(_t):
            if word in t: return i
        return -1                                  # 문장이 없으면(예: Q4 채운 뒤 문구 변경) 그 단계는 장면 끝에 나오지 않게 -1
    spec = next((fn for k, fn in SPEC if k == sc['key']), None) or next((fn for k, fn in SPEC if ':' not in k and k in sc['title']), 'none')
    d = spec(L) if spec not in ('none', None) else dict(kind='bullets', data={})
    frames = sum(x['frames'] for x in lines) + 18 if lines else 72
    title = d.get('title') or re.sub(r'^[\d\-\. \[]+|\s*·.*$|\]$', '', sc['title'])
    scenes.append({'kind': d['kind'], 'title': title, 'sub': d.get('sub'), 'source': d.get('source'), 'rail': d.get('rail', 0),
                   'data': d['data'], 'lines': lines, 'frames': frames})
missing = sum(1 for s in scenes for l in s['lines'] if not l['audio'])
holes = sum(1 for s in secs for l in s['lines'] if '{{' in l['text'] or '○' in l['text'])
out = {'fps': FPS, 'scenes': scenes, 'missing': missing, 'holes': holes}
json.dump(out, open(os.path.join(VID, 'e1.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print(f'장 {len(scenes)} · 길이 {sum(s["frames"] for s in scenes)/FPS/60:.1f}분 · 목소리 없는 문장 {missing} · 대본 빈자리 {holes}')
print('종류', sorted({s['kind'] for s in scenes}))
bad = [(s['title'], k) for s in scenes for k, v2 in [('at', s['data'].get('at', []))] for x in v2 if x == -1]
if bad: print('문장 못 찾은 단계', bad)
for c in CO3: print(c, '분기', QS[c]['q'][0], '→', QS[c]['q'][-1], '· 이익 몇 배', QS[c]['opx'], '· 매출 몇 배', QS[c]['revx'])
