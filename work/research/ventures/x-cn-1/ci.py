# X-CN-1 매일 빌드 — kygstar77-creator.github.io 저장소 GitHub Actions(.github/workflows/x-cn-1-daily.yml)에서 돈다.
# (today.md 대역 18:21 지시, firemap-venture-builder 2026-10-01) 원본은 retire-age-kr ventures/x-cn-1, `deploy.py ci`가 복사한다.
#  1) build.py 원문 대조 — 사실표와 한 칸이라도 다르면 exit 2, 원문을 못 받으면 exit 3 → 실패 = 저장소 주인에게 이메일(사람 검수). 푸시 없음.
#  2) 바뀐 글자가 도장·상태(dyn 자리)뿐인지 — 쪽마다 편집 통과 표시(.edit.json) 해시가 그대로여야 한다. 아니면 exit 4.
#  3) 파일 목록이 공개본과 같아야 한다(새 쪽·빠진 쪽 = 사람 검수). 아니면 exit 5.
#  4) 통과하면 site/ 를 저장소 /exam-dates-kr/ 로 덮는다. 커밋·푸시는 워크플로가 한다.
import os, sys, re, json, hashlib, shutil, subprocess, fnmatch
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, 'site')
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))   # .github/build/x-cn-1 → 저장소 루트
LIVE = os.path.join(REPO, 'exam-dates-kr')
IGNORE = ('*.edit.json', '_*')
DYN = re.compile(rb'(?s)<!--dyn-->.*?<!--/dyn-->|/\*dyn\*/.*?/\*/dyn\*/|data-state="[a-z]*"')   # deploy.py와 같은 식


def sha(p):
    b = open(p, 'rb').read().replace(b'\r\n', b'\n')
    return hashlib.sha256(DYN.sub(b'', b)).hexdigest()[:16]


def files(top):
    out = set()
    for d, _, fs in os.walk(top):
        for f in fs:
            if not any(fnmatch.fnmatch(f, g) for g in IGNORE):
                out.add(os.path.relpath(os.path.join(d, f), top).replace(os.sep, '/'))
    return out


def main():
    env = dict(os.environ, XCN1_CI='1', FMKIT=os.path.join(LIVE, 'fmkit.js'))
    r = subprocess.run([sys.executable, os.path.join(HERE, 'build.py')], env=env)
    if r.returncode:
        sys.exit(f'build.py 실패 (exit {r.returncode}) — 2=원문 표 바뀜, 3=원문 못 받음. 푸시 안 함, 사람 검수.')
    bad = []
    for rel in sorted(files(SITE)):
        if not rel.endswith('.html'):
            continue
        mark = os.path.join(SITE, rel + '.edit.json')
        want = json.load(open(mark, encoding='utf-8')).get('sha') if os.path.exists(mark) else None
        got = sha(os.path.join(SITE, rel))
        if got != want:
            bad.append(f'{rel}: 편집 통과 {want} ≠ 지금 {got}')
    if bad:
        print('\n'.join(bad))
        sys.exit(4)
    a, b = files(SITE), files(LIVE)
    if a != b:
        print('새 파일', sorted(a - b), '빠진 파일', sorted(b - a))
        sys.exit(5)
    shutil.rmtree(LIVE)
    shutil.copytree(SITE, LIVE, ignore=shutil.ignore_patterns(*IGNORE))
    st = json.load(open(os.path.join(HERE, 'facts', '_verified.json'), encoding='utf-8'))
    print('통과 — 도장', st.get('hanneunggeom'))


if __name__ == '__main__':
    main()
