# silson24clm1114 직접 계산 — 원자료 raw/fsc_87818_pdf.txt(금융위 2026-09-30 보도자료, 9/28 기준) · raw/fsc_86854.txt(2026-05-11 보도자료, 5/6 기준)
import datetime as D
ALL, DONE, EXP = 105643, 50340, 101550           # 9/28 전체·연계 완료·연계 예상
S1_ALL, S1_DONE, S2_ALL, S2_DONE = 7810, 4685, 97833, 45655
H9, B9, C9, P9 = 1107, 3578, 24995, 20608          # 9/28 병원·보건소·의원·약국
H5, B5, C5, P5 = 827, 3573, 12875, 13339           # 5/6
DONE5 = H5 + B5 + C5 + P5; assert DONE5 == 30614; print("9/28 병원+보건소+의원+약국 합 %d · 표 합계 %d · 차이 %d(원문 그대로, 의원·약국 칸 합 45,603 vs 2단계 45,655)" % (H9 + B9 + C9 + P9, DONE, DONE - (H9 + B9 + C9 + P9)))
d0, d1, end = D.date(2026, 5, 6), D.date(2026, 9, 28), D.date(2026, 12, 31)
n = (d1 - d0).days; left = (end - d1).days
print('연계율 %.1f%% · 100곳 중 %.0f곳' % (DONE / ALL * 100, DONE / ALL * 100))
print('1단계 %.1f%% · 2단계 %.1f%%' % (S1_DONE / S1_ALL * 100, S2_DONE / S2_ALL * 100))
print('5/6→9/28 %d일 · 늘어난 곳 %d · 하루 평균 %.1f곳' % (n, DONE - DONE5, (DONE - DONE5) / n))
print('의원 %d→%d (%.2f배, +%d) · 약국 %d→%d (+%d) · 병원 +%d · 보건소 +%d' % (C5, C9, C9 / C5, C9 - C5, P5, P9, P9 - P5, H9 - H5, B9 - B5))
print('의원·약국 늘어난 몫 %.1f%%' % ((C9 - C5 + P9 - P5) / (DONE - DONE5) * 100))
for tg in (0.8, 0.9):
    need = tg * ALL - DONE
    print('목표 %d%%: %.0f곳 · 더 필요 %.0f곳 · 9/28→12/31 %d일 · 하루 %.1f곳 · 지금까지 속도의 %.2f배' % (tg * 100, tg * ALL, need, left, need / left, need / left / ((DONE - DONE5) / n)))
pace = (DONE - DONE5) / n
print('지금 속도로 12/31 연계 %.0f곳 → %.1f%%' % (DONE + pace * left, (DONE + pace * left) / ALL * 100))
print('지금 속도로 80%% 닿는 날: %s' % (d1 + D.timedelta(days=(0.8 * ALL - DONE) / pace)))
print('연계 예상인데 아직 안 된 곳 %d (%.1f%%)' % (EXP - DONE, (EXP - DONE) / ALL * 100))
print('2단계 연계 예상 96,685 − 완료 45,655 = %d' % (96685 - 45655))
SUB, INS = 5210000, 40350000
print('실손24 가입자 521만 / 피보험자 4,035만 = %.1f%% · %.1f명 중 1명' % (SUB / INS * 100, INS / SUB))
SUB5 = 3770000
print('가입자 5/6 377만 → 9/28 521만: +144만, %.0f%% 증가' % ((SUB / SUB5 - 1) * 100))
print('청구 461만건 / 가입자 521만 = %.2f건' % (4610000 / SUB))
