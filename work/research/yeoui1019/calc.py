# 여의도동 아파트 매매 — 같은 단지·같은 전용면적끼리 층별 가격 (국토부 실거래 rt/11560_*, 2025-11~2026-10, 계약취소·공공기관 매수 제외)
import json, os, statistics as st, collections, sys
sys.stdout.reconfigure(encoding='utf-8')
RT = os.path.join(os.path.dirname(__file__), '..', 'rt')
def num(s): return float(str(s or '0').replace(',', '') or 0)
months = [f'2025{m:02d}' for m in (11, 12)] + [f'2026{m:02d}' for m in range(1, 11)]
allr = []
for m in months: allr += json.load(open(os.path.join(RT, f'11560_{m}_trade.json'), encoding='utf-8'))
R = [r for r in allr if not r.get('cdealType') and r.get('buyerGbn') != '공공기관' and r['umdNm'] == '여의도동']
print('영등포구 전체', len(allr), '여의도동(취소·공공 제외)', len(R), '취소', sum(1 for r in allr if r.get('cdealType') and r['umdNm']=='여의도동'), '공공기관', sum(1 for r in allr if r.get('buyerGbn')=='공공기관' and r['umdNm']=='여의도동'))
print('최초 계약일', min(r['dealYear']+r['dealMonth'].zfill(2)+r['dealDay'].zfill(2) for r in R), '마지막', max(r['dealYear']+r['dealMonth'].zfill(2)+r['dealDay'].zfill(2) for r in R))
g = collections.defaultdict(list)
for r in R: g[(r['aptNm'], round(num(r['excluUseAr']), 1))].append((int(r['floor']), num(r['dealAmount']) / 1e4))
print('\n[묶음: 단지·면적 | 건수 | 저층(1~5층) 중간값 | 고층(10층~) 중간값 | 차이]')
tab = []
for k, v in sorted(g.items(), key=lambda x: -len(x[1])):
    lo = [p for f, p in v if f <= 5]; hi = [p for f, p in v if f >= 10]
    if len(lo) >= 2 and len(hi) >= 2:
        a, b = st.median(lo), st.median(hi); tab.append((k, len(v), len(lo), a, len(hi), b, (b / a - 1) * 100))
        print(f'{k[0]} {k[1]}㎡ | {len(v)} | {len(lo)}건 {a:.2f}억 | {len(hi)}건 {b:.2f}억 | {(b/a-1)*100:+.1f}%')
print('묶음', len(tab), '개, 차이 가운데 값', f'{st.median(x[-1] for x in tab):+.1f}%', '범위', f'{min(x[-1] for x in tab):+.1f}~{max(x[-1] for x in tab):+.1f}%', '플러스', sum(1 for x in tab if x[-1] > 0))
# 합쳐 보기: 거래 6건 이상 묶음, 값/묶음 중간값
print('\n[거래 6건 이상 묶음을 합쳐: 층 구간별 (값 ÷ 그 묶음 중간값)]')
bk = collections.defaultdict(list); used = 0; groups = 0
for k, v in g.items():
    if len(v) >= 6:
        groups += 1; med = st.median(p for f, p in v); used += len(v)
        for f, p in v:
            b = '5층 이하' if f <= 5 else ('6~9층' if f <= 9 else '10층 이상')
            bk[b].append(p / med)
print('묶음', groups, '개, 거래', used, '건')
for b in ('5층 이하', '6~9층', '10층 이상'):
    print(b, len(bk[b]), f'건, 묶음 중간값 대비 {st.median(bk[b])*100:.1f}%')
# 시범 79.2, 대교 95.5 개별
for key in (('시범', 79.2), ('대교', 95.5), ('진주', 48.3)):
    print(key, sorted(g[key]))
# 층 정보 있는 최고·최저
fl = [int(r['floor']) for r in R]; print('여의도동 거래 층 분포: 1~4층', sum(1 for f in fl if f<=4), '5~9', sum(1 for f in fl if 5<=f<=9), '10+', sum(1 for f in fl if f>=10))
