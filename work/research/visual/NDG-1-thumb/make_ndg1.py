# NDG-1(12/2 공개) 썸네일 시안 — visual 2026-11-26 17시. 꼴 = N-2 thumb_A(꽉 찬 실사·흰 줄·큰 글 두 줄 아래 40~45%·주황 둘째 줄),
#   공용 기본값 thumb_base.KW(테두리 1280 약 10px·덮개 60)+brighten(밝기 중앙값 90 목표) — backlog ①(11/26 benchmark 지시).
#   문구 = copywriter 11/25 07:55 C-36 1위(research/copy/ndg1/titles.md): 흰 '노도강 아파트 · 국토부 실거래 3만 8천 건' /
#   큰 흰 '같은 주 정반대 뉴스' · 주황 '어느 쪽이 맞았나?'(합 16자, 결론 숫자 0 — C-36). 알약 없음.
#   사진 Pexels(라이선스 https://www.pexels.com/license/) — credits.json. 사람 얼굴 0, 단지 이름 글자는 흐림.
import os, sys, json, importlib
from PIL import Image, ImageDraw, ImageFilter
sys.stdout.reconfigure(encoding='utf-8')
O = os.path.dirname(os.path.abspath(__file__)); V = os.path.dirname(O); RES = os.path.dirname(V); sys.path.insert(0, V)
import thumb_base as TB
sys.path.insert(0, os.path.join(V, 'CC-1-thumb')); M = importlib.import_module('make_cc1'); sys.path.pop(0)
M.H = os.path.join(O, 'photo'); M.O = O; M.PILL = None
M.TOP = '노도강 아파트 · 국토부 실거래 3만 8천 건'
M.BIG = ['같은 주 정반대 뉴스', '어느 쪽이 맞았나?']
assert sum(len(t.replace(' ', '')) for t in M.BIG) in range(16, 25) and all(len(t.replace(' ', '')) <= 12 for t in M.BIG)
sc = open(os.path.join(RES, 'longform', 'ep', 'NDG-1', 'script.md'), encoding='utf-8').read()
assert '38,022' in sc, '3만 8천 건 근거(대본 26행 38,022건) 없음'

PH = {  # id: (파일, 설명, 흐릴 곳 box 1920 기준 또는 None)
    '31728574': ('seoul_apartment_buildings_2_31728574.jpg', '강 건너 아파트 단지와 뒤 바위산(북쪽 산 느낌) · 다리', None),
    '19848427': ('seoul_apartment_buildings_5_19848427.jpg', '산 위에서 본 안개 낀 아파트 단지들', None),
    '41136598': ('서울_아파트_단지_5_41136598.jpg', '아래에서 올려다본 고층 아파트 두 동·은행나무', 'brand'),
}
CRED = {'31728574': 'https://www.pexels.com/photo/31728574/', '19848427': 'https://www.pexels.com/photo/district-of-modern-residential-skyscrapers-19848427/',
        '41136598': 'https://www.pexels.com/ko-kr/photo/41136598/'}


def prep(pid, ya, xa=0.5, zoom=1.0):
    fn, _, blur = PH[pid]; raw = Image.open(os.path.join(M.H, fn)).convert('RGB')
    if blur == 'brand':   # 왼쪽 동 옆면 단지 이름 글자 흐림(상표·단지명 C-19)
        r = raw.width / 480; box = tuple(int(v * r) for v in (60, 90, 120, 200))
        raw.paste(raw.crop(box).filter(ImageFilter.GaussianBlur(int(18 * r / 4))), box[:2])
    im, g = TB.brighten(raw, 100); tmp = f'_tmp_{pid}.jpg'; im.save(os.path.join(M.H, tmp), quality=95); return tmp, g


if __name__ == '__main__':
    kw = dict(TB.KW); kw.pop('top', None); out = []
    for name, pid, ya in (('ndg1_a.png', '31728574', 0.35), ('ndg1_b.png', '19848427', 0.25), ('ndg1_c.png', '41136598', 0.2)):
        tmp, g = prep(pid, ya); M.make(name, tmp, ya, **kw); os.remove(os.path.join(M.H, tmp))
        out.append(dict(file=name, photo=pid, page=CRED[pid], desc=PH[pid][1], gamma=g, luma=round(TB.luma(os.path.join(O, name)), 1)))
        print(name, '감마', g, '밝기 중앙값', out[-1]['luma'])
    json.dump(dict(top=M.TOP, big=M.BIG, license='https://www.pexels.com/license/', items=out), open(os.path.join(O, 'credits.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
