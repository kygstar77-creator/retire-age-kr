# H-5 교체 썸네일 (visual 2026-11-24 09시) — C-36 결론 숫자 빼기 · copywriter 08:11 요청 문구 그대로, make_h5.py make() 그대로
#   흰 줄 '송도 아파트 84㎡ · 국토부 실거래' / 큰 흰 '폭락이라던 송도' / 큰 주황 '84㎡ 지금은 고점의 몇 %?' · 알약 없음
#   '폭락' 말은 영상 0장 '검색창에 송도 집값을 치면 폭락이 먼저 따라 나온다'(떠도는 말 C-38) — 우리 주장 아님
import make_h5 as m
m.TOP = '송도 아파트 84㎡ · 국토부 실거래'; m.BIG = ['폭락이라던 송도', '84㎡ 지금은 고점의 몇 %?']; m.PILL = None
m.make('h5_n1.png', 'songdo_park_canal_18495181.jpg', 0.25, band=0, tshade=(380, 0), sw=15, tsw=9)    # o1 꼴(테두리 10px·덮개 0)
m.make('h5_n2.png', 'songdo_canal_dusk_37736994.jpg', 0.35, band=0, tshade=(380, 0), sw=15, tsw=9)    # 해 질 녘 운하
m.make('h5_n3.png', 'songdo_towers_918291.jpg', 0.3, band=0, tshade=(380, 0), sw=15, tsw=9)          # 고층 유리 건물
# 첫 판 둘째 줄 138px(첫 줄 246px)로 412에서 작음 → ① 둘째 줄 '84㎡' 빼기(흰 줄에 이미 84㎡) ② 폭 배분 바꾸기
m.BIG = ['폭락이라던 송도', '지금은 고점의 몇 %?']
m.make('h5_n4.png', 'songdo_canal_dusk_37736994.jpg', 0.35, band=0, tshade=(380, 0), sw=15, tsw=9, targets=(0.78, 0.90))
m.make('h5_n6.png', 'songdo_park_canal_18495181.jpg', 0.25, band=0, tshade=(380, 0), sw=15, tsw=9, targets=(0.78, 0.90))
m.BIG = ['폭락이라던 송도', '84㎡ 지금은 고점의 몇 %?']
m.make('h5_n5.png', 'songdo_canal_dusk_37736994.jpg', 0.35, band=0, tshade=(380, 0), sw=15, tsw=9, targets=(0.66, 0.95))
