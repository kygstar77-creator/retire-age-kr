# 금감원 finlife 적금·정기예금 원자료 저장 (은행권 020000) — saving1011b
import sys, json, time; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
sys.stdout.reconfigure(encoding='utf-8')
import apis
k = apis.key('finlife')
for kind, ep in [('saving','savingProductsSearch'),('deposit','depositProductsSearch')]:
    allb, allo = [], []
    for pg in (1,2,3):
        d = apis._j(f'http://finlife.fss.or.kr/finlifeapi/{ep}.json?auth={k}&topFinGrpNo=020000&pageNo={pg}').get('result', {})
        allb += d.get('baseList', []); allo += d.get('optionList', [])
        if pg >= int(d.get('max_page_no', 1) or 1): break
    json.dump({'at': time.strftime('%Y-%m-%d %H:%M'), 'base': allb, 'opt': allo}, open(f'fin_{kind}.json','w',encoding='utf-8'), ensure_ascii=False, indent=0)
    print(kind, len(allb), len(allo))
