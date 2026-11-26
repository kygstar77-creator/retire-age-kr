# benchmark-loop 11/26 지시 3 (thumb-gap-1126.md 3위) — visual 2026-11-26 09시. 큰 글·위 줄·사진은 지금 판(SQ-1 c1b · CC-1 e2) 그대로.
#   b1 = 공용 기본값(thumb_base.KW: 테두리 1280 약 10px·덮개 60)+밝기 보정만
#   b2 = b1 + 우리 facts 값 그림을 사진 속 화면에(SQ-1 왼쪽 모니터: 2011-10→2026-10 나스닥100만·반반 달마다 선, calc_mix 같은 걸음 ·
#        CC-1 탁자 위 휴대폰: 2025-11-20→2026-11-20 KODEX 커버드콜·TIGER 다우존스 종가 선, cc1_calc 같은 원자료). 그림에 글자·숫자 0(C-36 답 숫자 없음).
import os, sys, io, contextlib, importlib
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.stdout.reconfigure(encoding='utf-8')
V = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); O = os.path.dirname(os.path.abspath(__file__))
RES = os.path.dirname(V); sys.path.insert(0, V)
import thumb_base as TB


def mod(folder, name):
    sys.path.insert(0, os.path.join(V, folder)); m = importlib.import_module(name); sys.path.pop(0); return m


def calc(ep, name):
    p = os.path.join(RES, 'longform', 'ep', ep); cwd = os.getcwd(); os.chdir(p); sys.path.insert(0, p)
    try:
        with open(os.devnull, 'w', encoding='utf-8') as n, contextlib.redirect_stdout(n): return importlib.import_module(name)
    finally:
        os.chdir(cwd); sys.path.pop(0)


def screen(series, w, h, cols, widths, bg=(16, 22, 34), lo=None, hi=None, pad=(0.06, 0.10, 0.06, 0.12), grid=(44, 54, 70)):
    """화면 속 선 그림 — 글자 0. series 끼리 같은 축."""
    im = Image.new('RGB', (w, h), bg); d = ImageDraw.Draw(im)
    allv = [v for s in series for v in s]; lo = min(allv) if lo is None else lo; hi = max(allv) if hi is None else hi
    L, T, R, B = w * pad[0], h * pad[1], w * (1 - pad[2]), h * (1 - pad[3])
    for g in range(5): yy = T + (B - T) * g / 4; d.line([(L, yy), (R, yy)], fill=grid, width=max(2, h // 300))
    for s, c, wd in zip(series, cols, widths):
        n = len(s); pts = [(L + (R - L) * i / (n - 1), B - (B - T) * (v - lo) / (hi - lo)) for i, v in enumerate(s)]
        d.line(pts, fill=c, width=wd, joint='curve')
    return im


S = mod('SQ-1-thumb', 'make_sq1'); sys.path.insert(0, os.path.join(V, 'SQ-1-thumb'))
M = mod('CC-1-thumb', 'make_cc1')


def out_to(mod_, name, pic_im, ya, **kw):
    """make()는 photo/ 이름을 받으니 임시 사진으로 저장 후 부름 → 결과를 bright1126/로 옮김."""
    tmp = f'_b1126_{name}.jpg'; pic_im.save(os.path.join(mod_.H, tmp), quality=95)
    mod_.make(name, tmp, ya, **kw)
    for suf in ('', '_412', '_168'):
        fn = name.replace('.png', f'{suf}.png'); os.replace(os.path.join(mod_.O, fn), os.path.join(O, fn))
    os.remove(os.path.join(mod_.H, tmp))


def final_luma(name): return TB.luma(os.path.join(O, name))


if __name__ == '__main__':
    # ── SQ-1 (c1b 문구) ──
    S.PILL = None; S.BIG = ['나스닥100에만 넣었다면', 'SCHD랑 반반이면 얼마?']; TOPS = '2011년 1억원 · 나스닥100과 SCHD'
    raw = Image.open(os.path.join(S.H, 'chart_point_5833757.jpg')).convert('RGB')
    CM = calc('SQ-1', 'calc_mix')
    def path(w, start=(2011, 10), end=(2026, 10)):   # sq1boards.path와 같은 걸음(w = SCHD 비중)
        ms = [m for m in CM.months if start <= m <= end]; a, b = w, 1 - w; out = [1.0]
        for p, m in zip(ms, ms[1:]):
            a *= CM.S[m] / CM.S[p]; b *= CM.Q[m] / CM.Q[p]; v = a + b; out.append(v)
            if m[1] == 10: a, b = v * w, v * (1 - w)
        assert abs(out[-1] - CM.run(w, start, end)[0]) < 1e-9; return out
    q, h = path(0.0), path(0.5)
    assert (round(q[-1], 2), round(h[-1], 2)) == (13.56, 10.10), (q[-1], h[-1])   # calc_mix_out_1112 SCHD 0% 13.56억·50% 10.10억
    # 오른쪽 모니터(남의 시세 글자 'H:9089' 등)는 흐리게, 왼쪽 모니터(x 238~904, y 104~1000)는 우리 선으로 — 가리키는 손은 남김
    sq_r = raw.copy(); rb = raw.filter(ImageFilter.GaussianBlur(14)); mk = Image.new('L', raw.size, 0); ImageDraw.Draw(mk).rectangle((925, 0, raw.width, raw.height), fill=255)
    sq_blurR = Image.composite(rb, raw, mk.filter(ImageFilter.GaussianBlur(8)))
    chart = screen([q, h], 1332, 1792, [(245, 247, 250), (120, 190, 255)], [16, 14], pad=(0.06, 0.08, 0.06, 0.50))
    keep = TB.skin_mask(raw); kk = Image.new('L', raw.size, 0); kk.paste(keep.crop((0, 380, 760, 820)), (0, 380))   # 손은 화면 왼쪽 아래(y 380~820)만
    sq_fact = TB.screen_paste(sq_blurR, chart.filter(ImageFilter.GaussianBlur(1.2)), [(238, 104), (904, 104), (904, 1000), (238, 1000)], keep=kk)
    kwS = dict(TB.KW, top=TOPS)
    for nm, base, blur in (('sq1_b1.png', raw, 14), ('sq1_b2.png', sq_fact, 0)):
        im, g = TB.brighten(base.filter(ImageFilter.GaussianBlur(blur)) if blur else base, 112)
        out_to(S, nm, im, 0.2, **kwS); print('  감마', g, '· 최종 밝기 중앙값', final_luma(nm))

    # ── CC-1 (e2 문구) ──
    M.TOP = 'KODEX 미국배당커버드콜 vs TIGER 미국배당다우존스'; M.BIG = ['같은 1억, 배당 ETF 둘', '1년 뒤 누가 더 남았나?']
    raw = Image.open(os.path.join(M.H, 'p_6328948.jpg')).convert('RGB')
    C = calc('CC-1', 'cc1_calc'); import datetime as dt
    s0 = dt.date(2025, 11, 20)
    days = sorted(d for d in C.K_px if s0 <= d <= C.END and d in C.T_px)
    k = [C.K_px[d] / C.K_px[s0] for d in days]; t = [C.T_px[d] / C.T_px[s0] for d in days]
    assert (round(C.K_px[s0]), round(C.K_px[C.END]), round(C.T_px[s0]), round(C.T_px[C.END])) == (12605, 11170, 12615, 14505)   # cc1_calc_out_1122 시작가·끝가
    chart = screen([t, k], 1180, 520, [(245, 247, 250), (120, 190, 255)], [12, 12], bg=(14, 18, 26), pad=(0.05, 0.12, 0.05, 0.12))
    cc_fact = TB.screen_paste(raw, chart.filter(ImageFilter.GaussianBlur(0.8)), [(1532, 596), (1768, 680), (1740, 768), (1497, 684)])
    kwC = dict(TB.KW); kwC.pop('top', None)
    for nm, base, ya in (('cc1_b1.png', raw, 0.3), ('cc1_b2.png', cc_fact, 0.9)):
        im, g = TB.brighten(base, 112)
        out_to(M, nm, im, ya, **kwC); print('  감마', g, '· 최종 밝기 중앙값', final_luma(nm))
    for nm in ('SQ-1-thumb/sq1_c1b.png', 'CC-1-thumb/cc1_e2.png'): print(nm, '지금 판 밝기 중앙값', TB.luma(os.path.join(V, nm)))
