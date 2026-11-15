# 금리인하요구권 2026 상반기(은행연합회) — 가계 신용 vs 주택담보 계산 · firemap-write 11/15
import json, sys, re, html
sys.stdout.reconfigure(encoding='utf-8')
T = json.load(open('raw/kfb_tables.json', encoding='utf-8'))
def num(s):
    s = s.replace(',', '').strip()
    return None if s in ('-', '') else float(s)
def parse(rows):
    out = {}; bank = None; grp = None
    for r in rows[1:]:
        r = [c for c in r]
        if r and r[-1] == '' : r = r[:-1]
        if len(r) == 9: bank, grp, r = r[0], r[1], r[2:]
        elif len(r) == 8: grp, r = r[0], r[1:]
        if len(r) != 7: continue
        k = r[0]
        if k == '전체합계': grp = '전체합계'
        out.setdefault(bank, {})[(grp, k)] = dict(zip(['신청','수용','감면','인하','수용률','비대면'], map(num, r[1:])))
    return out
for per in ['2026-1', '2025-2', '2025-1']:
    D = parse(T[per]); print('=====', per, '은행', len(D))
    tot = {}
    for b, d in D.items():
        for key in [('가계대출','신용'), ('가계대출','(주택담보)'), ('가계대출','소계'), ('전체합계','전체합계')]:
            x = d.get(key) or (d.get(('전체합계','전체합계')) if key[0]=='전체합계' else None)
            if not x or x['신청'] is None or x['수용'] is None: continue
            t = tot.setdefault(key, [0,0,0])
            t[0]+=x['신청']; t[1]+=x['수용']; t[2]+=x['감면'] or 0
        s, h = d.get(('가계대출','신용')), d.get(('가계대출','(주택담보)'))
        if s and s['수용'] and h and h['수용']:
            print(f"{b:14} 신용 수용률 {s['수용률']:5}% 인하 {s['인하']}%p 1건당 {s['감면']*1e6/s['수용']/1e4:6.1f}만원 | 주담 수용률 {h['수용률']:5}% 인하 {h['인하']}%p 1건당 {h['감면']*1e6/h['수용']/1e4:6.1f}만원")
    for k, (a, c, m) in tot.items():
        print('합계', k, f'신청 {a:,.0f} 수용 {c:,.0f} 수용률 {c/a*100:.1f}% 감면 {m:,.0f}백만원 1건당 {m*1e6/c/1e4:.1f}만원')
# 5대 은행만 · 전체합계(기업 포함) 은행 합
D = parse(T['2026-1']); D2 = parse(T['2025-2'])
for nm, DD in [('2026상', D), ('2025하', D2)]:
    a = sum(d[('전체합계','전체합계')]['신청'] for d in DD.values() if d.get(('전체합계','전체합계')) and d[('전체합계','전체합계')]['신청'])
    c = sum(d[('전체합계','전체합계')]['수용'] for d in DD.values() if d.get(('전체합계','전체합계')) and d[('전체합계','전체합계')]['수용'])
    m = sum(d[('전체합계','전체합계')]['감면'] or 0 for d in DD.values() if d.get(('전체합계','전체합계')))
    print(nm, f'전체 신청 {a:,.0f} 수용 {c:,.0f} 수용률 {c/a*100:.1f}% 감면 {m:,.0f}백만원')
for b in ['KB국민은행','신한은행','하나은행','우리은행','NH농협은행','카카오뱅크']:
    s, h = D[b][('가계대출','신용')], D[b][('가계대출','(주택담보)')]
    print('예시', b, '신용 1억원×', s['인하'], '%p =', round(1e8*s['인하']/100/1e4), '만원/년 · 주담 3억원×', h['인하'], '%p =', round(3e8*h['인하']/100/1e4), '만원/년')
for b in ['KB국민은행','신한은행','하나은행','우리은행','NH농협은행']:
    print('비대면', b, D[b][('가계대출','소계')]['비대면'])
