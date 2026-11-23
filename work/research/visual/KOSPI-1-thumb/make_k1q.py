# KOSPI-1 k1_q (copywriter 2026-11-24 — C-36 결론 숫자 금지·C-38 떠도는 말/조건으로 열기). 사진·꼴은 k1_d3 그대로(손 사진, 화면 흐림), 알약은 뺌(답 숫자 없음).
import os, sys, inspect
sys.stdout.reconfigure(encoding='utf-8')
O = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, O)
import make_kospi1 as M
src = inspect.getsource(M.make)
src = chr(10).join(l for l in src.split(chr(10)) if 'rounded_rectangle' not in l and 'PILL, font=pf, fill=WHITE' not in l)   # 알약 그리기 두 줄만 빼기
exec(compile(src, 'make_nopill', 'exec'), M.__dict__)
VARS = {
    'k1_qa.png': ('1995년부터 매일 마감 가격으로 셈', ['코스피 5% 넘게 빠진 날', '그 뒤 1년은 어땠을까?']),
    'k1_qb.png': ('코스피 하루 5% 넘게 빠진 날 · 31년 기록', ['이만큼 빠졌으면', '더는 안 떨어질까?']),
}
PIC = {'k1_qc.png': ('candle_down_35118208.jpg', 0.15, 150), 'k1_qd.png': ('frustrated_monitors_5831256.jpg', 0.25, 170)}   # 55세 '눈에 걸리는 게 없다'(qa 6장 중 5위) → 차트·모니터 사진 시험
VARS['k1_qc.png'] = VARS['k1_qa.png']; VARS['k1_qd.png'] = VARS['k1_qa.png']
# 레드팀: 제목 '…그 뒤 1년은 어땠을까?'와 큰 글이 통째 겹침(C-26) → 큰 둘째 줄을 대본 3장 첫 물음으로
VARS['k1_qe.png'] = ('1995년부터 매일 마감 가격으로 셈', ['코스피 5% 넘게 빠진 날', '그다음엔 더 떨어졌을까?']); PIC['k1_qe.png'] = PIC['k1_qc.png']
for out, (top, big) in VARS.items():
    M.TOP = top; M.BIG = big
    pic, ya, band = PIC.get(out, ('hands_phone_blur_d3.jpg', 0.2, 190))
    M.make(out, pic, ya, band=band, tshade=(400, 160), sw=13, tsw=8)
