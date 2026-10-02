# B10 단지 전세가율 순위 — undervalue.py와 같은 규칙(해제·공공기관 매입 제외, 5㎡ 면적대, 매매·전세 각 2건↑, 전용 40㎡대↑)
# 다른 점 하나: 짝 열쇠에 법정동(umdNm)을 넣는다. 같은 구 안 같은 이름 단지(노원 '극동' = 상계동 1996 + 하계동 1988)가 한 덩어리로 섞였다.
import json, glob, os, re, statistics, collections, sys
sys.stdout.reconfigure(encoding='utf-8')
W = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'); RT = os.path.join(W, 'research', 'rt')
sgg = json.load(open(os.path.join(W, 'research', 'seoul_sgg.json'), encoding='utf-8'))
num = lambda s: int(re.sub(r'[^\d]', '', s or '0') or 0)
def band(a):
    try: return int(float(a) // 5 * 5)
    except: return None
sale = collections.defaultdict(list); jeon = collections.defaultdict(list); by = collections.defaultdict(set)
for lawd, gu in sgg.items():
    for ym in ('202607', '202608', '202609'):
        for kind in ('trade', 'rent'):
            f = os.path.join(RT, f'{lawd}_{ym}_{kind}.json')
            if not os.path.exists(f): continue
            for r in json.load(open(f, encoding='utf-8')):
                nm = (r.get('aptNm') or '').strip(); b = band(r.get('excluUseAr'))
                if not nm or b is None: continue
                k = (gu, (r.get('umdNm') or '').strip(), nm, b)
                if kind == 'trade':
                    if num(r.get('dealAmount')) > 0 and not r.get('cdealType') and r.get('buyerGbn') != '공공기관':
                        sale[k].append(num(r.get('dealAmount'))); by[k].add(r.get('buildYear'))
                else:
                    if num(r.get('monthlyRent')) == 0 and num(r.get('deposit')) > 0: jeon[k].append(num(r.get('deposit')))
rows = []
for k in sale:
    if k[3] >= 40 and len(sale[k]) >= 2 and len(jeon.get(k, [])) >= 2:
        p, j = statistics.median(sale[k]), statistics.median(jeon[k]); r = j / p
        if 0.2 < r < 1.2: rows.append(dict(gu=k[0], dong=k[1], apt=k[2], band=k[3], sale=p, jeonse=j, ratio=r, ns=len(sale[k]), nj=len(jeon[k]), year='/'.join(sorted(y for y in by[k] if y))))
rows.sort(key=lambda d: -d['ratio'])
print('pairs', len(rows), 'median', round(statistics.median(d['ratio'] for d in rows) * 100, 1), '>=80%', sum(d['ratio'] >= .8 for d in rows), '<=25%', sum(d['ratio'] <= .25 for d in rows))
for d in rows[:12] + rows[-12:]:
    print(f"{d['gu']} {d['dong']} {d['apt']} {d['band']}㎡대 {d['year']} | 매매 {d['sale']:,.0f} 전세 {d['jeonse']:,.0f} 차이 {d['sale']-d['jeonse']:,.0f}만원 | {d['ratio']*100:.1f}% (매매{d['ns']}·전세{d['nj']})")
json.dump(rows, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rank.json'), 'w', encoding='utf-8'), ensure_ascii=False)
