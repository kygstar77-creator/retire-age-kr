# C-1 썸네일용 잔액 경로 — ep/C-1/calc.py의 path()·run()을 그대로 쓰되 calc_out.txt는 건드리지 않는다(쓰기 줄만 막음).
# 출력 paths9798.json: 3억·월 200만원, 배당(A) 1997·1998년 시작 연말 잔액(억원). calc_out 3) '1997:29+ 1998:11'과 assert.
import json, pathlib, re, io, contextlib
HERE = pathlib.Path(__file__).resolve().parent
EP = HERE.parents[1] / 'longform' / 'ep' / 'C-1'
src = (EP / 'calc.py').read_text(encoding='utf-8')
src = src.replace("(HERE / 'calc_out.txt').write_text(", "_noop(").replace("(HERE / 'calc_out.txt').open('a', encoding='utf-8').write(", "_noop(")
assert src.count('_noop(') == 2
g = {'__file__': str(EP / 'calc.py'), '__name__': 'c1calc', '_noop': lambda *a, **k: None}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src, str(EP / 'calc.py'), 'exec'), g)
R, YEARS, path, run = g['R_KRW'], g['YEARS'], g['path'], g['run']
out = {}
for s in (1997, 1998):
    rs = [R[y] for y in YEARS if y >= s]
    out[s] = [round(v / 1e8, 2) for v in path(300_000_000, 24_000_000, rs, 'A')]
    out[f'run{s}'] = run(300_000_000, 24_000_000, rs, 'A')[0]
calc = (EP / 'calc_out.txt').read_text(encoding='utf-8')
line = re.search(r'3\.00억원 · 월 200만원 · A: .*', calc).group(0)
assert ' 1997:29+ ' in line and ' 1998:11 ' in line, line
assert out['run1997'] is None and out['run1998'] == 11 and out[1998][-1] == 0 and len(out[1998]) == 11, out
json.dump({'1997': out[1997], '1998': out[1998]}, open(HERE / 'paths9798.json', 'w'), indent=0)
print(out)
