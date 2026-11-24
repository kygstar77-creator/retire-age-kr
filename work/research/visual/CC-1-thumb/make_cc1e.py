# CC-1 cc1_e (visual 2026-11-24 17시) — copywriter 08:11 [요청]·C-36(결론 숫자 금지): make_cc1.py 꼴 그대로, 문구만 바꿈. 트랙:C
#   흰 줄 'KODEX 미국배당커버드콜 vs TIGER 미국배당다우존스' · 큰 흰 '같은 1억, 배당 ETF 둘' · 큰 주황 '1년 뒤 누가 더 남았나?' · 알약 없음 · 답 숫자 0
#   e = a판 사진(p_4475469 어두운 탁자 달러 세는 손) · e2 = c판 사진(p_6328948) — 짝 비교용
import make_cc1 as M
M.TOP = 'KODEX 미국배당커버드콜 vs TIGER 미국배당다우존스'
M.BIG = ['같은 1억, 배당 ETF 둘', '1년 뒤 누가 더 남았나?']
assert sum(len(t.replace(' ', '')) for t in M.BIG) in range(16, 25) and all(len(t.replace(' ', '')) <= 12 for t in M.BIG)
assert not any(ch.isdigit() for ch in ''.join(M.BIG).replace('1억', '').replace('1년', ''))   # 답 숫자 없음(조건 '1억·1년'만)
kw = dict(band=190, tshade=(330, 160), sw=13, tsw=8)
M.make('cc1_e.png', 'p_4475469.jpg', 0.25, **kw)
M.make('cc1_e2.png', 'p_6328948.jpg', 0.3, **kw)
