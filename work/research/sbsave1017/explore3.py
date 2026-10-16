import json, sys
sys.stdout.reconfigure(encoding='utf-8')
d = json.load(open('raw/finlife_saving_1017.json', encoding='utf-8'))
base = {(b['fin_co_no'], b['fin_prdt_cd']): b for b in d['030300']['base']}
opts = [o for o in d['030300']['opt'] if o['save_trm']=='12']
opts.sort(key=lambda o: -(o['intr_rate'] or 0))
seen=set(); n=0
for o in opts:
    b = base[(o['fin_co_no'], o['fin_prdt_cd'])]
    k=(b['kor_co_nm'], b['fin_prdt_nm'])
    if k in seen: continue
    seen.add(k); n+=1
    if n>14: break
    print(f"{o['intr_rate']}/{o['intr_rate2']} {o['rsrv_type']}{o['intr_rate_type']} | {b['kor_co_nm']} | {b['fin_prdt_nm']} | lim={b['max_limit']} deny={b['join_deny']} | 대상: {b['join_member']} | 방법: {b['join_way']}\n   etc: {(b['etc_note'] or '')[:150]!r}\n   우대: {(b['spcl_cnd'] or '')[:120]!r}")
