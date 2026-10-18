# SCHD 분기 배당을 배당락일 한국은행 매매기준율로 원화 환산 (2026-10-18 firemap-write)
import sys, json, os
sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import apis
fx = {a: float(b) for a, b, _ in json.load(open('raw/ecos_731Y001_1018.json', encoding='utf-8'))}
def rate(d):
    d = d.replace('-', ''); k = max(x for x in fx if x <= d); return k, fx[k]
divs = apis.dividends('SCHD', 2)
json.dump(divs, open('raw/schd_div_yahoo_1018.json', 'w'), indent=0)
N = 2000; W = 0.15
out = []
for d, a in divs:
    k, r = rate(d)
    won = a * r
    out.append((d, a, k, r, won, N * a, N * won, N * won * (1 - W)))
    print(f'{d} ${a:.3f} 환율({k}) {r:,.1f} 1주 {won:,.1f}원 | {N}주 ${N*a:,.0f} 세전 {N*won:,.0f}원 세후(15%) {N*won*(1-W):,.0f}원')
j, s = out[-2], out[-1]
print(f'6월→9월 달러 {(s[1]/j[1]-1)*100:+.2f}% 환율 {(s[3]/j[3]-1)*100:+.2f}% 원화 {(s[4]/j[4]-1)*100:+.2f}%')
print(f'{N}주 세전 차 {s[6]-j[6]:,.0f}원 · 세후 차 {s[7]-j[7]:,.0f}원 · 달러 차 ${s[5]-j[5]:,.0f}')
y1 = out[-4:]; y0 = out[-8:-4]
for nm, g in (('최근4회(25.12~26.09)', y1), ('그전4회(24.12~25.09)', y0)):
    print(nm, f'1주 ${sum(x[1] for x in g):.3f}', f'1주 {sum(x[4] for x in g):,.1f}원', f'{N}주 세후 {sum(x[7] for x in g):,.0f}원')
print(f'1년 달러 {(sum(x[1] for x in y1)/sum(x[1] for x in y0)-1)*100:+.2f}% 원화 {(sum(x[4] for x in y1)/sum(x[4] for x in y0)-1)*100:+.2f}%')
q = apis.av_quote('SCHD'); print('SCHD', q)
p = float(q['종가']); last = max(fx); print(f'{N}주 평가 ${N*p:,.0f} × {fx[last]} ({last}) = {N*p*fx[last]:,.0f}원')
hi = max(fx.items(), key=lambda x: x[1]); print('2024-09 이후 최고', hi, '최근', last, fx[last], f'{(fx[last]/hi[1]-1)*100:+.1f}%')
oct_ = {k: v for k, v in fx.items() if k.startswith('202610')}; lo = min(oct_.items(), key=lambda x: x[1])
prev = max(k for k, v in fx.items() if k < lo[0] and v <= lo[1]); print('10월 최저', lo, '그 아래였던 마지막 날', prev, fx[prev])
# 흔한 계산(최근 1년 배당 합 × 오늘 환율)과 실제 날짜별 환율 계산 비교
s1 = sum(x[1] for x in y1); now = fx[last]
naive = s1 * now * N * (1 - W); real = sum(x[7] for x in y1)
print(f'흔한 계산 1주 {s1*now:,.1f}원 · {N}주 세후 {naive:,.0f}원 · 실제 {real:,.0f}원 · 차 {real-naive:,.0f}원 ({(naive/real-1)*100:+.1f}%)')
