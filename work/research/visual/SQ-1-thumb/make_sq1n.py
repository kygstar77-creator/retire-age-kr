# SQ-1 6차 판(visual 11/20) — make_sq1.py 그대로, 문구만 원화로(copywriter 11/19 18:54) + 두 가지 사실 고침:
#   흰 줄 '15년 전 1억원 넣었다면' → '2011년에 1억원 넣었다면'(editor A101 11/20: 'N년 전' 막힘, 계산 시작 2011-10)
#   큰 글 '16.4억'·'12.2억' → '16억'·'12억'(aitell A31 소수점 막힘 · calc_krw_out_1120 16.39억·12.21억 반올림)
#   알약 = 원화 최대 낙폭(calc_krw_out_1120 15년 0% -27.9% · 50% -13.6%) → '-28% → -14%'
#   o = 지금 꼴(sw13·덮개 170) · p = H-5 o1 테두리 꼴(benchmark 11/20 지시: 테두리 약 10px(1280 기준)·덮개 걷음·밝게)
import make_sq1 as S
S.BIG = ['나스닥100 16억', '반반 섞으면 12억']
S.PILL = '가장 크게 빠진 폭 -28% → -14%'
TOP = '2011년에 1억원 넣었다면'
if __name__ == '__main__':
    S.make('sq1_o.png', 'chart_point_5833757.jpg', 0.2, band=170, tshade=(380, 140), sw=13, tsw=8, blur=14, pk=0.92, top=TOP)
    S.make('sq1_p.png', 'chart_point_5833757.jpg', 0.2, band=60, tshade=(380, 90), sw=15, tsw=9, blur=14, pk=0.92, top=TOP)
