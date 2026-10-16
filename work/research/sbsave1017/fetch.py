import sys, json
sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
sys.stdout.reconfigure(encoding='utf-8')
import apis
out = {}
for g in ('020000', '030300'):
    rows = []; base_all = {}; opt_all = []
    p = 1
    while True:
        k = apis.key('finlife')
        d = apis._j(f'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={k}&topFinGrpNo={g}&pageNo={p}').get('result', {})
        if d.get('err_cd') != '000': print('err', g, p, d.get('err_cd'), d.get('err_msg')); break
        for b in d.get('baseList', []): base_all[(b['fin_co_no'], b['fin_prdt_cd'])] = b
        opt_all += d.get('optionList', [])
        mp = int(d.get('max_page_no', 1)); print(g, p, '/', mp, len(d.get('optionList', [])))
        if p >= mp: break
        p += 1
    out[g] = {'base': list(base_all.values()), 'opt': opt_all}
json.dump(out, open('raw/finlife_saving_1017.json', 'w', encoding='utf-8'), ensure_ascii=False)
print({g: (len(v['base']), len(v['opt'])) for g, v in out.items()})
b = out['020000']['base'][0]; print(b); print(out['020000']['opt'][0])
