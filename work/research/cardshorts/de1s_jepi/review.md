# de1s_jepi 관문 기록 (D-ETF-1 mkAxQPGaDqc 클립, M1S live) — 11/1 PD

| 관문 | 결과 | 근거 |
|---|---|---|
| 경쟁 | compete.md | compete.md |
| 이해 시험 | 40·50·60세 1~3차(9명) 뜻 맞음, 판정 통과 | understand.md |
| 제목 | 'JEPI 분배율 8%, 5년 동안 돈은 얼마나 불었을까'(해시태그 빼고 26자·숫자 2) | upload.json · title_gemini.json |
| 렌더 | 10/29 렌더본은 이해 시험 3차 고침 전 판 + 안전 영역 29/50프레임(배경 7578628 앱 화면·7490451 계산기 자판·38667523 tradingview·39494572 'CFDs on Gold' 글자) → 배경 4칸 교체 → 2차 8프레임(5366344 빗방울을 글자로 읽음·끝 장면 6639799 얼굴·두 값 한 줄 974px) → 배경 2칸 더 교체·safeframe 글자 하한 72→56·긴 답은 손 밑줄 → 11/1 19:31 3차(1차 시도 소리 404 일시 오류, 파일 그대로 다시) · 말·숫자·박자 그대로 | render_1101c.log · de1jclip.py.pre1101bg · video/de1s_jepi.json.pre1101bg |
| 쉿소리 | 렌더 −10.9dB → deess --chirp-short 뒤 틀 밑(None) · −17.0 LUFS·TP −1.5 | deess_1101c.log |
| 치직 | 0개 | clickscan |
| 안전 영역 | 50프레임 전부 안 | safezone.gate |
| 디자인 | 배경 실사 100%·자막 기준 100% | bgcheck.gate |
| 배경 저작권 | Pexels License, 설명란 출처 줄 새 클립으로 | upload.json |

## 눈 검사 — sheet_1101c.png(14장)
잘림·겹침·숫자 오타 0 · 얼굴·상표 0(손·찻잔·뒷모습·화분만) · 끝 '10년으로 늘리면 HDV 10.4% · S&P500 15.4%'는 56px로 줄어 한 줄 안, 주황 동그라미 화면 안. 흠: 5년·10년 두 값 줄이 다른 박자보다 글자가 작음(170→56) — 다음 클립부터 두 값은 박자 둘로 나눔.
올리기 전 확인: 숫자는 2026-10-16 마감 기준 지난 값(설명란 기준일 줄)이라 그대로 맞음. 야후 다시 받기는 확인 안 함.

판정: 통과 (19:34 firemap-video-producer) — 업로드는 w1g1clips_check ⓓ(m1clip 6/10)에 막혀 회의 결정 대기

# 11/2 판 (c1clip — C1S live) · firemap-video-producer 07:02
| 관문 | 결과 | 근거 |
|---|---|---|
| 틀 | c1clip(C1S look live) — E-18 통과(c1clip 최근 3편 중앙 1,025 vs 채널 20편 980) · 장면 몸통은 M1S live와 같은 LiveSceneBody라 화면 차이는 작음(틀 이름만 바뀐 것에 가까움 — 회의·youtube-loop 판정대로 따름) | w1g1clips_check form_check |
| 답 5초 안(A-49·A71·A72) | '많이들 이렇게 생각하시죠' 줄 뺌, 계산법·단서 줄 답 뒤로 · 말 '7.5%' 약 4초·화면 '매년 7.5%만' 4.3초(옛 판 19.5초) · 말·숫자 새로 0 | de1jclip.py 11/2 |
| 4~15초 줄 — 질문 안/곁가지 | 4~15초 = 7.5% 이유('주가는 거의 오르지 않았다')·'배당만 보면 반쪽'·계산법 — 모두 질문 안, 곁가지 0 | |
| 밝기(B-46) | Y 31.3→63.9 · 60 미만 칸 69%→24% (기준 Y≥52·≤30%) — 어두운 클립 4칸·빗창 2칸 교체, 비트코인 무늬 동전 클립(8369909) 뺌 | bright.py |
| 이해 시험 | 4차 40·50·60세 3명 뜻 맞음 | understand.md |
| 쉿소리·음량 | deess 뒤 틀 밑 · −17.0 LUFS · TP −1.2 | deess_1102.log |
| 치직 | 0 | clickscan |
| 안전 영역 | 46프레임 전부 안 | safezone.gate |
| 디자인 | 배경 실사 100%·자막 기준 100% | bgcheck.gate |
| 눈 검사 | sheet_1102.png — 잘림·겹침·숫자 오타 0, 얼굴 0, 첫 칸 유리병에 작은 영문 글자(상표 아님, 안전 영역 통과) | sheet_1102.png |
| 표지 | cover_1102.png(0.2초 화면) — 첫 표지 실측(today 벤치마크 지시) | upload.json cover |
렌더 메모: 디스크 5~7GB라 Remotion이 public 5.9GB 복사를 다 못 해 소리 404 → 06:29 묶음에 이 편 파일 262MB만 채워 렌더.
판정: 통과 (11/2 07:02 firemap-video-producer)
