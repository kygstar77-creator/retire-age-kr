# x1s_deposit 관문 기록 (X-1 WcBOePkyOOQ 클립, M1S live) — 10/26 17:20 칸

| 관문 | 결과 | 근거 |
|---|---|---|
| 경쟁 | compete.md 6편 | compete.md · compete_raw.json |
| 이해 시험 | 40·50·60세 1~4차(새 심사관 12명) 뜻 맞음, 4차 고친 뒤 판정 통과 | understand.md |
| 제목 | '달러 예금 이자 3%, 환율 몇 % 내리면 마이너스일까' — 제미나이 9.5, 이해 시험에서 '0원'→'마이너스' | upload.json title_review |
| 렌더 | 10/25 23:04 렌더(10/23 03:48 'No frame found' 실패 뒤 다시) → 안전 영역 걸림 1곳(21.0초 배경 6963836 키보드 자판 글자가 아래 672px 안 글자 상자) → 그 칸 배경만 8661806(동전) start 12로 바꿔 23:34 다시 렌더, 말·글자·박자 그대로 | render_1025b.log · x1s_deposit.json.pre1025b |
| 쉿소리 | 렌더 −9.4dB → deess --chirp-short 뒤 쉿소리 틀 밑(None, x1s_hedge와 같은 판정) · 음량 −17.0 LUFS·TP −1.4 | deess_1025b.log |
| 치직 | 0개 | video/clickscan.py scan(렌더본 소리) |
| 꼴 ⓐ~ⓓ | 통과 | w1g1clips_check.form_check |
| 0초 빈 곳 | 0% | emptyscan.frame0 |
| 안전 영역 | 52프레임 전부 안 | safezone.gate |
| 디자인 | 배경 실사 98%·자막 기준 100%·흰 판 경고 없음 | bgcheck.gate |
| 배경 저작권 | Pexels License, 6963836(cottonbro) 빠져 설명란 출처에서도 뺌 | upload.json description |

## 눈 검사 — sheet_1025b.png(12장) + 16·18·20·21초
잘림·겹침·숫자 오타 0. '원화로 바꾸는 날 ?' → '그날 환율' 손 동그라미 그대로. 흠 하나: 동전 실사가 19초·28초 두 번 나옴(같은 클립 다른 구간) — 다음 클립부터 한 편 안 같은 클립 2번 피함.
올리기 전 확인: 화면·설명 숫자는 기준일이 박힌 지나간 값(금리 조회기준일 10/16·환율 10/15)이라 그대로 맞음. 오늘 KB 금리 다시 조회는 확인 안 함.

판정: 통과 (10/25 23:38 firemap-video-producer)
