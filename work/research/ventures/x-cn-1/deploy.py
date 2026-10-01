# X-CN-1 시험 일정 배포 — 검사 2개를 통과해야 push한다 (workflow.md 편집 관문, firemap-venture-builder 2026-10-01).
#  ① work/aitell.py 점수: 각 HTML의 화면 글자가 기준 이하
#  ② 편집 통과 표시: site/<경로>.edit.json 의 sha가 지금 파일 해시와 같다(통과 뒤 바뀌면 무효 — 매일 바뀌는 도장·대조 시각은 빼고 잰다)
# 사용: py -3.12 deploy.py check          검사만
#       py -3.12 deploy.py push           검사 통과 시 site/ 를 kygstar77-creator.github.io 저장소 /exam-dates-kr/ 로 push(main = 공개, kit/ghio.py)
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
FOLDER = 'exam-dates-kr'


def pages():
    for d, _, fs in os.walk(SITE):
        for f in fs:
            if f.endswith('.html'):
                yield os.path.join(d, f)


# 편집 표시 해시에서 빼는 자리(매일 빌드로 바뀌는 것만): 도장·대조 시각·맨 위 줄 계산값과 data-state 값.
# build.py가 <!--dyn-->…<!--/dyn--> / /*dyn*/…/*/dyn*/ 로 감싼다. 그 문장을 만드는 src/nextline.cjs는 쪽 안에 실려 해시에 남는다
# (editor-web 16:14 조건 ⓑ — 매일 빌드마다 편집 표시가 무효가 되던 문제).
DYN = re.compile(rb'(?s)<!--dyn-->.*?<!--/dyn-->|/\*dyn\*/.*?/\*/dyn\*/|data-state="[a-z]*"')


def sha(p):
    b = open(p, 'rb').read().replace(b'\r\n', b'\n')  # 줄끝(CRLF) 변환에 흔들리지 않게
    return hashlib.sha256(DYN.sub(b'', b)).hexdigest()[:16]


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
    ghio.sync(SITE, FOLDER, ignore=('*.edit.json', '_*'))


if __name__ == '__main__':
    a = sys.argv[1:] or ['check']
    if a[0] == 'hash':
        print(sha(a[1]))
    elif a[0] == 'push':
        push()
    else:
        sys.exit(0 if check() else 1)
