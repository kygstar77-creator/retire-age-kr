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
def node_line(F, verified_at, at_ms, mod='nextline.cjs'):
    js = ("const N=require(%s);const F=JSON.parse(require('fs').readFileSync(0,'utf8'));"
          "process.stdout.write(JSON.stringify(N.nextLine(F,%s,%d)))") % (
        json.dumps(os.path.join(HERE, 'src', mod)), json.dumps(verified_at), at_ms)
    out = subprocess.run(['node', '-e', js], input=json.dumps(F, ensure_ascii=False), capture_output=True, text=True, encoding='utf-8', check=True)
    return json.loads(out.stdout)


def esc(s):
    return html.escape(s or '', quote=True)


# 디자인 반려 16:14 반영: 상태 문장(main·after)이 먼저, 도장은 같은 문단 끝·같은 크기(--dark-sub).
# 하루 넘김(stale)은 줄을 비우고 흰 버튼이 '공식 일정 확인하기'가 된다(.next[data-state=stale] CSS). 글자 변경 0.
def line_inner(L):
    if L['state'] == 'stale':
        return ''
    # 채점 10/2 고칠 점 ①②: 도장은 맨 위 작게, 큰 글자 1줄(main) + 설명 1줄(after)
    k = f'<span class="kick">{esc(L["k"])}</span>' if L.get('k') else ''
    d = f'<span class="after">{esc(L["d"])}</span>' if L.get('d') else ''
    return f'<span class="stamp">{esc(L["stamp"])}</span>{k}<strong>{esc(L["b"])}</strong>{d}'


# 편집 표시(.edit.json) 해시에서 빼는 자리: 매일 바뀌는 도장·대조 시각·맨 위 줄 계산값(<!--dyn-->…<!--/dyn-->, /*dyn*/…/*/dyn*/)과
# data-state 값. 그 글자를 만드는 nextline.cjs는 쪽 안에 그대로 실려 해시에 들어간다 → 문장이 바뀌면 여전히 무효.
def dyn(s):
    return f'<!--dyn-->{s}<!--/dyn-->'


DOW = '월화수목금토일'


# 채점 10/2 v3 ③: '접수했다면' 상자는 · 이어 붙인 줄 → 항목별 한 줄 목록
def sub_html(L):
    if not L.get('subh'):
        return ''
    return f'<p class="subh">{esc(L["subh"])}</p><ul>' + ''.join(f'<li>{esc(x)}</li>' for x in L.get('subs', [])) + '</ul>'


def d_txt(s, with_time=True):
    d = datetime.datetime.fromisoformat(s)
    t = f'{d.month}/{d.day}({DOW[d.weekday()]})'
    return t + (f' {d:%H:%M}' if with_time and 'T' in s else '')


def mdd(s):
    d = datetime.datetime.fromisoformat(s)
    return f'{d.month}/{d.day}'


def span(v):
    return f'{d_txt(v[0])} ~ {d_txt(v[1])}'


def alarm(name):
    # 마감 일정에만 하루 전 알림(VALARM). 알림 글은 일정 이름 그대로 — 새 문구 0 (toeic/review.md ③, 공식 알림톡 따라잡기)
    return f'BEGIN:VALARM\r\nTRIGGER:-P1D\r\nACTION:DISPLAY\r\nDESCRIPTION:{name}\r\nEND:VALARM\r\n' if name.endswith('마감') else ''


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
                      f'SUMMARY:한능검 {name}\r\nDESCRIPTION:출처 {F["org"]} {F["source_url"]}\r\n{alarm("한능검 " + name)}END:VEVENT')
    return 'BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//exam-dates-kr//KO\r\nCALSCALE:GREGORIAN\r\n' + '\r\n'.join(ev) + '\r\nEND:VCALENDAR\r\n'


CSS = open(os.path.join(HERE, 'src', 'style.css'), encoding='utf-8').read()


def page(title, desc, path, body, extra_head='', noindex=False, org='국사편찬위원회', foot='원서접수·변경·환불은 공식 누리집에서 합니다.'):
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
<p>이 사이트는 {esc(org)}{'이' if org.endswith('M') else '가'} 만든 곳이 아닙니다. {esc(foot)}</p>
<p><a href="{BASE}/privacy/">개인정보처리방침</a></p>
</footer>
</div>
</body>
</html>
'''


def build_hnk(F, verified_at, now):
    L = node_line(F, verified_at, int(now.timestamp() * 1000))
    rows, past_rows = [], []   # 채점 10/2 고칠 점 ③: 남은 회차 위, 지난 회차는 접기 — 날짜 따라 행이 옮겨 가므로 dyn 자리(매일 빌드가 편집 해시를 깨지 않게)
    for r in F['rounds']:
        past = datetime.datetime.fromisoformat(r['result']).replace(tzinfo=KST) < now
        (past_rows if past else rows).append(f'<tr{" class=past" if past else ""}><th scope="row">제{r["no"]}회</th>'
                    f'<td>{d_txt(r["apply"][0], False)}~<br>{d_txt(r["apply"][1], False)}</td>'
                    f'<td>{d_txt(r["exam"])}</td><td>{d_txt(r["result"])}</td></tr>')
    thead = '<thead><tr><th scope="col">회차</th><th scope="col">원서접수</th><th scope="col">시험일</th><th scope="col">합격자발표</th></tr></thead>'
    past_no = [r['no'] for r in F['rounds'] if datetime.datetime.fromisoformat(r['result']).replace(tzinfo=KST) < now]
    past_box = (f'<details class="past"><summary>지난 회차(제{past_no[0]}~{past_no[-1]}회)</summary>'
                f'<div class="tbl"><table>{thead}<tbody>{"".join(past_rows)}</tbody></table></div></details>') if past_no else ''
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
    # beat-1st 10/2: 지역별 접수 시각(공식 제80회 안내) — 표의 '10:00'이 모든 지역 시작이 아닐 수 있다. 확인 시각을 같이 적는다.
    rn = F.get('region_note')
    region = ''
    if rn:
        ck = datetime.datetime.fromisoformat(rn['checked_at'])
        region = (f'<p class="note">{esc(rn["text"])} '
                  f'<span class="nowrap">출처: <a href="{esc(rn["source_url"])}" rel="nofollow">공식 제80회 안내</a> · 공지사항 {ck.month}/{ck.day} {ck:%H:%M} 확인</span></p>')
    notes = ''.join(f'<li>{esc(n)}</li>' for n in F['notes_official'])
    read = datetime.datetime.fromisoformat(F['read_at'])
    ver = datetime.datetime.fromisoformat(verified_at) if verified_at else None
    vjs = json.dumps(verified_at)
    data = json.dumps({'F': F}, ensure_ascii=False).replace('</', '<\\/')
    nl = open(os.path.join(HERE, 'src', 'nextline.cjs'), encoding='utf-8').read()
    body = f'''<h1>한능검 시험일정 2026 — 제80·81회 남은 일정</h1>
<div class="next" id="next" data-state="{L["state"]}">
<p class="line" id="line">{dyn(line_inner(L))}</p>
<div class="acts">
<a class="btn primary" id="ics" href="hanneunggeom-2026.ics" download>캘린더에 넣기</a>
<a class="btn primary official" id="offbtn" href="{esc(F["source_url"])}" rel="nofollow">공식 일정 확인하기</a>
<button class="linkbtn" id="copy" type="button">링크 복사</button>
</div>
</div>
<div class="sub" id="sub">{dyn(sub_html(L))}</div>

<h2>2026년 회차별 일정</h2>
<div class="tbl"><table>
{thead}
<tbody>{dyn("".join(rows))}</tbody>
</table></div>
{dyn(past_box)}

<h2>남은 회차 자세히</h2>
{"".join(detail)}
{region}

<h2>공식 안내</h2>
<ul class="notes">{notes}</ul>

<p class="src">출처: <a id="official" href="{esc(F["source_url"])}" rel="nofollow">{esc(F["org"])} 한국사능력검정시험 누리집 · 시험 일정</a> · 원문을 사람이 읽은 시각 {read.month}/{read.day} {read:%H:%M} · 원문과 자동 대조한 시각 {dyn(f"{ver.month}/{ver.day} {ver:%H:%M}" if ver else "없음")}. 대조가 하루를 넘기면 맨 위 줄은 공식 일정 링크로 바뀝니다.</p>
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
    : '<span class="stamp">' + e(L.stamp) + '</span>' + (L.k ? '<span class="kick">' + e(L.k) + '</span>' : '') + '<strong>' + e(L.b) + '</strong>' + (L.d ? '<span class="after">' + e(L.d) + '</span>' : '');
  document.getElementById('sub').innerHTML = L.subh ? '<p class="subh">' + e(L.subh) + '</p><ul>' + L.subs.map(function (x) {{ return '<li>' + e(x) + '</li>'; }}).join('') + '</ul>' : '';
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


# ---------- 토익(X-CN-1 2편, 2026-10-05) ----------
# 원문 m.exam.toeic.co.kr 시험일정 텍스트: '2026.10.11 (일) 09:20 정기접수 : 26.08.24 (월) 10:00~26.09.28 (월) 10:00
#  특별추가 : 26.09.30 (수) 10:00~26.10.07 (수) 13:00 성적발표 : 2026.10.20 (화) 12:00'
_D = r'(\d{2,4})\.(\d\d)\.(\d\d)\s*\([^)]*\)\s*(\d\d:\d\d)'
T_ROW = re.compile(_D + r'\s*정기접수\s*:\s*' + _D + r'\s*~\s*' + _D + r'\s*특별추가\s*:\s*' + _D + r'\s*~\s*' + _D
                   + r'\s*성적발표\s*:\s*' + _D)


def parse_toeic(raw):
    raw = re.sub(r'(?s)<(script|style)[^>]*>.*?</\1>', ' ', raw)
    text = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', raw)))
    got = {}
    for g in T_ROW.findall(text):
        f = lambda y, m, d, h: f'{y if len(y) == 4 else "20" + y}-{m}-{d}T{h}'
        exam = f(*g[0:4])
        got[exam] = {'exam': exam, 'apply': [f(*g[4:8]), f(*g[8:12])], 'extra': [f(*g[12:16]), f(*g[16:20])], 'result': f(*g[20:24])}
    return got, text


def verify_toeic(F):
    req = urllib.request.Request(F['source_url'], headers={'User-Agent': 'Mozilla/5.0 (Linux; Android 13) Mobile'})
    raw = urllib.request.urlopen(req, timeout=20).read().decode('utf-8', 'replace')
    got, text = parse_toeic(raw)
    diffs = []
    if not got:
        return ['원문에서 회차를 하나도 못 읽음 — 쪽 구조 바뀜']
    for r in F['rounds']:
        g = got.get(r['exam'])
        if not g:
            # 지난 회차는 원문에서 빠질 수 있다 — 성적발표가 지난 회차만 봐준다
            if datetime.datetime.fromisoformat(r['result']).replace(tzinfo=KST) > now_kst():
                diffs.append(f"{r['exam']} 시험: 원문에 없음")
            continue
        for k in ('apply', 'extra', 'result'):
            if g[k] != r[k]:
                diffs.append(f"{r['exam']} {k}: 사실표 {r[k]} ≠ 원문 {g[k]}")
    extra = sorted(set(got) - {r['exam'] for r in F['rounds']})
    if extra:
        diffs.append(f'원문에 새 회차 {extra} — 사실표에 넣어야 함')
    for key in F['notes_official']:
        if key not in text:
            diffs.append(f'원문 안내 문구 바뀜: "{key}" 없음')
    return diffs


def ics_toeic(F, now):
    ev = []
    for r in F['rounds']:
        x = d_txt(r['exam'], False)
        items = [(f'{x} 시험 정기접수 마감', r['apply'][1]), (f'{x} 시험 특별추가 시작', r['extra'][0]),
                 (f'{x} 시험 특별추가 마감', r['extra'][1]), (f'{x} 시험', r['exam']), (f'{x} 시험 성적발표', r['result'])]
        for i, (name, v) in enumerate(items):
            d = datetime.datetime.fromisoformat(v).replace(tzinfo=KST)
            if d < now - datetime.timedelta(days=1):
                continue
            u = d.astimezone(datetime.timezone.utc)
            ev.append(f'BEGIN:VEVENT\r\nUID:toeic-{r["exam"][:10]}-{i}@exam-dates-kr\r\nDTSTAMP:{now.astimezone(datetime.timezone.utc):%Y%m%dT%H%M%SZ}\r\n'
                      f'DTSTART:{u:%Y%m%dT%H%M%SZ}\r\nDTEND:{(u + datetime.timedelta(minutes=30)):%Y%m%dT%H%M%SZ}\r\n'
                      f'SUMMARY:토익 {name}\r\nDESCRIPTION:출처 {F["org"]} {F["source_url"]}\r\n{alarm("토익 " + name)}END:VEVENT')
    return 'BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//exam-dates-kr//KO\r\nCALSCALE:GREGORIAN\r\n' + '\r\n'.join(ev) + '\r\nEND:VCALENDAR\r\n'


# 375px에서 표가 옆으로 밀리지 않게 표 칸은 날짜·시각 두 줄(한능검 표의 '~<br>'과 같은 방식)
def d2(v):
    return d_txt(v, False) + '<br>' + v[11:16]


def build_toeic(F, verified_at, now):
    L = node_line(F, verified_at, int(now.timestamp() * 1000), 'toeic.cjs')
    past = lambda r: datetime.datetime.fromisoformat(r['result']).replace(tzinfo=KST) < now
    row = lambda r: (f'<tr{" class=past" if past(r) else ""}><th scope="row">{d_txt(r["exam"], False)}</th>'
                     f'<td>{d2(r["apply"][1])}</td><td>{d2(r["extra"][1])}</td><td>{d2(r["result"])}</td></tr>')
    rows = [row(r) for r in F['rounds'] if not past(r)]
    past_rows = [row(r) for r in F['rounds'] if past(r)]
    thead = '<thead><tr><th scope="col">시험일</th><th scope="col">정기접수<br>마감</th><th scope="col">특별추가<br>마감</th><th scope="col">성적발표</th></tr></thead>'
    past_box = (f'<details class="past"><summary>지난 회차({len(past_rows)}개)</summary>'
                f'<div class="tbl"><table>{thead}<tbody>{"".join(past_rows)}</tbody></table></div></details>') if past_rows else ''
    detail = []
    for r in F['rounds']:
        if past(r):
            continue
        detail.append(f'''<section class="card">
<h3>{d_txt(r["exam"], False)} 시험</h3>
<dl>
<dt>정기접수</dt><dd>{span(r["apply"])}</dd>
<dt>특별추가</dt><dd>{span(r["extra"])}</dd>
<dt>시험일</dt><dd>{d_txt(r["exam"])}</dd>
<dt>성적발표</dt><dd>{d_txt(r["result"])}</dd>
</dl>
</section>''')
    notes = ''.join(f'<li>{esc(n)}</li>' for n in F['notes_official'])
    read = datetime.datetime.fromisoformat(F['read_at'])
    ver = datetime.datetime.fromisoformat(verified_at) if verified_at else None
    data = json.dumps({'F': F}, ensure_ascii=False).replace('</', '<\\/')
    nl = open(os.path.join(HERE, 'src', 'toeic.cjs'), encoding='utf-8').read()
    body = f'''<h1>토익 시험일정 2026 — 남은 접수 마감·성적발표</h1>
<div class="next" id="next" data-state="{L["state"]}">
<p class="line" id="line">{dyn(line_inner(L))}</p>
<div class="acts">
<a class="btn primary" id="ics" href="toeic-2026.ics" download>캘린더에 넣기</a>
<a class="btn primary official" id="offbtn" href="{esc(F["source_url"])}" rel="nofollow">공식 일정 확인하기</a>
<button class="linkbtn" id="copy" type="button">링크 복사</button>
</div>
</div>
<div class="sub" id="sub">{dyn(sub_html(L))}</div>

<h2>2026년 시험별 일정</h2>
<div class="tbl"><table>
{thead}
<tbody>{dyn("".join(rows))}</tbody>
</table></div>
{dyn(past_box)}

<h2>남은 시험 자세히</h2>
{dyn("".join(detail))}

<h2>공식 안내</h2>
<ul class="notes">{notes}</ul>

<p class="src">출처: <a id="official" href="{esc(F["source_url"])}" rel="nofollow">{esc(F["org"])} TOEIC 공식 사이트 · 시험일정</a> · 원문을 사람이 읽은 시각 {read.month}/{read.day} {read:%H:%M} · 원문과 자동 대조한 시각 {dyn(f"{ver.month}/{ver.day} {ver:%H:%M}" if ver else "없음")}. 대조가 하루를 넘기면 맨 위 줄은 공식 일정 링크로 바뀝니다.</p>
<script>{nl}</script>
<script src="../fmkit.js"></script>
<script>
(function () {{
  var D = {data};
  D.V = /*dyn*/{json.dumps(verified_at)}/*/dyn*/;
  var L = NextLine.nextLine(D.F, D.V, Date.now());
  var box = document.getElementById('next'), p = document.getElementById('line');
  function e(s) {{ return String(s).replace(/[&<>"]/g, function (c) {{ return {{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]; }}); }}
  box.setAttribute('data-state', L.state);
  p.innerHTML = L.state === 'stale' ? ''
    : '<span class="stamp">' + e(L.stamp) + '</span>' + (L.k ? '<span class="kick">' + e(L.k) + '</span>' : '') + '<strong>' + e(L.b) + '</strong>' + (L.d ? '<span class="after">' + e(L.d) + '</span>' : '');
  document.getElementById('sub').innerHTML = L.subh ? '<p class="subh">' + e(L.subh) + '</p><ul>' + L.subs.map(function (x) {{ return '<li>' + e(x) + '</li>'; }}).join('') + '</ul>' : '';
  var log = window.FMKit ? FMKit.log : function () {{}};
  if (window.FMKit) FMKit.init({{ site: 'x-cn-1', lang: 'ko', accent: '{ACCENT}' }});
  log('line_view', {{ state: L.state, page: 'toeic' }});
  document.getElementById('ics').addEventListener('click', function () {{ log('ics_click', {{ state: L.state, page: 'toeic' }}); }});
  document.getElementById('official').addEventListener('click', function () {{ log('official_click', {{ state: L.state, page: 'toeic' }}); }});
  document.addEventListener('click', function (ev) {{ if (ev.target.closest && ev.target.closest('a.official')) log('official_click', {{ state: 'stale', page: 'toeic' }}); }});
  document.getElementById('copy').addEventListener('click', function () {{
    var u = location.origin + location.pathname + '?utm_source=share&utm_medium=x-cn-1', b = this;
    (navigator.clipboard ? navigator.clipboard.writeText(u) : Promise.reject()).then(function () {{
      b.textContent = '복사됨'; log('link_copy', {{ ok: 1, page: 'toeic' }});
    }}, function () {{ window.prompt('링크', u); log('link_copy', {{ ok: 0, page: 'toeic' }}); }});
  }});
}})();
</script>'''
    title = '토익 시험일정 2026 — 정기접수·특별추가 마감, 성적발표'
    desc = 'TOEIC 정기시험 2026년 10~12월 회차별 정기접수·특별추가 마감과 성적발표. 지금 가장 먼저 닫히는 접수를 맨 위에 두고, YBM 원문과 대조한 시각을 함께 적습니다.'
    return page(title, desc, '/toeic/', body, org=F['org'], foot='접수·변경·취소는 공식 사이트에서 합니다.'), L


def main():
    offline = '--offline' in sys.argv
    EX = [('hanneunggeom', verify), ('toeic', verify_toeic)]
    FS = {k: json.load(open(os.path.join(HERE, 'facts', k + '.json'), encoding='utf-8')) for k, _ in EX}
    st = json.load(open(STATE, encoding='utf-8')) if os.path.exists(STATE) else {}
    now = now_kst()
    if not offline:
        for key, fn in EX:
            try:
                diffs = fn(FS[key])
            except Exception as ex:  # 원문을 못 받으면 도장은 그대로(하루 넘으면 화면이 물러남)
                diffs = None
                print(key, '원문 받기 실패 — 도장 그대로:', ex)
                if os.environ.get('XCN1_CI'):  # 매일 빌드(GitHub Actions)는 여기서 실패로 끝내 이메일을 받는다
                    sys.exit(3)
            if diffs:
                print(key, '대조 불일치 — 빌드 중지:')
                for d in diffs:
                    print('  ', d)
                sys.exit(2)
            if diffs == []:
                st[key] = now.isoformat()
                print(key, '대조 일치 →', st[key])
        json.dump(st, open(STATE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for d in ('hanneunggeom', 'toeic', 'privacy'):
        os.makedirs(os.path.join(SITE, d), exist_ok=True)
    doc, L = build_hnk(FS['hanneunggeom'], st.get('hanneunggeom'), now)
    open(os.path.join(SITE, 'hanneunggeom', 'index.html'), 'w', encoding='utf-8', newline='\n').write(doc)
    open(os.path.join(SITE, 'hanneunggeom', 'hanneunggeom-2026.ics'), 'w', encoding='utf-8', newline='').write(ics(FS['hanneunggeom'], now))
    doc, LT = build_toeic(FS['toeic'], st.get('toeic'), now)
    open(os.path.join(SITE, 'toeic', 'index.html'), 'w', encoding='utf-8', newline='\n').write(doc)
    open(os.path.join(SITE, 'toeic', 'toeic-2026.ics'), 'w', encoding='utf-8', newline='').write(ics_toeic(FS['toeic'], now))
    root = page('시험 일정', '공식 원문과 대조한 시험 일정 모음.', '/',
                '<h1>시험 일정</h1>\n<ul class="list"><li><a href="hanneunggeom/">한능검 시험일정 2026</a></li>'
                '<li><a href="toeic/">토익 시험일정 2026</a></li></ul>', noindex=True, org='국사편찬위원회·YBM', foot='접수는 각 공식 누리집에서 합니다.')
    open(os.path.join(SITE, 'index.html'), 'w', encoding='utf-8', newline='\n').write(root)
    shutil.copy(os.path.join(HERE, 'src', 'privacy.html'), os.path.join(SITE, 'privacy', 'index.html'))
    shutil.copy(os.environ.get('FMKIT') or os.path.join(HERE, '..', 'uk-pay', 'site', 'fmkit.js'), os.path.join(SITE, 'fmkit.js'))
    open(os.path.join(SITE, 'robots.txt'), 'w', newline='\n').write(f'User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n')
    open(os.path.join(SITE, 'sitemap.xml'), 'w', newline='\n').write(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f'<url><loc>{BASE}/hanneunggeom/</loc><lastmod>{now:%Y-%m-%d}</lastmod></url>\n'
        f'<url><loc>{BASE}/toeic/</loc><lastmod>{now:%Y-%m-%d}</lastmod></url>\n</urlset>\n')
    print('빌드 완료', now.isoformat(), '| 한능검:', L.get('stamp'), '—', L['main'], '| 토익:', LT['main'], '·', LT.get('after'))

if __name__ == '__main__':
    main()
