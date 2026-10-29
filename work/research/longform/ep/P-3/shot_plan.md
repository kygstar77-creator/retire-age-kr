# P-3 장면 구상 (shot_plan) — 2026-10-26 youtube-loop (공개 10/29)

- 본 방법: compete.md 상위 편 중 4편을 제미나이(gemini-3-flash-preview, 구글 공식 YouTube URL 입력, 다운로드 없음)에게 '화면만' 장면별로 받아 적게 했다(10/26 15:49~15:50). 4편: x8xekxiTt4Q(시니어닷컴 37.6만)·4lMjJ8iKpog(연금이야기 56.7만)·W42NW4wF5LU(리클래스 12.9만)·qUslcyzFx9Q(여운봉 부자사관학교 4.7만). F-kUZT3bX1A(연금박사 이영주)는 뉴스 대담형이라 보지 않았다.
- &t=초는 제미나이가 적은 장면 시작 시각(±20초쯤 어긋날 수 있음). 장면을 만드는 담당은 만들기 전에 그 시각을 브라우저로 한 번 열어 눈으로 확인하고, 비교 그림 shotcmp/rNN.jpg를 만들 때 경쟁 화면을 캡처한다(커밋 안 함).
- 대본 기준: script.md v1(10/22 a23 반영본). 장 이름은 script.md 머리 그대로.
- 지금 상태: '경쟁 장면'·'장면 계획(구상·도구·만들 파일 경로)'까지. **파일·비교 그림·품질 판정 칸은 만들 차례**(visual-designer·video-producer) — shot_check는 파일이 생기고 새 심사관이 '같음·나음'을 적어야 통과한다.
- 판은 TallyFrame(노트 종이 결, 한 화면 한 문장, 주황은 답 하나), 실사는 Pexels(license 칸, 얼굴 없음 — 손·뒷모습·창가·물건) 또는 스톡이 안 맞는 자리만 이 PC RealVisXL V5.0(얼굴·글자 없음, 이상한 손 나오면 버림 — 쓰면 containsSyntheticMedia True 그대로). 계산은 [표]. 남의 차트·뉴스·지식iN 캡처는 쓰지 않고 우리 글씨로 다시 쓴다. 이름 붙은 가상 인물 없음, 네이버 부동산 화면 없음.

## 경쟁이 피부양자 문턱을 보여 준 방법 (제미나이가 본 것)
- 시니어닷컴(#1~#8): 3~5초마다 바뀜. 진행자 + 빨간 큰 글자('수천만 원 손해'), 녹색 바탕 장 제목, 연기 연수별 연소득 표에 '탈락!' 도장, 계산식(130만×12), '2.1% 인상' 인포그래픽. AI로 만든 노인 고민 장면에 말풍선 자막.
- 연금이야기(#9~#16): 진행자는 둥근 PIP로 작게, 장부·바다·동전 더미·돈 뭉치 사진 배경 위에 글자 설명이 10~20초마다 바뀜. 배경 사진은 1~2분 동안 그대로. '50%' 큰 숫자, 자동차 아이콘 + 100%/50% 부과 비율, 계산기 배경 위 원칙 목록.
- 리클래스(#17~#20): 50~60초마다 바뀜. 검은 바탕 노랑·흰 큰 글씨로 사례 조건, 소득별 세금·건보료 상세 표, 공적·사적·금융 → 세금·건보료 흐름도, 직장·지역 보험료 구성 비교표.
- 여운봉(#21~#29): 40~50초마다 바뀜. 저울·온도계·버스 일러스트, '연 2천만(월 166만)' 기준선 앞 노년 여성 일러스트, AI 상황 장면(1천만원 갈림길·'+1원' 경고등·공단 서류 제출), 재산 과표 3단계 기준표, 시세 → 공시가 → 과표 흐름도, A/B 판정 요약표.
- 공통: 진행자 얼굴이 화면 절반 이상(리클래스 빼고). 우리는 진행자가 없으니 그 자리를 손·물건 실사와 판이 번갈아 맡는다. 경쟁의 AI 사람 장면(#2·#23·#24·#29)은 얼굴 있는 가상 인물이라 따라 하지 않고, 같은 '고민하는 순간'을 얼굴 없는 손·물건으로 바꾼다.
- 빈자리: 네 편 모두 '언제부터 고지서가 오나'를 달력으로 보여 준 장면이 없다(compete.md 결론과 같음) → 4장 달력 판이 우리 몫.

# 경쟁 장면
| # | 영상 주소(&t=초) | 채널 | 무엇을 어떻게 보여 줬나 | 종류 | 확인일 |
|---|---|---|---|---|---|
| 1 | https://www.youtube.com/watch?v=x8xekxiTt4Q&t=2 | 시니어닷컴 | 흰 바탕에 '수천만 원 이상 손해' 빨간 큰 글자로 첫 3초 | 큰 숫자 자막 | 2026-10-26 |
| 2 | https://www.youtube.com/watch?v=x8xekxiTt4Q&t=15 | 시니어닷컴 | AI로 만든 노인이 공단 앞에서 고민, 말풍선 자막 "고갈된다는데..." | AI 상황 장면 | 2026-10-26 |
| 3 | https://www.youtube.com/watch?v=x8xekxiTt4Q&t=51 | 시니어닷컴 | 녹색 바탕 '1. 국민연금, 언제 받는게 좋을까?' 장 제목 | 장 제목 자막 | 2026-10-26 |
| 4 | https://www.youtube.com/watch?v=x8xekxiTt4Q&t=120 | 시니어닷컴 | '월 130만 원 × 12 = 연 1,560만 원' 계산식 | 계산식 | 2026-10-26 |
| 5 | https://www.youtube.com/watch?v=x8xekxiTt4Q&t=265 | 시니어닷컴 | 가입자 종류(지역·직장·피부양자) 인포그래픽 + 연 2,000만 원 기준 | 구조 도식 | 2026-10-26 |
| 6 | https://www.youtube.com/watch?v=x8xekxiTt4Q&t=330 | 시니어닷컴 | 연기 연수별 연소득 표에 안전·마지노선 표시, '4년 연기' 줄에 빨간 '탈락!' 도장 | 표+도장 효과 | 2026-10-26 |
| 7 | https://www.youtube.com/watch?v=x8xekxiTt4Q&t=484 | 시니어닷컴 | '2026년 1월부터 2.1% 인상' 아이콘 인포그래픽 | 아이콘 목록 | 2026-10-26 |
| 8 | https://www.youtube.com/watch?v=x8xekxiTt4Q&t=394 | 시니어닷컴 | '5년 연기 순이익 27만' vs '3년 연기 28만' 나란히 비교 표 | 비교 표 | 2026-10-26 |
| 9 | https://www.youtube.com/watch?v=4lMjJ8iKpog&t=0 | 연금이야기 | 거실 소파 진행자 + 아래 흰 큰 글자 '탈락 20만 명' | 진행자+큰 자막 | 2026-10-26 |
| 10 | https://www.youtube.com/watch?v=4lMjJ8iKpog&t=81 | 연금이야기 | 흐린 장부 배경 위 '1·2·9' 탈락 규칙 글자, 진행자 둥근 PIP | 문서 배경+글자 | 2026-10-26 |
| 11 | https://www.youtube.com/watch?v=4lMjJ8iKpog&t=317 | 연금이야기 | 바다 배경 팔 벌린 실루엣 사진 위 소득 종류별 자막 | 사진+글자 | 2026-10-26 |
| 12 | https://www.youtube.com/watch?v=4lMjJ8iKpog&t=466 | 연금이야기 | 계산기 사진 배경 위 합산소득 원칙 요약 목록 | 사진+목록 | 2026-10-26 |
| 13 | https://www.youtube.com/watch?v=4lMjJ8iKpog&t=514 | 연금이야기 | 자동차 아이콘 + 소득별 부과 비율(100% vs 50%) | 아이콘+숫자 | 2026-10-26 |
| 14 | https://www.youtube.com/watch?v=4lMjJ8iKpog&t=530 | 연금이야기 | 배경에 크게 '50%' — 판정은 전액, 부과는 절반 | 큰 숫자 자막 | 2026-10-26 |
| 15 | https://www.youtube.com/watch?v=4lMjJ8iKpog&t=552 | 연금이야기 | 쌓인 동전 더미 사진 위 보수 외 소득 건보료 설명 | 사진(돈)+글자 | 2026-10-26 |
| 16 | https://www.youtube.com/watch?v=4lMjJ8iKpog&t=628 | 연금이야기 | 돈 뭉치 사진 배경 위 계산 수식 '약 59,000원' | 사진+계산식 | 2026-10-26 |
| 17 | https://www.youtube.com/watch?v=W42NW4wF5LU&t=0 | 리클래스 | 검은 바탕 노랑·흰 큰 글씨로 사례 조건(연금·금융소득·주택) + 질문 | 큰 숫자 자막 | 2026-10-26 |
| 18 | https://www.youtube.com/watch?v=W42NW4wF5LU&t=51 | 리클래스 | '소득과 세금/건보료' 소득 항목별 반영 비중 상세 표 | 표 | 2026-10-26 |
| 19 | https://www.youtube.com/watch?v=W42NW4wF5LU&t=192 | 리클래스 | 공적연금·사적연금·금융소득 → 종합소득세·건보료 연결 흐름도 | 흐름 도식 | 2026-10-26 |
| 20 | https://www.youtube.com/watch?v=W42NW4wF5LU&t=540 | 리클래스 | 직장·지역가입자 보험료 구성(소득·재산·요양) 비교 표 | 비교 표 | 2026-10-26 |
| 21 | https://www.youtube.com/watch?v=qUslcyzFx9Q&t=1 | 여운봉 부자사관학교 | 수입 vs 지출 저울 일러스트 | 비유 그림 | 2026-10-26 |
| 22 | https://www.youtube.com/watch?v=qUslcyzFx9Q&t=168 | 여운봉 부자사관학교 | '연 2,000만 원(월 166만 원)' 기준선 앞에 선 노년 여성 일러스트 | 기준선 그림 | 2026-10-26 |
| 23 | https://www.youtube.com/watch?v=qUslcyzFx9Q&t=275 | 여운봉 부자사관학교 | 1,000만 원 이하(유지)·초과(박탈) 갈림길에 선 남성 | AI 상황 장면 | 2026-10-26 |
| 24 | https://www.youtube.com/watch?v=qUslcyzFx9Q&t=429 | 여운봉 부자사관학교 | 1,000만 원 선에 '+1원' 경고등이 켜지는 장면 | AI 상황 장면 | 2026-10-26 |
| 25 | https://www.youtube.com/watch?v=qUslcyzFx9Q&t=601 | 여운봉 부자사관학교 | 은퇴자 A(유지)·B(박탈) 최종 판정과 예상 월 보험료 요약표 | 비교 표 | 2026-10-26 |
| 26 | https://www.youtube.com/watch?v=qUslcyzFx9Q&t=727 | 여운봉 부자사관학교 | 공적연금(100% 반영) vs 사적연금(제외) 두 칸 비교 화면 | 두 칸 비교 | 2026-10-26 |
| 27 | https://www.youtube.com/watch?v=qUslcyzFx9Q&t=920 | 여운봉 부자사관학교 | 재산 과세표준 구간별 피부양자 유지 3단계 기준표 | 단계 표 | 2026-10-26 |
| 28 | https://www.youtube.com/watch?v=qUslcyzFx9Q&t=1042 | 여운봉 부자사관학교 | 시세 → 공시가격 → 공정시장가액비율 → 과표 흐름도 | 흐름 도식 | 2026-10-26 |
| 29 | https://www.youtube.com/watch?v=qUslcyzFx9Q&t=1550 | 여운봉 부자사관학교 | 공단에 해촉증명서를 내는 여성 | AI 상황 장면 | 2026-10-26 |

# 장면 계획
| 장 | 대본 줄(요지) | 구상 | 따라 한 경쟁 장면 # | 도구 | 파일 | 비교 그림 | 품질 판정 |
|---|---|---|---|---|---|---|---|
| 0. 여는 말 | 안녕하세요, 파이어맵 · 피부양자 이야기 | 아침 햇빛 우편함에서 봉투를 꺼내는 손(얼굴 없음), 위 글자 '파이어맵' | #9 · #2 | Pexels 스톡 영상 | bg/p3/stock/mailbox_hand.mp4 | shotcmp/r01.jpg | 만들 차례 |
| 0. 여는 말 | 연금 만원 더 → 보험료 매달 7만원 가까이 | 큰 글자 한 줄 '연금 +1만원 → 건보료 매달 7만원 가까이', 뒤 숫자만 주황 | #1 · #17 | Remotion TallyFrame | bg/p3/board/p3_hook.png | shotcmp/r02.jpg | 만들 차례 |
| 0. 여는 말 | 그 자리가 어디일까요 · 피부양자는 한 푼도 안 냄 | 식탁 위 연금 통지서 봉투·돋보기·찻잔(글자 없음) | #2 · #15 | AI 실사 RealVisXL V5.0(이 PC) | bg/p3/ai/notice_magnifier.png | shotcmp/r03.jpg | 만들 차례 |
| 0. 여는 말 | 65세 · 자녀 직장보험 피부양자 · 국민연금 월 165만원 | 조건 카드 넷(나이·피부양자·월 165만원·재산 거의 없음), 이름 없음 | #17 · #4 | Remotion TallyFrame | bg/p3/board/p3_condition.png | shotcmp/r04.jpg | 만들 차례 |
| 0. 여는 말 | 166만원 0원 · 167만원 매달 6만 8천원쯤 | '월 166만원 → 0원' / '월 167만원 → ?' → 말 닿을 때 '약 6만 8천원' + 손 동그라미 | #6 · #14 | Remotion TallyFrame | bg/p3/board/p3_answer.png | shotcmp/r05.jpg | 만들 차례 |
| 0. 여는 말 | 아무것도 안 해도 넘을 수 있음 | 벽 달력 장이 바람에 넘어가는 장면(사람 없음) | #7 · #3 | Pexels 스톡 영상 | bg/p3/stock/calendar_flip.mp4 | shotcmp/r06.jpg | 만들 차례 |
| 1. 문턱은 정확히 얼마인가 | 지식iN 질문 하나 | 공단 지사 창구 앞 번호표 쥔 손(얼굴·간판 없음) | #2 · #29 | Pexels 스톡 영상 | bg/p3/stock/queue_ticket.mp4 | shotcmp/r07.jpg | 만들 차례 |
| 1. 문턱은 정확히 얼마인가 | 연금 2천만 넘으면 건보료 얼마냐는 질문 | 메모지에 질문 요지 한 줄(우리 글씨, 캡처 아님) + 날짜 작게 | #2 · #9 | Remotion TallyFrame | bg/p3/board/p3_kin_q.png | shotcmp/r08.jpg | 만들 차례 |
| 1. 문턱은 정확히 얼마인가 | 기준 연 2천만원 · 한 달 166만원 남짓 | 문턱 자 0~3천만원 눈금, 2천만원에 주황 선 하나 → 아래 '월 166만원' | #22 · #5 | Remotion TallyFrame | bg/p3/board/p3_ruler.png | shotcmp/r09.jpg | 만들 차례 |
| 1. 문턱은 정확히 얼마인가 | 국민연금은 받은 돈 전부 셈 | 펼친 통장 입금 줄을 짚는 손가락(글자 흐리게) | #15 · #11 | Pexels 스톡 영상 | bg/p3/stock/passbook_finger.mp4 | shotcmp/r10.jpg | 만들 차례 |
| 1. 문턱은 정확히 얼마인가 | 연금저축·IRP는 안 셈 | 두 칸 '국민연금·공무원연금 → 셈' / '연금저축·IRP → 안 셈' | #26 · #19 | Remotion TallyFrame | bg/p3/board/p3_public_private.png | shotcmp/r11.jpg | 만들 차례 |
| 2. 넘으면 매달 얼마인가 | 지역가입자 · 고지서가 본인 이름으로 | 창가에서 고지서 봉투 뜯는 손 | #16 · #15 | Pexels 스톡 영상 | bg/p3/stock/open_bill.mp4 | shotcmp/r12.jpg | 만들 차례 |
| 2. 넘으면 매달 얼마인가 | 연금 절반 × 7.19% = 6만원쯤 | 식 조각 '167만원' → '× 절반' → '× 7.19%' → '= ?' → 열림 | #4 · #16 · #14 | Remotion TallyFrame(표) | bg/p3/board/p3_calc_health.png | shotcmp/r13.jpg | 만들 차례 |
| 2. 넘으면 매달 얼마인가 | 장기요양 13.14% · 8천원쯤 · 합계 6만 8천원 | 같은 식 아래 한 줄 덧붙음 '+ 장기요양', 합계 칸만 주황 | #20 · #16 | Remotion TallyFrame(표) | bg/p3/board/p3_calc_ltc.png | shotcmp/r14.jpg | 만들 차례 |
| 2. 넘으면 매달 얼마인가 | 집 같은 재산이 있으면 재산에도 보험료가 따로 붙어 커짐 | 탁자 위 계산기 두드리는 손, 옆 서류 글자 흐리게 | #12 | Pexels 스톡 영상 | bg/p3/stock/calculator_hand.mp4 | shotcmp/r15.jpg | 만들 차례 |
| 2. 넘으면 매달 얼마인가 | 표: 166 0원 / 167 6.8만 / 170 6.9만 / 200 8.1만 | 계단 표 4줄, 166→167 칸에서 뜀 표시 | #6 · #25 | Remotion TallyFrame(표) | bg/p3/board/p3_step_table.png | shotcmp/r16.jpg | 만들 차례 |
| 2. 넘으면 매달 얼마인가 | 10년이면 800만원 넘음 | 달력 칸 120개가 차례로 칠해지고 끝에 '800만원 넘음' | #8 · #15 | Remotion TallyFrame | bg/p3/board/p3_10years.png | shotcmp/r17.jpg | 만들 차례 |
| 2. 넘으면 매달 얼마인가 | 국민연금은 해마다 1월에 물가만큼 오름 · 올해 2.1% | 달력 1월 칸을 넘기는 손 | #7 | Pexels 스톡 영상 | bg/p3/stock/calendar_jan.mp4 | shotcmp/r18.jpg | 만들 차례 |
| 2. 넘으면 매달 얼마인가 | 내년 168만원 남짓 · 기준 위 | 막대 '165만' 위로 2.1% 화살표 → '168만 남짓', 문턱 선 넘는 자리 손 동그라미 | #7 · #22 | Remotion TallyFrame | bg/p3/board/p3_raise.png | shotcmp/r19.jpg | 만들 차례 |
| 2. 넘으면 매달 얼마인가 | 164만원부터 이렇게 됨 · 163만원은 유지 | 두 줄 '164만 → 내년 넘음' / '163만 → 안 넘음', 164 줄에 도장 | #6 · #24 | Remotion TallyFrame | bg/p3/board/p3_164_163.png | shotcmp/r20.jpg | 만들 차례 |
| 3. "깎아 준다던데요?" | 탈락해도 처음 몇 년은 깎아 준다는 말 | 함정 카드 앞면 말풍선 '탈락하면 처음엔 깎아 준대' → 뒤집기 | #2 · #23 | Remotion TallyFrame | bg/p3/board/p3_trap_cut.png | shotcmp/r21.jpg | 만들 차례 |
| 3. "깎아 준다던데요?" | 80% → 60% → 40% → 20% · 올해 8월에 끝 | 계단 다섯 칸, 마지막 '2026년 8월분'에서 멈춤 | #27 · #6 | Remotion TallyFrame | bg/p3/board/p3_cut_steps.png | shotcmp/r22.jpg | 만들 차례 |
| 3. "깎아 준다던데요?" | 예전 기사·영상 계산은 지우셔야 | 오래된 신문 묶음을 서랍에 넣는 손(제목 흐리게) | #10 | Pexels 스톡 영상 | bg/p3/stock/old_paper.mp4 | shotcmp/r23.jpg | 만들 차례 |
| 4. 언제 다시 보나 | 연금 오르면 바로 그달부터 탈락? 아님 | 종이 달력 2026년 11월(실제 날짜, 1일 일요일)에 손 동그라미 — AI 달력 3장이 가짜 날짜·이상한 손이라 판으로 바꿈(K-1 r32와 같음) | #7 · #3 | Remotion TallyFrame(종이 판, p3boards.py) | bg/p3/board/p3_calendar_nov.png | shotcmp/r24.jpg | 만들 차례 |
| 4. 언제 다시 보나 | 연금은 늘 작년 한 해 받은 돈으로 봄 | 달력 한 장 '1~10월' / '11~12월' 두 칸, 연금은 두 칸 모두 '작년 연금' | #28 · #18 | Remotion TallyFrame | bg/p3/board/p3_calendar_rule.png | shotcmp/r25.jpg | 만들 차례 |
| 4. 언제 다시 보나 | 내년에 오른 연금은 그다음 해 판정에 | 타임라인 '올해' → '내년 연금 오름' → '그다음 해 판정·고지서', 마지막 칸 주황 | #28 · #6 | Remotion TallyFrame | bg/p3/board/p3_timeline.png | shotcmp/r26.jpg | 만들 차례 |
| 4. 언제 다시 보나 | 이자·배당은 11월이 갈림길 · 그달 통지 꼭 보기 | 현관 우편함 앞 흰 봉투를 든 손(뒷모습) | #2 · #29 | Pexels 스톡 영상 | bg/p3/stock/mail_november.mp4 | shotcmp/r27.jpg | 만들 차례 |
| 5. 이자·배당이 섞이면 | 예금 이자도 신경 쓰임 | 통장 정리기에 통장을 넣는 손 | #15 | Pexels 스톡 영상 | bg/p3/stock/passbook_atm.mp4 | shotcmp/r28.jpg | 만들 차례 |
| 5. 이자·배당이 섞이면 | 999만원이면 0원? 답이 엇갈림 | 메모지 질문 한 줄 + 답 세 칸이 서로 다른 색 '?' (우리 글씨) | #23 · #24 | Remotion TallyFrame | bg/p3/board/p3_kin_999.png | shotcmp/r29.jpg | 만들 차례 |
| 5. 이자·배당이 섞이면 | 1천만원 이하 안 더함 · 넘으면 전부 | 1천만원 선 — 아래 '안 더함' / 위 '전부 더함', 선 넘는 순간 막대 전체 주황 | #24 · #23 · #13 | Remotion TallyFrame | bg/p3/board/p3_1000_line.png | shotcmp/r30.jpg | 만들 차례 |
| 5. 이자·배당이 섞이면 | 선 근처면 공단 고객센터에 먼저 | 탁자 위 휴대폰을 집어 드는 손(화면 글자 없음) + 자막 1577-1000 | #29 | Pexels 스톡 영상 | bg/p3/stock/phone_pickup.mp4 | shotcmp/r31.jpg | 만들 차례 |
| 5. 이자·배당이 섞이면 | 연 1,000만 + 1,100만 → 탈락 · 매달 11만원쯤 | 식 표 '1,000만 + 1,100만 = 2,100만 → 탈락 → 월 약 11만원' | #25 · #16 | Remotion TallyFrame(표) | bg/p3/board/p3_mix_calc.png | shotcmp/r32.jpg | 만들 차례 |
| 6. 누구라면 달라지나 | 집이 있으면 길이 갈림 | 갈림길 세 갈래 '집이 있다' / '사업을 한다' / '연금저축만 있다' | #23 · #21 | Remotion TallyFrame | bg/p3/board/p3_three_roads.png | shotcmp/r33.jpg | 만들 차례 |
| 6. 누구라면 달라지나 | 재산 과표 5억 4천만원 넘으면 | 해 질 녘 아파트 외벽 창문들(사람·간판 없음, 시세 화면 아님) | #28 · #11 | Pexels 스톡 영상 | bg/p3/stock/apartment_windows.mp4 | shotcmp/r34.jpg | 만들 차례 |
| 6. 누구라면 달라지나 | 소득 기준 1천만원으로 · 9억 넘으면 안 됨 | 3단 기준표 '5.4억 이하 2천만' / '5.4~9억 1천만' / '9억 초과 안 됨' | #27 | Remotion TallyFrame(표) | bg/p3/board/p3_property.png | shotcmp/r35.jpg | 만들 차례 |
| 7. 흔한 말 하나 | 연금을 일찍 당겨 받아 줄이면? | 가을 공원 벤치에 앉은 두 사람의 뒷모습 | #22 · #2 | Pexels 스톡 영상 | bg/p3/stock/bench_backs.mp4 | shotcmp/r36.jpg | 만들 차례 |
| 7. 흔한 말 하나 | 한 해 일찍 → 평생 6% 줄어듦 vs 탈락 월 6만 8천원 | 저울 — 왼쪽 '평생 6% 줄어듦' / 오른쪽 '?' → 말 닿을 때 '월 약 6만 8천원' | #21 · #8 | Remotion TallyFrame | bg/p3/board/p3_scale.png | shotcmp/r37.jpg | 만들 차례 |
| 7. 흔한 말 하나 | 미뤄 받으면 괜찮다는 말 · 세 번 오르면 2천만원 넘음 | 달력 네 칸 '1,896만' → '1,936만' → '1,976만' → '?' → '2,018만' + 문턱 선 넘음 + 손 동그라미 | #6 · #7 | Remotion TallyFrame | bg/p3/board/p3_four_years.png | shotcmp/r38.jpg | 만들 차례 |
| 8. 그래서 할 일 | 연금 통지서를 꺼내 보는 것 | 서랍에서 접힌 서류를 꺼내 펼치는 손(글자 흐리게) | #12 | Pexels 스톡 영상 | bg/p3/stock/drawer_paper.mp4 | shotcmp/r39.jpg | 만들 차례 |
| 8. 그래서 할 일 | 셈·확인·신청 세 가지 | 할 일 카드 세 장이 한 장씩 '셈' · '확인' · '신청' | #12 · #3 | Remotion TallyFrame | bg/p3/board/p3_todo3.png | shotcmp/r40.jpg | 만들 차례 |
| 8. 그래서 할 일 | 만원 더 받는 게 손해가 되는 자리 · 맺는 말 | 창가 찻잔과 접힌 고지서, 김이 오름 — 3초 이상 숨(글자 없음) | #15 · #11 | AI 실사 RealVisXL V5.0(이 PC) | bg/p3/ai/tea_bill_steam.png | shotcmp/r41.jpg | 만들 차례 |

빠진 것: 경쟁이 많이 쓴 '진행자 얼굴'(#9 등)과 'AI로 만든 노인·남성·부부'(#2·#23·#24·#29)는 얼굴 있는 가상 인물이라 쓰지 않고, 같은 순간을 손·물건 실사로 바꿨다. 뉴스 헤드라인·지식iN 화면 캡처는 남의 자료라 우리 글씨 판으로 다시 쓴다. 저울(#21)·기준선(#22)·갈림길(#23) 비유는 일러스트 캐릭터 없이 판 위 선·도형으로만 옮긴다(캐릭터 없음).
비율: 41줄 중 실사 17줄(Pexels 14 · RealVisXL 3, 약 41%), 판 24줄. 판이 이어지는 자리(0장 r04·r05, 2장 r13·r14, 2장 r19·r20, 3장 r21·r22, 4장 r25·r26, 7장 r37·r38)도 한 판이 20초를 넘지 않게 말 단위로 나눈다.
