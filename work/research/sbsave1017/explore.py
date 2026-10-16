import json, statistics as st, collections, re, sys
sys.stdout.reconfigure(encoding='utf-8')
d = json.load(open('raw/finlife_saving_1017.json', encoding='utf-8'))
for g, nm in (('020000','은행'),('030300','저축은행')):
    base = {(b['fin_co_no'], b['fin_prdt_cd']): b for b in d[g]['base']}
    print(nm, 'companies', len({b['kor_co_nm'] for b in base.values()}), 'products', len(base))
    c = collections.Counter((o['save_trm'], o['rsrv_type'], o['intr_rate_type']) for o in d[g]['opt'] if o['save_trm']=='12')
    print(' 12m opts by (rsrv,type):', c)
    print(' join_deny:', collections.Counter(b['join_deny'] for b in base.values()))
    print(' max_limit non-null:', sum(1 for b in base.values() if b['max_limit']), [b['max_limit'] for b in list(base.values())[:8]])
    print(' dcls_month', collections.Counter(b['dcls_month'] for b in base.values()))
