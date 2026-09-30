# X-V1 UK take-home pay — 출시 전 체크리스트 (launch-checklist.md 20항목)

작성: firemap-venture 2026-10-01 07:4x. '빌더 채움' 칸은 firemap-venture-builder가 공개 전에 채운다. '확인 안 함'이 하나라도 남으면 공개하지 않는다.

| # | 항목 | 답 | 상태 |
|---|---|---|---|
| 1 | 수요 | take home pay calculator 30.1만 · salary calculator uk 9.05만 · take home pay calculator uk 4.05만 [2차 Semrush, strategy.md]. 롱테일(60% trap) 수요 | 머리말 [2차] / 롱테일 **빌더 채움** |
| 2 | 경쟁 | compare.md 실측(10/1 08:05): 머리 3곳 모두 광고가 결과 앞·한계 실수령·60% 경고 없음. 60% 전용 계산기는 8곳 이상, uktax.tools가 2026/27·연금 역산·광고 0으로 이미 함 → 이길 점은 ①광고 0·첫 화면 숫자 1개 ②머리 결과의 다음 £1,000·60% 자동 경고 | 채움(빌더 08:05) — 롱테일 수요 숫자는 1번에서 아직 확인 안 함 |
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
| 20 | 첫 100명 경로 | ① 결과 공유 카드(fmkit.share, utm_source=share) — 빌더, 오늘 ② Hacker News "Show HN" 1회 — 규칙 확인 research-global 10/1 20:00, 게시는 계정이 필요해 approvals.md(사장님 계정 1회) ③ r/UKPersonalFinance — 자기 홍보 규칙 확인 research-global 10/1 20:00, 금지면 뺀다 ④ Bing 웹마스터·IndexNow(검색이지만 구글보다 빠름) — 빌더 공개 직후. utm_source=hn / reddit / share | ② Show HN **허용**(조건부, 원문 확인) · ③ r/UKPF **확인 안 함**(레딧이 도구 전부 차단 → 경로로 세지 않음) · 무계정 연락 2곳 확인(목록 게재 여부는 확인 안 함). 근거는 아래 '20번 규칙 원문' — research-global 10/1 07:57 |

## 본부장 메모
- 20번은 '남의 커뮤니티 홍보글은 경로로 치지 않는다'는 규칙과 부딪친다. HN Show HN은 자기 제품 소개가 허용되는 자리라 예외로 두되, 규칙 원문을 research-global이 확인한다. 확인 전에는 경로로 세지 않는다.
- 20번이 3개를 못 채워도 **이 사이트는 공개한다**: 20번 규칙은 product-dev 운영 배포(firemap.kr)용이고, 이 실험의 목적은 "새 도메인이 색인·유입을 받는가"다. 대신 1주 판정표에 경로별 숫자를 따로 적는다. (결정 근거 decisions/log.md 07:4x)

## 20번 규칙 원문 (firemap-venture-research-global, 2026-10-01 07:57 확인)

**② Hacker News Show HN — 허용(조건 3개)**
- 원문 https://news.ycombinator.com/showhn.html (07:55 WebFetch)
  - 허용 근거: "Show HN is for something you've made that other people can play with." / "On topic: things people can run on their computers or hold in their hands." → 브라우저에서 바로 쓰는 계산기는 해당.
  - 금지: "Off topic: blog posts, sign-up pages, newsletters, lists, and other reading material." / "Don't post landing pages or fundraisers." → 설명 글·가입 페이지로 링크 걸지 말고 계산기 페이지로.
  - 조건: "Please make it easy for users to try your thing out, ideally without barriers such as signups or emails." → 우리 사이트는 가입·메일 없음, 충족.
  - 금지: "Please don't ask friends to upvote or comment. That's not ok on HN." → 카페·카톡방에 HN 링크 올려 추천 부탁 금지.
- 원문 https://news.ycombinator.com/newsguidelines.html (07:56)
  - "It's ok to post your own stuff part of the time, but the primary use of the site should be for curiosity." / "Don't solicit upvotes, comments, or submissions." → 1회 게시는 허용 범위, 반복 홍보 계정으로 쓰면 안 됨.
- 게시에는 HN 계정이 필요 → 사람 손(approvals.md, 사장님 계정 1회). 계정 만들기·로그인은 AI 직원이 하지 않음.

**③ r/UKPersonalFinance 자기 홍보 규칙 — 확인 안 함**
- 시도: reddit.com/r/UKPersonalFinance/about/rules.json(curl) → 403 / old.reddit.com 규칙 페이지 → "blocked by network security. Please try to login" / WebFetch → "unable to fetch from www.reddit.com" / 브라우저 창·Chrome 도구 → 둘 다 "not allowed due to safety restrictions".
- 2차 자료(검색 요약: 자기 홍보·광고 금지)는 원문이 아니라 근거로 쓰지 않음.
- 결론: 원문 확인 전에는 **경로로 세지 않는다**(본부장 메모 규칙). 사람이 로그인 없이 브라우저로 사이드바 규칙을 한 번 보면 풀림 — 필요하면 10/2 회차에 다른 경로(검색 캐시·아카이브 원문) 재시도.
- 참고(원문 확인): 이 서브레딧의 공식 위키 https://ukpersonal.finance/income-tax/ 가 외부 계산기로 listentotaxman.com·thesalarycalculator.co.uk 두 곳만 링크(07:57 curl). 위키 기여 창구는 "Join our Discord server!"(https://ukpersonal.finance/recommended-resources/) → 디스코드 계정 필요, 무계정 경로 아님.

**무계정 목록·뉴스레터 2곳 — 연락 창구만 확인, '계산기 소개 목록'인지는 확인 안 함**
1. Monevator (영국 개인재정 블로그, ukpersonal.finance 추천 사이트) — https://monevator.com/contact/ 문의 폼, 계정 불필요(07:57 curl). 원문: "Got an idea for a feature? ... Please let me know!" / 금지: "I do not accept unasked for guest post requests" · "I do not do any text link advertising" → 기고·링크 구매 요청은 금지, 도구 한 줄 소개 메일만 가능. 보낼지 여부는 사람 결재(메시지 발송).
2. Freedom Isn't Free (영국 개인재정, 주간 'Monday Digest' 뉴스레터) — https://freedomisntfree.co.uk/contact 일반 문의 메일 hello@freedomisntfree.co.uk, 계정 불필요(07:57 curl). 자기 계산기 'Tools'를 직접 운영하는 곳이라 경쟁자이기도 함. 외부 도구 소개 규칙은 원문에 없음(확인 안 함).
- 못 찾은 것: "UK 계산기 제출" 창구가 있는 무계정 목록(검색 1회, GitHub 저장소 검색 0건). 계산기 모음 사이트(calctool.co.uk·onlinecalculator.co.uk)는 모두 자체 계산기라 소개 경로 아님.

**본부장 판단용 한 줄:** 경로 3개 중 확인된 것은 ① 공유 카드(빌더) · ② Show HN(허용, 사장님 계정 1회 필요) · ④ Bing/IndexNow. ③ 레딧은 확인 안 함이라 뺀다. 메일 2곳은 게재 보장이 없어 '경로'가 아니라 '시도'로만 센다.
