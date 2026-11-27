# NDG-1 3장 점 그림 재료 — calc.py ③과 같은 셈(같은 단지·면적, 2021 최고 vs 2026-07~11 중앙, 7~11월 3건↑)을 묶음 하나하나 비율로 뽑는다 (motion 2026-11-27)
# 출력: calc_dots_out.json {n, median, over, under80, per_gu, dots:[{gu, r}]} — r은 지금/2021최고(소수 4자리)
import runpy, io, contextlib, json, os, sys, statistics as st
sys.stdout.reconfigure(encoding='utf-8')
here = os.path.dirname(os.path.abspath(__file__))
class _Sink(io.StringIO):
    def reconfigure(self, **k): pass
with contextlib.redirect_stdout(_Sink()):
    ns = runpy.run_path(os.path.join(here, 'calc.py'))
res = ns['res']; rat = [x[4] for x in res]
out = dict(src='calc.py ③ (국토교통부 실거래, work/research/rt)', n=len(res), median=round(st.median(rat)*100, 1),
           over=sum(1 for x in rat if x >= 1), under80=sum(1 for x in rat if x < 0.8),
           per_gu={g: dict(n=len([x for x in res if x[0][0]==g]), median=round(st.median([x[4] for x in res if x[0][0]==g])*100, 1)) for g in ns['GU'].values()},
           dots=[dict(gu=x[0][0], r=round(x[4], 4)) for x in res])
json.dump(out, open(os.path.join(here, 'calc_dots_out.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print({k: v for k, v in out.items() if k != 'dots'})
