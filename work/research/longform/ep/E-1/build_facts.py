"""E-1 메모리 3사 실적 원자료 → 분기표 (2026-09-30).
마이크론: SEC XBRL companyfacts(분기 3개월값만, 4분기는 연간-9개월 누적으로 계산, 표시).
SK하이닉스·삼성전자: OpenDART 단일회사 주요계정(fnlttSinglAcnt, 연결). 1·3분기·반기 3개월값, 4분기=연간-3개 분기 합.
출력: raw/*.json 원본, quarters.json(계산표). 값은 원 단위 그대로, 화면·대본은 이 파일에서만 뽑는다."""
import json, os, sys, urllib.request, datetime
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, 'raw')
def d(s): return datetime.date.fromisoformat(s)

# ---- 마이크론 (회계연도 9월 초 끝)
f = json.load(open(os.path.join(R, 'mu_facts.json'), encoding='utf-8'))['facts']['us-gaap']
def mu_series(tag):
    q, fy, cum9 = {}, {}, {}
    for x in f[tag]['units']['USD']:
        if 'start' not in x: continue
        days = (d(x['end']) - d(x['start'])).days
        if 80 <= days <= 100: q[x['end']] = x['val']
        elif 350 <= days <= 380: fy[x['end']] = (x['start'], x['val'])
    out = {k: {'v': v, 'calc': False} for k, v in q.items()}
    for end, (start, val) in fy.items():
        if end in out: continue
        three = [v for k, v in q.items() if start < k < end]
        if len(three) == 3: out[end] = {'v': val - sum(three), 'calc': True}
    return dict(sorted(out.items()))
mu = {}
for name, tags in (('매출', ['Revenues', 'RevenueFromContractWithCustomerExcludingAssessedTax']), ('영업이익', ['OperatingIncomeLoss']), ('순이익', ['NetIncomeLoss'])):
    s = {}
    for t in tags:
        if t in f: s.update(mu_series(t))
    mu[name] = s

# ---- DART
key = open(r'C:\Users\강영준\Documents\dart_key.txt', encoding='utf-8-sig').read().strip().split('=')[-1].strip()
CORP = {'SK하이닉스': '00164779', '삼성전자': '00126380'}
RC = [('11013', 'Q1'), ('11012', 'Q2'), ('11014', 'Q3'), ('11011', 'FY')]
def dart(corp, year, rc):
    p = os.path.join(R, f'dart_{corp}_{year}_{rc}.json')
    if not os.path.exists(p):
        u = f'https://opendart.fss.or.kr/api/fnlttSinglAcnt.json?crtfc_key={key}&corp_code={corp}&bsns_year={year}&reprt_code={rc}'
        j = json.load(urllib.request.urlopen(u, timeout=30))
        if j.get('status') != '000': return None
        json.dump(j, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
    return json.load(open(p, encoding='utf-8'))
def num(s): return int(s.replace(',', '')) if s and s.strip() not in ('', '-') else None
kr = {}
ACC = {'매출': '매출액', '영업이익': '영업이익', '순이익': '당기순이익'}
for nm, corp in CORP.items():
    kr[nm] = {k: {} for k in ACC}
    for y in (2024, 2025, 2026):
        got = {}
        for rc, lab in RC:
            j = dart(corp, y, rc)
            if not j: continue
            for row in j['list']:
                if row['fs_div'] != 'CFS': continue
                for k, a in ACC.items():
                    if row['account_nm'] == a: got.setdefault(lab, {})[k] = num(row['thstrm_amount'])
        for k in ACC:
            for lab in ('Q1', 'Q2', 'Q3'):
                if lab in got and got[lab].get(k) is not None: kr[nm][k][f'{y}{lab}'] = {'v': got[lab][k], 'calc': False}
            if 'FY' in got and all(f'{y}{l}' in kr[nm][k] for l in ('Q1', 'Q2', 'Q3')):
                kr[nm][k][f'{y}Q4'] = {'v': got['FY'][k] - sum(kr[nm][k][f'{y}{l}']['v'] for l in ('Q1', 'Q2', 'Q3')), 'calc': True}
out = {'기준': '2026-09-30 받음. 마이크론=달러(분기 끝 날짜 키), 한국 2사=원(연도+분기 키). calc=True는 연간-나머지 분기로 계산한 값',
       '마이크론': mu, **kr}
json.dump(out, open(os.path.join(H, 'quarters.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for nm in ('마이크론', 'SK하이닉스', '삼성전자'):
    print('==', nm)
    s = out[nm]
    for k in list(s['매출'])[-10:]:
        rv = s['매출'][k]['v']; oi = s['영업이익'].get(k, {}).get('v')
        print(f"  {k}  매출 {rv:>20,}  영업이익 {oi if oi is None else format(oi, ','):>20}  이익률 {'' if not oi else round(oi / rv * 100, 1)}%  {'(계산)' if s['매출'][k]['calc'] else ''}")
