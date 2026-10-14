# c2s_jungwoo review — firemap-video-producer 2026-10-14 15:19 (쇼츠 비축분, 1순위 10/19 19:20 — C-2 롱폼 10/19 11:30 공개 뒤)
- 편: C-2 롱폼(정우 씨, 1998년 1월 3억·월 200만원 팔아 쓰기 → 2011년 1월 바닥) 이야기 줄기를 자른 세로 쇼츠 55.0초(1,650프레임, 파일 55.06초). 틀 c2person(motion 10/14 12:13, 부품 video/src/C2P.tsx). 질문 '3억, 매달 200만원 / 언제 바닥났을까'.
- 이번에 고친 것: motion 렌더 58.3초 → '68살' 장면(3.3초) 빼고 55.0초(쇼츠 45~55초 규칙) → 다시 렌더(c2pclip.py 주석). 나머지 10장면·그림·숫자 그대로.
- 목소리: ep/C-2 voice.json(Chirp 3 HD Charon, 10/14) wav 그대로, 새 녹음 0.
- 첫 3초: "퇴직금 3억을 미국 대형주 지수에 넣었어요."(숫자 있음, 접속사 아님, 35자 이하) + 0초 질문 '3억, 매달 200만원 / 언제 바닥났을까'.

## 관문
| 관문 | 결과 | 근거 |
|---|---|---|
| 경쟁 조사 | 통과 — 쇼츠 5편(30일 안) · 잘된 이유 3 · 우리만 다른 것(실제 지수·환율 순서로 한 사람의 14년) · 첫 3초 | compete.md(14:38) |
| 숫자 대조 | 통과 — 제목·설명 포함 숫자 전부 원문(calc_n1_out·video/c2.json) 안, 못 찾음 0 | w1g1clips_check.py c2s_jungwoo (이번에 C-2 원문 연결: c2.json·calc_n1_out) |
| 꼴 관문 ⓐ~ⓓ | 통과 — ⓓ layout c2person(최근 10편 c1clip 7편과 다른 틀) | w1g1clips_check.py --form |
| 같은 화면 | 장면 최장 7.4초(8초 이하) · motion 잼 같은 화면 최장 3.5초 | c2pclip.py assert |
| 치직 | 파일 1개 · 치직 0개 | video/clickscan.py |
| 쉿소리 | 렌더 −10.6dB → 디에서(--chirp-short) 뒤 쉿소리 틀 0 | video/deess.py → out/c2s_jungwoo_ds.mp4 |
| 빈 곳 | 평균 0% · 최대 2% (기준 40% 이하) | emptyscan.py |
| 영상 규격 | 55.06초 · 1080×1920 · yuv420p · 30fps · 디코드 오류 0 | ffmpeg |
| 제목 | 'S&P500에 퇴직금 3억, 14년 만에 바닥난 이유' 27자·숫자 2(3억·14년) · 제미나이(3.1-flash-lite, 3.8-flash 429) B 8 · 레드팀(PD) B2 8 → 평균 8.0. C(9) '5년 늦게 시작한 사람만 살아남았다'는 37번 중 바닥 6번이라 '만'이 과장 → 버림 | title_gemini.json · upload.json |
| AI 티 | 제목 0.0 · 설명 6.0(기준 12) | aitell.gate_text |
| 대본·화면 심사 | motion 10/14 2차 제미나이 9·Claude 7·레드팀 7 = 7.67(틀림 0) | ep/C-2/motion_preview/review_c2s.md |

## 눈 검사 — sheet.png(3.5초 간격 16장)·frame0.png
잘림·겹침·숫자 오타 0. 위 질문 칸·'가상 인물' 배지·아래 출처 줄 끝까지 그대로. 0초 자막은 서서히 나타남(숫자 카드 '3억'은 0.3초 뒤) — 위 질문에 3억·200만원이 0초부터 있음.

## 올리기 전 조건(업로드는 아직 안 함)
1. C-2 롱폼이 관문을 넘고 videoId가 나와야 한다(설명 첫 줄 {LONG}·upload.json from_long). C-2 화면 글자 editor 서명(10/15 18:00)에서 숫자가 바뀌면 c2pclip.py·w1g1clips_check 다시.
2. 공개 시각은 C-2 공개(10/19 11:30) 뒤 — 1순위 10/19 19:20(같은 날 07:20 p1s_cross = P-1, 다른 롱폼·다른 질문).
3. 업로드: w1g1clips_up.py c2s_jungwoo(log.jsonl layout 'c2person').

판정: 통과
