# 실험 사이트 공용 배포 — kygstar77-creator.github.io (사용자 사이트 저장소, main 푸시 = 공개) 아래 /<폴더>/ 로 올린다.
# 레드팀 결정(decisions/2026-10-01-consolidate.md): 실험은 전부 firemap.kr 밖, 이 저장소 아래 폴더로 — 새 실험마다 사장님 손 0번.
# 각 실험의 deploy.py가 자기 검사(aitell·편집 표시)를 통과한 뒤에만 sync()를 부른다. 다른 실험 폴더는 건드리지 않는다.
import os, shutil, subprocess

CLONE = os.path.join(os.path.expanduser('~'), 'Documents', 'GitHub', 'kygstar77-creator.github.io')
REMOTE = 'https://github.com/kygstar77-creator/kygstar77-creator.github.io.git'
BASE = 'https://kygstar77-creator.github.io/'
ID = ['-c', 'user.name=kygstar77-creator', '-c', 'user.email=kygstar77@gmail.com']


def git(*a, check=True):
    return subprocess.run(['git', '-C', CLONE, *a], check=check, capture_output=True, text=True, encoding='utf-8')


def sync(site, folder, ignore=('*.edit.json',), msg=None):
    if not os.path.isdir(os.path.join(CLONE, '.git')):
        subprocess.run(['git', 'clone', '-q', REMOTE, CLONE], check=True)
    if git('rev-parse', '--verify', 'HEAD', check=False).returncode == 0:
        git('pull', '-q', '--rebase', 'origin', 'main')
    dst = os.path.join(CLONE, folder)
    shutil.rmtree(dst, ignore_errors=True)
    shutil.copytree(site, dst, ignore=shutil.ignore_patterns(*ignore))
    git('add', '-A', '--', folder)
    if git('diff', '--cached', '--quiet', '--', folder, check=False).returncode == 0:
        print(f'바뀐 것 없음 → {BASE}{folder}/')
        return
    git(*ID, 'commit', '-q', '-m', msg or f'deploy {folder}', '--', folder)
    git('push', '-q', 'origin', 'HEAD:main')
    print(f'push 완료 → {BASE}{folder}/ (Pages 반영 1~2분)')
