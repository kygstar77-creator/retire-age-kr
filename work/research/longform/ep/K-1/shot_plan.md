# K-1 장면 구상 (shot_plan) — 2026-10-21 youtube-loop (공개 10/28 11:30 · 관문 10/27 11:30)

- 본 방법: 같은 주제 경쟁 롱폼 7편을 제미나이가 영상 통째로 본 쪼개기(breakdown/<id>_break.md — 말+화면, 구글 공식 YouTube URL 입력, 다운로드 없음)에서 장면을 뽑았다. 10/21 새로 쪼갠 4편: XrFYylvD3G0(KBS)·5wYVYUrG4Ds(월급쟁이경제학)·0TTacba86Os(월급쟁이부자들)·O_3hsLUl3-4(싹풀TV) · 이미 쪼갠 3편: Wmky4kF4z0E(스튜디오 경향 10/18)·VBzycZvbd9g(재테크읽어주는 파일럿 10/19)·V4mCCBmoCdc(PLUS TV 10/19, 대담이라 장면 안 씀).
- &t=초는 제미나이 쪼개기의 구간 시작 시각(±20초쯤 어긋날 수 있음). 장면을 만드는 담당은 만들기 전에 그 시각을 브라우저로 한 번 열어 눈으로 확인한다(H-3처럼 비교 그림 shotcmp/rNN.jpg 만들 때 경쟁 화면 캡처 — 커밋 안 함).
- 대본 기준: script.md v1.4(10/21 심사 3명 반영). 장 이름은 script.md 머리 그대로.
- 지금 상태: '경쟁 장면'·'장면 계획(구상·도구·만들 파일 경로)'까지. **파일·비교 그림·품질 판정 칸은 만들 차례**(visual-designer·video-producer, today.md [지시]) — shot_check는 파일이 생기고 새 심사관이 '같음·나음'을 적어야 통과한다.
- 판은 TallyFrame(노트 종이 결, 주황은 답 하나), 실사는 Pexels(license 칸) 또는 이 PC RealVisXL V5.0(얼굴 없음·글자 없음 — 쓰면 containsSyntheticMedia True 그대로). 남의 차트·뉴스 캡처는 쓰지 않는다(경쟁 #2·#9·#12처럼 뉴스·앱 캡처를 쓰는 자리는 우리 원자료 그림으로 바꿈).

## 경쟁이 금리를 보여 준 방법 (쪼개기에서 본 것)
- KBS(#1~#5): 3~5초마다 바뀜. '3억 대출 월 상환액 변화' 단계 흐름도, '0.25%p/0.50%p 인상 시 추가 이자' 표, 은행 창구·현금 인출 실사, 마트 장보기 실사, '예대금리차 2.22%p' 큰 숫자 자막. 막대그래프 7회 이상.
- 월급쟁이경제학(#6~#9): 원형 캐릭터 일러스트 + 선 그래프. 은행 건물에서 돈이 빠져나가는 애니메이션, **옛날 이야기(1991 일본)는 세피아·흑백 톤**, 모래시계·청구서 쓰는 손.
- 월급쟁이부자들(#10~#13): 금리 산정 구조 박스 인포그래픽(조달금리+가산+가감), 돈 흐름 화살표 다이어그램, 관전 포인트 체크박스 목록, 시점 표시가 붙은 가격 꺾은선.
- 싹풀TV(#14~#16): '기준+가산−우대' 공식 도표, 법령 원문 문서 노출, '5억 대출 시 100만 원' 계산식 큰 글자, 질문 자막으로 장 넘김.
- 스튜디오 경향(#17~#19): 칠판 판서로 숫자 쓰기(타격음), 실물 국채 증서 그래픽에 돋보기·화살표, 지폐 계수기 B-roll.
- 파일럿(#20~#21): 미 10년 금리 그래프에 줌인, 원인 1·2·3 번호 아이콘.
- 공통: 사람 얼굴(진행자)이 화면 절반 — 우리는 진행자가 없으니 그 자리를 '손·물건 실사'(대본 화면 지시 그대로)와 판이 번갈아 맡는다. AI로 만든 사람 장면은 7편에서 보지 못했다(캐릭터 일러스트만).

# 경쟁 장면
| # | 영상 주소(&t=초) | 채널 | 무엇을 어떻게 보여 줬나 | 종류 | 확인일 |
|---|---|---|---|---|---|
| 1 | https://www.youtube.com/watch?v=XrFYylvD3G0&t=0 | KBS News | '3억 대출 시 월 상환액 변화' 고정 5년 → 변동 전환 단계 흐름도 | 흐름도+큰 숫자 | 2026-10-21 |
| 2 | https://www.youtube.com/watch?v=XrFYylvD3G0&t=61 | KBS News | '0.25%p·0.50%p 인상 시 추가 이자' 한국은행 자료 표 | 표 | 2026-10-21 |
| 3 | https://www.youtube.com/watch?v=XrFYylvD3G0&t=154 | KBS News | 은행 창구·현금 인출 실사 위 '코픽스 4개월 연속 상승' 자막 | 실사(은행) | 2026-10-21 |
| 4 | https://www.youtube.com/watch?v=XrFYylvD3G0&t=241 | KBS News | 마트 장보기 실사 → '예대금리차 2.22%p' 큰 숫자 | 실사+큰 숫자 | 2026-10-21 |
| 5 | https://www.youtube.com/watch?v=XrFYylvD3G0&t=346 | KBS News | '고정금리 비중 41.6%' 통계 자막 + 은행 창구 상담 장면 | 실사+숫자 | 2026-10-21 |
| 6 | https://www.youtube.com/watch?v=5wYVYUrG4Ds&t=0 | 월급쟁이경제학 | 얇은 얼음 위를 걷는 캐릭터 일러스트(위험 비유) | 비유 그림 | 2026-10-21 |
| 7 | https://www.youtube.com/watch?v=5wYVYUrG4Ds&t=120 | 월급쟁이경제학 | 은행 건물에서 돈이 빠져나가는 애니메이션, 예금 통장 든 캐릭터 | 움직이는 그래픽 | 2026-10-21 |
| 8 | https://www.youtube.com/watch?v=5wYVYUrG4Ds&t=300 | 월급쟁이경제학 | 1991 일본 거품 이야기를 세피아·흑백 톤으로 바꿔 '지난 일' 표시 | 옛날 톤 | 2026-10-21 |
| 9 | https://www.youtube.com/watch?v=5wYVYUrG4Ds&t=420 | 월급쟁이경제학 | 청구서 쓰는 손, 모래시계(시간이 다가옴) | 물건·손 | 2026-10-21 |
| 10 | https://www.youtube.com/watch?v=0TTacba86Os&t=0 | 월급쟁이부자들TV | 아파트 배경 위 '주담대 6%' 큰 숫자로 시작 | 실사+큰 숫자 | 2026-10-21 |
| 11 | https://www.youtube.com/watch?v=0TTacba86Os&t=231 | 월급쟁이부자들TV | 금리 산정 구조 박스 인포그래픽(조달금리 + 가산 + 가감조정) | 구조 도식 | 2026-10-21 |
| 12 | https://www.youtube.com/watch?v=0TTacba86Os&t=355 | 월급쟁이부자들TV | 화살표 아이콘으로 은행 돈 흐름 다이어그램 | 흐름 도식 | 2026-10-21 |
| 13 | https://www.youtube.com/watch?v=0TTacba86Os&t=1060 | 월급쟁이부자들TV | 관전 포인트를 체크박스 목록으로 | 체크 목록 | 2026-10-21 |
| 14 | https://www.youtube.com/watch?v=O_3hsLUl3-4&t=0 | 싹풀TV 이승희세무사 | '대출금리 = 기준 + 가산 − 우대' 공식 도표 | 공식 도표 | 2026-10-21 |
| 15 | https://www.youtube.com/watch?v=O_3hsLUl3-4&t=60 | 싹풀TV 이승희세무사 | 법정 비용 목록 + 법령 원문 문서(번호·시행일) 노출 | 원문 문서 | 2026-10-21 |
| 16 | https://www.youtube.com/watch?v=O_3hsLUl3-4&t=180 | 싹풀TV 이승희세무사 | '5억 대출 시 100만 원' 계산식 큰 글자 인포그래픽 | 계산식 | 2026-10-21 |
| 17 | https://www.youtube.com/watch?v=Wmky4kF4z0E&t=81 | 스튜디오 경향 | 칠판에 '$40조' 숫자를 분필로 쓰며 타격음 | 손글씨 숫자 | 2026-10-21 |
| 18 | https://www.youtube.com/watch?v=Wmky4kF4z0E&t=315 | 스튜디오 경향 | 실물 국채 증서 그래픽에 만기·이자율 돋보기 확대 | 문서 확대 | 2026-10-21 |
| 19 | https://www.youtube.com/watch?v=Wmky4kF4z0E&t=25 | 스튜디오 경향 | 지폐 계수기 B-roll로 '내 지갑' 연결 | 실사(돈) | 2026-10-21 |
| 20 | https://www.youtube.com/watch?v=VBzycZvbd9g&t=0 | 재테크읽어주는 파일럿 | 미 10년 국채금리 수치·그래프, 중요 수치에서 줌인 | 선 그래프 | 2026-10-21 |
| 21 | https://www.youtube.com/watch?v=VBzycZvbd9g&t=60 | 재테크읽어주는 파일럿 | 원인 1·2·3 번호 아이콘 목록 | 번호 목록 | 2026-10-21 |

# 장면 계획
| 장 | 대본 줄(요지) | 구상 | 따라 한 경쟁 장면 # | 도구 | 파일 | 비교 그림 | 품질 판정 |
|---|---|---|---|---|---|---|---|
| 0. 예고 | 안녕하세요, 파이어맵 · 미국 국채금리 5% | 은행 창구 앞 의자, 번호표 쥔 손(얼굴 없음) | #3 · #10 | Pexels 스톡 영상 | bg/k1/stock/bank_ticket.mp4 | shotcmp/r01.jpg | 만들 차례 |
| 0. 예고 | 내 예금·대출 이자는 얼마나? | 통장 두 줄 '예금 이자 ?' '대출 이자 ?' | #10 | Remotion TallyFrame | bg/k1/board/k1_two_q.png | shotcmp/r02.jpg | 만들 차례 |
| 0. 예고 | 예금 1억 다음 달 만기 | 식탁 위 휴대폰 '예금 만기 안내' 문자·찻잔(글자는 우리가 얹음) | #9 | AI 실사 RealVisXL V5.0(이 PC) | bg/k1/ai/phone_tea.png | shotcmp/r03.jpg | 만들 차례 |
| 0. 예고 | 2021년 고정금리 대출, 고정 끝남 | 현관 신발장 위 열쇠와 서류 봉투 | #9 | AI 실사 RealVisXL V5.0(이 PC) | bg/k1/ai/keys_envelope.png | shotcmp/r04.jpg | 만들 차례 |
| 0. 예고 | +74만원 · +28만원 | 이름 두 칸 옆 '?' → 말 닿을 때 열림, 손 동그라미 | #1 · #16 | Remotion TallyFrame | bg/k1/board/k1_answer2.png | shotcmp/r05.jpg | 만들 차례 |
| 0. 예고 | 질문 다섯 줄 | 질문 다섯 줄이 번호와 함께 하나씩 | #21 · #13 | Remotion TallyFrame(표) | bg/k1/board/k1_q5.png | shotcmp/r06.jpg | 만들 차례 |
| 1. 미국 국채금리 5%, 무슨 숫자인가 | 국채금리는 나라가 빌릴 때 내는 이자 | 신문 경제면 넘기는 손(제목 흐리게) | #19 | Pexels 스톡 영상 | bg/k1/stock/newspaper_hand.mp4 | shotcmp/r07.jpg | 만들 차례 |
| 1. 미국 국채금리 5%, 무슨 숫자인가 | 1만 달러 빌려주면 한 해 500달러 | 증서 모양 종이에 '1만 달러 × 5% = 500달러', 이자 칸 돋보기 | #18 · #17 | Remotion TallyFrame | bg/k1/board/k1_bond_note.png | shotcmp/r08.jpg | 만들 차례 |
| 1. 미국 국채금리 5%, 무슨 숫자인가 | 9월 중순 5% · 19일 · 최고 5.31% | 2023~2026 미 10년 선, 5% 점선, 넘는 자리 줌인+손 동그라미 | #20 | Remotion 선 그래프(FRED DGS10) | bg/k1/board/k1_dgs10.png | shotcmp/r09.jpg | 만들 차례 |
| 1. 미국 국채금리 5%, 무슨 숫자인가 | 2007년 6월 5.1% · 주담대 6% 넘음 | 2007 칸만 바랜 색 타임라인 | #8 | Remotion TallyFrame(바랜 색) | bg/k1/board/k1_2007.png | shotcmp/r10.jpg | 만들 차례 |
| 1. 미국 국채금리 5%, 무슨 숫자인가 | 미국 5.10% vs 한국 4.18% | 두 나라 막대 나란히, 한국 쪽 주황 아님(답은 차이 '1%p 가까이') | #2 | Remotion TallyFrame | bg/k1/board/k1_us_kr_now.png | shotcmp/r11.jpg | 만들 차례 |
| 2. 내 예금 이자는 얼마나 따라왔나 | 먼저 예금부터 | 펼친 예금 통장 위 손가락(금리 칸 흐리게) | #7 | Pexels 스톡 영상 | bg/k1/stock/passbook.mp4 | shotcmp/r12.jpg | 만들 차례 |
| 2. 내 예금 이자는 얼마나 따라왔나 | 2.5% → 3.4% | 막대 둘 '작년 8월' '올해 8월' 높이 먼저, 숫자 '?' → 열림 | #2 · #4 | Remotion TallyFrame | bg/k1/board/k1_dep_bar.png | shotcmp/r13.jpg | 만들 차례 |
| 2. 내 예금 이자는 얼마나 따라왔나 | 1억 × 금리 − 세금 = 212만 → 287만 | 식 조각 두 줄, 답 자리 '?' → '74만원' | #16 · #17 | Remotion TallyFrame | bg/k1/board/k1_dep_calc.png | shotcmp/r14.jpg | 만들 차례 |
| 2. 내 예금 이자는 얼마나 따라왔나 | 다른 영상 댓글 사연 2억 | 휴대폰 댓글 창 스크롤하는 손(글자 안 읽히게) | #9 | AI 실사 RealVisXL V5.0(이 PC) | bg/k1/ai/phone_scroll.png | shotcmp/r15.jpg | 만들 차례 |
| 2. 내 예금 이자는 얼마나 따라왔나 | 5년 전 1.2% · 98만원 | 동전 더미 셋 '5년 전·1년 전·지금', 지난 것은 바랜 색 | #8 · #7 | Remotion TallyFrame(바랜 색) | bg/k1/board/k1_coins3.png | shotcmp/r16.jpg | 만들 차례 |
| 2. 내 예금 이자는 얼마나 따라왔나 | 코픽스 8월 → 9월 다시 오름 | 코픽스 막대 8월·9월, 9월 한 칸 더 높게 | #3 | Remotion TallyFrame | bg/k1/board/k1_cofix89.png | shotcmp/r17.jpg | 만들 차례 |
| 2. 내 예금 이자는 얼마나 따라왔나 | 대출−예금 차이 1.5%p 그대로 | 두 선 사이 간격에 색, 간격 숫자 '?' → 열림 | #4 | Remotion 선 그래프(ECOS 121Y006·121Y002) | bg/k1/board/k1_gap.png | shotcmp/r18.jpg | 만들 차례 |
| 3. 내 대출 이자는 — 고정형과 변동형 | 고정형·변동형 둘로 나뉨 | 거실 탁자 위 대출 서류 넘기는 손(글자 흐리게) | #5 | Pexels 스톡 영상 | bg/k1/stock/loan_papers.mp4 | shotcmp/r19.jpg | 만들 차례 |
| 3. 내 대출 이자는 — 고정형과 변동형 | 고정 +0.94 · 변동 +0.45 | 막대 둘 1년 오른 폭 '?' → 열림 | #2 | Remotion TallyFrame | bg/k1/board/k1_fix_var.png | shotcmp/r20.jpg | 만들 차례 |
| 3. 내 대출 이자는 — 고정형과 변동형 | 4월부터 순서 바뀜 | 두 선이 2026.04에서 엇갈리는 자리 손 동그라미 | #20 · #13 | Remotion 선 그래프(ECOS 121Y006) | bg/k1/board/k1_cross.png | shotcmp/r21.jpg | 만들 차례 |
| 3. 내 대출 이자는 — 고정형과 변동형 | 3억·30년 142만 → 159만 | 표 3줄, 마지막 칸 주황 | #1 · #2 | Remotion TallyFrame(표) | bg/k1/board/k1_3eok_table.png | shotcmp/r22.jpg | 만들 차례 |
| 3. 내 대출 이자는 — 고정형과 변동형 | 변동형은 왜 덜 올랐을까(장 안 쉼) | 빗방울 맺힌 창가 빗물 | #6 | Pexels 스톡 영상 | bg/k1/stock/rain_window.mp4 | shotcmp/r23.jpg | 만들 차례 |
| 3. 내 대출 이자는 — 고정형과 변동형 | 코픽스 + 은행이 붙이는 금리 · 세 갈래 | 공식 박스 '내 금리 = 코픽스 + 가산' → 코픽스가 세 갈래(신규·잔액·신잔액)로 갈림 | #11 · #14 · #12 | Remotion TallyFrame(도식) | bg/k1/board/k1_cofix3.png | shotcmp/r24.jpg | 만들 차례 |
| 3. 내 대출 이자는 — 고정형과 변동형 | 조심 두 가지 | 함정 카드 앞·뒷면(뒤집기) | #15 · #13 | Remotion TallyFrame | bg/k1/board/k1_trap.png | shotcmp/r25.jpg | 만들 차례 |
| 4. 미국 때문일까 | 흔한 말 하나를 숫자로 | 흐린 날 창가 식은 커피잔 | #6 | Pexels 스톡 영상 | bg/k1/stock/coffee_cloudy.mp4 | shotcmp/r26.jpg | 만들 차례 |
| 4. 미국 때문일까 | 미국 +0.4 vs 한국 +1.5 | 막대 둘 '?' → 열림, 한국 막대 주황 | #2 · #21 | Remotion TallyFrame | bg/k1/board/k1_us_kr_1y.png | shotcmp/r27.jpg | 만들 차례 |
| 4. 미국 때문일까 | 9월까지 넣으면 +0.87 vs +1.61 | 같은 막대에 9월 칸이 덧붙어 자람 | #20 | Remotion TallyFrame | bg/k1/board/k1_us_kr_sep.png | shotcmp/r28.jpg | 만들 차례 |
| 4. 미국 때문일까 | 같은 쪽으로 움직인 달 열에 일곱 vs 다섯 | 163칸 달력 점(같은 쪽 칸만 칠함) 두 장 나란히 | #12 | Remotion TallyFrame(점 칸, calc4_out) | bg/k1/board/k1_samedir.png | shotcmp/r29.jpg | 만들 차례 |
| 4. 미국 때문일까 | 기준금리 2.50 → 2.75 → 3.00 | 계단 두 칸, 날짜 작게 | #1 | Remotion TallyFrame | bg/k1/board/k1_base_steps.png | shotcmp/r30.jpg | 만들 차례 |
| 4. 미국 때문일까 | 2023년 가을 4.2% → 3.6% | 2023 타임라인 바랜 색 | #8 | Remotion TallyFrame(바랜 색) | bg/k1/board/k1_2023.png | shotcmp/r31.jpg | 만들 차례 |
| 5. 고정 끝나는 사람은 얼마나 오르나 | 고정금리 대출 이야기 | 벽걸이 달력 넘기는 손, 한 칸 빨간 동그라미 | #9 | AI 실사 RealVisXL V5.0(이 PC) | bg/k1/ai/calendar_hand.png | shotcmp/r32.jpg | 만들 차례 |
| 5. 고정 끝나는 사람은 얼마나 오르나 | 126만 → 154만, +28만 | 단계 흐름도 '2021 고정 2.98% → 5년 → 남은 원금 × 4.88% × 25년 = ?' | #1 · #16 | Remotion TallyFrame(흐름도) | bg/k1/board/k1_reset_flow.png | shotcmp/r33.jpg | 만들 차례 |
| 5. 고정 끝나는 사람은 얼마나 오르나 | 변동형으로 다시 정하면 +22만 | 같은 흐름도 끝 칸이 두 갈래(고정 +28 · 변동 +22) | #1 | Remotion TallyFrame | bg/k1/board/k1_reset_two.png | shotcmp/r34.jpg | 만들 차례 |
| 6. 그래서 볼 날짜 | 정리 세 줄 | 노트에 세 줄 적는 손 | #9 · #17 | Pexels 스톡 영상 | bg/k1/stock/notebook_hand.mp4 | shotcmp/r35.jpg | 만들 차례 |
| 6. 그래서 볼 날짜 | 날짜 한 줄 찾기(변동·고정·예금) | 체크박스 세 줄 표, 다음 코픽스 발표 11/16 | #13 | Remotion TallyFrame(표) | bg/k1/board/k1_check3.png | shotcmp/r36.jpg | 만들 차례 |
| 6. 그래서 볼 날짜 | 끝 — 숨 쉴 3초 | 해 질 녘 창가 빈 의자·식탁 위 통장(글자 없음) | #19 | Pexels 스톡 영상 | bg/k1/stock/dusk_table.mp4 | shotcmp/r37.jpg | 만들 차례 |

빠진 것: 경쟁이 많이 쓴 '뉴스 헤드라인 캡처'(#3·#10 류)는 남의 자료라 쓰지 않는다 — 대신 우리 원자료 그래프(#20 줌인 연출)로. 캐릭터 일러스트(#6·#7)는 브랜드 규칙(캐릭터 없음, C-18)이라 손·물건 실사로 바꿨다.
