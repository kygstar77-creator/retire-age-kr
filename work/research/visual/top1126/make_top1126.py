# benchmark-loop 11/26 지시 1·2 (thumb-gap-1126.md ② 1위·2위) — copywriter 2026-11-26. 큰 글·사진·꼴은 지금 판 그대로, 위 작은 줄만 바꿈.
#   ⓐ 위 줄 없앰(' ') · ⓑ 대본 안 박힌 날짜 사건 값(지어낸 인용 0, A88 상대 시점 0)
#   CC-1 ⓑ 대본 158행 '1년 끝을 2025년 12월로 자르면 커버드콜이 훨씬 앞섰습니다' · SQ-1 ⓑ 대본 72·73행 2022년 나스닥100(QQQ) −32.6% · KOSPI-1 대본 38·39행 2026-11-20 하루 −5.21%
import os, sys, importlib, inspect
sys.stdout.reconfigure(encoding='utf-8')
V = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def mod(folder, name):
    sys.path.insert(0, os.path.join(V, folder)); m = importlib.import_module(name); sys.path.pop(0); return m
# CC-1 (cc1_e2 꼴: make_cc1e.py)
M = mod('CC-1-thumb', 'make_cc1')
M.BIG = ['같은 1억, 배당 ETF 둘', '1년 뒤 누가 더 남았나?']; kw = dict(band=190, tshade=(330, 160), sw=13, tsw=8)
for out, top in (('cc1_t0.png', ' '), ('cc1_t1.png', '2025년 12월엔 커버드콜이 앞섰다')):
    M.TOP = top; M.make(out, 'p_6328948.jpg', 0.3, **kw)
# SQ-1 (sq1_c1b 꼴: make_sq1c36.py)
S = mod('SQ-1-thumb', 'make_sq1'); sys.path.insert(0, os.path.join(V, 'SQ-1-thumb')); from make_sq1q import KW
S.PILL = None; S.BIG = ['나스닥100에만 넣었다면', 'SCHD랑 반반이면 얼마?']
for out, top in (('sq1_t0.png', ' '), ('sq1_t1.png', '2022년 한 해 나스닥100 −33%')):
    S.make(out, 'chart_point_5833757.jpg', 0.2, **dict(KW, top=top))
# KOSPI-1 (공개본 k1_qc 꼴: make_k1q.py, 알약 그리기 뺀 make)
K = mod('KOSPI-1-thumb', 'make_kospi1')
src = inspect.getsource(K.make)
src = chr(10).join(l for l in src.split(chr(10)) if 'rounded_rectangle' not in l and 'PILL, font=pf, fill=WHITE' not in l)
exec(compile(src, 'make_nopill', 'exec'), K.__dict__)
K.TOP = '11월 20일 코스피 −5.21%'; K.BIG = ['코스피 5% 넘게 빠진 날', '그 뒤 1년은 어땠을까?']
K.make('k1_t1.png', 'candle_down_35118208.jpg', 0.15, band=150, tshade=(400, 160), sw=13, tsw=8)
