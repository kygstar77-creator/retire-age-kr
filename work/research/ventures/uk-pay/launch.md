# X-V1 UK take-home pay — 출시 전 체크리스트 (launch-checklist.md 20항목)

작성: firemap-venture 2026-10-01 07:4x. '빌더 채움' 칸은 firemap-venture-builder가 공개 전에 채운다. '확인 안 함'이 하나라도 남으면 공개하지 않는다.

| # | 항목 | 답 | 상태 |
|---|---|---|---|
| 1 | 수요 | take home pay calculator 30.1만 · salary calculator uk 9.05만 · take home pay calculator uk 4.05만 [2차 Semrush, strategy.md]. 롱테일(60% trap) 수요 | 머리말 [2차] / 롱테일 **빌더 채움** |
| 2 | 경쟁 | 1등 thesalarycalculator(광고·복잡한 화면). 이길 점 2개는 brief 5장 | **빌더 채움**(compare.md 실측 후 확정) |
| 3 | 사용자 | 30초: 연봉 입력 → 월 실수령 확인 → 60% 구간이면 경고 클릭. 공유 이유: 연봉 협상·이직 비교. `second_opinion.py brief.md 사용자` | **빌더 채움**(결과 한 줄) |
| 4 | 돈 | 첫 1주 광고 0 → 수익 0원(의도). 판정 목적은 색인·유입 시험. 키우기 시 애드센스(RPM 약 $2 [2차 약한 근거]) — 로드맵 10월 기여 0원, '시험 중 엔진' | 답함 |
| 5 | AI 시대 가치 | AI 채팅도 실수령을 대략 알려 준다. 우리만: 원문 링크·기준일 달린 정확 계산, 60% 구간 연금 기여액 역산, 결과 카드 | 답함 |
| 6 | 정책 | 광고 없음 → 애드센스 영향 없음. 페이지 4개·찍어낸 페이지 0(scaled content 해당 없음). 유튜브·네이버·쿠팡 무관 | 답함 |
| 7 | 법 | 영국 FSMA s21: 금융상품 홍보 없음(연금 기여는 계산만, 상품명 없음). UK GDPR: 입력값 브라우저 계산·서버 전송 없음, 측정은 구간만 → 개인정보 최소. 광고·CMP는 켜지 않음(결재 대기). gov.uk OGL 출처 표시. 사칭 금지(이름·로고) | 답함(법 참모 strategy_법.md) |
| 8 | 사람 손 | 고객 응대 없음(문의 메일만, 응답 의무 없음 문구). 세금 해 바뀔 때 갱신은 AI 직원(다음 해 4/6 전, 담당 venture-builder) | 답함 |
| 9 | 발행 패턴 | 페이지 4개 1회 공개. 반복 발행 없음 | 답함 |
| 10 | 측정 | fmkit site=uk-pay, calc_submit{bucket}·trap_view·share, utm 자동 | 운영 도착 확인 **빌더 채움** |
| 11 | 판정 | brief 8장(1주 10/8, 키우기면 4주 10/29) | 답함 |
| 12 | 되돌리기 | 저장소 Pages 끄기 또는 robots noindex 커밋 1개. 담당 venture-builder | 답함 |
| 13 | 격리 | kygstar77-creator 계정·새 저장소만. 스꾸(whenuwere-cmd) 저장소·Cloudflare·Supabase d7ff3fad 닿지 않음. 측정은 파이어맵 Supabase c7cd8a90 | 답함 |
| 14 | 놓친 것 | 레드팀(strategy_레드팀.md): 머리 검색어 비현실 → 롱테일, CMP, 4주 기준 롱테일. 추가 확인: 세금 해 표기 오류 시 신뢰 손상 → 기준일 크게 | 답함 |
| 15 | 검색 위젯 | 구글이 결과 화면에서 영국 실수령을 바로 계산해 주는지 | **빌더 채움**(구글 검색 1회 캡처) |
| 16 | 색인 제출 | 사이트맵·서치콘솔·IndexNow, JS 없이 본문 | **빌더 채움** |
| 17 | 법 개정 감시 | 영국 세금 해 4/6 시작. 매년 3월 Budget·Spring Statement 뒤 확인, 담당 venture-builder, 달력 2027-03-20 | 답함 |
| 18 | 공개 설정 되읽기 | 공개 후 curl로 robots·sitemap·noindex 없음 확인 | **빌더 채움** |
| 19 | 내부 방문 제외 | 점검은 ?fm_internal=1 | **빌더 채움**(internal:1 확인) |
| 20 | 첫 100명 경로 | ① 결과 공유 카드(fmkit.share, utm_source=share) — 빌더, 오늘 ② Hacker News "Show HN" 1회 — 규칙 확인 research-global 10/1 20:00, 게시는 계정이 필요해 approvals.md(사장님 계정 1회) ③ r/UKPersonalFinance — 자기 홍보 규칙 확인 research-global 10/1 20:00, 금지면 뺀다 ④ Bing 웹마스터·IndexNow(검색이지만 구글보다 빠름) — 빌더 공개 직후. utm_source=hn / reddit / share | 경로 ②③ 규칙 확인 전이면 ①④만으로 공개하고 10/2에 보강 — **3개 조건은 ②③ 확인 뒤 채움** |

## 본부장 메모
- 20번은 '남의 커뮤니티 홍보글은 경로로 치지 않는다'는 규칙과 부딪친다. HN Show HN은 자기 제품 소개가 허용되는 자리라 예외로 두되, 규칙 원문을 research-global이 확인한다. 확인 전에는 경로로 세지 않는다.
- 20번이 3개를 못 채워도 **이 사이트는 공개한다**: 20번 규칙은 product-dev 운영 배포(firemap.kr)용이고, 이 실험의 목적은 "새 도메인이 색인·유입을 받는가"다. 대신 1주 판정표에 경로별 숫자를 따로 적는다. (결정 근거 decisions/log.md 07:4x)
