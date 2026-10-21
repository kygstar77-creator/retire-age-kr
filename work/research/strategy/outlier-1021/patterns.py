# 돈 주제 아웃라이어(조회÷구독 ≥10, 조회 3,000+, 구독 1만 미만, 90일)에서 제목 구조별 숫자
import json, re, sys, statistics, collections, csv, os
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
ch = json.load(open(os.path.join(H,'channels.json'),encoding='utf-8')); vd = json.load(open(os.path.join(H,'videos.json'),encoding='utf-8'))
MONEY = re.compile(r'연금|퇴직|은퇴|노후|세금|절세|상속|증여|양도세|종부세|재산세|건보료|건강보험|기초수급|수급자|지원금|복지|혜택|아파트|부동산|집값|전세|월세|청약|재건축|입지|실거래|연봉|월급|실수령|성과급|호봉|돈|원 |만원|억|재산|자산|순자산|보험|주식|배당|ETF|금리|대출|환율|금값|기업|회장|재벌|가계도|영업이익|경제|생활비|예금|적금|저축|절약|짠테크|소득|폐업|창업|실업급여|일자리|요양|실버타운|부자|퇴사')
PAT = [
 ('한장표쇼츠(≤12초)', lambda v,t: v['sec'] <= 12),
 ('순위·TOP N', lambda v,t: re.search(r'TOP ?\d+|순위|\d+위|랭킹|1위', t, re.I)),
 ('N가지·N선 목록', lambda v,t: re.search(r'\d+ ?가지|\d+선\b|\d+곳|\d+개', t)),
 ('~한 (진짜) 이유', lambda v,t: re.search(r'이유', t)),
 ('나이·인물 사연(N세 ○○한 남자…)', lambda v,t: re.search(r'\d{2}세|\d0대 (남자|여자|부부|가장|주부|부장)|살 (남자|여자)', t) and re.search(r'남자|여자|부부|가장|주부|부장|아내|남편', t)),
 ('A vs B 비교', lambda v,t: re.search(r'vs|VS|비교|차이', t)),
 ('계산·얼마 받나(질문)', lambda v,t: re.search(r'얼마|몇 살|몇살|계산|받을까|받나|이득', t)),
 ('모르면 손해·놓치는', lambda v,t: re.search(r'모르면|놓치|손해|날리', t)),
 ('총정리·완전정리·한눈에', lambda v,t: re.search(r'총정리|완전정리|한눈에|한 장|정리', t)),
 ('연예인·재벌·인물 돈', lambda v,t: re.search(r'연예인|회장|재벌|가계도|스타|가수|배우', t)),
 ('지역·단지(입지·아파트 역사)', lambda v,t: re.search(r'입지|신도시|아파트 \||\| [가-힣]+아파트|단지|동네|구 |시 ', t) and re.search(r'아파트|입지|신도시|단지', t)),
 ('속보·발표·바뀐다(제도 뉴스)', lambda v,t: re.search(r'속보|발표|바뀌|달라지|개편|인상|시행|부터', t)),
 ('실패·몰락·위기(사건)', lambda v,t: re.search(r'몰락|위기|폭락|무너|파산|망한|망할|비극|충격', t)),
]
rows = []
for cid, vs in vd.items():
    c = ch[cid]; subs = max(c['subs'],1)
    for v in vs:
        x = v['views']/subs
        if x >= 10 and v['views'] >= 3000 and MONEY.search(v['title']):
            rows.append(dict(v, x=x, cid=cid, ch=c['title'], subs=c['subs'], opened=c['opened']))
print('돈 주제 아웃라이어', len(rows), '채널', len({r['cid'] for r in rows}), '| 50배+', sum(r['x']>=50 for r in rows), '| 개설 12개월 안 채널', len({r['cid'] for r in rows if r['opened']>='2025-10-21'}))
res = []
for name, f in PAT:
    m = [r for r in rows if f(r, r['title'])]
    if not m: continue
    chs = collections.Counter(r['cid'] for r in m)
    res.append(dict(pattern=name, videos=len(m), channels=len(chs), new_ch=len({r['cid'] for r in m if r['opened']>='2025-10-21'}),
        med_x=round(statistics.median([r['x'] for r in m]),1), med_views=round(statistics.median([r['views'] for r in m])),
        short_share=round(sum(r['sec']<=180 for r in m)/len(m),2), x50=sum(r['x']>=50 for r in m),
        long_n=sum(r['sec']>180 for r in m), long_med_views=round(statistics.median([r['views'] for r in m if r['sec']>180])) if any(r['sec']>180 for r in m) else None))
for r in res: print(r)
json.dump(dict(total=len(rows), patterns=res), open(os.path.join(H,'patterns.json'),'w',encoding='utf-8'), ensure_ascii=False, indent=1)
with open(os.path.join(H,'money_outliers.csv'),'w',encoding='utf-8-sig',newline='') as f:
    w = csv.writer(f); w.writerow(['x_subs','views','subs','sec','pub','opened','channel','id','title'])
    for r in sorted(rows, key=lambda r:-r['x']): w.writerow([round(r['x'],1), r['views'], r['subs'], r['sec'], r['pub'], r['opened'], r['ch'], r['id'], r['title']])
