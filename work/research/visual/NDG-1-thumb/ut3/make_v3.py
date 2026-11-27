# NDG-1 썸네일 다음 판(visual 11/27 09시) — copywriter 11/26 18:56 요청: 문구 ut2/make_copy_v2.py + 윗줄 '2021년부터 노도강 실거래 3만 8천 건',
#   사진 교체(6/6 '한강 다리라 노도강 같지 않음·회색이라 묻힘') → 다리·강 없는 주거지 + 뒤 바위산(북쪽 산 느낌), 밝게. 얼굴 없음(C-17).
#   사진 Pexels(https://www.pexels.com/license/) — photo/sources.json. 꼴 N-2 thumb_A(make_cc1.make), 공용 기본값 thumb_base.KW.
import os, sys, json, importlib
O = os.path.dirname(os.path.abspath(__file__)); P = os.path.dirname(O); sys.path.insert(0, P)
N = importlib.import_module('make_ndg1'); M = N.M; TB = N.TB
M.TOP = '2021년부터 노도강 실거래 3만 8천 건'
M.BIG = ['거래 끊겼다 vs 신고가', '어느 쪽이 맞았나?']
assert sum(len(t.replace(' ', '')) for t in M.BIG) in range(16, 25) and all(len(t.replace(' ', '')) <= 12 for t in M.BIG)
sc = open(os.path.join(P, '..', '..', 'longform', 'ep', 'NDG-1', 'script.md'), encoding='utf-8').read()
assert '38,022' in sc and '2021' in sc, '3만 8천 건·2021년 근거 없음'
N.PH['13045678'] = ('seoul_rock_mountain_13045678.jpg', '바위 능선 아래 빽빽한 주거지(아파트·빌라), 맑은 날 · 다리·강 없음', None)
N.PH['34746850'] = ('seoul_skyline_mountain_34746850.jpg', '바위 봉우리 산줄기 아래 시가지 · 다리·강 없음', None)
kw = dict(TB.KW); kw.pop('top', None); out = []
for name, pid, ya in (('ndg1_d.png', '13045678', 0.12),):  # e(34746850)는 하늘이 너무 넓어 11/27 버림
    tmp, g = N.prep(pid, ya); M.O = O; M.make(name, tmp, ya, **kw); os.remove(os.path.join(M.H, tmp))
    out.append(dict(file=name, photo=pid, page=f'https://www.pexels.com/photo/{pid}/', desc=N.PH[pid][1], gamma=g, luma=round(TB.luma(os.path.join(O, name)), 1)))
    print(name, g, out[-1]['luma'])
json.dump(dict(top=M.TOP, big=M.BIG, license='https://www.pexels.com/license/', items=out), open(os.path.join(O, 'credits.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
