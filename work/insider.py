# -*- coding: utf-8 -*-
"""SEC EDGAR Form 4 최근 제출분에서 '내부자 매수(코드 P)'만 뽑는다.
사용: python work/insider.py [건수]
출처: https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=4 (무키·공개)
"""
import sys, re, json, urllib.request, xml.etree.ElementTree as ET
sys.stdout.reconfigure(encoding='utf-8')
UA = {'User-Agent': 'firemap research kygstar77@gmail.com'}

def get(u, t=25):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=t).read()

def main(n=60):
    idx = get(f'https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=4&dateb=&owner=include&count={n}&output=atom').decode('utf-8', 'ignore')
    links = re.findall(r'<link rel="alternate" type="text/html" href="([^"]+)"/>', idx)
    seen, out = set(), []
    for href in links:
        acc = href.rsplit('/', 1)[-1].replace('-index.htm', '')
        if acc in seen: continue
        seen.add(acc)
        base = href.rsplit('/', 1)[0]
        try:
            txt = get(base + '/' + acc + '.txt').decode('utf-8', 'ignore')
        except Exception:
            continue
        m = re.search(r'<ownershipDocument>.*?</ownershipDocument>', txt, re.S)
        if not m: continue
        try:
            d = ET.fromstring(m.group(0))
        except Exception:
            continue
        def tx(p):
            e = d.find(p); return e.text.strip() if e is not None and e.text else ''
        issuer = tx('issuer/issuerName'); tick = tx('issuer/issuerTradingSymbol')
        owner = tx('reportingOwner/reportingOwnerId/rptOwnerName')
        rel = d.find('reportingOwner/reportingOwnerRelationship')
        roles = []
        if rel is not None:
            for tag, lab in (('isDirector','이사'), ('isOfficer','임원'), ('isTenPercentOwner','10%주주')):
                e = rel.find(tag)
                if e is not None and (e.text or '').strip() in ('1', 'true'): roles.append(lab)
            ot = rel.find('officerTitle')
            if ot is not None and ot.text: roles.append(ot.text.strip())
        for t in d.findall('nonDerivativeTable/nonDerivativeTransaction'):
            code = t.findtext('transactionCoding/transactionCode', '').strip()
            if code != 'P': continue
            date = t.findtext('transactionDate/value', '').strip()
            sh = t.findtext('transactionAmounts/transactionShares/value', '').strip()
            pr = t.findtext('transactionAmounts/transactionPricePerShare/value', '').strip()
            own = t.findtext('postTransactionAmounts/sharesOwnedFollowingTransaction/value', '').strip()
            try: amt = float(sh) * float(pr)
            except Exception: amt = 0.0
            out.append(dict(issuer=issuer, ticker=tick, owner=owner, roles=' '.join(roles),
                            date=date, shares=sh, price=pr, amount=amt, owned=own,
                            url=(base if base.startswith('http') else 'https://www.sec.gov' + base) + '/' + acc + '-index.htm'))
    out.sort(key=lambda r: -r['amount'])
    for r in out:
        print(json.dumps(r, ensure_ascii=False))
    print(f'# 매수(P) {len(out)}건 / Form 4 {len(seen)}건 조회', file=sys.stderr)

if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 60)
