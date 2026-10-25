# 2026-10-22 firemap-write: 서울 아파트 매매 실거래 '해제' 계산 (raw/ = 국토부 RTMSDataSvcAptTradeDev, fetch.py)
# 1) 1년(계약 2025-11~2026-10) 해제 건수·비율  2) 계약월별 해제 비율  3) 계약→해제 걸린 날
# 4) 해제된 집이 같은 단지·같은 면적·같은 층으로 다시 신고된 비율(앞뒤 60일)·가격 차이
# 5) 그 단지·면적에서 앞선 거래(2025-07 이후)보다 비싼 값(이전 최고 넘김)의 해제 비율 vs 나머지
# 6) 등기: 계약 2025-11~2026-03, 해제 아닌 거래 중 등기일 빈칸 비율 · 계약→등기 걸린 날
import sys, os, json, glob, statistics as st, datetime as dt, collections
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sgg = json.load(open(os.path.join(HERE, '..', 'seoul_sgg.json'), encoding='utf-8'))
rows = []
for f in sorted(glob.glob(os.path.join(HERE, 'raw1026', '*_trade.json'))):
    for r in json.load(open(f, encoding='utf-8')):
        d = dt.date(int(r['dealYear']), int(r['dealMonth']), int(r['dealDay']))
        cd = None
        if r['cdealDay']:
            y, m, dd = r['cdealDay'].split('.'); cd = dt.date(2000 + int(y), int(m), int(dd))
        rg = None
        if r['rgstDate']:
            y, m, dd = r['rgstDate'].split('.'); rg = dt.date(2000 + int(y), int(m), int(dd))
        rows.append(dict(sgg=r['sggCd'], apt=r['aptSeq'], nm=r['aptNm'], ar=float(r['excluUseAr']), fl=r['floor'],
                         amt=int(r['dealAmount'].replace(',', '')), d=d, cd=cd, rg=rg, cancel=r['cdealType'] == 'O',
                         gbn=r['dealingGbn']))
print('전체 행', len(rows), '받은 파일', len(glob.glob(os.path.join(HERE, 'raw1026', '*_trade.json'))))
A, B = dt.date(2025, 11, 1), dt.date(2026, 10, 31)
yr = [r for r in rows if A <= r['d'] <= B]
n = len(yr); c = sum(r['cancel'] for r in yr)
print(f'\n§1 1년(계약 2025-11~2026-10) 신고 {n}건 · 해제 {c}건 · {c/n*100:.2f}%')
print('\n§2 계약월별 (신고·해제·비율)')
mon = collections.defaultdict(lambda: [0, 0])
for r in rows:
    k = r['d'].strftime('%Y-%m'); mon[k][0] += 1; mon[k][1] += r['cancel']
for k in sorted(mon): print(f'  {k} {mon[k][0]:>6} {mon[k][1]:>5} {mon[k][1]/mon[k][0]*100:5.2f}%')
lag = [(r['cd'] - r['d']).days for r in rows if r['cancel'] and r['cd']]
lag.sort()
print(f'\n§3 계약→해제 날(전체 기간 해제 {len(lag)}건) 가운데 {st.median(lag)}일 · 30일 안 {sum(x<=30 for x in lag)/len(lag)*100:.1f}% · 60일 안 {sum(x<=60 for x in lag)/len(lag)*100:.1f}% · 90일 넘음 {sum(x>90 for x in lag)/len(lag)*100:.1f}%')
# 계약 2025-07~2025-10(해제가 날 시간이 충분한 넉 달) 해제 비율 vs 최근 넉 달
def rate(a, b):
    s = [r for r in rows if a <= r['d'] <= b]; return len(s), sum(r['cancel'] for r in s)
for a, b in [(dt.date(2025,7,1), dt.date(2025,10,31)), (dt.date(2025,11,1), dt.date(2026,2,28)), (dt.date(2026,3,1), dt.date(2026,6,30)), (dt.date(2026,7,1), dt.date(2026,10,31))]:
    t, cc = rate(a, b); print(f'  계약 {a}~{b}: {t}건 중 해제 {cc} ({cc/t*100:.2f}%)')
# §4 다시 신고
key = collections.defaultdict(list)
for r in rows:
    if not r['cancel']: key[(r['apt'], round(r['ar'], 2), r['fl'])].append(r)
can = [r for r in yr if r['cancel']]
re_, diffs, same = 0, [], 0
for r in can:
    m = [x for x in key[(r['apt'], round(r['ar'], 2), r['fl'])] if abs((x['d'] - r['d']).days) <= 60]
    if m:
        re_ += 1; x = min(m, key=lambda x: abs((x['d'] - r['d']).days))
        diffs.append(x['amt'] - r['amt']); same += x['amt'] == r['amt']
print(f'\n§4 1년 해제 {len(can)}건 중 같은 단지·면적·층 해제 아닌 거래가 계약일 앞뒤 60일 안에 있음 {re_}건 ({re_/len(can)*100:.1f}%)')
print(f'   그중 같은 값 {same}건({same/re_*100:.1f}%) · 다시 신고 값이 더 낮음 {sum(d<0 for d in diffs)} · 더 높음 {sum(d>0 for d in diffs)} · 차이 가운데 {st.median(diffs)}만원')
# §5 이전 최고 넘김(그 단지·전용 정수 면적, 2025-07 이후 앞선 해제 아닌 거래 중 최고보다 높음)
grp = collections.defaultdict(list)
for r in sorted(rows, key=lambda r: r['d']): grp[(r['apt'], int(r['ar']))].append(r)
hi = [0, 0]; lo = [0, 0]
for g in grp.values():
    for r in g:
        if not (A <= r['d'] <= B): continue
        prev = [x['amt'] for x in g if x['d'] < r['d'] and not x['cancel']]   # 계약일이 앞선(같은 날 제외) 해제 아닌 거래만
        if not prev: continue
        t = hi if r['amt'] > max(prev) else lo; t[0] += 1; t[1] += r['cancel']
print(f'\n§5 앞선 거래 있는 1년 거래: 이전 최고보다 비쌈 {hi[0]}건 중 해제 {hi[1]} ({hi[1]/hi[0]*100:.2f}%) · 나머지 {lo[0]}건 중 해제 {lo[1]} ({lo[1]/lo[0]*100:.2f}%)')
# §6 등기
for a, b in [(dt.date(2025,7,1), dt.date(2025,12,31)), (dt.date(2026,1,1), dt.date(2026,3,31)), (dt.date(2026,4,1), dt.date(2026,6,30))]:
    s = [r for r in rows if a <= r['d'] <= b and not r['cancel']]
    e = sum(r['rg'] is None for r in s)
    print(f'§6 계약 {a}~{b} 해제 아닌 {len(s)}건 중 등기일 빈칸 {e} ({e/len(s)*100:.2f}%)')
gl = sorted((r['rg'] - r['d']).days for r in rows if r['rg'] and not r['cancel'])
print(f'   계약→등기 가운데 {st.median(gl)}일 · 90일 안 {sum(x<=90 for x in gl)/len(gl)*100:.1f}% · 120일 넘음 {sum(x>120 for x in gl)/len(gl)*100:.1f}%')
# §7 구별 1년 해제 비율(건수 300건 이상)
print('\n§7 구별 1년 해제 비율')
g7 = collections.defaultdict(lambda: [0, 0])
for r in yr: g7[r['sgg']][0] += 1; g7[r['sgg']][1] += r['cancel']
for k, (t, cc) in sorted(g7.items(), key=lambda kv: -kv[1][1]/kv[1][0]): print(f'  {sgg.get(k,k)} {t} {cc} {cc/t*100:.2f}%')
# §8 직거래 해제 비율
for gb in ('중개거래', '직거래'):
    s = [r for r in yr if r['gbn'] == gb]; cc = sum(r['cancel'] for r in s)
    print(f'§8 {gb} {len(s)}건 해제 {cc} ({cc/len(s)*100:.2f}%)')
# §9 다시 신고된 짝의 계약일이 같은지 · 계약월 묶음별 다시 신고 비율 · 다시 신고 안 된 해제 수
print()
def pair(r):
    m = [x for x in key[(r['apt'], round(r['ar'], 2), r['fl'])] if abs((x['d'] - r['d']).days) <= 60]
    return min(m, key=lambda x: abs((x['d'] - r['d']).days)) if m else None
pr = [(r, pair(r)) for r in can]
sd = sum(1 for r, x in pr if x and x['d'] == r['d'])
print(f"§9 1년 해제 중 다시 신고 짝의 계약일까지 같음 {sd}건 ({sd/len(can)*100:.1f}% of 해제) · 다시 신고 안 된 해제 {sum(1 for r,x in pr if not x)}건 = 1년 신고의 {sum(1 for r,x in pr if not x)/n*100:.2f}%")
for a, b in [(dt.date(2025,7,1), dt.date(2025,8,31)), (dt.date(2025,9,1), dt.date(2025,10,31)), (dt.date(2025,11,1), dt.date(2026,10,31))]:
    cs = [r for r in rows if a <= r['d'] <= b and r['cancel']]; t = len([r for r in rows if a <= r['d'] <= b])
    k2 = sum(1 for r in cs if pair(r))
    print(f"   계약 {a}~{b}: 신고 {t} 해제 {len(cs)} 다시 신고 {k2} ({k2/len(cs)*100:.1f}%) · 다시 신고 안 된 해제 {len(cs)-k2} ({(len(cs)-k2)/t*100:.2f}% of 신고)")
nore = [r for r, x in pr if not x]
print(f"   다시 신고 안 된 해제 {len(nore)}건 가격 가운데 {st.median([r['amt'] for r in nore])}만원 · 해제 전체 가운데 {st.median([r['amt'] for r in can])}만원 · 1년 해제 아닌 거래 가운데 {st.median([r['amt'] for r in yr if not r['cancel']])}만원")
# §10 6개월 넘게 등기 빈칸(계약 2025-11~2026-03, 해제 아님) 건수
s10 = [r for r in rows if dt.date(2025,11,1) <= r['d'] <= dt.date(2026,3,31) and not r['cancel']]
e10 = [r for r in s10 if r['rg'] is None]
print(f"§10 계약 2025-11~2026-03 해제 아닌 {len(s10)}건 중 등기일 빈칸 {len(e10)} ({len(e10)/len(s10)*100:.2f}%)")
# §11 1년(2025-11~2026-10 계약) 해제만으로 계약→해제 날
lag1 = sorted((r['cd'] - r['d']).days for r in yr if r['cancel'] and r['cd'])
print(f"§11 1년 해제 {len(lag1)}건 계약→해제 가운데 {st.median(lag1)}일 · 30일 안 {sum(x<=30 for x in lag1)/len(lag1)*100:.1f}% · 31~60 {sum(30<x<=60 for x in lag1)/len(lag1)*100:.1f}% · 61~90 {sum(60<x<=90 for x in lag1)/len(lag1)*100:.1f}% · 90 넘음 {sum(x>90 for x in lag1)/len(lag1)*100:.1f}%")
gl1 = sorted((r['rg'] - r['d']).days for r in yr if r['rg'] and not r['cancel'])
print(f"   1년 계약 등기 있는 {len(gl1)}건 계약→등기 가운데 {st.median(gl1)}일")
# §12 (레드팀 10/22 대조군) 계약일·가격까지 같은 짝: 해제 거래 vs 해제 아닌 거래(자기 자신 제외)
ex = collections.Counter((r['apt'], round(r['ar'], 2), r['fl'], r['d'], r['amt']) for r in rows if not r['cancel'])
c_same = sum(1 for r in can if ex[(r['apt'], round(r['ar'], 2), r['fl'], r['d'], r['amt'])] > 0)
nc = [r for r in yr if not r['cancel']]
n_same = sum(1 for r in nc if ex[(r['apt'], round(r['ar'], 2), r['fl'], r['d'], r['amt'])] > 1)
n_60 = sum(1 for r in nc if len([x for x in key[(r['apt'], round(r['ar'], 2), r['fl'])] if x is not r and abs((x['d'] - r['d']).days) <= 60]) > 0)
print(f"§12 1년 해제 {len(can)}건 중 계약일·가격까지 같은 해제 아닌 거래 있음 {c_same}건 ({c_same/len(can)*100:.1f}%) · 해제 아닌 {len(nc)}건 중 같은 조건 짝 {n_same}건 ({n_same/len(nc)*100:.1f}%) · 해제 아닌 거래도 ±60일 같은 단지·면적·층 짝 {n_60} ({n_60/len(nc)*100:.1f}%)")
