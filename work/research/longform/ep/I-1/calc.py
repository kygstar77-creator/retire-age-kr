# I-1 calc — 같은 돈·같은 ETF, 계좌만 바꾼 5년 세후 영수증 (youtube-loop 2026-10-11)
# 자료: raw/funetf_360750_nav.json(일별 종가 clsp·기준가 fp·과표기준가 taxFp, 제로인 funetf 집계 — 종가는 야후 360750.KS와 6개 날짜 일치 확인)
#       raw/funetf_360750_div.json(분배금 기준일·주당 금액)
# 세법: facts.txt [T1~T3] 일반 15.4% · [L1·L2] ISA 200/400만원 비과세 뒤 9.9% 분리과세 · [L7] 손익통산
# 과세식(운용사 상품 페이지 원문, raw/tiger_360750_taxnote.txt): 매매차익 Min(매매차익, 과표 증분)×15.4% · 분배금 Min(현금분배금, 과표증분)×15.4%
# 가정(화면에 그대로 밝힌다): 매년 10/11 이후 첫 거래일 종가로 2천만원어치 정수 주 매수(5번, 총 1억원), 분배금은 세후 현금으로 기준일 3거래일 뒤 종가에 다시 삼,
#   끝은 마지막 자료일 종가에 전부 매도. 수수료·호가 차이 무시. ISA 안 소득도 같은 배당소득 계산식(Min)으로 셈.
import json, os, math
H = os.path.dirname(os.path.abspath(__file__))
nav = sorted(json.load(open(os.path.join(H, 'raw/funetf_360750_nav.json'), encoding='utf-8')), key=lambda r: r['gijunYmd'])
divs = sorted(json.load(open(os.path.join(H, 'raw/funetf_360750_div.json'), encoding='utf-8')), key=lambda r: r['gijunYmd'])
days = [r['gijunYmd'] for r in nav]
P = {r['gijunYmd']: r['clsp'] for r in nav}
TX = {r['gijunYmd']: r['taxFp'] for r in nav}

def on_or_after(d):
    for x in days:
        if x >= d: return x
    return None

def plus(d, k):
    i = days.index(d); return days[min(i + k, len(days) - 1)]

END = days[-1]
BUYS = [on_or_after(f'{y}1011') for y in range(2021, 2026)]
AMT = 20_000_000

def run(kind, buys=BUYS):
    """kind: 'gen'(일반 15.4% 원천) | 'isa'(계좌 안 비과세 누적, 해지 때 정산)"""
    lots = []  # [day, qty, price, taxFp]
    cash = 0.0; paid_in = 0; tax = 0.0; isa_income = 0.0; dist_gross = 0.0; bind = []
    fin_by_year = {}
    events = [(b, 'buy') for b in buys]
    prev_rec = None
    for dv in divs:
        rec = dv['gijunYmd']
        if rec < buys[0] or rec > END: prev_rec = rec if rec <= END else prev_rec; continue
        events.append((rec, 'div', dv['divAmt'], prev_rec)); prev_rec = rec
    events.sort(key=lambda e: (e[0], 0 if e[1] == 'div' else 1))
    pending = []  # (day, cash) 재투자
    def reinvest_upto(day):
        nonlocal cash
        for p in [p for p in pending if p[0] <= day]:
            pending.remove(p)
            q = int(cash // P[p[0]])
            if q: lots.append([p[0], q, P[p[0]], TX[p[0]]]); cash -= q * P[p[0]]
    for e in events:
        reinvest_upto(e[0])
        if e[1] == 'buy':
            d = e[0]; cash += AMT; paid_in += AMT
            q = int(cash // P[d]); lots.append([d, q, P[d], TX[d]]); cash -= q * P[d]
        else:
            rec, _, amt, prev = e
            sh = sum(l[1] for l in lots)
            if not sh: continue
            base_prev = TX[on_or_after(prev)] if prev and on_or_after(prev) else TX[on_or_after(buys[0])]
            dtx = TX[rec] - base_prev
            taxable_ps = max(0.0, min(amt, dtx))
            if taxable_ps < amt: bind.append((rec, amt, round(dtx, 2)))
            gross = amt * sh; dist_gross += gross
            y = rec[:4]; fin_by_year[y] = fin_by_year.get(y, 0) + taxable_ps * sh
            if kind == 'gen':
                t = math.floor(taxable_ps * sh * 0.154); tax += t; cash += gross - t
            else:
                isa_income += taxable_ps * sh; cash += gross
            pending.append((plus(rec, 3), None))
    reinvest_upto(END)
    # 끝: 전부 매도
    sell = P[END]; txe = TX[END]; gain_taxable = 0.0; gross_sale = 0.0
    for d, q, p, tx in lots:
        gross_sale += q * sell
        gain_taxable += max(0.0, min(sell - p, txe - tx)) * q  # 손실 lot 없음 확인은 아래
    loss_lots = [l for l in lots if sell < l[2]]
    fin_by_year[END[:4]] = fin_by_year.get(END[:4], 0) + gain_taxable
    if kind == 'gen':
        t = math.floor(gain_taxable * 0.154); tax += t
        final = gross_sale + cash - t
    else:
        isa_income += gain_taxable
        final_pre = gross_sale + cash
    out = dict(kind=kind, paid_in=paid_in, lots=len(lots), shares=sum(l[1] for l in lots), dist_gross=round(dist_gross),
               gain_taxable=round(gain_taxable), loss_lots=len(loss_lots), bind=bind, fin_by_year={k: round(v) for k, v in fin_by_year.items()})
    if kind == 'gen':
        out.update(tax=round(tax), final=round(final))
    else:
        for lab, ex in (('isa_general', 2_000_000), ('isa_seomin', 4_000_000)):
            t = math.floor(max(0.0, isa_income - ex) * 0.099)
            out[lab] = dict(income=round(isa_income), exempt=ex, tax=t, final=round(final_pre - t))
    return out

if __name__ == '__main__':
    g = run('gen'); i = run('isa')
    L = []
    L.append(f'# I-1 calc_out — 실행 자료 마지막 날 {END} (TIGER 미국S&P500 360750)')
    L.append(f'[K0] 매수일 {BUYS} · 1회 {AMT:,}원 · 총 {g["paid_in"]:,}원 · 매도 {END} 종가 {P[END]:,.0f}원 · 과표기준가 {TX[END]}')
    L.append(f'[K1] 첫 매수 종가 {P[BUYS[0]]:,.0f}원 → 끝 {P[END]:,.0f}원 ({P[END]/P[BUYS[0]]*100-100:.1f}%)')
    L.append(f'[G1] 일반계좌: 낸 세금 합계 {g["tax"]:,}원 · 세후 손에 쥔 돈 {g["final"]:,}원 · 분배금 받은 총액(세전) {g["dist_gross"]:,}원 · 매도 과세 차익 {g["gain_taxable"]:,}원')
    for k in ('isa_general', 'isa_seomin'):
        r = i[k]; L.append(f'[I_{k}] ISA({"일반형" if k=="isa_general" else "서민형"}): 계좌 안 과세 대상 소득 {r["income"]:,}원 − 비과세 {r["exempt"]:,}원 → 세금 {r["tax"]:,}원 · 해지 때 손에 쥔 돈 {r["final"]:,}원 · 일반계좌보다 {r["final"]-g["final"]:+,}원')
    L.append(f'[I0] ISA 분배금 총액(세전) {i["dist_gross"]:,}원 · 재투자 lot {i["lots"]} vs 일반 {g["lots"]} · 최종 주수 ISA {i["shares"]} vs 일반 {g["shares"]}')
    L.append(f'[X1] 분배금 Min이 과표증분 쪽으로 걸린 분기: {g["bind"] or "없음"} · 손실 lot: 일반 {g["loss_lots"]}·ISA {i["loss_lots"]}')
    L.append(f'[X2] 일반계좌 해마다 배당소득(과세분) {g["fin_by_year"]} — 매도한 해({END[:4]})에 2천만원 넘는지: {"넘음" if g["fin_by_year"][END[:4]] > 20_000_000 else "안 넘음"} (소득세법 §14③6 이자·배당 합계 2천만원 이하만 분리과세, raw/sodeuk_14.txt)')
    st = math.floor(g['gain_taxable'] * 0.154)
    L.append(f'[G2] 일반계좌 세금 나눔: 판 날 {st:,}원 + 분배금 원천징수 {g["tax"]-st:,}원')
    L.append(f'[I2] 세금 차이(일반 − ISA 일반형) {g["tax"]-i["isa_general"]["tax"]:,}원 · 나머지 {i["isa_general"]["final"]-g["final"]-(g["tax"]-i["isa_general"]["tax"]):,}원은 분배금을 세금 떼기 전 금액으로 다시 산 몫')
    s = '\n'.join(L); print(s)
    open(os.path.join(H, 'calc_out.txt'), 'w', encoding='utf-8').write(s + '\n')
