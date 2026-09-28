# 부산 16개 구·군 국민평형(전용 80~86㎡) 매매 중앙값 · 5억 이하 비율. 해제 거래(cdealType=O) 제외.
import sys, os, json, glob, statistics as st, collections as C
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
NAME = {'26110':'중구','26140':'서구','26170':'동구','26200':'영도구','26230':'부산진구','26260':'동래구','26290':'남구','26320':'북구',
        '26350':'해운대구','26380':'사하구','26410':'금정구','26440':'강서구','26470':'연제구','26500':'수영구','26530':'사상구','26710':'기장군'}
def num(s): return int(''.join(ch for ch in (s or '0') if ch.isdigit()) or 0)
allrows, per, allcnt, cancel, agentnm = [], C.defaultdict(list), 0, 0, C.defaultdict(C.Counter)
for f in sorted(glob.glob(os.path.join(HERE, 'raw', '*.json'))):
    code = os.path.basename(f)[:5]
    for r in json.load(open(f, encoding='utf-8')):
        allcnt += 1
        if (r.get('cdealType') or '').strip(): cancel += 1; continue
        ar = float(r.get('excluUseAr') or 0)
        if not (80 <= ar <= 86): continue
        p = num(r.get('dealAmount'))
        per[code].append((p, r.get('aptNm'), r.get('umdNm'), ar, r.get('dealYear'), r.get('dealMonth'), r.get('dealDay'), r.get('floor')))
        agentnm[code][r.get('estateAgentSggNm')] += 1
print(f'전체 신고 {allcnt}건 · 해제 {cancel}건 제외 · 국민평형 {sum(len(v) for v in per.values())}건')
res = []
for code, v in per.items():
    ps = sorted(x[0] for x in v)
    u5 = sum(1 for x in ps if x <= 50000)
    top = C.Counter(x[1] for x in v).most_common(1)[0]
    mx = max(v); mn = min(v)
    res.append(dict(code=code, name=NAME[code], n=len(ps), med=int(st.median(ps)), u5n=u5, u5=round(100*u5/len(ps),1),
                    min=mn[0], minapt=f'{mn[2]} {mn[1]}', max=mx[0], maxapt=f'{mx[2]} {mx[1]} {mx[3]}㎡ {mx[4]}.{mx[5]}.{mx[6]} {mx[7]}층', top=top[0], topn=top[1],
                    agent=agentnm[code].most_common(1)[0][0]))
res.sort(key=lambda d: d['med'])
for d in res:
    print(f"{d['name']:5s} 중앙 {d['med']:>6,}만 · {d['n']:>4}건 · 5억이하 {d['u5n']}건 {d['u5']}% · 최저 {d['min']:,}({d['minapt']}) · 최고 {d['max']:,}({d['maxapt']}) · 최다 {d['top']} {d['topn']}건 · 중개소명 {d['agent']}")
allp = sorted(x[0] for v in per.values() for x in v)
print(f"부산 전체 국민평형 중앙 {int(st.median(allp)):,}만 · 5억 이하 {sum(1 for x in allp if x<=50000)}건/{len(allp)}건 = {100*sum(1 for x in allp if x<=50000)/len(allp):.1f}%")
big = [d for d in res if d['n'] >= 15]
print('15건 이상 구·군', len(big), '· 중앙 5억 이하', sum(1 for d in big if d['med'] <= 50000))
print(f"최고/최저 중앙 배수 {big[-1]['name']} {big[-1]['med']} / {big[0]['name']} {big[0]['med']} = {big[-1]['med']/big[0]['med']:.2f}")
json.dump(res, open(os.path.join(HERE, 'data84.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
