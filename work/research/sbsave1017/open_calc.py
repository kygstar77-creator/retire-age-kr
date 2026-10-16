# 가입 대상 제한 없는 적금만 — 공시 '가입 대상' 칸 글자로 거른다(finlife join_member)
import json, re, sys, statistics as st
sys.stdout.reconfigure(encoding='utf-8')
d = json.load(open('raw/finlife_saving_1017.json', encoding='utf-8'))
def nm(s): return s.replace('주식회사 ','').replace(' 주식회사','').replace('농협은행주식회사','농협은행').replace('\n','').strip()
OPEN = re.compile(r'제한\s*없|누구나|모든\s*고객|^(?:만\s*\d+\s*세\s*이상\s*)?(?:내국인\s*)?(?:실명의\s*)?개인(?:\s*고객)?(?:\s*(?:및|/|또는)\s*(?:개인사업자|법인)(?:\s*고객)?)*$|^내.외국인')
def rows(g):
    base = {(b['fin_co_no'], b['fin_prdt_cd']): b for b in d[g]['base']}
    out = []
    for o in d[g]['opt']:
        if o['save_trm'] != '12' or o['intr_rate'] is None: continue
        b = base[(o['fin_co_no'], o['fin_prdt_cd'])]
        jm = re.sub(r'\s+', ' ', (b['join_member'] or '')).strip()
        way = b['join_way'] or ''
        out.append(dict(co=nm(b['kor_co_nm']), prd=re.sub(r'\s+', ' ', b['fin_prdt_nm']).strip(), r=o['intr_rate'], rmax=o['intr_rate2'], rs=o['rsrv_type'], it=o['intr_rate_type'],
                        lim=b['max_limit'], jm=jm, way=way, open=bool(OPEN.search(jm)), online=('인터넷' in way or '스마트폰' in way), etc=(b['etc_note'] or '').replace('\n', ' / ')[:90]))
    return out
for g, lab in (('020000', '은행'), ('030300', '저축은행')):
    R = rows(g)
    print('=====', lab, '12개월 줄', len(R), '대상 제한 없음 판정', sum(x['open'] for x in R), '(그중 앱·인터넷 가입', sum(x['open'] and x['online'] for x in R), ')')
    best = {}
    for x in R:
        if not x['open']: continue
        if x['co'] not in best or x['r'] > best[x['co']]['r']: best[x['co']] = x
    print('  대상 제한 없는 상품이 있는 회사', len(best), '곳, 회사별 최고 기본금리 중앙', st.median([x['r'] for x in best.values()]))
    for x in sorted(best.values(), key=lambda x: -x['r'])[:12]:
        print(f"   {x['r']:.2f}/{x['rmax']} {x['rs']}{x['it']} {x['co']} | {x['prd'][:26]} | 한도 {x['lim']} | 대상 {x['jm'][:24]} | {'앱' if x['online'] else '영업점만'} | {x['etc'][:60]}")
    # 판정 안 된 대상 칸 값 목록(검수용)
    other = sorted({x['jm'][:40] for x in R if not x['open']})
    print('  [제한 있음으로 본 대상 칸]', len(other), other[:40])
