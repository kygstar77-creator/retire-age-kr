# -*- coding: utf-8 -*-
"""SEC EDGAR Form 4에서 '내부자 매수(코드 P)'만 뽑는다.

사용: py -3.12 work/insider.py [상위건수=20] [--days N=2] [--max M=400] [--min-amt 달러]
출처: 일별 인덱스 https://www.sec.gov/Archives/edgar/daily-index/<연>/QTR<분기>/form.<YYYYMMDD>.idx (무키·공개)

2026-09-23 고침: 예전에는 browse-edgar?action=getcurrent 피드를 썼는데 그게 최근 20건만 줘서
매수(P)가 회당 1건밖에 안 잡혔다(tools-wanted.md 16시 기록). 일별 인덱스는 그날 접수분 전체를 준다
— 2026-09-22 하루치 Form 4 847건 확인. SEC 요청 한도(초당 10회)를 지키려 0.12초씩 쉬고,
한 회차에 --max 건까지만 읽는다(기본 400).
"""
import sys, re, json, time, datetime, urllib.request, xml.etree.ElementTree as ET
sys.stdout.reconfigure(encoding='utf-8')
UA = {'User-Agent': 'firemap research kygstar77@gmail.com'}
GAP = 0.12                      # SEC 초당 10회 한도 — 넉넉히 8회/초

def get(u, t=25):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=t).read()

def day_index(d):
    """그날 접수된 Form 4의 (회사명, CIK, 접수일, 경로) 목록. 주말·공휴일은 404 → 빈 목록."""
    u = f'https://www.sec.gov/Archives/edgar/daily-index/{d.year}/QTR{(d.month - 1) // 3 + 1}/form.{d:%Y%m%d}.idx'
    try:
        txt = get(u).decode('utf-8', 'ignore')
    except Exception as e:
        print(f'# {d:%Y-%m-%d} 인덱스 없음({type(e).__name__})', file=sys.stderr)
        return []
    rows = []
    for l in txt.splitlines():
        m = re.match(r'^4\s{2,}(.+?)\s{2,}(\d+)\s+(\d{8})\s+(edgar/data/\S+\.txt)\s*$', l)
        if m: rows.append((m.group(1).strip(), m.group(2), m.group(3), m.group(4)))
    return rows

def parse_form4(txt, url):
    """Form 4 원문에서 매수(P) 거래만 뽑는다. 원문에 있는 숫자만 쓴다."""
    m = re.search(r'<ownershipDocument>.*?</ownershipDocument>', txt, re.S)
    if not m: return []
    try: d = ET.fromstring(m.group(0))
    except Exception: return []
    def tx(p):
        e = d.find(p); return e.text.strip() if e is not None and e.text else ''
    issuer, tick = tx('issuer/issuerName'), tx('issuer/issuerTradingSymbol')
    owner = tx('reportingOwner/reportingOwnerId/rptOwnerName')
    rel, roles = d.find('reportingOwner/reportingOwnerRelationship'), []
    if rel is not None:
        for tag, lab in (('isDirector', '이사'), ('isOfficer', '임원'), ('isTenPercentOwner', '10%주주')):
            e = rel.find(tag)
            if e is not None and (e.text or '').strip() in ('1', 'true'): roles.append(lab)
        ot = rel.find('officerTitle')
        if ot is not None and ot.text: roles.append(ot.text.strip())
    out = []
    for t in d.findall('nonDerivativeTable/nonDerivativeTransaction'):
        if t.findtext('transactionCoding/transactionCode', '').strip() != 'P': continue
        sh = t.findtext('transactionAmounts/transactionShares/value', '').strip()
        pr = t.findtext('transactionAmounts/transactionPricePerShare/value', '').strip()
        try: amt = float(sh) * float(pr)
        except Exception: amt = 0.0
        out.append(dict(issuer=issuer, ticker=tick, owner=owner, roles=' '.join(roles),
                        date=t.findtext('transactionDate/value', '').strip(), shares=sh, price=pr,
                        amount=amt,
                        owned=t.findtext('postTransactionAmounts/sharesOwnedFollowingTransaction/value', '').strip(),
                        url=url))
    return out

def main(argv):
    top = int(argv[0]) if argv and not argv[0].startswith('--') else 20
    def opt(name, dflt):
        return type(dflt)(argv[argv.index(name) + 1]) if name in argv else dflt
    days, cap, min_amt = opt('--days', 2), opt('--max', 400), opt('--min-amt', 0.0)

    filings, d, tried = [], datetime.date.today(), 0
    while len({f[2] for f in filings}) < days and tried < days + 6:
        filings += day_index(d)
        d -= datetime.timedelta(days=1); tried += 1
        time.sleep(GAP)
    filings = filings[:cap]

    out, read, seen = [], 0, set()
    for name, cik, filed, path in filings:
        url = 'https://www.sec.gov/Archives/' + path
        acc = path.rsplit('/', 1)[-1]     # 같은 접수번호가 발행사·신고자 CIK 경로로 두 번 올라온다
        if acc in seen: continue
        seen.add(acc)
        try:
            out += parse_form4(get(url).decode('utf-8', 'ignore'), url)
        except Exception:
            pass
        read += 1
        time.sleep(GAP)
    out = [r for r in out if r['amount'] >= min_amt]
    out.sort(key=lambda r: -r['amount'])
    for r in out[:top]:
        print(json.dumps(r, ensure_ascii=False))
    print(f'# 매수(P) {len(out)}건 / Form 4 {read}건 조회 ({days}일치, 상위 {min(top, len(out))}건 출력)',
          file=sys.stderr)

if __name__ == '__main__':
    main(sys.argv[1:])
