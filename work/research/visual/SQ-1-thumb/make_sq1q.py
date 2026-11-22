# SQ-1 2차 시안(visual 11/22) — make_sq1n.py p판 그대로, 문구만(youtube-loop 11/22 16:52 요청 · 이해 시험 ut1122):
#   ① 알약 '-28% → -14%' 3/3 못 읽음(무엇의 낙폭? 50세 '16억→12억 4억 손해'로 읽음) → 화살표 빼고 누구의 하락인지 이름 붙임
#   ② SCHD 글자 없음 3/3('반반이 무엇과 무엇') → 큰 글 둘째 줄에 SCHD
#   사실 ep/SQ-1/calc_krw_out_1120.txt 15년: 원화 끝값 0% 16.39억 · 50% 12.21억 · 원화 최대낙폭 0% -27.9% · 50% -13.6% (반올림 16억·12억·-28%·-14%)
#   q = 알약 youtube-loop 예시 그대로 '원화로 센 가장 큰 하락 · …' · r = 알약 짧게(168 대비)
import make_sq1 as S
TOP = '2011년에 1억원 넣었다면'
S.BIG = ['나스닥100만 16억', 'SCHD 반반 섞으면 12억']
assert sum(len(t.replace(' ', '')) for t in S.BIG) <= 24 and all(len(t.replace(' ', '')) <= 12 for t in S.BIG)
KW = dict(band=60, tshade=(420, 110), sw=15, tsw=9, blur=14, top=TOP)
if __name__ == '__main__':
    pass
    S.PILL = '원화로 센 가장 큰 하락 · 나스닥100만 -28% · 반반 -14%'
    S.make('sq1_q.png', 'chart_point_5833757.jpg', 0.2, pk=0.92, **KW)
    S.PILL = '가장 큰 하락 나스닥100만 -28% · 반반 -14%'
    S.make('sq1_r.png', 'chart_point_5833757.jpg', 0.2, pk=1.0, **KW)
    # s = q·r 짝 비교에서 p에 못 이김(둘째 줄 길어 SCHD 안 읽힘·168 과부하) → SCHD는 흰 줄로, 큰 글은 p 길이로
    S.BIG = ['나스닥100만 16억', '반반 섞으면 12억']
    S.PILL = '가장 큰 하락 나스닥100만 -28% · 반반 -14%'
    S.make('sq1_s.png', 'chart_point_5833757.jpg', 0.2, pk=0.92, **dict(KW, top='2011년 1억원, 나스닥100과 SCHD에 넣었다면'))
