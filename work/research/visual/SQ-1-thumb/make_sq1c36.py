# SQ-1 C-36 무숫자판 (visual 2026-11-24) — today.md youtube-loop 05:02 ② · s2 꼴(make_sq1q.py KW·사진 그대로), 답 숫자(16억·12억·-28%·-14%) 전부 뺌, 알약 없음
#   제목 1위 '나스닥100과 SCHD, 15년 전 1억 넣었다면 지금 얼마일까'와 통째 겹침 피함(C-26)
#   '나스닥100에만'은 11/22 이해 2차 168에서 '나스닥100만'→'100만 원' 오독(1/3) 때문에 '에만'
import make_sq1 as S
from make_sq1q import KW
S.PILL = None
TOP = '2011년 1억원 · 나스닥100과 SCHD'
def chk():
    assert sum(len(t.replace(' ', '')) for t in S.BIG) <= 24 and all(len(t.replace(' ', '')) <= 12 for t in S.BIG), S.BIG
S.BIG = ['나스닥100에만 넣었다면', '반반 섞었다면 얼마?']; chk()
S.make('sq1_c1.png', 'chart_point_5833757.jpg', 0.2, **dict(KW, top=TOP))
S.BIG = ['나스닥100에만 vs 반반', '15년 뒤 누가 더 남았나?']; chk()
S.make('sq1_c2.png', 'chart_point_5833757.jpg', 0.2, **dict(KW, top=TOP))
S.BIG = ['나스닥100에만 vs 반반', '더 크게 빠진 쪽은?']; chk()   # 영상 4장 낙폭 물음(남은 궁금증 '-28%는 언제')
S.make('sq1_c3.png', 'chart_point_5833757.jpg', 0.2, **dict(KW, top=TOP))
