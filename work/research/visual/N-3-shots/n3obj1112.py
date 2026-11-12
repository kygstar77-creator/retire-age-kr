"""N-3 판 몸통 사물 그림 — visual-designer 2026-11-12 (지시 quality-gap-1112 ②: 판의 50% 이상에 사물 그림, 자체 제작만).
지금 판(n3fit1110 등 결과)을 base로 한 번 떠 두고(video/public/bg/n3/board_base1112/, 없을 때만), 그 위에 그림 하나를 빈 자리에 붙인다.
빈 자리는 글자·선(잉크) 없는 가장 큰 정사각형을 자동으로 찾는다(여백 40px) — 글자를 덮지 않게.
판 이름·크기·글자·숫자 그대로(그림만 더함) → screen_text 재서명 없음. 검사: py -3.12 work/boardcheck.py n3
n3fit1110 등을 다시 돌렸으면 board_base1112를 지우고 이것을 다시 돌린다.
사용: py -3.12 n3obj1112.py [이름 ...]
"""
import os, sys, shutil
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'K-1-shots'))
import k1boards as K
from PIL import Image

D = os.path.join(K.WORK, 'video', 'public', 'bg', 'n3', 'board')
BASE = os.path.join(K.WORK, 'video', 'public', 'bg', 'n3', 'board_base1112')
# 판 이름 → 그림(판 문장의 '무엇'). 같은 그림은 한 편 4번까지(n3_seven 통장 포함).
PLAN = {   # 11/12 최종 — 상자 감지(boardcheck ⑥) 넘는 그림만(n3obj_try.py로 대 봄: 영수증·달력·고지서 일부는 안쪽 네모가 상자로 잡혀 뺌)
    'n3_4760': 'coins',        # 연봉 5,000 − 식대 240 = 4,760 (금액 크기)
    'n3_leak_q': 'coins',      # 무엇이 얼마나 빠질까 — 떼는 돈
    'n3_ladder_a': 'coins',    # 연봉 사다리 — 통장 한 달 금액 크기
    'n3_raise_top': 'coins',   # 1억 위로 오를 때 남는 몫
    'n3_8020': 'bankbook',     # 덜 떼기·그대로·더 떼기 — 통장 675·653·631
    'n3_back357': 'bankbook',  # 통장 한 달 357만원
    'n3_hook357': 'bankbook',  # 연봉 5천 → 통장에 한 달
    'n3_rev300': 'calculator', # 거꾸로 — 통장 300만원이 찍히려면 연봉은 (계산)
    'n3_rev_q': 'calculator',  # 거꾸로 계산
    'n3_top25_q': 'calculator',# 통장에 얼마? (계산)
    'n3_taxsteps': 'bill',     # 소득세율 계단 — 낼 세금
    'n3_three_money': 'flow',  # 계약서 연봉 → 총급여 → 통장(세 가지 돈의 순서) — 고지서는 기울기 따라 상자로 잡혀 뺌
    'n3_sameformula': 'calculator',  # 같은 계산식 — 흐름 화살표는 식 첫 항처럼 읽혀(11/12 심사) 계산기로, 왼쪽 아래
    'n3_nontax': 'scale',      # 식대 비과세 있음 vs 없음 비교
}
# 뺀 것: x18·why_q(빈 자리가 숫자·제목에 붙어 '저울 × 2'로 읽힘), ladder_c(계산기 3번 넘음)
# n3_seven은 n3fit1110에서 '통장 ?' 대신 통장 그림을 직접 그림(여기 없음)
PAD, SMIN, SMAX = 40, 200, 320
SPOT = {'n3_nontax': (960, 560, 220), 'n3_sameformula': (380, 800, 230)}   # 11/12 심사 뒤 손 자리: 저울은 357·352 사이, 계산기는 식과 떨어진 왼쪽 아래
PAD_ONE = {'n3_nontax': 75, 'n3_sameformula': 110}   # 11/12 새 심사관: 저울이 '352만원'에, 흐름이 식 첫 항에 붙어 읽힘 → 더 띄움


def ink_mask(im):
    a = np.asarray(im.convert('RGB')).astype(int)
    g = a.mean(axis=2)
    return (g < 190) | ((a[..., 0] - a[..., 2]) > 60)   # 검은·회색 글자·선, 주황


def find_spot(m, pad=None):
    """잉크 없는 정사각형(여백 PAD 포함) 중 가장 큰 것 — 위아래 가장자리(제목줄·출처줄) 빼고."""
    PAD = pad or globals()['PAD']
    Hh, Ww = m.shape
    ii = np.pad(m.astype(np.int32).cumsum(0).cumsum(1), ((1, 0), (1, 0)))
    def clear(x0, y0, x1, y1): return ii[y1, x1] - ii[y0, x1] - ii[y1, x0] + ii[y0, x0] == 0
    for s in range(SMAX, SMIN - 1, -10):
        best = None
        for cy in range(170 + s // 2 + PAD, 1000 - s // 2 - PAD, 10):
            for cx in range(60 + s // 2 + PAD, Ww - 60 - s // 2 - PAD, 10):
                x0, y0, x1, y1 = cx - s // 2 - PAD, cy - s // 2 - PAD, cx + s // 2 + PAD, cy + s // 2 + PAD
                if clear(x0, y0, x1, y1):
                    dc = abs(cy - 540) + 0.3 * abs(cx - 960)   # 가운데 띠에 가까운 곳
                    if best is None or dc < best[0]: best = (dc, cx, cy)
        if best: return best[1], best[2], s
    return None


def main(names):
    os.makedirs(BASE, exist_ok=True)
    for n in names or PLAN:
        src = os.path.join(D, n + '.png'); base = os.path.join(BASE, n + '.png')
        if not os.path.exists(base): shutil.copy(src, base)
        im = Image.open(base).convert('RGB')
        sp = SPOT.get(n) or find_spot(ink_mask(im), PAD_ONE.get(n))
        if not sp: print('자리 없음 — base로 되돌림', n); im.save(src); continue
        cx, cy, s = sp
        K.obj(im, PLAN[n], cx, cy, s, rot=3 if sum(map(ord, n)) % 2 else -3)  # hash()는 실행마다 달라 판이 바뀜
        im.save(src)
        print(f'{n}\t{PLAN[n]}\t({cx},{cy}) {s}px')


if __name__ == '__main__':
    main(sys.argv[1:])
