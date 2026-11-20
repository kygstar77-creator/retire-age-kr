"""SQ-1 calc_tax (2026-11-21): 같은 1억·같은 과거 값으로 '국내 상장 ETF(TIGER 미국나스닥100·미국배당다우존스 꼴)' vs
'미국 상장 ETF(QQQ·SCHD) 해외 직투' — 끝(2026-10 말)에 한 번에 팔면 세금 떼고 원화로 얼마가 남나.
세법 근거: tax_sources_1121.md (law.go.kr 조문 원문 raw/law1121/*.txt, 국세청 안내, 확인일 2026-11-21)
자료: raw/yh_SCHD_1112.json·raw/yh_QQQ_1112.json(야후 월봉 close·adjclose), raw/ecos_usdkrw_daily_1116.json(ECOS 731Y001 매매기준율 월말)
과거값이지 앞으로의 기대가 아니고, 투자 권유가 아니다.
실행: py -3.12 calc_tax.py > calc_tax_out_1121.txt   (SQ-1 폴더에서)
"""
import json, io, contextlib, sys
sys.stdout.reconfigure(encoding='utf-8')
with contextlib.redirect_stdout(io.StringIO()):
    import calc_mix as cm
import datetime as dt

# ── 자료 ────────────────────────────────────────────────────────────────
def load_close(s):
    r = json.load(open(f'raw/yh_{s}_1112.json', encoding='utf-8'))['chart']['result'][0]
    out = {}
    for t, c in zip(r['timestamp'], r['indicators']['quote'][0]['close']):
        d = dt.datetime.fromtimestamp(t, dt.UTC); out[(d.year, d.month)] = c
    return out
C = {'SCHD': load_close('SCHD'), 'QQQ': load_close('QQQ')}
A = {'SCHD': cm.S, 'QQQ': cm.Q}
rows = json.load(open('raw/ecos_usdkrw_daily_1116.json', encoding='utf-8'))['StatisticSearch']['row']
FX = {}
for r in rows:
    t = r['TIME']; FX[(int(t[:4]), int(t[4:6]))] = float(r['DATA_VALUE'])  # 달마다 마지막 영업일 값이 남음

# ── 세율(출처는 tax_sources_1121.md 번호) ──────────────────────────────
US_WHT = 0.15          # [R2] 한미조세조약 제12조②가 15%(국세청 제한세율표)
KR_DIV = 0.14          # [R3] 소득세법 제129조①2호나 14%
LOCAL = 0.10           # [R7] 지방세법 제103조의13 특별징수 = 소득세의 10% · 종합소득분 제92조① 표준세율표(캡처 raw/law1121/지방세법_제92조_표.png 11/21) = 제55조 세율의 1/10과 같음(②조례 ±50%는 무시)
CG_RATE = 0.20         # [R1] 소득세법 제104조①12호나 20%
CG_LOCAL = 0.02        # [R1] 지방세법 제103조의3①12호나 1천분의 20
CG_DED = 2_500_000     # [R1] 소득세법 제103조①2호 연 250만원
THRESH = 20_000_000    # [R4] 소득세법 제14조③6호 2천만원
BRACKETS = [(14_000_000, .06, 0), (50_000_000, .15, 1_260_000), (88_000_000, .24, 5_760_000),
            (150_000_000, .35, 15_440_000), (300_000_000, .38, 19_940_000), (500_000_000, .40, 25_940_000),
            (1_000_000_000, .42, 35_940_000), (float('inf'), .45, 65_940_000)]  # [R5] 제55조① 표(캡처 raw/law1121/소득세법_제55조_표.png, 마지막 개정 2022.12.31 → 2023 귀속부터 2026 귀속까지 같은 표)
def T(x):
    if x <= 0: return 0.0
    for top, r, d in BRACKETS:
        if x <= top: return x * r - d

def fin_tax(div, ftax, gain, other):
    """한 해 금융소득(배당 div + 국내 상장 매매차익 gain, 원)에 붙는 국세(소득세)·지방세.
    other = 금융소득 뺀 다른 종합소득 과세표준(소득공제 끝난 값으로 봄).
    2천만 이하: 원천징수로 끝(14%, 외국세 차감 129조④⑤·한도 14%).
    초과: 제62조 큰 금액 − 다른 소득만의 세액 = 금융소득 때문에 늘어난 세액, 외국납부세액공제는 제57조① 한도식(A×B/C, 캡처 11/21) 그대로."""
    F = div + gain
    if F <= 0: return 0.0, 0.0, False
    if F <= THRESH:
        nat = KR_DIV * F - min(ftax, KR_DIV * div)
        comp = False
    else:
        A = max(T(F - THRESH + other) + THRESH * KR_DIV, KR_DIV * F + T(other))   # 제62조 종합소득산출세액
        credit = min(ftax, A * div / (F + other))   # 제57조① 공제한도 = A × 국외원천소득/종합소득금액(other는 과세표준으로 근사)
        nat = A - T(other) - credit
        comp = True
    return nat, nat * LOCAL, comp

# ── 보유 흐름: 사고 그대로 둠(비율 맞춤 안 함 — 맞추면 매도라 과세가 생김) ──
def hold(w, start, end=(2026, 10)):
    ms = [m for m in cm.months if start <= m <= end]
    fx0 = FX[ms[0]]
    pos = {}
    for t, wt in (('SCHD', w), ('QQQ', 1 - w)):
        if wt > 0: pos[t] = {'usd': wt * 1e8 / fx0, 'basis': wt * 1e8}
    year = {}  # 연도 → [직투 배당소득(총액,원), 미국세(원), 국내상장 분배(세후기준가 기준, 원)]
    for p, m in zip(ms, ms[1:]):
        for t, h in pos.items():
            ar = A[t][m] / A[t][p]; cr = C[t][m] / C[t][p]
            dg = h['usd'] * max(ar - cr, 0.0)          # 이달 분배(총액, 달러) 어림 = 총수익 − 가격수익
            h['usd'] = h['usd'] * ar - US_WHT * dg      # 미국 15% 떼고 재투자
            k = dg * FX[m]
            h['basis'] += (1 - US_WHT) * k               # 재투자분은 그달 환율로 산 것
            y = year.setdefault(m[0], [0.0, 0.0, 0.0])
            y[0] += k; y[1] += US_WHT * k; y[2] += (1 - US_WHT) * k
    fx1 = FX[ms[-1]]
    val = sum(h['usd'] for h in pos.values()) * fx1
    basis = sum(h['basis'] for h in pos.values())
    return val, basis, year, ms[-1][0]

def scenario(w, start, other):
    val, basis, year, last = hold(w, start)
    gain = val - basis
    # 직투: 배당은 해마다 금융소득, 매매차익은 양도소득 분리과세(제4조①·제104조)
    d_tax = 0.0; d_comp = []
    for y, (dk, ft, _) in sorted(year.items()):
        n, l, c = fin_tax(dk, ft, 0.0, other); d_tax += n + l
        if c: d_comp.append(y)
    cg = max(gain - CG_DED, 0.0)
    d_cg = cg * (CG_RATE + CG_LOCAL)
    direct = val - d_tax - d_cg
    # 국내 상장: 분배·매매차익 모두 배당소득(제17조①5호·시행령 제26조의2), 판 해에 매매차익이 금융소득에 더해짐
    k_tax = 0.0; k_comp = []; k_last = None
    for y, (_, ft, dist) in sorted(year.items()):
        g = gain if y == last else 0.0
        n, l, c = fin_tax(dist, ft, g, other); k_tax += n + l
        if c: k_comp.append(y)
        if y == last: k_last = (dist, g, n + l)
    kr = val - k_tax
    # 판 해 매매차익이 2천만원 아래로 나뉘어 원천징수 15.4%로만 끝났다면(비교용)
    flat_last = (KR_DIV * k_last[1]) * (1 + LOCAL)
    return dict(val=val, basis=basis, gain=gain, direct=direct, d_tax=d_tax, d_cg=d_cg, d_comp=d_comp,
                kr=kr, k_tax=k_tax, k_comp=k_comp, k_last=k_last, flat_last=flat_last,
                divsum=sum(v[0] for v in year.values()), ussum=sum(v[1] for v in year.values()))

eok = lambda x: f'{x/1e8:.2f}억'
man = lambda x: f'{x/1e4:,.0f}만'
print('SQ-1 calc_tax — 1억원 한 번에 넣고 2026-10 말 한 번에 팔았을 때 세후 원화 (과거값, 투자 권유 아님)')
print('계산일 2026-11-21 · 세법 근거 tax_sources_1121.md · 현행(2026.11 확인) 세법을 모든 해에 똑같이 적용')
print('단순화(이 숫자를 쓸 때 같이 밝힐 것):')
print(' 1) 국내 상장 ETF = 같은 기간 QQQ·SCHD와 똑같이 움직였다고 봄(과표기준가 = 시장가, 국내 ETF 실제 가격·추적오차·상장일 무시 — TIGER 미국배당다우존스는 2023 상장이라 15·10년은 가상)')
print(' 2) 분배금: 야후 adjclose(총수익)−close(가격) 차로 달마다 분배액을 어림, 미국 15% 떼고 그달 재투자. 국내는 14%−외국세(한도 14%)=0이라 추가 원천징수 없음(직투 제129조④, 국내 상장 제129조⑤⑥)')
print(' 3) 2천만원 넘는 해의 종합과세 추가 세금은 그해 밖에서 내고 끝값에서 단순 차감(복리 영향 무시). 외국납부세액공제 한도 = 종합소득산출세액×국외원천소득/종합소득금액(제57조①), 129조⑦·57조② 이월공제는 넣지 않음')
print(' 4) 다른 소득: 0원 / 연 5,000만원(소득공제 끝난 종합소득 과세표준으로 봄) 두 갈래. 소득공제·세액공제(기본공제 등) 0으로 봄')
print(' 5) 섞은 비율(50%)은 처음 반반 사고 그대로 둠 — 매년 비율 맞춤은 파는 거래라 세금이 생겨 빼고 계산. 그래서 세전 끝값이 calc_krw(매년 맞춤 12.21억 등)와 다름')
print(' 6) 환전 수수료·보수 차이·증권거래 비용 제외. 직투 매매차익 원화 환산은 산 달·판 달 월말 매매기준율(국세청 안내는 결제일 환율)')
print(' 7) 배당가산(Gross-up): 직투 배당(제17조①6호)은 제17조③ 대상 아님, 국내 상장 ETF 분배(①5호)의 시행령 위임분은 확인 안 함 → 둘 다 가산 없이 계산')
print(' 7-2) 끝값이 calc_krw보다 낮은 까닭: calc_krw는 분배를 세금 없이 전액 재투자(adjclose), 여기는 미국 15%를 떼고 재투자')
print(' 8) 건강보험료(피부양자 자격·지역 보험료) 영향: 확인 필요(숫자 없음). 종합과세 지방소득세 표준세율표(지방세법 제92조) 표는 확인 안 함 → 소득세의 10%로 계산')
print()
for lbl, st in [('15년(2011-10→2026-10)', (2011, 10)), ('최근 10년(2016-10→2026-10)', (2016, 10)), ('최근 5년(2021-10→2026-10)', (2021, 10))]:
    print(f'■ {lbl}  환율 {FX[st]:,.1f} → {FX[(2026,10)]:,.1f}원')
    for w in [1.0, 0.5, 0.0]:
        a = scenario(w, st, 0); b = scenario(w, st, 50_000_000)
        print(f'  SCHD {int(w*100):>3}% (QQQ {int(100-w*100)}%): 국내 세금 전 원화 끝값 {eok(a["val"])}(미국 15% 원천징수는 이미 뺀 값) · 산 값(재투자 포함) {eok(a["basis"])} · 매매차익 {eok(a["gain"])} · 받은 분배 합 {eok(a["divsum"])}(미국 15% {man(a["ussum"])}원은 이미 빠짐)')
        for nm, s in (('다른 소득 0', a), ('다른 소득 5천만', b)):
            print(f'    [{nm}] 직투 세후 {eok(s["direct"])} (양도세 22% {man(s["d_cg"])}원 + 배당 종합과세 추가 {man(s["d_tax"])}원{" · 종합과세 해 "+",".join(map(str,s["d_comp"])) if s["d_comp"] else ""})'
                  f' | 국내 상장 세후 {eok(s["kr"])} (세금 {man(s["k_tax"])}원{" · 종합과세 해 "+",".join(map(str,s["k_comp"])) if s["k_comp"] else ""})'
                  f' | 차이(직투−국내) {(s["direct"]-s["kr"])/1e4:+,.0f}만원')
        dist, g, tl = b['k_last']; dista, ga, tla = a['k_last']
        print(f'    한 해에 몰아 판 값: 국내 상장 2026년 세금 다른 소득 0 {man(tla)}원 · 5천만 {man(tl)}원 vs 매매차익을 2천만원 밑으로 나눠 15.4%로만 끝났다면 {man(a["flat_last"])}원 → 늘어난 몫 {man(tla-a["flat_last"])}·{man(tl-b["flat_last"])}원')
    print()
print('읽는 법: 직투는 매매차익이 분리과세 22%(250만원 공제)로 끝. 국내 상장은 매매차익이 배당소득이라 판 해 금융소득이 2천만원을 넘으면 다른 소득과 합쳐 누진세율(최고 45%+지방 4.5%)로 감.')
