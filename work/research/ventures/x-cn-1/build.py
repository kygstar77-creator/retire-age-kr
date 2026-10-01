# X-CN-1 시험 일정 사이트 빌드 (firemap-venture-builder, 2026-10-01)
#  1) 공식 원문을 받아 사실표(facts/*.json)와 한 칸씩 대조한다. 하나라도 다르면 빌드를 멈춘다(틀린 날짜는 안 나간다).
#  2) 대조가 맞으면 그 시각을 도장(verified_at)으로 찍는다 — 사람이 찍지 않는다(예술가 조건 ②).
#     원문을 못 받으면 지난 도장을 그대로 둔다 → 24시간 넘으면 화면이 그 줄만 '공식 일정 확인하기'로 물러난다(조건 ③).
#  3) site/ 에 쪽·캘린더(.ics)·sitemap·robots를 쓴다. '다음 할 일 한 줄'은 src/nextline.cjs 하나로 빌드(node)와 브라우저가 같이 계산.
# 사용: py -3.12 build.py            대조 + 빌드
#       py -3.12 build.py --offline  대조 없이 빌드(도장은 지난 값 그대로, 점검용)
# 매일 06:00 KST 빌드는 kygstar77-creator.github.io 저장소 GitHub Actions(x-cn-1-daily.yml)가 ci.py로 돌린다 — 이 파일이 원본, deploy.py ci 가 복사.
import sys, os, re, json, html, subprocess, datetime, urllib.request, shutil
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, 'site')
STATE = os.path.join(HERE, 'facts', '_verified.json')
BASE = 'https://kygstar77-creator.github.io/exam-dates-kr'   # 저장소 생기면 이 주소(결재함)
ACCENT = '#24508f'
KST = datetime.timezone(datetime.timedelta(hours=9))


def now_kst():
    return datetime.datetime.now(KST).replace(microsecond=0)


# ---------- 1) 원문 대조 ----------
DT = re.compile(r'(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일\s*\([^)]*\)\s*(\d{1,2}:\d{2})?')


def cell_vals(c):
    out = []
    for y, m, d, hm in DT.findall(c):
        s = f'{y}-{int(m):02d}-{int(d):02d}'
        out.append(s + ('T' + hm.zfill(5) if hm else ''))
    return out


def parse_official(raw):
    raw = re.sub(r'(?s)<(script|style)[^>]*>.*?</\1>', ' ', raw)
    tables = re.findall(r'(?s)<table.*?</table>', raw)
    got = {}
    cols = [['apply', 'cancel_seat', 'exam', 'result'], ['change_site', 'photo', 'ticket'], ['refund100', 'refund50']]
    for ti, tb in enumerate(tables[:3]):
        for tr in re.findall(r'(?s)<tr.*?</tr>', tb):
            cells = [html.unescape(re.sub(r'<[^>]+>', ' ', c)) for c in re.findall(r'(?s)<t[dh][^>]*>(.*?)</t[dh]>', tr)]
            if not cells:
                continue
            m = re.search(r'제\s*(\d+)\s*회', cells[0])
            if not m:
                continue
            r = got.setdefault(int(m.group(1)), {'no': int(m.group(1))})
            for k, c in zip(cols[ti], cells[1:]):
                v = cell_vals(c)
                r[k] = v if len(v) == 2 else (v[0] if v else None)
    text = html.unescape(re.sub(r'<[^>]+>', ' ', raw))
    return got, re.sub(r'\s+', ' ', text)


def verify(F):
    req = urllib.request.Request(F['source_url'], headers={'User-Agent': 'Mozilla/5.0'})
    raw = urllib.request.urlopen(req, timeout=20).read().decode('utf-8', 'replace')
    got, text = parse_official(raw)
    diffs = []
    for r in F['rounds']:
        g = got.get(r['no'])
        if not g:
            diffs.append(f"제{r['no']}회: 원문에 없음")
            continue
        for k, v in r.items():
            if k in ('no', 'advanced_only'):
                continue
            if g.get(k) != v:
                diffs.append(f"제{r['no']}회 {k}: 사실표 {v} ≠ 원문 {g.get(k)}")
    extra = sorted(set(got) - {r['no'] for r in F['rounds']})
    if extra:
        diffs.append(f'원문에 새 회차 {extra} — 사실표에 넣어야 함')
    for key in ('심화만 시행', '취소좌석 접수는 접수 잔여석에 한함'):
        if key not in text:
            diffs.append(f'원문 안내 문구 바뀜: "{key}" 없음')
    return diffs


# ---------- 2) 쪽 만들기 ----------
def node_line(F, verified_at, at_ms):
    js = ("const N=require(%s);const F=JSON.parse(require('fs').readFileSync(0,'utf8'));"
          "process.stdout.write(JSON.stringify(N.nextLine(F,%s,%d)))") % (
        json.dumps(os.path.join(HERE, 'src', 'nextline.cjs')), json.dumps(verified_at), at_ms)
    out = subprocess.run(['node', '-e', js], input=json.dumps(F, ensure_ascii=False), capture_output=True, text=True, encoding='utf-8', check=True)
    return json.loads(out.stdout)


def esc(s):
    return html.escape(s or '', quote=True)


# 디자인 반려 16:14 반영: 상태 문장(main·after)이 먼저, 도장은 같은 문단 끝·같은 크기(--dark-sub).
# 하루 넘김(stale)은 줄을 비우고 흰 버튼이 '공식 일정 확인하기'가 된다(.next[data-state=stale] CSS). 글자 변경 0.
def line_inner(L):
    if L['state'] == 'stale':
        return ''
    after = f' · <span class="after">{esc(L["after"])}</span>' if L['after'] else ''
    return f'<strong>{esc(L["main"])}</strong>{after} — <span class="stamp">{esc(L["stamp"])}</span>'


# 편집 표시(.edit.json) 해시에서 빼는 자리: 매일 바뀌는 도장·대조 시각·맨 위 줄 계산값(<!--dyn-->…<!--/dyn-->, /*dyn*/…/*/dyn*/)과
# data-state 값. 그 글자를 만드는 nextline.cjs는 쪽 안에 그대로 실려 해시에 들어간다 → 문장이 바뀌면 여전히 무효.
def dyn(s):
    return f'<!--dyn-->{s}<!--/dyn-->'


DOW = '월화수목금토일'


def d_txt(s, with_time=True):
    d = datetime.datetime.fromisoformat(s)
    t = f'{d.month}/{d.day}({DOW[d.weekday()]})'
    return t + (f' {d:%H:%M}' if with_time and 'T' in s else '')


def mdd(s):
    d = datetime.datetime.fromisoformat(s)
    return f'{d.month}/{d.day}'


def span(v):
    return f'{d_txt(v[0])} ~ {d_txt(v[1])}'


def ics(F, now):
    ev = []
    for r in F['rounds']:
        n = r['no']
        items = [(f'제{n}회 원서접수 시작', r['apply'][0]), (f'제{n}회 원서접수 마감', r['apply'][1]),
                 (f'제{n}회 취소좌석 접수 시작', r['cancel_seat'][0]), (f'제{n}회 취소좌석 접수 마감', r['cancel_seat'][1]),
                 (f'제{n}회 수험표 출력 시작', r['ticket']), (f'제{n}회 시험', r['exam']), (f'제{n}회 합격자발표', r['result'])]
        for name, v in items:
            d = datetime.datetime.fromisoformat(v).replace(tzinfo=KST)
            if d < now - datetime.timedelta(days=1):
                continue
            uid = f'hanneunggeom-{n}-{re.sub(r"[^a-z0-9]", "", name.encode("utf-8").hex())[:24]}@exam-dates-kr'
            if 'T' in v:
                u = d.astimezone(datetime.timezone.utc)
                when = f'DTSTART:{u:%Y%m%dT%H%M%SZ}\r\nDTEND:{(u + datetime.timedelta(minutes=30)):%Y%m%dT%H%M%SZ}'
            else:
                when = f'DTSTART;VALUE=DATE:{d:%Y%m%d}\r\nDTEND;VALUE=DATE:{(d + datetime.timedelta(days=1)):%Y%m%d}'
            ev.append(f'BEGIN:VEVENT\r\nUID:{uid}\r\nDTSTAMP:{now.astimezone(datetime.timezone.utc):%Y%m%dT%H%M%SZ}\r\n{when}\r\n'
                      f'SUMMARY:한능검 {name}\r\nDESCRIPTION:출처 {F["org"]} {F["source_url"]}\r\nEND:VEVENT')
    return 'BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//exam-dates-kr//KO\r\nCALSCALE:GREGORIAN\r\n' + '\r\n'.join(ev) + '\r\nEND:VCALENDAR\r\n'


CSS = open(os.path.join(HERE, 'src', 'style.css'), encoding='utf-8').read()


def page(title, desc, path, body, extra_head='', noindex=False):
    url = BASE + path
    robots = '<meta name="robots" content="noindex">' if noindex else ''
    return f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{robots}<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta name="theme-color" content="#f5f6f8">
{extra_head}<style>{CSS.replace('{{ACCENT}}', ACCENT)}</style>
</head>
<body>
<div class="wrap">
<header><a href="{BASE}/">시험 일정</a></header>
<main>
{body}
</main>
<footer>
<p>이 사이트는 {esc('국사편찬위원회')}가 만든 곳이 아닙니다. 원서접수·변경·환불은 공식 누리집에서 합니다.</p>
<p><a href="{BASE}/privacy/">개인정보처리방침</a></p>
</footer>
</div>
</body>
</html>
'''


def build_hnk(F, verified_at, now):
    L = node_line(F, verified_at, int(now.timestamp() * 1000))
    rows = []
    for r in F['rounds']:
        past = datetime.datetime.fromisoformat(r['result']).replace(tzinfo=KST) < now
        rows.append(f'<tr{" class=past" if past else ""}><th scope="row">제{r["no"]}회</th>'
                    f'<td>{mdd(r["apply"][0])}~{mdd(r["apply"][1])}</td>'
                    f'<td>{d_txt(r["exam"])}</td><td>{d_txt(r["result"])}</td></tr>')
    detail = []
    for r in F['rounds']:
        if datetime.datetime.fromisoformat(r['result']).replace(tzinfo=KST) < now:
            continue
        lv = ' · 심화만 시행' if r.get('advanced_only') else ''
        detail.append(f'''<section class="card" id="r{r["no"]}">
<h3>제{r["no"]}회{lv}</h3>
<dl>
<dt>원서접수</dt><dd>{span(r["apply"])}</dd>
<dt>취소좌석 접수</dt><dd>{span(r["cancel_seat"])}</dd>
<dt>권역 및 시험장 변경</dt><dd>{span(r["change_site"])}</dd>
<dt>사진 수정</dt><dd>{span(r["photo"])}</dd>
<dt>수험표 출력</dt><dd>{d_txt(r["ticket"])}부터</dd>
<dt>시험일</dt><dd>{d_txt(r["exam"])}</dd>
<dt>합격자발표</dt><dd>{d_txt(r["result"])}</dd>
<dt>접수 취소 100% 환불</dt><dd>{span(r["refund100"])}</dd>
<dt>접수 취소 50% 환불</dt><dd>{span(r["refund50"])}</dd>
</dl>
</section>''')
    notes = ''.join(f'<li>{esc(n)}</li>' for n in F['notes_official'])
    read = datetime.datetime.fromisoformat(F['read_at'])
    ver = datetime.datetime.fromisoformat(verified_at) if verified_at else None
    vjs = json.dumps(verified_at)
    data = json.dumps({'F': F}, ensure_ascii=False).replace('</', '<\\/')
    nl = open(os.path.join(HERE, 'src', 'nextline.cjs'), encoding='utf-8').read()
    body = f'''<h1>한능검 시험일정 2026 — 제80·81회 남은 일정</h1>
<div class="next" id="next" data-state="{L["state"]}">
<p class="line" id="line">{dyn(line_inner(L))}</p>
<p class="sub" id="sub">{dyn(esc(L.get("sub", "")))}</p>
<div class="acts">
<a class="btn primary" id="ics" href="hanneunggeom-2026.ics" download>캘린더에 넣기</a>
<a class="btn primary official" id="offbtn" href="{esc(F["source_url"])}" rel="nofollow">공식 일정 확인하기</a>
<button class="btn ghost" id="copy" type="button">링크 복사</button>
</div>
</div>
<p class="src">출처: <a id="official" href="{esc(F["source_url"])}" rel="nofollow">{esc(F["org"])} 한국사능력검정시험 누리집 · 시험 일정</a></p>

<h2>2026년 회차별 일정</h2>
<div class="tbl"><table>
<thead><tr><th scope="col">회차</th><th scope="col">원서접수</th><th scope="col">시험일</th><th scope="col">합격자발표</th></tr></thead>
<tbody>{"".join(rows)}</tbody>
</table></div>

<h2>남은 회차 자세히</h2>
{"".join(detail)}

<h2>공식 안내</h2>
<ul class="notes">{notes}</ul>

<p class="src">원문을 사람이 읽은 시각 {read.month}/{read.day} {read:%H:%M} · 원문과 자동 대조한 시각 {dyn(f"{ver.month}/{ver.day} {ver:%H:%M}" if ver else "없음")}. 대조가 하루를 넘기면 맨 위 줄은 공식 일정 링크로 바뀝니다.</p>
<script>{nl}</script>
<script src="../fmkit.js"></script>
<script>
(function () {{
  var D = {data};
  D.V = /*dyn*/{vjs}/*/dyn*/;
  var L = NextLine.nextLine(D.F, D.V, Date.now());
  var box = document.getElementById('next'), p = document.getElementById('line');
  function e(s) {{ return String(s).replace(/[&<>"]/g, function (c) {{ return {{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]; }}); }}
  box.setAttribute('data-state', L.state);
  p.innerHTML = L.state === 'stale' ? ''
    : '<strong>' + e(L.main) + '</strong>' + (L.after ? ' · <span class="after">' + e(L.after) + '</span>' : '') + ' — <span class="stamp">' + e(L.stamp) + '</span>';
  document.getElementById('sub').textContent = L.sub || '';
  var log = window.FMKit ? FMKit.log : function () {{}};
  if (window.FMKit) FMKit.init({{ site: 'x-cn-1', lang: 'ko', accent: '{ACCENT}' }});
  log('line_view', {{ state: L.state, page: 'hanneunggeom' }});
  document.getElementById('ics').addEventListener('click', function () {{ log('ics_click', {{ state: L.state }}); }});
  document.getElementById('official').addEventListener('click', function () {{ log('official_click', {{ state: L.state }}); }});
  document.addEventListener('click', function (ev) {{ if (ev.target.closest && ev.target.closest('a.official')) log('official_click', {{ state: 'stale' }}); }});
  document.getElementById('copy').addEventListener('click', function () {{
    var u = location.origin + location.pathname + '?utm_source=share&utm_medium=x-cn-1', b = this;
    (navigator.clipboard ? navigator.clipboard.writeText(u) : Promise.reject()).then(function () {{
      b.textContent = '복사됨'; log('link_copy', {{ ok: 1 }});
    }}, function () {{ window.prompt('링크', u); log('link_copy', {{ ok: 0 }}); }});
  }});
}})();
</script>'''
    title = '한능검 시험일정 2026 — 제80회 취소좌석 접수·제81회 원서접수'
    desc = '한국사능력검정시험 2026년 제77~81회 원서접수·취소좌석 접수·시험일·합격자발표. 지금 할 일과 마감 시각을 맨 위에 두고, 국사편찬위원회 원문과 대조한 시각을 함께 적습니다.'
    return page(title, desc, '/hanneunggeom/', body), L


def main():
    offline = '--offline' in sys.argv
    F = json.load(open(os.path.join(HERE, 'facts', 'hanneunggeom.json'), encoding='utf-8'))
    st = json.load(open(STATE, encoding='utf-8')) if os.path.exists(STATE) else {}
    now = now_kst()
    if not offline:
        try:
            diffs = verify(F)
        except Exception as ex:  # 원문을 못 받으면 도장은 그대로(하루 넘으면 화면이 물러남)
            diffs = None
            print('원문 받기 실패 — 도장 그대로:', ex)
            if os.environ.get('XCN1_CI'):  # 매일 빌드(GitHub Actions)는 여기서 실패로 끝내 이메일을 받는다
                sys.exit(3)
        if diffs:
            print('대조 불일치 — 빌드 중지:')
            for d in diffs:
                print('  ', d)
            sys.exit(2)
        if diffs == []:
            st['hanneunggeom'] = now.isoformat()
            json.dump(st, open(STATE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            print('대조 일치 →', st['hanneunggeom'])
    v = st.get('hanneunggeom')
    os.makedirs(os.path.join(SITE, 'hanneunggeom'), exist_ok=True)
    os.makedirs(os.path.join(SITE, 'privacy'), exist_ok=True)
    doc, L = build_hnk(F, v, now)
    open(os.path.join(SITE, 'hanneunggeom', 'index.html'), 'w', encoding='utf-8', newline='\n').write(doc)
    open(os.path.join(SITE, 'hanneunggeom', 'hanneunggeom-2026.ics'), 'w', encoding='utf-8', newline='').write(ics(F, now))
    root = page('시험 일정', '공식 원문과 대조한 시험 일정 모음.', '/',
                '<h1>시험 일정</h1>\n<ul class="list"><li><a href="hanneunggeom/">한능검 시험일정 2026</a></li></ul>', noindex=True)
    open(os.path.join(SITE, 'index.html'), 'w', encoding='utf-8', newline='\n').write(root)
    shutil.copy(os.path.join(HERE, 'src', 'privacy.html'), os.path.join(SITE, 'privacy', 'index.html'))
    shutil.copy(os.environ.get('FMKIT') or os.path.join(HERE, '..', 'uk-pay', 'site', 'fmkit.js'), os.path.join(SITE, 'fmkit.js'))
    open(os.path.join(SITE, 'robots.txt'), 'w', newline='\n').write(f'User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n')
    open(os.path.join(SITE, 'sitemap.xml'), 'w', newline='\n').write(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f'<url><loc>{BASE}/hanneunggeom/</loc><lastmod>{now:%Y-%m-%d}</lastmod></url>\n</urlset>\n')
    print('빌드 완료', now.isoformat(), '| 맨 위 줄:', L.get('stamp'), '—', L['main'], '·', L.get('after'))


if __name__ == '__main__':
    main()
