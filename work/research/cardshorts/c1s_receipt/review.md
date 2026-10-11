# c1s_receipt review — firemap-video-producer 2026-10-11 (예약 10/14 07:20 칸)
- 편: C-1 롱폼(https://youtu.be/DBJaHJ2pVTw) 3·4장 '첫해 영수증'을 자른 세로 쇼츠 48.4초. 질문 '배당으로 받으면 첫해 얼마 빠질까?' → 답 배당 씨 7,223,493원 · 매도 씨 0원 → 이유 금융소득 1,000만원 문턱·양도소득은 건보료 목록에 없음.
- 목소리: ep/C-1/voice.json(Chirp 3 HD Charon) wav 그대로, 새 녹음 없음. c1.json 줄 [76, 23, 24, 25, 26, 27, 30, 31, 32, 33].
- 첫 3초: 줄 76 "같은 지수라도 배당으로 받으면 미국 세금에 지역 건보료까지 붙어서, 첫해에만 7백만원 넘게 더 빠졌어요." + 0초 판(배당 씨 한 달 영수증, '첫해 더 빠진 돈 7,223,493' 다 찍힌 상태)·답 칸 '배당 씨 7,223,493원 · 매도 씨 0원'.
- 화면: work/video/src/C1S.tsx(1080×1920, M1S v2 틀) · props work/video/c1s_receipt.json(research/cardshorts/c1clips.py가 video/c1.json에서 만듦) · 렌더 `npx remotion render src/c1s_index.ts C1S out/c1s_receipt.mp4 --props=c1s_receipt.json --pixel-format=yuv420p` → `deess.py --chirp` → out/c1s_receipt_ds.mp4.
- 제목: 배당으로 생활비 받으면 첫해 얼마 빠질까? 세금·건보료 7,223,493원 #shorts · 예약 2026-10-14T07:20:00+09:00
- 같은 날 다른 편: 10/14 19:20 칸은 아직 편 없음(TBD) — 그 칸을 채울 때 이 제목과 유사도 0.6 미만·다른 롱폼으로. 10/12 19:20 m1s_nhis70(건보료)과는 다른 날로 뗌(주제 겹침 피함).
- 제미나이 심사 한도: 오늘 flash 계열 429 → 받아쓰기는 flash-lite로 함, 별도 제미나이 심사 없음(관문은 아래 기계 관문·눈 검사).

## 관문
| 관문 | 결과 | 근거 |
|---|---|---|
| 경쟁 조사 | 통과 — compete.md 쇼츠 5개 이상(30일 안) · 잘된 이유 3 · 우리만 다른 것 · 첫 3초 문장 | cardshorts/c1s_receipt/compete.md |
| 숫자 대조 | 통과 — 화면·자막·답 칸·제목·설명 숫자 100개, 원문에 없는 숫자 0개 (원문 = ep/C-1/facts.txt · calc_out.txt · video/c1.json 편집 통과 화면 글자) | `py -3.12 work/research/cardshorts/c1clips_check.py c1s_receipt` |
| 치직 | 파일 1개 · 치직 0개 | `py -3.12 work/video/clickscan.py scan work/video/out/c1s_receipt_ds.mp4` |
| 쉿소리 | 통과 — c1s_receipt.mp4 voiced 1238 sib 31 sib_vs_voiced_db -10.2 / c1s_receipt_ds.mp4 voiced 1244 sib 2 sib_vs_voiced_db -12.0 (앞 = 렌더 그대로, 뒤 = 디에서). 기준 -12dB 이하. 처음 --chirp(C-1 롱폼 설정)로는 c1s_receipt -11.3dB라 못 넘음 → 클립용 --chirp-short(i=0.8, 2~4kHz -0.8dB만)로 네 편 모두. 디에서 뒤 쉿소리 틀이 10개 밑이라 deess.measure()는 None → 같은 식을 틀 수 제한 없이 잰 값. 한 편 틀 수가 1~9개뿐이라, 네 편 소리를 이어 붙여 같은 식으로 다시 잼: 렌더 -10.8dB(쉿소리 틀 171) → 디에서 -12.0dB(틀 8) | `deess.py --chirp-short` · research/cardshorts/c1clips_sib.py |
| 받아쓰기 | 줄 10개 중 10개 0.85 이상 · 낮은 줄: 없음 — 씨/시·매/메 같은 소리 차이뿐, 숫자는 다 맞음 → 통과 | `m1clips_hear.py`(gemini-3.1-flash-lite, flash 계열 429) · cardshorts/c1s_hear_1011.txt |
| 0초 프레임 | 통과 — frame0.png: 판·답 칸·위 질문이 0프레임부터 다 그려짐(첫 장면 full=움직임 끝난 시점부터) | frame0.png를 Read로 봄 |
| 0~3초 답 숫자 | 통과 — 아래 답 칸(0초부터 끝까지)에 답 숫자, 첫 말이 답 문장 | 위 '첫 3초' |
| 자막 | 10~16자 조각, 말 길이 비례로 약 2초마다 바뀜(M1S v2와 같은 chunks), 숫자 노랑 | C1S.tsx Caption |
| 장면 | 장면 5개(평균 9.7초, [7.4, 14.4, 10.4, 8.6, 7.6]초) + 장면 안 컷(약 2.5초마다 판 4.5% 당겼다 놓음)·줄마다 새 표시 — '장면 약 2초마다'는 컷 기준으로만 맞춤, 그림 자체가 2초마다 바뀌지는 않음 | C1S.tsx Frame |
| '설명란 링크' 문구 | 없음 — 화면·말·설명 모두. 설명 첫 줄은 '전체 계산: https://youtu.be/DBJaHJ2pVTw' 한 줄뿐(클릭 유도 말 없음) | upload.json |
| 영상 규격 | Duration: 00:00:48.49, start: 0.000000, bitrate: 793 kb/s · h264 (High) (avc1 / 0x31637661), yuv420p(progressive), 1080x | measure.json |

## 눈 검사 — sheet.png(fps=1/3, tile 6×3)와 대표 프레임 6장(eye/contact_*.png, 원본 eye/*.png)을 Read로 봄
1. 소리 있음: 통과 — AAC, 평균 -23.2 dB · 최대 -3.6 dB.
2. 빈 곳: 3초 간격 평균 33.2% · 가장 빈 장 42.0% · 아래 절반 평균 33.6% (emptyscan.py).
3. 5초 넘는 정지: 1초 간격 최장 정지 0초.
4. 대표 프레임(0·9.5·15·20·30·43초): 0초 배당 씨 아이콘·'가상 인물·계산용' 도장·한 달 영수증(월 2,000,000·월 211,664·연 4,683,524·7,223,493)·'매도 씨는 0원' 도장 다 보임 / 9.5초 첫해 영수증 한 줄씩 찍힘(31,223,493) / 15초 −4,683,524 / 20초 영수증 4줄 + '월 211,664원 · 건보료 다음 해 11월 고지서부터' / 30초 금융소득 문턱 자(1천만원 선, 배당 씨 분배 31,223,493원) / 43초 보험료 소득 목록 7줄(양도소득 '목록에 없음') + '건보료 0원'. 잘림·겹침 없음, 출처는 설명란(화면 출처 줄 없음 = M1S v2와 같음), 숫자 오타 없음(숫자 대조와 같음).
5. 질문에 답하는 그림: 영수증(배당 씨·매도 씨 나란히), 문턱 자, 소득 목록.
- 사물·상황 그림: 사람 아이콘·영수증 종이(톱니 아래끝)·도장.

판정: 통과
