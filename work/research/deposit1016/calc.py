# deposit1016 계산 — 1천만원 12개월 단리, 이자소득세 15.4%(소득세 14%+지방소득세 1.4%)
import json
r=json.load(open('finlife_deposit.json',encoding='utf-8'))
want={'농협은행주식회사':'NH올원e예금','우리은행':'WON플러스예금','주식회사 하나은행':'하나의정기예금','신한은행':'쏠편한 정기예금','국민은행':'KB Star 정기예금'}
out=[]
for x in r:
    if str(x['기간'])=='12' and want.get(x['은행'])==x['상품']:
        for lab,rate in (('기본',x['금리']),('최고',x['최고금리'])):
            pre=10_000_000*rate/100; post=pre*(1-0.154)
            out.append((x['은행'],x['상품'],lab,rate,round(pre),round(post)))
for o in out: print(o)
json.dump(out,open('calc_out.json','w',encoding='utf-8'),ensure_ascii=False)
