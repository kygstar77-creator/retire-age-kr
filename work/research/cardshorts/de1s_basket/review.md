# de1s_basket 관문 — firemap-video-producer 2026-11-13 (11/17 19:20 칸, 회의 11/13 21:39 지시)
| 관문 | 결과 | 근거 |
|---|---|---|
| 주제 근거 | kwvol 11/13: TIGER미국배당다우존스 25,250 · SOL미국배당다우존스 8,380 · SCHD 53,300 | compete.md |
| 경쟁 비교 | 6편(Data API·제미나이 영상 보기) · 다른 한 가지 = 업종 비중을 숫자로 맞대 '같이 담기'를 따짐(경쟁 0편) | compete.md |
| 틀 | c1clip(C1S live) · 원본 D-ETF-1 mkAxQPGaDqc · 배당ETF·지수 축(11/15·16 부동산 뒤) | |
| 꼴 관문 | 통과(첫 줄 33자·숫자 '2개' — 1판 37자·숫자 0으로 걸려 첫 줄 다시 받음) · ⓓ E-18 c1clip 998 vs 996 | w1g1clips_check --form |
| 숫자 대조 | 화면·말·제목·설명 30개 못 찾음 0(11/13 다시 받은 4종 값은 ep/D-ETF-1/calc_basket1113_out.txt) | w1g1clips_check |
| 올리기 전 확인 | 11/13 네이버 4종 세 업종 합 약 53% — 롱폼 '55%'(10/15) 줄은 쓰지 않고 '절반 넘게'로 새 녹음 · research.md S21 | raw/etf_*.json |
| 새 녹음 | 2줄(q2 첫 질문·half 절반 넘게, Charon 1.1·pause_v 2 같은 설정) · q2는 3번 받아 f0 롱폼에 가장 가까운 것(125.7 vs 약 136Hz) · 나머지 D-ETF-1 voice.json(3:13 앞 '예를 들어' 잘라냄·3:4 문장 끝에서 나눔) — 받아쓰기 전부 확인 | de1bclip.py |
| 길이 | 30.6초 | |
| 이해 시험 | 2차 3/3 통과(46·57·66세) · 2차 뒤 화면 글자 2곳·제목 '국내' 고침(3차 안 함) | understand.md |
| AI 티 | 제목·설명 0.0 | aitell |
| 렌더 1판 | 22:38 끝(−17.0 LUFS·TP −1.5) · 안전 영역 31프레임·디자인 실사 100%·0초 빈 곳 0%·치직 0 · **눈 검사 걸림**: 한 줄에 칸 두 개면 뒤 칸만 보임(장면2 '상품마다 담긴 돈'·장면3 'TIGER · SOL · ACE · KODEX' 빠짐) → 줄을 나눠 고침 | sheet_1113.png |
| 렌더 2판 | **3번 실패로 멈춤**(22:4x, 6343634 'No frame found' — 빈 메모리 0.25GB/15.4, 1판 때 4.2GB) · 회의 규칙대로 멈추고 보고 | render_part_0-459_3.log |
남은 것: 빈 메모리 2GB↑ 회차에서 render_1113.sh → deess·safezone·bgcheck·emptyscan·clickscan·눈 검사(장면2·3 칸 두 개 다 보이는지)·표지 cover_1113.png → '판정: 통과' 줄 → w1g1clips_up.py de1s_basket(11/17 19:20 publishAt) · 관문 기한 11/17 07:20
| 렌더 2판 | 11/14 02:19~02:28 1번에 통과(토막 2개, 빈 메모리 2.2GB) · −17.0 LUFS·TP −1.5 · 치직 0 · 안전 영역 31프레임 · 디자인 실사 100%·자막 100% · 0초 빈 곳 0% | render_1114.out |
| 눈 검사 2판 | sheet_1114a·b(1초 간격 31장)·eye1114/big3·zoom2 — 장면2 '상품마다 담긴 돈'·장면3 '국내 상품 이름 / TIGER · SOL · ACE · KODEX' 둘 다 보임 · 잘림·겹침 0 · 손 동그라미는 글자 바깥 · 끝 출처 줄 보임 | |
| 표지 | cover_1113.png(15.5초 '상품마다 담긴 돈 / 절반 넘게 세 업종에' 동그라미) | upload.json cover |
판정: 통과 (firemap-video-producer 2026-11-14 02:30)
