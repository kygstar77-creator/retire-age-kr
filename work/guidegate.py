# 자동 가이드(public/guide/*.html) AI 티 관문 — work/aitell.py 점수를 HTML 본문에 건다(2026-10-01).
#   py -3.12 work/guidegate.py check <html>            → 기준 넘고 편집 통과 표시 없으면 종료코드 4 + editor-web 요청 줄 출력
#   py -3.12 work/guidegate.py check <html> --request  → 막히면 그 요청 줄을 work/research/meeting/today.md 맨 아래에 붙인다
#   py -3.12 work/guidegate.py pass <html> <편집자>     → 편집 통과 표시(work/guide_editor_ok.json, 파일 sha 고정)
#   py -3.12 work/guidegate.py ci <base> <head>         → 두 커밋 사이 새로 생긴·바뀐 가이드만 검사(GitHub Actions)
# 왜: '[auto] guide' 커밋은 클라우드 루틴 'Firemap daily growth'(trig_01KmYx7HNYMGjHLy371XGxyc, 매일 09:00 KST)가
#     GitHub 커넥터 create_or_update_file로 main에 바로 올린다 — 저장소 안 발행기가 아니라서 aitell gate가 안 걸렸다
#     (10/1 09:14 8c18984 연금수령한도, editor-web이 10:41에 사후 수정). 루틴이 커밋 직전에 이 check를 부른다.
# 편집 통과 표시는 파일 sha로 묶인다 — 표시 뒤에 글이 바뀌면 무효.
import sys, os, re, json, hashlib, html, subprocess, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from aitell import score, LIMIT, LIMIT_SHORT  # noqa: E402

OK_DB = os.path.join(HERE, 'guide_editor_ok.json')
TODAY = os.path.join(HERE, 'research', 'meeting', 'today.md')


def body_text(raw):
    """사람이 읽는 본문만: <head>·script·style·nav·면책(.disc)·CTA 빼고 태그를 걷어 문단을 줄로."""
    m = re.search(r'<body[^>]*>(.*)</body>', raw, re.S | re.I)
    b = m.group(1) if m else raw
    b = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', b, flags=re.S | re.I)
    b = re.sub(r'<(\w+)[^>]*class="[^"]*\b(nav|disc|cta)\b[^"]*"[^>]*>.*?</\1>', ' ', b, flags=re.S | re.I)
    b = re.sub(r'</(p|h[1-6]|li|tr|div|table|ul|ol)>', '\n\n', b, flags=re.I)
    b = re.sub(r'<br\s*/?>', '\n', b, flags=re.I)
    b = re.sub(r'<[^>]+>', ' ', b)
    b = html.unescape(b)
    b = re.sub(r'[ \t]+', ' ', b)
    return re.sub(r'\n\s*\n+', '\n\n', b).strip()


def sha(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()[:16]


def load_ok():
    return json.load(open(OK_DB, encoding='utf-8')) if os.path.exists(OK_DB) else {}


def key(path):
    return os.path.basename(path)


def gate(path):
    """(올려도 되나, 사유, 걸린 곳, 점수)."""
    raw = open(path, encoding='utf-8').read()
    val, hits, n = score(body_text(raw))
    lim = LIMIT if n >= 300 else LIMIT_SHORT
    if val <= lim: return True, f'AI 티 {val}(기준 {lim}, 본문 {n}자)', hits, val
    ok = load_ok().get(key(path))
    if ok and ok.get('sha') == sha(path):
        return True, f'AI 티 {val}(기준 {lim}) — 편집 통과 {ok.get("who")} {ok.get("at")}', hits, val
    why = ' (편집 통과 뒤 글이 바뀜)' if ok else ''
    return False, f'AI 티 {val}이 기준 {lim}을 넘는다{why}', hits, val


def request_line(path, val, hits):
    now = datetime.datetime.now().strftime('%H:%M')
    rel = os.path.relpath(path, ROOT).replace('\\', '/') if os.path.isabs(path) else path
    return (f'- [요청] 자동 가이드 발행 보류(guidegate {now}) → firemap-editor-web: {rel} AI 티 {val}(기준 {LIMIT}) — '
            f'사람 말로 고친 뒤 `py -3.12 work/guidegate.py pass {rel} firemap-editor-web` 하고 dev 커밋. '
            f'걸린 곳: {"; ".join(hits[:4])}. 숫자·법 조문·구조 그대로.')


def main(a):
    if not a:
        print(open(__file__, encoding='utf-8').read().split('import')[0]); return 0
    if a[0] == 'check':
        ok, msg, hits, val = gate(a[1])
        if ok: print('통과:', msg); return 0
        print('올리지 않는다:', msg)
        for h in hits[:10]: print('   ', h)
        line = request_line(a[1], val, hits)
        print(line)
        if '--request' in a:
            with open(TODAY, 'a', encoding='utf-8') as f: f.write('\n' + line + '\n')
            print('today.md에 요청 줄을 붙였다')
        return 4
    if a[0] == 'pass':
        who = a[2] if len(a) > 2 else 'editor'
        db = load_ok()
        val = score(body_text(open(a[1], encoding='utf-8').read()))[0]
        db[key(a[1])] = {'sha': sha(a[1]), 'who': who, 'at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), 'score': val}
        json.dump(db, open(OK_DB, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, sort_keys=True)
        print('편집 통과 표시', key(a[1]), val); return 0
    if a[0] == 'ci':
        base, head = a[1], a[2]
        out = subprocess.run(['git', 'diff', '--name-only', '--diff-filter=AM', base, head, '--', 'public/guide/'],
                             cwd=ROOT, capture_output=True, text=True, encoding='utf-8').stdout.split()
        bad = 0
        for f in out:
            if not f.endswith('.html') or f.endswith('index.html'): continue
            ok, msg, hits, val = gate(os.path.join(ROOT, f))
            print(('통과 ' if ok else '막힘 ') + f + ' — ' + msg)
            if not ok:
                bad += 1
                for h in hits[:6]: print('    ', h)
                print('  ', request_line(f, val, hits))
        print(f'가이드 {len(out)}개 검사, 막힘 {bad}')
        return 4 if bad else 0
    print('모르는 명령:', a[0]); return 2


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main(sys.argv[1:]))
