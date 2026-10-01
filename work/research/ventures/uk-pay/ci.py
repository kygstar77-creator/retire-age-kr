# X-V1 uk-pay 매일 원문 대조 — kygstar77-creator.github.io 저장소 GitHub Actions(.github/workflows/uk-pay-daily.yml)에서 돈다.
# (backlog 3번, firemap-venture-builder 2026-10-01) 원본은 retire-age-kr ventures/uk-pay, `deploy.py ci`가 복사한다.
# 읽기만 한다 — 화면을 고치지 않고 푸시도 없다. 실패 = 저장소 주인에게 Actions 실패 이메일 → 사람이 checks.md 다시.
#  1) 공개본 /uk-take-home-pay/ 두 쪽 스크립트의 상수(PA·BASIC·UEL·학자금…)가 FACTS와 같아야 한다. 다르면 exit 2.
#  2) GOV.UK Content API 두 쪽 본문에 FACTS 근거 문장이 그대로 있어야 한다. 하나라도 없으면 exit 2(세율·과세연도 바뀜).
#  3) 원문을 못 받으면 exit 3.
#  4) 원문 갱신일(public_updated_at)이 checks.md에 적은 날보다 새로우면 알림만(문장이 그대로면 통과).
# 로컬: py -3.12 ci.py --local   (공개본 대신 site/ 를 읽는다)
import os, sys, re, json, html, time, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
LOCAL = '--local' in sys.argv
SITE = os.path.join(HERE, 'site') if LOCAL else os.path.abspath(os.path.join(HERE, '..', '..', '..', 'uk-take-home-pay'))

# 화면 식의 상수 — checks.md 1장(2026/27 rUK)
FACTS = {'PA': 12570, 'TAPER': 100000, 'BASIC': 37700, 'ADD': 125140, 'PT': 12570, 'UEL': 50270}
LOANS = {"'1'": 26900, "'2'": 29385, "'4'": 33795, "'5'": 25000, 'PGL': 21000}
PAGES = {'index.html': FACTS, '60-percent-tax-trap/index.html': FACTS}

# GOV.UK 원문 근거 문장(공백은 정규화해 비교). 2027/28이 되면 첫 줄부터 깨진다 → 사람이 새 연도로.
SRC = {
    'income-tax-rates': ('2024-11-07', [
        'The current tax year is from 6 April 2026 to 5 April 2027',
        'The standard Personal Allowance is £12,570',
        'Personal Allowance Up to £12,570 0%',
        'Basic rate £12,571 to £50,270 20%',
        'Higher rate £50,271 to £125,140 40%',
        'Additional rate over £125,140 45%',
        'allowance is zero if your income is £125,140 or above',
    ]),
    'guidance/rates-and-thresholds-for-employers-2026-to-2027': ('2026-09-01', [
        'apply from 6 April 2026 to 5 April 2027',
        '£12,570 per year PAYE tax rate',
        'Basic tax rate 20% Up to £37,700',
        'Higher tax rate 40% From £37,701 to £125,140',
        'Additional tax rate 45% Above £125,140',
        'Primary threshold £242 per week £1,048 per month £12,570 per year',
        'Upper earnings limit £967 per week £4,189 per month £50,270 per year',
        'A 0% 8% 2%',
        'student loan plan 1 £26,900 per year',
        'student loan plan 2 £29,385 per year',
        'student loan plan 4 £33,795 per year',
        'plan 5 £25,000 per year',
        'Student loan deductions 9%',
        'postgraduate loan £21,000 per year',
        'Postgraduate loan deductions 6%',
    ]),
}


def norm(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()


def fetch(path):
    url = 'https://www.gov.uk/api/content/' + path
    for i in range(3):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'uk-take-home-pay daily check (github actions)'})
            d = json.load(urllib.request.urlopen(req, timeout=30))
            det = d.get('details', {})
            body = det.get('body', '') or ' '.join(p.get('body', '') for p in det.get('parts', []))
            return d.get('public_updated_at', ''), norm(body)
        except Exception as e:  # noqa: BLE001
            err = e
            time.sleep(5 * (i + 1))
    print(f'원문 못 받음: {url} — {err}')
    sys.exit(3)


def consts(p):
    t = open(p, encoding='utf-8').read()
    got = {k: int(v) for k, v in re.findall(r'\b(PA|TAPER|BASIC|ADD|PT|UEL|PGL)\s*=\s*(\d+)', t)}
    m = re.search(r'SL\s*=\s*\{([^}]*)\}', t)
    if m:
        got.update({k: int(v) for k, v in re.findall(r"('\d')\s*:\s*(\d+)", m.group(1))})
    return got


def main():
    bad = []
    for rel, want in PAGES.items():
        p = os.path.join(SITE, rel)
        got = consts(p)
        want = dict(want, **(LOANS if rel == 'index.html' else {}))
        for k, v in want.items():
            if got.get(k) != v:
                bad.append(f'화면 상수 {rel} {k}: 기대 {v} ≠ 지금 {got.get(k)}')
    for path, (seen, phrases) in SRC.items():
        upd, text = fetch(path)
        for ph in phrases:
            if norm(ph) not in text:
                bad.append(f'원문 문장 없음 [{path}] "{ph}"')
        if upd[:10] > seen:
            print(f'알림: {path} 갱신일 {upd[:10]} (checks.md 기록 {seen}) — 문장 대조는 아래 결과')
    if bad:
        print('\n'.join(bad))
        sys.exit(2)
    print(f'통과 — 화면 상수 {len(PAGES)}쪽 · 원문 문장 {sum(len(v[1]) for v in SRC.values())}개 ({time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())})')


if __name__ == '__main__':
    main()
