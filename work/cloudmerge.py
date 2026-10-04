# 클라우드 세션 결과 자동 반영 — 사장님 10/3 "클라우드에서 조사한 것도 자동으로 바로 반영도 안 되잖아"
# origin/cloud/* 브랜치를 가져와 안전하면 dev에 합치고, 아니면 today.md에 [검수 요청] 한 줄.
#   py -3.12 work/cloudmerge.py          → 합치기
#   py -3.12 work/cloudmerge.py --dry    → 무엇을 할지만 출력
# 안전 기준: ① 충돌 없이 합쳐짐 ② 바뀐 .py가 전부 문법 통과 ③ work/tests/ 가 있으면 그 테스트 통과 ④ _boss_·.env·토큰 파일 없음
import subprocess, sys, os, datetime, glob, re
sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRY = '--dry' in sys.argv
def git(*a, check=True):
    r = subprocess.run(['git', '-C', ROOT, *a], capture_output=True, text=True, encoding='utf-8')
    if check and r.returncode: raise RuntimeError(' '.join(a) + ' → ' + (r.stderr or r.stdout)[-300:])
    return r.stdout.strip()
def note(line):
    with open(os.path.join(ROOT, 'work/research/meeting/today.md'), 'a', encoding='utf-8') as f: f.write(line + '\n')
git('fetch', '-q', 'origin')
if git('branch', '--show-current') != 'dev': print('dev 브랜치가 아님 — 멈춤'); sys.exit(1)
done = []
for b in [x.strip() for x in git('branch', '-r', '--no-merged', 'dev').splitlines() if x.strip().startswith('origin/cloud/')]:
    files = git('diff', '--name-only', f'dev...{b}').splitlines()
    bad = [f for f in files if re.search(r'(_boss_|\.env$|token|secret|credential)', f, re.I)]
    now = datetime.datetime.now().strftime('%m/%d %H:%M')
    # 발행 코드는 자동 반영 금지(10/4 사장님 "클라우드 방이 유튜브 마음대로 헤집다가 어뷰징 저품질 되면?"):
    # 카페·블로그·유튜브·쇼츠에 실제로 올리는 코드와 그 간격·상한·관문을 바꾸면 PC 발행 행동이 바뀐다 → 순돌이 검토 뒤 손으로 합친다.
    PUBLISH = r'^work/(naverpost|cafeapi|cafeedit|shortsdaily|shorts|ytlong|ytupload|f2_coupang|ytdesc_all|editgate|aitell|readcheck|patrol|blogimg)\.py$|^functions/|^\.github/|^wrangler'
    hot = [f for f in files if re.search(PUBLISH, f)]
    if hot:
        note(f'- [검수 요청] 순돌이 — {b}가 발행 코드 {hot[:4]}를 바꿈 → 자동 반영 안 함, 간격·상한·관문이 약해지지 않았는지 순돌이가 보고 손으로 합침 ({now})'); print(b, '발행 코드 — 검토 대기'); continue
    if bad:
        note(f'- [검수 요청] 순돌이 — {b} 비밀 파일 의심 {bad[:3]} → 자동 반영 안 함 ({now})'); print(b, '비밀 의심 — 건너뜀'); continue
    if DRY: print(b, len(files), '파일:', files[:8]); continue
    # 커밋 전에 검사한다(--no-commit). 실패하면 merge --abort — 합치기가 건드린 파일만 되돌리고 다른 직원의 작업 중 파일은 그대로 둔다.
    # (10/5 05:4x 첫 실행 때 실패 시 reset --hard HEAD~1을 써서 추적 파일의 커밋 안 된 수정까지 지울 수 있었다 — 고침)
    r = subprocess.run(['git', '-C', ROOT, 'merge', '--no-ff', '--no-commit', b], capture_output=True, text=True, encoding='utf-8', errors='replace')
    if r.returncode:
        git('merge', '--abort', check=False)
        note(f'- [검수 요청] 순돌이 — {b} dev와 충돌, 자동 반영 못 함 ({now})'); print(b, '충돌 — 되돌림'); continue
    pys = [os.path.join(ROOT, f) for f in files if f.endswith('.py') and os.path.exists(os.path.join(ROOT, f))]
    fail = [p for p in pys if subprocess.run([sys.executable, '-m', 'py_compile', p], capture_output=True).returncode]
    tests = sorted(glob.glob(os.path.join(ROOT, 'work/tests/test_*.py')))
    if not fail and tests:
        t = subprocess.run([sys.executable, '-m', 'pytest', '-q', '-p', 'no:cacheprovider', *tests], capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=ROOT)
        if t.returncode not in (0, 5): fail.append('pytest: ' + (t.stdout + t.stderr)[-300:])
    if fail:
        git('merge', '--abort', check=False)
        note(f'- [검수 요청] 순돌이 — {b} 합친 뒤 검사 실패 {str(fail)[:150]} → 되돌림 ({now})'); print(b, '검사 실패 — 되돌림'); continue
    git('commit', '-q', '--no-edit', '-m', f'cloudmerge: {b} 자동 반영')
    done.append(b); print(b, '반영', len(files), '파일')
    note(f'- 완료: cloudmerge {now} — {b} 자동 반영({len(files)}파일). 담당은 결과 문서를 읽고 상위 방법·규칙을 자기 일에 적용(ai-study → firemap-ai-lab, script-gate → firemap-editor, render-gates → firemap-video-producer)')
if done and not DRY:
    git('push', '-q', 'origin', 'dev')
print('끝 — 반영', len(done))
