# 운영 반영 관문(2026-10-05, firemap-venture-builder · 점검관 15:37 지시) — dev:main 푸시 묶음 안 커밋마다 편집·디자인 통과가 있는지 본다.
# 10/5 13:48 62d063e: 내 X-CN-1 커밋을 올리려던 dev:main 푸시에 c7d1ba4(연봉 v5, 편집 통과 전)가 같이 실려 운영에 나갔다.
# dev:main은 dev 끝까지 전부 올리므로 '내 커밋만 확인'으로는 못 막는다 → 묶음 전체를 커밋별로 본다.
#   py -3.12 work/shipgate.py            origin/main..dev 커밋별 한 줄(무엇이 필요한지·통과 줄이 있는지). 빠짐 있으면 종료코드 1
#   py -3.12 work/shipgate.py <a>..<b>   범위 지정
# 통과 기록 = work/research/shipgate.md 에 한 줄: `- <sha7> 편집 통과 <task-id HH:MM>` / `- <sha7> 디자인 통과 <task-id HH:MM>`
#   (해당 없음이면 `- <sha7> 편집 해당없음 <이유>`). 검수자 또는 커밋한 사람이 today.md 통과 줄을 보고 적는다.
# 판정(어림, 사람이 볼 것): 화면 코드(src/components·src/pages·src/ui·public/*.html, public/guide 제외)에서
#   더하거나 뺀 줄에 한글이 있으면 '편집', .css 이거나 className·style 줄이 바뀌면 '디자인'. 가이드는 guidegate.py, 계산식만(src/utils)은 대상 아님.
import os, re, sys, subprocess
sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, 'work', 'research', 'shipgate.md')
SCREEN = re.compile(r'^(src/(components|pages|ui)/|src/App\.|index\.html$|public/(?!guide/).*\.html$)')
HANGUL = re.compile(r'[가-힣]')
LOOK = re.compile(r'className|style=|<svg|\.css')


def git(*a):
    return subprocess.run(['git', '-C', ROOT, *a], capture_output=True, text=True, encoding='utf-8').stdout


def needs(sha):
    files = [f for f in git('show', '--name-only', '--format=', sha).split('\n') if SCREEN.match(f) or f.endswith('.css') and f.startswith('src/')]
    if not files:
        return files, set()
    need = set()
    diff = git('show', '--format=', '-U0', sha, '--', *files)
    for ln in diff.split('\n'):
        if ln[:1] in '+-' and ln[:3] not in ('+++', '---'):
            if HANGUL.search(ln.split('//')[0]):
                need.add('편집')
            if LOOK.search(ln):
                need.add('디자인')
    if any(f.endswith('.css') for f in files):
        need.add('디자인')
    return files, need


def ledger():
    return open(LEDGER, encoding='utf-8').read() if os.path.exists(LEDGER) else ''


def main():
    rng = sys.argv[1] if len(sys.argv) > 1 else 'origin/main..dev'
    shas = git('rev-list', '--reverse', rng).split()
    led, bad = ledger(), 0
    if not shas:
        print(f'shipgate: {rng} 올릴 커밋 0')
        return 0
    for s in shas:
        s7 = s[:7]
        subj = git('log', '-1', '--format=%s', s).strip()[:50]
        files, need = needs(s)
        if not need:  # 화면 글자·모양 변경 없는 커밋은 줄을 찍지 않는다(묶음 25개 중 대부분)
            continue
        have = {k for k in need if re.search(rf'^- {s7}\S* {k} (통과|해당없음)', led, re.M)}
        miss = need - have
        bad += bool(miss)
        tag = 'OK ' if not miss else 'NO '
        print(f'{tag} {s7} 필요 {"·".join(sorted(need))} / 기록 {"·".join(sorted(have)) or "없음"} — {subj}')
    print(f'shipgate: {rng} {len(shas)}커밋(화면 바뀐 것만 위에) 중 빠짐 {bad} → ' + ('푸시해도 됨' if not bad else
          '빠진 커밋은 검수 요청 후 work/research/shipgate.md에 통과 줄을 적고 푸시(남의 커밋이면 그 담당에게 [요청])'))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
