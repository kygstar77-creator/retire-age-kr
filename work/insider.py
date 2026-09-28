# -*- coding: utf-8 -*-
"""SEC EDGAR Form 4에서 '내부자 매수(코드 P)'만 뽑는다.

사용: py -3.12 work/insider.py [상위건수=20] [--days N=2] [--max M=400] [--min-amt 달러]
출처: 일별 인덱스 https://www.sec.gov/Archives/edgar/daily-index/<연>/QTR<분기>/form.<YYYYMMDD>.idx (무키·공개)

2026-09-23 고침: 예전에는 browse-edgar?action=getcurrent 피드를 썼는데 그게 최근 20건만 줘서
매수(P)가 회당 1건밖에 안 잡혔다(tools-wanted.md 16시 기록). 일별 인덱스는 그날 접수분 전체를 준다
— 2026-09-22 하루치 Form 4 847건 확인. SEC 요청 한도(초당 10회)를 지키려 0.12초씩 쉬고,
한 회차에 --max 건까지만 읽는다(기본 400).
"""
import sys, os, re, json, time, datetime, urllib.request, xml.etree.ElementTree as ET
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
        fx = price_currency_note(d, t)
        out.append(dict(fxnote=fx, issuer=issuer, ticker=tick, owner=owner, roles=' '.join(roles),
                        date=t.findtext('transactionDate/value', '').strip(), shares=sh, price=pr,
                        amount=amt,
                        owned=t.findtext('postTransactionAmounts/sharesOwnedFollowingTransaction/value', '').strip(),
                        url=url))
    return out

FX_WORDS = re.compile(r'peso|MXN|real(?:s)?|BRL|shekel|NIS|ILS|canadian dollar|CAD|euro|EUR|GBP|pound|yen|JPY|CHF|HKD|INR|rupee', re.I)

def price_currency_note(d, t):
    """단가(transactionPricePerShare)에 달린 각주가 외화를 말하면 그 문장을 돌려준다.

    2026-09-29 04시 원고: 세멕스(CX) 이사 매수 400,800주 @17.2812가 각주 F2 "Price in Mexican Pesos"였는데
    달러로 세어 690만 달러, 명단 3위로 올라왔다(실제 약 39만 달러). 뉴욕 ADR 1주 = CPO 10주라
    ADR 종가 9.5달러와 비율이 1.8배밖에 안 나 currency_flag의 3배 문턱을 통과했다.
    환율(exchange rate)까지 적어 달러로 바꿔 신고한 경우(NYAX: "paid in NIS ... exchange rate 3.047")는 달러로 본다.
    """
    ids = [e.get('id') for e in t.findall('transactionAmounts/transactionPricePerShare/footnoteId')]
    for fn in d.findall('footnotes/footnote'):
        if fn.get('id') not in ids: continue
        txt = ' '.join(''.join(fn.itertext()).split())
        if FX_WORDS.search(txt) and not re.search(r'exchange rate|converted', txt, re.I):
            return txt[:120]
    return ''

def us_close(ticker, _c={}):
    """미국 거래소 종가(달러). Form 4 단가가 달러가 맞는지 대조하는 데만 쓴다."""
    if ticker in _c: return _c[ticker]
    v = None
    try:
        u = f'https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range=5d&interval=1d'
        m = json.loads(urllib.request.urlopen(urllib.request.Request(
            u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=20).read())['chart']['result'][0]['meta']
        if (m.get('currency') or '').upper() == 'USD': v = m.get('regularMarketPrice')
    except Exception:
        pass
    _c[ticker] = v
    return v


def currency_flag(r):
    """달러가 아닌 본국 주식을 달러로 잘못 세는 것을 막는다.

    2026-09-24 사고: BANK BRADESCO 임원 9명의 Form 4에 적힌 단가 17.98을 달러로 읽어
    상위 12건 중 9건이 이 회사로 채워졌다. 서류의 종목은 'Preference shares - BBDC4'로
    상파울루 거래소 우선주였고 17.98은 헤알이었다(뉴욕 ADR BBD 종가는 3.57달러).
    달러로 치면 174만 달러, 헤알로 제대로 읽으면 약 33만 7천 달러다.
    그래서 미국 종가와 3배 넘게 벌어지면 금액을 믿지 않고 표시만 해 둔다.
    """
    if r.get('fxnote'):
        r['usd'] = False; r['flag'] = f"단가 각주가 외화: {r['fxnote']} (금액 신뢰 불가)"
        return r
    px = float(r.get('price') or 0)
    close = us_close(r.get('ticker') or '')
    if not px or not close:
        r['usd'] = None; r['flag'] = '미국 종가 확인 실패 - 통화 확인 필요'
        return r
    ratio = px / close if close else 0
    if ratio > 3 or ratio < 1 / 3:
        r['usd'] = False
        r['flag'] = f'단가 {px}가 미국 종가 {close}달러와 {ratio:.1f}배 차이 - 본국 통화일 수 있음(금액 신뢰 불가)'
    else:
        r['usd'] = True; r['flag'] = ''
    return r


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
    # 금액이 큰 쪽부터 통화를 대조한다. 달러가 확인된 게 top개 찰 때까지만 내려가서
    # 야후 호출을 아끼되, 확인 안 한 건이 조용히 사라지지 않게 한다.
    good, bad = [], []
    for r in out:
        if len(good) >= top: break
        currency_flag(r)
        (good if r.get('usd') is True else bad).append(r)
    for r in good[:top]:
        print(json.dumps(r, ensure_ascii=False))
    # 발굴한 종목을 파일로 남긴다. 안 남기면 B13 글 한 편 쓰고 목록이 사라져
    # B2 종목 분석이 그걸 못 쓴다 — 분석은 미리 적어 둔 20개 고정 목록만 돌고 있었다.
    # 사장님 2026-09-24: "주식도 비슷하게 조사하고 있는 거야?"
    try:
        import datetime as _dt
        pool = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'research', 'dig')
        os.makedirs(pool, exist_ok=True)
        day = _dt.date.today().isoformat()
        rows = [{'ticker': r.get('ticker'), 'issuer': r.get('issuer'), 'amount': r.get('amount'),
                 'date': r.get('date'), 'src': '내부자 매수(Form 4)'} for r in good[:top] if r.get('ticker')]
        json.dump(rows, open(os.path.join(pool, day + '_insider.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
        print(f'# 발굴 종목 {len(rows)}개 저장: research/dig/{day}_insider.json', file=sys.stderr)
    except Exception as e:
        print('# 발굴 종목 저장 실패: ' + repr(e)[:90], file=sys.stderr)
    if bad:
        print(f'# 통화 확인이 안 된 {len(bad)}건은 순위에서 뺐다 - 아래에 따로 적는다', file=sys.stderr)
        for r in bad[:top]:
            print('# 제외 ' + json.dumps({k: r[k] for k in ('issuer', 'ticker', 'owner', 'date', 'price', 'flag')},
                                        ensure_ascii=False), file=sys.stderr)
    print(f'# 매수(P) {len(out)}건 / Form 4 {read}건 조회 ({days}일치, 달러 확인 {len(good)}건 중 상위 {min(top, len(good))}건 출력)',
          file=sys.stderr)

if __name__ == '__main__':
    main(sys.argv[1:])
