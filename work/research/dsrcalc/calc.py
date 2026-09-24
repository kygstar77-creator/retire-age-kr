# DSR 한도로 대출 가능액 계산 — 원자료: 금감원 finlife 주담대 공시(2026년 9월), 금융위 DSR 40%
import sys, os, json, statistics as st
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
import apis

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, 'raw')
os.makedirs(RAW, exist_ok=True)

def pull():
    import urllib.request
    k = apis.key('finlife')
    out = []
    for g in ['020000']:
        for p in (1, 2, 3):
            u = f'http://finlife.fss.or.kr/finlifeapi/mortgageLoanProductsSearch.json?auth={k}&topFinGrpNo={g}&pageNo={p}'
            d = json.loads(urllib.request.urlopen(u, timeout=25).read().decode('utf-8'))['result']
            if d.get('err_cd') != '000': break
            base = {b['fin_prdt_cd']: b for b in d.get('baseList', [])}
            for o in d.get('optionList', []):
                b = base.get(o['fin_prdt_cd'], {})
                out.append(dict(은행=b.get('kor_co_nm'), 상품=b.get('fin_prdt_nm'), 공시월=b.get('dcls_month'),
                                금리유형=o.get('lend_rate_type_nm'), 상환방식=o.get('rpay_type_nm'),
                                최저=o.get('lend_rate_min'), 최고=o.get('lend_rate_max'), 평균=o.get('lend_rate_avg')))
            if int(d.get('max_page_no', 1)) <= p: break
    json.dump(out, open(os.path.join(RAW, 'mortgage.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return out

def monthly(principal, rate_pct, years):
    """원리금균등상환 월 납입액"""
    r = rate_pct / 100 / 12
    n = years * 12
    return principal * r / (1 - (1 + r) ** -n)

def loan_cap(annual_income, dsr_pct, rate_pct, years):
    """DSR 한도 안에서 빌릴 수 있는 원금"""
    cap_month = annual_income * dsr_pct / 100 / 12
    r = rate_pct / 100 / 12
    n = years * 12
    return cap_month * (1 - (1 + r) ** -n) / r

if __name__ == '__main__':
    rows = pull()
    lo = [float(x['최저']) for x in rows if x['최저']]
    hi = [float(x['최고']) for x in rows if x['최고']]
    print('== 금감원 주담대 공시(은행) ==')
    print('공시월', sorted(set(x['공시월'] for x in rows)), '상품옵션', len(rows), '은행', len(set(x['은행'] for x in rows)))
    print('최저금리 min %.2f / 중앙 %.2f / max %.2f' % (min(lo), st.median(lo), max(lo)))
    print('최고금리 min %.2f / 중앙 %.2f / max %.2f' % (min(hi), st.median(hi), max(hi)))
    for t in sorted(set(x['금리유형'] for x in rows if x['금리유형'])):
        v = [float(x['최저']) for x in rows if x['금리유형'] == t and x['최저']]
        print('  %s %d개 · 최저금리 중앙 %.2f (%.2f~%.2f)' % (t, len(v), st.median(v), min(v), max(v)))
    for t in sorted(set(x['상환방식'] for x in rows if x['상환방식'])):
        v = [float(x['최저']) for x in rows if x['상환방식'] == t and x['최저']]
        print('  %s %d개 · 최저금리 중앙 %.2f' % (t, len(v), st.median(v)))

    BASE = st.median(lo)
    print()
    print('== 연소득별 DSR 40%% 한도 (금리 %.2f%%, 원리금균등) ==' % BASE)
    print('연소득(만원) | 연 원리금 한도(만원) | 월 한도(만원) | 30년 한도(만원) | 40년 한도(만원)')
    for inc in (3000, 4000, 5000, 6000, 7000, 8000, 10000):
        y = inc * 10000
        print('%s | %.0f | %.1f | %.0f | %.0f' % (
            f'{inc:,}', y * .4 / 10000, y * .4 / 12 / 10000,
            loan_cap(y, 40, BASE, 30) / 10000, loan_cap(y, 40, BASE, 40) / 10000))

    print()
    print('== 금리별 한도 (연소득 5,000만원, DSR 40%, 30년) ==')
    print('금리 | 30년 한도(만원) | 월 원리금(만원)')
    for r in (3.70, 4.50, 5.25, 6.00, 6.51):
        cap = loan_cap(50000000, 40, r, 30)
        print('%.2f%% | %.0f | %.1f' % (r, cap / 10000, monthly(cap, r, 30) / 10000))

    print()
    print('== 스트레스 DSR 1.50%p를 얹었을 때 (연소득 5,000만원, 30년) ==')
    for r in (3.70, 5.25, 6.51):
        a = loan_cap(50000000, 40, r, 30)
        b = loan_cap(50000000, 40, r + 1.50, 30)
        print('%.2f%% → 한도 %.0f만원 / 스트레스 %.2f%% 적용 시 %.0f만원 (차이 %.0f만원, %.1f%%)' % (
            r, a / 10000, r + 1.5, b / 10000, (a - b) / 10000, (a - b) / a * 100))

    print()
    print('== 신용대출 4,000만원(금리 5.00%, 만기 5년)이 이미 있을 때 ==')
    other = monthly(40000000, 5.00, 5) * 12
    print('신용대출 연 원리금 %.0f만원' % (other / 10000))
    for inc in (4000, 5000, 6000, 7000):
        y = inc * 10000
        room = y * .4 - other
        cap = 0 if room <= 0 else loan_cap(room / .4 * 1.0, 40, BASE, 30)
        print('연소득 %s만원 · 남는 연 원리금 %.0f만원 · 주담대 한도 %.0f만원' % (f'{inc:,}', room / 10000, cap / 10000))
