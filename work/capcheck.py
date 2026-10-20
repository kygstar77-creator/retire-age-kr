"""자막 조각 검사(A50, 2026-10-20 motion): 대본 줄을 화면 자막과 같은 capChunks로 쪼개 조사·의존명사로 시작하는 조각을 센다.
쓰기: py -3.12 work/capcheck.py <say.txt ...> [--list]   · 조각 0이면 종료 0, 있으면 1
"""
import os, subprocess, sys, tempfile
V = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'video')
args = [a for a in sys.argv[1:] if a != '--list']
if not args:
    sys.exit(__doc__)
out = os.path.join(tempfile.gettempdir(), 'capcheck_bundle.js')
eb = os.path.join(V, 'node_modules', '.bin', 'esbuild.cmd' if os.name == 'nt' else 'esbuild')
subprocess.run([eb, os.path.join(V, 'scripts', 'capcheck.ts'), '--bundle', '--platform=node', f'--outfile={out}', '--log-level=warning'], check=True)
env = dict(os.environ, CAP_LIST='1' if '--list' in sys.argv else '')
sys.exit(subprocess.run(['node', out, *[os.path.abspath(a) for a in args]], env=env).returncode)
