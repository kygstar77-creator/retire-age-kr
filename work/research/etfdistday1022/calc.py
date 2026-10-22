# 분배락일·분배금 = 야후 chart events(운용사·KRX 공시로 대조). 가격 = 네이버 증권 모바일 일별 시세(수정 안 한 KRX 시가·종가).
# 앞날 종가 → 분배락일 시가 변화 vs 분배금. '하루 들고 있기' = 앞날 종가에 사서 분배락일 시가에 팜 + 분배금 세후(15.4%), 수수료 뺌.
import json, datetime, statistics as st, glob
names={'458730':'TIGER 미국배당다우존스','489250':'KODEX 미국배당다우존스','458760':'TIGER 미국배당+7%프리미엄다우존스','441680':'TIGER 미국나스닥100커버드콜(합성)'}
TAX=0.154; num=lambda s:int(str(s).replace(',',''))
ALL=[]
for t,nm in names.items():
    r=json.load(open(f'raw/yh_{t}.json'))['chart']['result'][0]
    ev={datetime.datetime.fromtimestamp(int(k)).date():v['amount'] for k,v in r['events']['dividends'].items()}
    px={}
    for f in glob.glob(f'raw/nvm_{t}_*.json'):
        for x in json.load(open(f,encoding='utf-8')):
            px[datetime.date.fromisoformat(x['localTradedAt'][:10])]=(num(x['openPrice']),num(x['closePrice']))
    days=sorted(px); rows=[]
    for d,amt in sorted(ev.items()):
        if d not in px: print('  가격 없음',d); continue
        i=days.index(d); pc=px[days[i-1]][1]; o,c=px[d]
        rows.append(dict(d=d,prev=days[i-1],amt=amt,pc=pc,o=o,c=c,do=pc-o,dc=pc-c,od=(o-pc)+amt*(1-TAX)))
    print(f'== {t} {nm} n={len(rows)}')
    for x in rows:
        print(x['d'],'앞날',x['prev'],f"분배금{x['amt']:.0f} 앞날종가{x['pc']} 시가{x['o']} 종가{x['c']} 시가하락{x['do']} 종가하락{x['dc']} 하루{x['od']:+.1f} 율{x['amt']/x['pc']*100:.2f}%")
    a=[x['amt'] for x in rows]; do=[x['do'] for x in rows]; dc=[x['dc'] for x in rows]; od=[x['od'] for x in rows]
    print(f"평균 분배금 {st.mean(a):.1f} 세금 {st.mean(a)*TAX:.1f} | 시가하락 평균 {st.mean(do):.1f} 중앙 {st.median(do):.1f} | 종가하락 평균 {st.mean(dc):.1f} | 하루 평균 {st.mean(od):+.1f} 중앙 {st.median(od):+.1f} 플러스 {sum(v>0 for v in od)}/{len(od)}")
    print(f"분배금 대비 시가하락 {st.mean(do)/st.mean(a)*100:.0f}% 종가하락 {st.mean(dc)/st.mean(a)*100:.0f}% | 시가가 분배금 이상 떨어짐 {sum(p>=q for p,q in zip(do,a))}/{len(a)} · 시가가 그대로거나 오름 {sum(p<=0 for p in do)}/{len(a)}")
    ALL+=rows
od=[x['od'] for x in ALL]
print(f"== 전체 {len(od)}번: 하루 손익 플러스 {sum(v>0 for v in od)} 마이너스 {sum(v<0 for v in od)} 평균 {st.mean(od):+.1f}원/주 중앙 {st.median(od):+.1f}")
# 덧셈(레드팀 10/22): 세금 안 뗀 경우(ISA·연금계좌), 종가에 판 경우, 상품별 평균, 수수료 편도 0.015%
print('== 덧셈')
import collections
by=collections.defaultdict(list)
for x in ALL: by[x['amt']>0].append(x)
nt=[(x['o']-x['pc'])+x['amt'] for x in ALL]; cl=[(x['c']-x['pc'])+x['amt']*(1-TAX) for x in ALL]
fee=[x['od']-0.00015*(x['pc']+x['o']) for x in ALL]
print(f"세금 안 뗌 평균 {st.mean(nt):+.1f} 이득 {sum(v>0 for v in nt)}/{len(nt)}")
print(f"종가에 팜 평균 {st.mean(cl):+.1f} 이득 {sum(v>0 for v in cl)}/{len(cl)}")
print(f"수수료 0.015%x2 평균 {st.mean(fee):+.1f} 이득 {sum(v>0 for v in fee)}/{len(fee)}")
gain=[v for v in od if v>0]; loss=[v for v in od if v<0]
print(f"이득 평균 {st.mean(gain):+.1f} 손해 평균 {st.mean(loss):+.1f}")
