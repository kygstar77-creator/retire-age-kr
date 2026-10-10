# m1clip 4편 전체 영상 점검 — firemap-shorts 2026-10-10 19:29
렌더본 work/video/out/m1s_*.mp4 를 shortsdaily.whole_measure 로 잼(소리·빈 곳 3초 간격·가장 긴 멈춤). 기준: 평균 −50dB 이상 · 빈 곳 ≤40% · 멈춤 ≤5초.

| 편 | 영상 | 공개 | 소리(dB) | 빈 곳 최대 | 최장 멈춤 | 기계 몫 |
|---|---|---|---|---|---|---|
| m1s_need100 | fF_5yIxBnC8 | 10/10 19:20 공개 | −20.1 | 20.8% | 0초 | 통과 |
| m1s_minmonth | aYCWFSzynJI | 10/11 19:20 예약 | −20.5 | 21.0% | 0초 | 통과 |
| m1s_nhis70 | xmmkdtLhmXs | 10/12 19:20 예약 | −19.0 | 21.5% | 1초 | 통과 |
| m1s_total1y | gvOdoH5-HbM | 10/13 19:20 예약 | −21.0 | 21.4% | 0초 | 통과 |

- 전체 영상 점검: 통과 — 답하는 그림: m1s_need100 3초 판(work/video/out/m1s_need100_sheet.png, 18칸)을 눈으로 봄. 제목 '얼마 있어야 할까?'에 SCHD 4.85억원·JEPQ 1.38억원·ACE 5.10억원이 상품별로 하나씩 동그라미로 나오고, 끝에 막대 3개로 모아 답한다. 아래 자막 띠와 출처 줄까지 화면 아래가 차 있다.
- 비교: rate30_b(카드 쇼츠)는 같은 점검에서 5/5 미달(무음·빈 곳 80%·멈춤 8초)이었다. m1clip은 롱폼 목소리라 소리 문제가 없고, 장면이 계속 바뀐다.
- 남은 눈 점검: 예약 3편 판(work/video/out/m1s_{minmonth,nhis70,total1y}_sheet.png)은 공개 전 회차에 본다.
- 제목 숫자 점검(기계)은 cardshort spec 전용이라 m1clip spec(work/video/m1s_*.json)에 바로 못 씀 → 영상 PD와 m1clips_up.py 연결할 때 함께.
