# h1helio1021 — h1s_helio(헬리오시티 84㎡ 20억 직거래 vs 같은 달 가운데 값) 짝 글 계산. 국토부 실거래 송파구(research/rt/11710_*, 2026-10-20 23:13 다시 받음).
import sys, os, json, glob, statistics as st, collections
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); RT = os.path.join(H, '..', 'rt')
num = lambda s: float(str(s).replace(',', '') or 0)
ms = ['202511','202512','202601','202602','202603','202604','202605','202606','202607','202608','202609','202610']
rows = []
for m in ms:
    d = json.load(open(os.path.join(RT, f'11710_{m}_trade.json'), encoding='utf-8')); rows += d
tot = len(rows)
rows = [r for r in rows if not r.get('cdealType') and r.get('buyerGbn') != '공공기관']
print('송파구 2025-11~2026-10 매매 받은', tot, '해제·공공 뺀', len(rows))
b = [r for r in rows if 80 <= num(r['excluUseAr']) < 85]
print('84㎡대(전용 80~85)', len(b), '| 거래 유형', collections.Counter(r.get('dealingGbn') for r in b))
for r in b: r['ym'] = r['dealYear'] + r['dealMonth'].zfill(2); r['amt'] = num(r['dealAmount'])
# 헬리오시티
hel = [r for r in b if r['aptNm'].replace(' ', '') == '헬리오시티' and r['umdNm'] == '가락동']
print('\n§1 헬리오시티 84㎡대', len(hel), '건 가운데', st.median(r['amt'] for r in hel), '최저', min(r['amt'] for r in hel), '최고', max(r['amt'] for r in hel), '유형', collections.Counter(r.get('dealingGbn') for r in hel))
byym = collections.defaultdict(list)
for r in hel: byym[r['ym']].append(r)
for ym in sorted(byym): print(' ', ym, len(byym[ym]), '건 가운데', st.median(x['amt'] for x in byym[ym]), '최저', min(x['amt'] for x in byym[ym]), '최고', max(x['amt'] for x in byym[ym]))
print('\n§2 헬리오시티 직거래 84㎡대')
for r in hel:
    if r.get('dealingGbn') == '직거래':
        oth = [x['amt'] for x in byym[r['ym']] if x is not r]
        print(' ', r['ym'], r['dealDay'], r['amt'], r['floor'] + '층', '등기', r.get('rgstDate'), '| 같은 달 나머지', len(oth), '건 가운데', st.median(oth) if oth else None, '최저', min(oth) if oth else None)
# 송파구 전체: 직거래 vs 같은 단지·같은 달 중개
print('\n§3 송파구 84㎡대 직거래 vs 같은 단지·같은 달 중개거래(3건 이상일 때만)')
key = lambda r: (r['aptNm'].replace(' ', ''), r['umdNm'], r['ym'])
brk = collections.defaultdict(list)
for r in b:
    if r.get('dealingGbn') == '중개거래': brk[key(r)].append(r['amt'])
dd = [r for r in b if r.get('dealingGbn') == '직거래']
print(' 직거래', len(dd), '/', len(b), '= %.1f%%' % (len(dd) / len(b) * 100))
cmp_ = []
for r in dd:
    v = brk.get(key(r), [])
    if len(v) >= 3:
        med = st.median(v); cmp_.append((r, med, (r['amt'] / med - 1) * 100))
print(' 비교 가능', len(cmp_), '건 | 비율(%) 가운데', round(st.median(c[2] for c in cmp_), 1), '| 평균', round(st.mean(c[2] for c in cmp_), 1), '| 낮은 건', sum(1 for c in cmp_ if c[2] < 0), '| 5% 넘게 낮은 건', sum(1 for c in cmp_ if c[2] < -5), '| 10% 넘게 낮은 건', sum(1 for c in cmp_ if c[2] < -10), '| 같거나 높은 건', sum(1 for c in cmp_ if c[2] >= 0), '| 20% 넘게 낮은', sum(1 for c in cmp_ if c[2] < -20))
for r, med, p in sorted(cmp_, key=lambda x: x[2]):
    print('  ', r['aptNm'], r['umdNm'], r['ym'], r['dealDay'], r['amt'], r['floor'] + '층', '| 같은 달 중개', len(brk[key(r)]), '건 가운데', med, '| %+.1f%%' % p, '등기', r.get('rgstDate'), '| 매수/매도', r.get('buyerGbn'), r.get('slerGbn'))
print('\n 비교 못 한 직거래(같은 달 같은 단지 중개 3건 미만)', len(dd) - len(cmp_))
# 같은 달 같은 단지 중개거래 안에서 최저가가 직거래 가격보다 낮은 정도 → 중개끼리도 벌어지는 정도
sp = []
for k, v in brk.items():
    if len(v) >= 5: sp.append((min(v) / st.median(v) - 1) * 100)
print('\n§4 비교: 중개거래끼리 같은 단지·같은 달(5건 이상) 최저가가 가운데 값보다 낮은 정도 — 곳 수', len(sp), '가운데', round(st.median(sp), 1), '%', '| 10% 넘게 낮은', sum(1 for x in sp if x < -10), '곳')
# 헬리오시티 중개거래끼리: 가장 낮은 달 vs 가운데
json.dump(dict(helio=[dict(ym=r['ym'], day=r['dealDay'], amt=r['amt'], floor=r['floor'], gbn=r.get('dealingGbn')) for r in hel],
               cmp=[dict(apt=r['aptNm'], umd=r['umdNm'], ym=r['ym'], day=r['dealDay'], amt=r['amt'], floor=r['floor'], med=med, pct=p) for r, med, p in cmp_]),
          open(os.path.join(H, 'calc_out.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

print('\n§5 헬리오시티 2026-05 84㎡대 평균·가운데 값: 직거래 넣었을 때 vs 뺐을 때')
may = byym['202605']; allv = [r['amt'] for r in may]; brkv = [r['amt'] for r in may if r.get('dealingGbn') != '직거래']
print(' 넣음', len(allv), '건 평균', round(st.mean(allv)), '가운데', st.median(allv), '| 뺌', len(brkv), '건 평균', round(st.mean(brkv)), '가운데', st.median(brkv))
print(' 평균 차', round(st.mean(brkv) - st.mean(allv)), '가운데 차', st.median(brkv) - st.median(allv))
print('\n§6 헬리오시티 중개거래 85건 중 20억대 이하 / 최저 중개 / 그 달')
bk = sorted(hel, key=lambda r: r['amt'])
for r in bk[:4]: print(' ', r['ym'], r['dealDay'], r['amt'], r['floor'] + '층', r.get('dealingGbn'))
print('\n§7 송파 직거래 43건 단지 수·비교 못 한 사유 분포')
cn = collections.Counter(len(brk.get(key(r), [])) for r in dd)
print(' 같은 달 같은 단지 중개 건수별 직거래 수', sorted(cn.items()))
print(' 직거래 43건 값 범위', min(r['amt'] for r in dd), max(r['amt'] for r in dd), '가운데', st.median(r['amt'] for r in dd))
print(' 중개 1303건 가운데', st.median(r['amt'] for r in b if r.get('dealingGbn') == '중개거래'))
print(' 직거래 건수 단지별', collections.Counter(r['aptNm'] for r in dd).most_common(6))
print(' 직거래 월별', sorted(collections.Counter(r['ym'] for r in dd).items()))
