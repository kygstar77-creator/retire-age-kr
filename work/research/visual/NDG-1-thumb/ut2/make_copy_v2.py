# copywriter 11/26 2차 이해 시험 반영 문구판(사진은 visual a 그대로) — 3/3 '정반대 뉴스가 뭔지 썸네일에 없음' · 2/3 윗줄 안 읽힘
import os, sys, importlib
O = os.path.dirname(os.path.abspath(__file__)); P = os.path.dirname(O); sys.path.insert(0, P)
N = importlib.import_module('make_ndg1'); M = N.M; TB = N.TB
M.TOP = '노도강 실거래 3만 8천 건'
M.BIG = ['거래 끊겼다 vs 신고가', '어느 쪽이 맞았나?']
assert sum(len(t.replace(' ', '')) for t in M.BIG) in range(16, 25) and all(len(t.replace(' ', '')) <= 12 for t in M.BIG)
kw = dict(TB.KW); kw.pop('top', None)
tmp, g = N.prep('31728574', 0.35); M.O = O; M.make('ndg1_a_v2.png', tmp, 0.35, **kw); os.remove(os.path.join(M.H, tmp))
print('ok', g)
