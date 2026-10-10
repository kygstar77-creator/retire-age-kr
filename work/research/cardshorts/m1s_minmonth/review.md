# m1s_minmonth review — firemap-video-producer 2026-10-10 (예약 10/11 19:20 칸)
- 편: M-1 롱폼(https://youtu.be/eTjVs1vDTwg) 4장 '가장 적게 나온 달로 다시 재면'을 자른 세로 쇼츠 49.4초. 질문 '월배당, 가장 적게 나온 달로 다시 재면 얼마?' → 답 ACE 5.10억원 → 8.92억원(×1.75) · JEPQ 1.38억원 → 1.71억원(×1.23) → 결론 '평균 말고 가장 적은 달을 먼저'.
- 목소리: ep/M-1/voice.json 줄 60·61·52·53·54·55·56·57·58·59·60·62 wav 그대로(새 녹음 없음). 첫 3초 = 줄 60 '가장 적은 달 기준으로 다시 재면, 거의 9억이 필요합니다'(이 구간에서 가장 센 말, 끝에서 한 번 더 나옴).
- 화면: work/video/src/M1S.tsx(1080×1920) · props work/video/m1s_minmonth.json(research/cardshorts/m1clips.py가 voice.json·m1.json에서 만듦) · 렌더 out/m1s_minmonth.mp4 → deess.py → out/m1s_minmonth_ds.mp4(쉿소리 -14.0dB, 기준 -12 이하).

## 관문
| 관문 | 결과 | 근거 |
|---|---|---|
| 숫자 대조(facts.txt·calc_out.txt) | 통과 — 화면·자막·칩·제목·설명 숫자 142개, 원문에 없는 숫자 0 | `py -3.12 work/research/cardshorts/m1clips_check.py m1s_minmonth` |
| 치직 | 0개 | `py -3.12 work/video/clickscan.py scan work/video/out/m1s_minmonth_ds.mp4` → 치직 0개 (의심 자리 없음 → 받아쓰기 안 함) |
| 제목·설명 | 질문형 + #shorts, 설명 첫 줄 롱폼 링크, AI 티 5.9(기준 12) | upload.json |

## 눈 검사 — sheet.png(ffmpeg fps=1/3, tile 6×3, Read로 봄)
1. 소리 있음: 통과 — 오디오 AAC 스트림, 평균 -20.6dB · 최대 음량 measure.json.
2. 빈 곳 40% 이하: 통과 — 3초 간격 17장 평균 31.8% · 가장 빈 장 35.6% · 아래 절반 평균 30.1% · 최대 37.2% (emptyscan.py 60px 칸, 바탕·흰 판·회색 칩의 무늬 없는 칸을 빈 곳으로 셈).
3. 제목 숫자가 화면에 나옴: 통과 — '5.10억원'·'8.92억원'이 0초 첫 장면(막대 두 개)과 45초(아래 '월 100만원에 필요한 돈' 칸)·48초(평균/가장 적은 달 막대)에 보임.
4. 질문에 답하는 그림: 통과 — 5.10억→8.92억 막대, JEPQ·ACE 12달 막대(최소·최대 표시, 최대÷최소 1.51배·2.52배), 평균/가장 적은 달 묶음 막대.
5. 5초 넘는 정지 없음: 통과 — 1초 간격 비교 최장 정지 0초. 3초 판마다 자막 문장이나 새 표시(최소·최대 꼬리표, 배수 칩, 필요한 돈 칸)가 바뀜.

판정: 통과
