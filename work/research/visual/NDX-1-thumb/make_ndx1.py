# NDX-1(12/4 공개, 관문 12/3 11:30) 썸네일 시안 — visual 2026-11-27 17시. 꼴 = N-2 thumb_A(꽉 찬 실사·흰 줄·큰 글 두 줄 아래 40~45%·주황 둘째 줄),
#   공용 기본값 thumb_base.KW + brighten(밝기 중앙값 90 목표 — NDG-1 회색 교훈).
#   문구 = copywriter 11/27 07:57 [요청](research/copy/ndx1/titles.md): 흰 '나스닥100 · 1986년부터 일별 종가' /
#   큰 흰 '고점에 물렸던 하락 35번' · 주황 '며칠 만에 풀렸나?'(합 19자, 답 숫자 0 — C-36 남은 질문). 알약 없음.
#   사진 Pexels(라이선스 https://www.pexels.com/license/) — photo/sources.json·credits.json. 얼굴 0(뒷모습·손), 화면 글자는 남의 앱 UI라 흐림 대상 없음(차트만).
import os, sys, json, importlib
from PIL import Image, ImageFilter
sys.stdout.reconfigure(encoding='utf-8')
O = os.path.dirname(os.path.abspath(__file__)); V = os.path.dirname(O); RES = os.path.dirname(V); sys.path.insert(0, V)
import thumb_base as TB
sys.path.insert(0, os.path.join(V, 'CC-1-thumb')); M = importlib.import_module('make_cc1'); sys.path.pop(0)
M.H = os.path.join(O, 'photo'); M.O = O; M.PILL = None
M.TOP = '나스닥100 · 1986년부터 일별 종가'
M.BIG = ['고점에 물렸던 하락 35번', '며칠 만에 풀렸나?']
assert sum(len(t.replace(' ', '')) for t in M.BIG) in range(16, 25) and all(len(t.replace(' ', '')) <= 12 for t in M.BIG)
fx = open(os.path.join(RES, 'longform', 'ep', 'NDX-1', 'facts.txt'), encoding='utf-8').read()
assert '1986~2026 35번' in fx and '1986-01-02' in fx, '35번·1986년 근거(facts.txt) 없음'

PH = {  # 이름: (설명, ya, Pexels id)
    'ndx_hands_wait': ('흰 책상, 차트 띄운 노트북 앞에 깍지 낀 손(기다림)', 0.55, 6801647),
    'ndx_hands_lens': ('노트북 차트 앞 깍지 낀 손·돋보기', 0.35, 7691749),
}

B2 = sys.argv[1:] == ['b2']  # 11/27 18:52 copywriter [요청] b 사진 그대로 글자만(c39/result.md 이해 1차 고침)
if B2:
    M.TOP = '나스닥100 · 1986년부터 40년'  # facts.txt 1986-01-02~2026-11 (40.9년) — '일별 종가' 뺌
    M.BIG = ['고점에 물렸던 하락 35번', '언제 본전 됐나?']
    assert sum(len(t.replace(' ', '')) for t in M.BIG) in range(16, 25) and all(len(t.replace(' ', '')) <= 12 for t in M.BIG)
    PH = {k: v for k, v in PH.items() if k == 'ndx_hands_wait'}

B3 = sys.argv[1:] == ['b3']  # 11/28 07:52 copywriter [요청] b2 사진·큰 글 그대로, 흰 줄만 박힌 날짜 시험
if B3:
    # 요청 문구 '11월 20일 고점보다 −19.8%'는 11/20을 고점으로 읽힘 — 사실(facts.txt 6행)은 '11/20 종가가 그때까지 고점보다 −19.8%' → 쉼표로 끊음
    M.TOP = '나스닥100 · 11월 20일, 고점보다 −19.8%'
    M.BIG = ['고점에 물렸던 하락 35번', '언제 본전 됐나?']
    assert '2026-11-20 25,028.98(−19.8%' in fx, '−19.8% 근거(facts.txt) 없음'
    PH = {k: v for k, v in PH.items() if k == 'ndx_hands_wait'}

if __name__ == '__main__':
    kw = dict(TB.KW); kw.pop('top', None); out = []
    for name, (key, (desc, ya, pid)) in zip(('ndx1_b3.png',) if B3 else ('ndx1_b2.png',) if B2 else ('ndx1_b.png', 'ndx1_c.png'), PH.items()):
        raw = Image.open(os.path.join(M.H, key + '.jpg')).convert('RGB')
        # 11/27 ndx_back_chart(7567522) 뺌 — 화면이 코인 거래소(CAKE/USDT)라 나스닥과 안 맞고, 흐림 상자가 머리를 가름
        im, g = TB.brighten(raw, 100); tmp = f'_tmp_{key}.jpg'; im.save(os.path.join(M.H, tmp), quality=95)
        M.make(name, tmp, ya, **kw); os.remove(os.path.join(M.H, tmp))
        out.append(dict(file=name, photo=pid, page=f'https://www.pexels.com/photo/{pid}/', desc=desc, gamma=g, luma=round(TB.luma(os.path.join(O, name)), 1)))
        print(name, '감마', g, '밝기 중앙값', out[-1]['luma'])
    json.dump(dict(top=M.TOP, big=M.BIG, license='https://www.pexels.com/license/', items=out), open(os.path.join(O, 'credits_b3.json' if B3 else 'credits_b2.json' if B2 else 'credits.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
