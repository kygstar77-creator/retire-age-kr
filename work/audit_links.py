# 링크 관문 — 카페 글(pkg)·영상 설명(meta.json desc)·쇼츠 설명에 든 링크를 work/research/growth/utm.md 규칙으로 검사한다.
#   python3 work/audit_links.py <pkg 폴더 | meta.json | 글 .txt> [...]     → 걸리면 종료 코드 1
#   python3 work/audit_links.py --live ...                                  → 주소를 실제로 열어 본다(HEAD→GET, 네트워크가 막히면 '확인 안 함')
# 검사(근거 = growth/utm.md 2026-09-30 '형식'·'utm_source'·'utm_medium'·'utm_campaign'):
#   - firemap.kr 링크: utm_source·utm_medium·utm_campaign 셋 다 있어야 한다(없으면 GA4·session_start 집계가 쪼개짐).
#   - utm 값: 영문 소문자·숫자·'-'·'_'만. source/medium은 utm.md 표에 있는 값만.
#   - 한 글·한 설명에 firemap.kr 링크는 1개(utm.md '형식').
#   - 경로: src/firemap-v2/toolPages.js의 path와 '/'만 있는 경로로 본다(없는 경로 = 깨진 링크).
#   - http:// 링크, 주소 끝에 붙은 문장부호(').,' 등)는 깨진 링크로 본다.
#   - cafe.naver.com/firemap 첫 화면 링크는 경고(글 번호 없이 '카페에 표' 약속이면 찾을 수 없음 — RULES.md 2026-10-02 audit 줄 '설명란에서 카페 표를 약속하면 그 글 주소').
import json, os, re, sys
from urllib.parse import urlsplit, parse_qs

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = re.compile(r'https?://[^\s<>"\'\]]+')
SOURCES = {'youtube', 'shorts', 'cafe', 'blog', 'openchat', 'clip', 'share', 'hn', 'email'}
MEDIUMS = {'profile', 'desc', 'comment', 'post', 'notice', 'kakao', 'copy', 'outreach'}
VAL = re.compile(r'^[a-z0-9_-]+$')
TRAIL = '.,)。」』!?;:'


def known_paths(root=ROOT):
    p = os.path.join(root, 'src', 'firemap-v2', 'toolPages.js')
    paths = {'/'}
    if os.path.exists(p):
        paths |= set(re.findall(r"path:\s*'([^']+)'", open(p, encoding='utf-8').read()))
    return paths


def texts_of(target):
    """검사할 (이름, 글) 목록."""
    if os.path.isdir(target):
        out = []
        for f in sorted(os.listdir(target)):
            if re.fullmatch(r'(c\d\d|title)\.txt', f):
                out.append((f, open(os.path.join(target, f), encoding='utf-8').read()))
        return [(os.path.basename(os.path.dirname(target.rstrip('/'))) or target, '\n'.join(t for _, t in out))]
    if target.endswith('.json'):
        d = json.load(open(target, encoding='utf-8'))
        return [(target, d.get('desc') or d.get('description') or '')]
    return [(target, open(target, encoding='utf-8').read())]


def check_url(u, paths):
    issues = []
    raw = u
    if u[-1] in TRAIL:
        issues.append(('거부', f'주소 끝에 문장부호가 붙음: {raw}'))
        u = u.rstrip(TRAIL)
    sp = urlsplit(u)
    host = sp.netloc.lower()
    if sp.scheme == 'http':
        issues.append(('거부', f'http:// 링크(https 아님): {u}'))
    if host in ('firemap.kr', 'www.firemap.kr'):
        q = parse_qs(sp.query)
        for k in ('utm_source', 'utm_medium', 'utm_campaign'):
            if k not in q:
                issues.append(('거부', f'{k} 없음: {u}'))
        for k in ('utm_source', 'utm_medium', 'utm_campaign'):
            for v in q.get(k, []):
                if not VAL.match(v):
                    issues.append(('거부', f'{k}={v} — 영문 소문자·숫자·-·_만: {u}'))
        if q.get('utm_source') and q['utm_source'][0] not in SOURCES:
            issues.append(('거부', f"utm_source={q['utm_source'][0]} — utm.md 표에 없는 값: {u}"))
        if q.get('utm_medium') and q['utm_medium'][0] not in MEDIUMS:
            issues.append(('거부', f"utm_medium={q['utm_medium'][0]} — utm.md 표에 없는 값: {u}"))
        path = sp.path or '/'
        if path not in paths:
            issues.append(('거부', f'사이트에 없는 경로 {path}: {u}'))
    if host == 'cafe.naver.com' and sp.path.rstrip('/') == '/firemap':
        issues.append(('경고', f'카페 첫 화면 링크(글 번호 없음): {u}'))
    return issues


def check_text(name, text, paths):
    urls = URL.findall(text)
    issues = []
    for u in urls:
        issues += check_url(u, paths)
    fm = [u for u in urls if urlsplit(u.rstrip(TRAIL)).netloc.lower() in ('firemap.kr', 'www.firemap.kr')]
    if len(fm) > 1:
        issues.append(('거부', f'firemap.kr 링크 {len(fm)}개 — 한 글·설명에 1개(utm.md)'))
    camps = {parse_qs(urlsplit(u).query).get('utm_campaign', [''])[0] for u in fm}
    if len(camps) > 1:
        issues.append(('거부', f'한 글 안 utm_campaign이 서로 다름: {sorted(camps)}'))
    return urls, issues


def live(u):
    try:
        import requests
        r = requests.head(u, allow_redirects=True, timeout=15)
        if r.status_code >= 400 or r.status_code == 405:
            r = requests.get(u, allow_redirects=True, timeout=15)
        return r.status_code
    except Exception as e:  # 프록시 차단·DNS 실패
        return f'확인 안 함({type(e).__name__})'


def main(argv):
    do_live = '--live' in argv
    argv = [a for a in argv if a != '--live']
    if not argv:
        print('사용법: python3 work/audit_links.py [--live] <pkg 폴더 | meta.json | .txt> [...]'); return 2
    paths = known_paths()
    bad = 0
    for t in argv:
        for name, text in texts_of(t):
            urls, issues = check_text(name, text, paths)
            fails = [s for k, s in issues if k == '거부']
            print(f"== {name}: 링크 {len(urls)} · 거부 {len(fails)} · 경고 {sum(1 for k, _ in issues if k == '경고')}")
            for k, s in issues:
                print(f'  [{k}] {s}')
            if do_live:
                for u in urls:
                    print(f'  [열어 봄] {live(u.rstrip(TRAIL))} {u}')
            bad += bool(fails)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main(sys.argv[1:]))
