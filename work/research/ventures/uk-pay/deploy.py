# X-V1 uk-pay 배포 — 검사 2개를 통과해야 push한다 (workflow.md 편집 관문, firemap-venture-builder 2026-10-01).
#  ① work/aitell.py 점수: 각 HTML의 화면 글자가 기준 이하
#  ② 편집 통과 표시: site/<경로>.edit.json 의 sha가 지금 파일 해시와 같다(통과 뒤 바뀌면 무효)
# 사용: py -3.12 deploy.py check          검사만
#       py -3.12 deploy.py push           검사 통과 시 site/ 를 kygstar77-creator.github.io 저장소 /uk-take-home-pay/ 로 push(main = 공개, kit/ghio.py)
#       py -3.12 deploy.py ci             ci.py·uk-pay-daily.yml 을 저장소 .github/ 로 복사·push(매일 GOV.UK 원문 대조, 읽기 전용)
#       py -3.12 deploy.py hash <파일>    편집자가 .edit.json 에 넣을 sha
import sys, os, re, json, hashlib, html, subprocess, tempfile, shutil
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, 'site')
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'work'))
import aitell  # noqa: E402

sys.path.insert(0, os.path.join(HERE, '..', 'kit'))
import ghio  # noqa: E402
FOLDER = 'uk-take-home-pay'


def pages():
    for d, _, fs in os.walk(SITE):
        for f in fs:
            if f.endswith('.html'):
                yield os.path.join(d, f)


def sha(p):
    return hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16]  # 줄끝(CRLF) 변환에 흔들리지 않게


def visible(p):
    t = open(p, encoding='utf-8').read()
    t = re.sub(r'(?s)<(script|style)[^>]*>.*?</\1>|<!--.*?-->', ' ', t)
    metas = ' '.join(re.findall(r'<meta[^>]+content="([^"]+)"', t))
    return html.unescape(re.sub(r'<[^>]+>', ' ', t) + ' ' + metas)


def check():
    bad = 0
    for p in pages():
        rel = os.path.relpath(p, SITE)
        val, hits, n = aitell.score(visible(p))
        lim = aitell.LIMIT if n >= 300 else aitell.LIMIT_SHORT
        mark = p + '.edit.json'
        ok_edit = os.path.exists(mark) and json.load(open(mark, encoding='utf-8')).get('sha') == sha(p)
        flag = 'OK' if (val <= lim and ok_edit) else 'NO'
        bad += flag == 'NO'
        print(f'{flag} {rel}: aitell {val}/{lim} · 편집 표시 {"맞음" if ok_edit else "없음/무효"}')
    return bad == 0


def push():
    if not check():
        sys.exit('검사 실패 — push 안 함')
    ghio.sync(SITE, FOLDER, ignore=('*.edit.json',))


def ci():
    # 매일 점검은 github.io 저장소 Actions가 돈다(retire-age-kr엔 Actions 금지). 원본은 여기, 저 쪽은 복사본.
    if ghio.git('rev-parse', '--verify', 'HEAD', check=False).returncode == 0:
        ghio.git('pull', '-q', '--rebase', 'origin', 'main')
    dst = os.path.join(ghio.CLONE, '.github', 'build', 'uk-pay')
    os.makedirs(dst, exist_ok=True)
    shutil.copy(os.path.join(HERE, 'ci.py'), dst)
    wf = os.path.join(ghio.CLONE, '.github', 'workflows')
    os.makedirs(wf, exist_ok=True)
    shutil.copy(os.path.join(HERE, 'uk-pay-daily.yml'), wf)
    ghio.git('add', '-A', '--', '.github/build/uk-pay', '.github/workflows/uk-pay-daily.yml')
    if ghio.git('diff', '--cached', '--quiet', '--', '.github', check=False).returncode == 0:
        print('바뀐 것 없음')
        return
    ghio.git(*ghio.ID, 'commit', '-q', '-m', 'uk-pay: daily GOV.UK check (Actions)', '--', '.github/build/uk-pay', '.github/workflows/uk-pay-daily.yml')
    ghio.git('push', '-q', 'origin', 'HEAD:main')
    print('push 완료 — .github/workflows/uk-pay-daily.yml')


if __name__ == '__main__':
    a = sys.argv[1:] or ['check']
    if a[0] == 'hash':
        print(sha(a[1]))
    elif a[0] == 'push':
        push()
    elif a[0] == 'ci':
        ci()
    else:
        sys.exit(0 if check() else 1)
