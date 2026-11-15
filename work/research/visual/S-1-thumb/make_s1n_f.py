# S-1 f(visual 11/15 09시) — copywriter 07:52 요청: e3 168px 오른쪽 아래 반이 검음 → 내려가는 봉 차트를 화면 가로 2/3까지 채움.
#   e3와 사진·문구·글자 자리·색·테두리·덮개 같음, 사진 확대(zoom)와 자르는 자리만 바꿈. 상자·띠 없음.
import runpy, sys
sys.argv = ['x']
g = runpy.run_path('make_s1n.py', run_name='lib')  # make_s1n.py 끝의 make(...) 호출이 다시 돌아 기존 판을 같은 값으로 다시 씀(내용 같음)
make = g['make']
T = '삼성전자 주가|2017년부터 실적 발표 날'
# f: 봉 구간(원본 가로 0~40%)이 화면 2/3 — 확대 1.67, 왼쪽 끝, 위 봉 보이게
make('s1n_f.png', 'candle_down_35118208_kr.jpg', 0.18, T, top_sizes=[150, 84], sw=15, band=200, tshade=0, target=0.86, xa=0.0, zoom=1.67)
# f2: 확대 1.45(봉이 조금 작고 화면 60%쯤)
make('s1n_f2.png', 'candle_down_35118208_kr.jpg', 0.15, T, top_sizes=[150, 84], sw=15, band=200, tshade=0, target=0.86, xa=0.0, zoom=1.45)
