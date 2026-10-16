# X-1 환율 편 계산 v2 (2026-10-16 밤 자료조사 담당) — 옛 판(끝날 10/12)은 calc_v1_1012.py · calc_out_1012.txt.
#   py -3.12 work/research/longform/ep/X-1/calc.py            → calc_out.txt
# 원문: raw/collect_20261016.json (collect_1016.py가 받음)
#   - 한국은행 ECOS 731Y001 원/달러(0000001)·원/100엔(0000002) 매매기준율, 일별 2024-01-02~
#   - 야후 SPY·QQQ 종가(가격, 배당 미포함) · 네이버 증권 하나은행 USD 고시 · 국내 상장 ETF 종가(KRX, 네이버 siseJson)
# 날짜 규칙(옛 판과 같음): 같은 달력 날짜에 미국 종가와 한국 매매기준율이 둘 다 있는 날. 시작일이 빠지면 그 앞의 가장 가까운 날.
#   미국 종가는 받은 날(한국 날짜) 이전 날짜만 쓴다(미국 장이 아직 안 끝난 날 제외).
# 끝날 = 둘 다 있는 마지막 날. 환전 수수료·세금·배당은 넣지 않는다(매매기준율 그대로 — 실제 환전보다 유리한 값).
# 공개 전날(10/21) collect_1016.py → calc.py를 다시 돌려 끝날만 바꾼다.
import json, os, sys, statistics
sys.stdout.reconfigure(encoding='utf-8')
D = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(D, 'raw', 'collect_20261016.json')
o = json.load(open(RAW, encoding='utf-8'))
cut = o['fetched'][:10]
ymd = lambda k: k[:4] + '-' + k[4:6] + '-' + k[6:]
usd = {ymd(k): v for k, v in o['USD']}; jpy = {ymd(k): v for k, v in o['JPY100']}
spy = {k: v for k, v in o['SPY'] if k < cut}; qqq = {k: v for k, v in o['QQQ'] if k < cut}
both = sorted(set(usd) & set(spy))
def on(d, keys=both):
    c = [x for x in keys if x <= d]; return c[-1]
END = both[-1]
STARTS = [('1년 전', '2025-10-13'), ('올해 첫날', '2026-01-02'), ('환율 최고점', '2026-07-02'), ('석 달 전', '2026-07-13')]
W = lambda x: f'{x:,.0f}'
out = [f'원문 {os.path.basename(RAW)} (받은 시각 {o["fetched"]}) · 끝날 {END}: 원/달러 {usd[END]:,} · 원/100엔 {jpy[END]} · SPY {spy[END]:.2f} · QQQ {qqq[END]:.2f}',
       f'참고: ECOS 최신 {max(usd)} 원/달러 {usd[max(usd)]:,} · 원/100엔 {jpy[max(jpy)]}', '']

out.append('## 1. 1억원을 그날 달러로 바꿔 두었다면(매매기준율, 수수료 없음) → 끝날 원화')
for name, s in STARTS + [('2024년 첫날(예외)', '2024-01-02')]:
    d = on(s); dollars = 1e8 / usd[d]; now = dollars * usd[END]
    out.append(f'{name} {d}: 환율 {usd[d]:,} → 달러 {dollars:,.0f} → {W(now)}원 ({now-1e8:+,.0f}원, {(now/1e8-1)*100:+.2f}%)')
out.append('')

out.append('## 2. 1억원으로 그날 SPY·QQQ를 샀다면 — 달러 수익률 / 환율 / 원화 수익률 (가격 기준)')
for name, s in STARTS:
    d = on(s); fxr = usd[END] / usd[d] - 1
    for sym, px in (('SPY', spy), ('QQQ', qqq)):
        r = px[END] / px[d] - 1; rk = (1 + r) * (1 + fxr) - 1
        out.append(f'{name} {d} {sym}: 달러 {r*100:+.2f}% · 환율 {fxr*100:+.2f}% · 원화 {rk*100:+.2f}% → 1억 → {W(1e8*(1+rk))}원 ({1e8*rk:+,.0f}원) · 달러−원화 {(r-rk)*100:.2f}%p = {W(1e8*(r-rk))}원')
out.append('')

out.append('## 3. 해외 결제 1,000달러·10만엔이 원화로 얼마(매매기준율, 카드 수수료 없음) — 끝날 대비')
for name, s in STARTS:
    d = on(s)
    out.append(f'{name} {d}: 1,000달러 {W(usd[d]*1000)}원 → {W(usd[END]*1000)}원 ({(usd[END]-usd[d])*1000:+,.0f}원) · 10만엔 {W(jpy[d]*1000)}원 → {W(jpy[END]*1000)}원 ({(jpy[END]-jpy[d])*1000:+,.0f}원)')
out.append('')

hi = max(usd.items(), key=lambda x: x[1]); lo = min(usd.items(), key=lambda x: x[1])
jlo = min(jpy.items(), key=lambda x: x[1]); jhi = max(jpy.items(), key=lambda x: x[1])
out.append(f'## 4. 범위(2024-01-02~{max(usd)}): 원/달러 최고 {hi[0]} {hi[1]:,} · 최저 {lo[0]} {lo[1]:,} · 원/100엔 최고 {jhi[0]} {jhi[1]} · 최저 {jlo[0]} {jlo[1]}')
ds = [k for k in usd if k <= END]; below = sum(1 for k in ds if usd[k] <= usd[END])
out.append(f'  2024년 이후 {len(ds)}거래일 중 끝날({usd[END]:,})보다 같거나 낮았던 날 {below}일 = {below/len(ds)*100:.1f}% · 높았던 날 {len(ds)-below}일')
ds25 = [k for k in ds if k >= '2025-01-01']; b25 = sum(1 for k in ds25 if usd[k] <= usd[END])
out.append(f'  2025년 이후 {len(ds25)}거래일 중 같거나 낮았던 날 {b25}일 = {b25/len(ds25)*100:.1f}%')
jd = [k for k in jpy if k <= END]; jb = sum(1 for k in jd if jpy[k] <= jpy[END])
out.append(f'  원/100엔: 2024년 이후 {len(jd)}거래일 중 끝날({jpy[END]})보다 같거나 낮았던 날 {jb}일 = {jb/len(jd)*100:.1f}%')
out.append('')

# 5. 하나은행 고시 — 끝날과 같은 날짜 회차
h = {x['localTradedAt']: x for x in o['HANA_USD']}
f = lambda s: float(str(s).replace(',', ''))
hd = END if END in h else max(k for k in h if k <= END)
x = h[hd]; mid, cb, cs, snd = f(x['closePrice']), f(x['cashBuyValue']), f(x['cashSellValue']), f(x['sendValue'])
out.append(f'## 5. 바꾸는 순간 드는 돈 — 하나은행 {hd} 고시(네이버 증권 marketIndex, 그날 마지막 회차)')
out.append(f'USD 매매기준율 {mid:,.2f} · 현찰 살 때 {cb:,.2f}(+{cb-mid:.2f}원, {(cb/mid-1)*100:.2f}%) · 현찰 팔 때 {cs:,.2f} · 송금 보낼 때 {snd:,.2f}(+{snd-mid:.2f}원, {(snd/mid-1)*100:.2f}%)')
out.append(f'1,000달러 현찰 우대 0%: {W(cb*1000)}원(+{W((cb-mid)*1000)}원) · 우대 50%: +{W((cb-mid)*500)}원 · 우대 90%: +{W((cb-mid)*100)}원 · 사서 바로 팔면 {W((cb-cs)*1000)}원({(cb/cs-1)*100:.2f}%)')
out.append(f'1억원어치 현찰 우대 0%로 사면 받는 달러 {1e8/cb:,.0f}달러 vs 매매기준율 {1e8/mid:,.0f}달러 → {1e8/mid-1e8/cb:,.0f}달러 덜 = 원화 {W((1e8/mid-1e8/cb)*mid)}원어치')
out.append('')

# 6. 분할 환전 — 1억을 12번(매달 첫 거래일) 나눠 바꿨다면
months = sorted({k[:7] for k in usd if '2025-11' <= k[:7] <= END[:7]})
firsts = [min(k for k in usd if k[:7] == m) for m in months][-12:]
dol = sum((1e8 / len(firsts)) / usd[k] for k in firsts); avg = 1e8 / dol
out.append(f'## 6. 분할 환전 — 1억을 {len(firsts)}번 나눠(매달 첫 거래일 {firsts[0]}~{firsts[-1]}, 매번 {W(1e8/len(firsts))}원) 달러로')
out.append('  날짜·환율: ' + ' · '.join(f'{k[5:]} {usd[k]:,}' for k in firsts))
out.append(f'  모은 달러 {dol:,.0f} · 평균 환율 {avg:,.1f} → 끝날 원화 {W(dol*usd[END])}원 ({dol*usd[END]-1e8:+,.0f}원, {(dol*usd[END]/1e8-1)*100:+.2f}%)')
for name, s in STARTS[:2] + STARTS[2:3]:
    d = on(s); out.append(f'  비교 한 번에 {name} {d}: {W(1e8/usd[d]*usd[END])}원')
out.append('')

# 7. 국내 상장 S&P500 ETF — 환노출 vs 환헤지(H), 같은 운용사(KODEX), KRX 종가 + 분배금(세전, 재투자 안 함)
#    분배금 원문: 삼성자산운용 divid-info API(raw/samsungfund_divid_2ETFE4·2ETFI3_20261017.json). 기준일 3일 전까지 산 경우만 받는다고 친다(KRX 결제 T+2).
import datetime as _dt
def divs(fn):
    j = json.load(open(os.path.join(D, 'raw', fn), encoding='utf-8'))
    return [(ymd(x['basicD']), float(x['dividA'])) for x in j['dividList']]
dv1 = divs('samsungfund_divid_2ETFE4_20261017.json'); dv2 = divs('samsungfund_divid_2ETFI3_20261017.json')
def got(dv, s, e):
    return sum(a for b, a in dv if (_dt.date.fromisoformat(b) - _dt.date.fromisoformat(s)).days >= 3 and b <= e)
k1 = {ymd(k): v for k, v in o['KR_379800']}; k2 = {ymd(k): v for k, v in o['KR_449180']}; k3 = {ymd(k): v for k, v in o['KR_360750']}
KE = max(k1)
out.append(f'## 7. 국내 상장 S&P500 ETF 1억 — KODEX 미국S&P500(379800, 환노출) vs KODEX 미국S&P500(H)(449180, 환헤지) · 끝 {KE} KRX 종가 + 그동안 분배금(세전·재투자 안 함) · 총보수는 가격에 이미 반영')
for name, s in STARTS + [('2024년 첫날(예외)', '2024-01-02')]:
    d = on(s, sorted(k1)); g1 = got(dv1, d, KE); g2 = got(dv2, d, KE)
    a = (k1[KE] + g1) / k1[d] - 1; b = (k2[KE] + g2) / k2[d] - 1; a0 = k1[KE] / k1[d] - 1; b0 = k2[KE] / k2[d] - 1
    out.append(f'{name} {d}: 환노출 {k1[d]:,}→{k1[KE]:,}+분배 {g1:.0f}원 {a*100:+.2f}%(가격만 {a0*100:+.2f}%) → {W(1e8*(1+a))}원 · 환헤지 {k2[d]:,}→{k2[KE]:,}+분배 {g2:.0f}원 {b*100:+.2f}%(가격만 {b0*100:+.2f}%) → {W(1e8*(1+b))}원 · 차(헤지−노출) {1e8*(b-a):+,.0f}원')
out.append('')

# 8. 본전 환율 — 지금 주가 그대로일 때 몇 원이 되면 원화로 본전인가
out.append('## 8. 본전 환율 — 그날 산 SPY가 지금 주가 그대로라면, 환율이 몇 원으로 돌아와야 원화로 1억 본전인가')
for name, s in STARTS:
    d = on(s); r = spy[END] / spy[d]; be = usd[d] / r
    out.append(f'{name} {d}: 그날 환율 {usd[d]:,} ÷ SPY 배수 {r:.4f} = 본전 환율 {be:,.1f}원 (끝날 {usd[END]:,}원보다 {be-usd[END]:+,.1f}원)')
out.append('')

# 9. 1천만원 단위(말하기 쉬운 단위) — 최고점 날 SPY
d = on('2026-07-02'); r = spy[END] / spy[d] - 1; rk = (1 + r) * (usd[END] / usd[d]) - 1
out.append(f'## 9. 1천만원 단위 — 최고점 {d} SPY: 달러로만 보면 {W(1e7*(1+r))}원, 원화로 {W(1e7*(1+rk))}원({1e7*rk:+,.0f}원) · 차 {W(1e7*(r-rk))}원')

# 10. 달러 정기예금 — KB국민은행 외화예금 금리안내(조회기준일 2026.10.16) 거주자 USD 12개월이상~18개월미만 연 3.64833%(같은 쪽 다른 표 12개월 3.70314% — 낮은 값으로 계산)
#     이자소득세 14%+지방소득세 1.4% = 15.4%(소득세법 제129조). 원화로 바꿀 때 환율은 그날 값.
r_dep = 0.0364833; r_net = r_dep * (1 - 0.154)
dol = 1e8 / usd[END]
out.append('')
out.append(f'## 10. 끝날 1억을 달러 1년 정기예금(연 {r_dep*100:.3f}%, 세후 {r_net*100:.2f}%)에 — 달러 {dol:,.0f} → 1년 뒤 {dol*(1+r_net):,.0f}달러')
be = usd[END] / (1 + r_net)
out.append(f'  1년 뒤 환율이 {be:,.1f}원보다 낮으면 세후 이자보다 환율 손실이 큼(끝날 {usd[END]:,}원보다 {usd[END]-be:,.1f}원 아래 = {(1-be/usd[END])*100:.2f}%)')
for x in (1300, 1250, 1400):
    out.append(f'  1년 뒤 {x:,}원이면 원화 {W(dol*(1+r_net)*x)}원({dol*(1+r_net)*x-1e8:+,.0f}원)')
# 11. 카드 해외결제 수수료 — KB국민카드 해외이용 종합안내(비자 1.1%·마스터 1.0% + 해외서비스 0.25%), 현대카드(비자 1.1%·마스터 1% + 0.18%)
out.append('')
out.append('## 11. 1,000달러 카드 결제 수수료(끝날 매매기준율로 친 원화 기준, 카드사 실제 적용 환율은 다를 수 있음)')
for nm, f_ in (('KB 비자 1.1%+0.25%', 0.0135), ('KB 마스터 1.0%+0.25%', 0.0125), ('현대 비자 1.1%+0.18%', 0.0128), ('현대 마스터 1%+0.18%', 0.0118)):
    out.append(f'  {nm} = {f_*100:.2f}% → {W(usd[END]*1000*f_)}원')
out.append(f'  비교: 현찰 살 때 스프레드 1.75%(우대 0%) → 1,000달러 {W(usd[END]*1000*0.0175)}원어치')
open(os.path.join(D, 'calc_out.txt'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('\n'.join(out))
