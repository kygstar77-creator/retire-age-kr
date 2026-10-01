# G12 Google Workspace 애드온 — 경쟁·가격·리뷰 불만·검증 요건 (compare.md)

> 조사: firemap-venture-research-global, 2026-10-01 10:12~10:2x. 요청 근거 plans/g12-workspace-addon.md '다음' ①~④.
> 측정 방법: Marketplace 앱 화면은 `curl ?hl=en` 원본 HTML의 aria-label 값(설치·평점)과 내장 브라우저 Reviews 탭(기본 정렬 'Helpful' 첫 10개). 가격은 각 회사 가격 페이지·결제 페이지 원문. 로그인 없음.
> 주의: 영어 화면은 설치 수를 '1M+'처럼 반올림해 보인다. 기획서의 '167만+·97만+·113만+'(08:4x 한국어 화면)와 단위가 다르다 — 둘 다 화면 값이고 모순 아님.

## ① 경쟁 — 설치·평점·가격 (Marketplace 화면 10:1x)

| # | 앱 (개발사) | 하는 일 | 설치 | 평점(평가 수) | Marketplace 가격 표기 | 실제 가격표 원문 |
|---|---|---|---|---|---|---|
| 1 | Form Publisher (Form Publisher) | 폼 응답→문서·PDF 생성·승인 | 24M+ | 4.58 (4,264) | Free of charge with paid features | Free $0: 월 20건·1 user / Individual **$99 billed annually**($8.25/월) 무제한 / Business **$690 billed annually** 도메인 무제한 [form-publisher.com/pricing] |
| 2 | Form Approvals (Form Approvals LLC) | 응답 승인 흐름 | 10M+ | 4.7 (1,197) | Free of charge with paid features | Free $0: 월 응답 20건 / Individual **$96/12개월**(또는 $36/3개월) 월 100건 / Team **$600/12개월** 월 1,000건. "No per-seat pricing", 관리자만 라이선스 [formapprovals.com/pricing] |
| 3 | CAPY: Form Choice Eliminator & Choice Limiter (AddonForge) | 선택지 수량 제한 | 8M+ | 4.77 (2,880) | Free of charge trial | Trial 7일 / 1 Year **$39.00/yr**(per user) / Lifetime **$99.00**(per user) [addonforge.thrivecart.com/choice-limit/ 결제 화면] |
| 4 | CLOSY: Form Limiter & Response Limit via Sheet (AddonForge) | 응답 수 제한(시트 값 기준) | 975K+ | 4.67 (252) | Free of charge trial | 1 Year **$24.00/yr** / Lifetime **$59.00** [addonforge.thrivecart.com/limit-form/] |
| 5 | PerformFlow (performflow) | 승인 흐름+문서 생성 | 1M+ | 4.37 (162) | Free of charge with paid features | Free $0: 월 이메일 100통(약 25건) / Individual **$6.50/월(6개월)·$9/월(1개월)** / Team **$29/월(6개월)·$39/월(1개월)**, 30일 환불 [performflow.com/pricing] |
| 참 | FORMeleon (AddonForge) | **현재 제목 "Choice Limit by Spreadsheet Value"**(9/28 갱신, 기획서의 '선택지 수량 제한'과 같은 계열) | 1M+ | 4.58 (304) | Free of charge trial | $24.00/yr · Lifetime $59.00 [addonforge.thrivecart.com/start-and-stop-form/] |
| 참 | Form Limiter: Response Limit & Choice Eliminator (개발사 확인 안 함) | 응답 제한+선택지 제한 | 1M+ | 4.86 (543) | Free of charge trial | 확인 안 함 |
| 참 | Choice Eliminator Lite (Accemy & SW gApps) | 선택지 제거(옛 1위) | 9M+ | **2.76 (102)** | Not available | — |
| 참 | FREE Form Approvals Workflow Form Publisher - Bolo | 승인+문서 | 283K+ | 4.58 (114) | Free of charge | 무료(2023-12-27 이후 갱신 없음) |

- 보이는 구조: AddonForge 한 회사가 같은 기능을 이름만 바꿔 7개 이상 운영(CAPY·LIMIT IT·Choice Eliminator X·CLOSY·FORM PAL·FORMeleon·SEAL — addonforge.com 메뉴), 자칭 "Over 25 MIO installs". 가격은 연 $24~39 또는 평생 $59~99, 사용자당.
- 가격대 요약(원문 값만): 유틸형 **연 $24~$39 / 평생 $59~$99**, 문서·승인형 **연 $96~$99(개인)·$600~$690(팀)**, 월 구독형 $6.50~$39.
- 결제 수단: AddonForge = ThriveCart 결제 페이지(외부). 다른 회사 결제 수단은 확인 안 함.

## ② Google OAuth 검증 — 원문

| 항목 | 원문 | 출처 |
|---|---|---|
| 검증 필요 없는 경우 | "personal use (fewer than 100 users)" · "development/testing/staging mode" · 서비스 계정만 · "only used by people in your Google Workspace or Cloud Identity organization" · 관리자가 trusted apps에 추가 | support.google.com/cloud/answer/13464323 |
| Apps Script 예외 | "Verification isn't required for Google Apps Script projects whose owner and users belong to the same Google Workspace domain or customer." | developers.google.com/apps-script/guides/client-verification |
| 민감·제한 범위 공통 요구 | 브랜드 검증(홈페이지·개인정보처리방침·도메인 소유), 기능 시연 영상(OAuth 동의 화면 포함), Limited Use 준수, 최소 범위 | support.google.com/cloud/answer/13464321 |
| 제한 범위 추가 요구 | "Annual security assessment from a Google empanelled group of security assessors" (CASA) | 같은 곳 |
| 기간 | Brand "2-3 Business days" · Sensitive "10 Business days" · Restricted "6 weeks" ("not guaranteed") | support.google.com/cloud/answer/13463817 |
| 비용 | "Google does not charge the developer any fees for security assessment." 평가 비용은 "agreed on between the developer and the assessor without any involvement from Google" | 같은 곳 |
| CASA 실제 금액 | 2차 출처만: "$500-$4,500", TAC Security Tier 2 "$540 per year" — **Google 원문 아님, 평가사 가격표 직접 확인 안 함** | deepstrike.io 블로그 (WebSearch 요약) |
| 응답 시간(Apps Script) | "Most verification requests receive a response within 24 to 72 hours." | apps-script/guides/client-verification |

**범위(scope) 분류 — 원문으로 확인된 것과 안 된 것**
- `forms.currentonly` 설명: "View and manage forms that this application has been installed in" (developers.google.com/identity/protocols/oauth2/scopes). **민감도 분류는 이 표에 없음 → 확인 안 함.** 2차 출처(Medium 개발자 후기)는 "검증 대상 아님"이라 쓰지만 Google 원문 아님.
- `spreadsheets.currentonly`: Sheets API 범위표(민감도 표기 있는 표)에 **없음**. 애드온 범위 문서엔 "Grants temporary access to the open spreadsheet's content", "only available within Apps Script Services" (workspace/add-ons/concepts/workspace-scopes). 분류 확인 안 함.
- 같은 Sheets 표의 원문 분류: `spreadsheets` Sensitive · `spreadsheets.readonly` Sensitive · `drive.file` "Recommended Non-sensitive" · `drive` Restricted · `drive.readonly` Restricted (developers.google.com/workspace/sheets/api/scopes).
- 경쟁사가 실제로 요구하는 권한(Marketplace Permissions 탭 원문): AddonForge 앱 = "View and manage forms that this application has been installed in"(=forms.currentonly) + "only the specific Google Drive files you use with this app"(=drive.file) + "Send email as you" + "Connect to an external service" + "Allow this application to run when you are not present". 즉 **1위 유틸들은 제한(Restricted) 범위 없이 돈다** — CASA 없이 가능한 구성이라는 실례. 반면 Form Publisher·Choice Eliminator Lite는 "all of your Google Drive files"(=drive, Restricted)를 요구.
- 미검증 앱 사용자 상한 숫자: 확인 안 함(support.google.com/cloud/answer/9028764 본문에 숫자 없음).

## ③ 리뷰 1~2점 불만 (Reviews 탭 'Helpful' 정렬 첫 10개, 10:1x)

| 앱 | 첫 10개 별점 | 1~2점 원문(짧게) |
|---|---|---|
| CAPY (8M+) | 2·1 포함 | 2★ "Now that free tier no longer exists … completely useless if you don't pay." / 1★ "within a day noticed that the selection limiting was not working. When I checked, CAPY said I have to pay $37 … nothing about a fee during setup" |
| Choice Eliminator Lite (9M+) | 2412231411 | 2★ "I have only been able to use this app successfully once … people choosing the options that are supposed to be removed" / 1★ "There is no configure link/option" / 1★ "What happened to allowing limits? … signing students up for band lessons" |
| Form Publisher (24M+) | 4515555155 | 1★ "They now ONLY have email support … extremely slow" / 1★ "Very hard to figure out how to use … no tutorial" |
| Form Approvals (10M+) | 1~2점 1개 | 2★ "I am not receiving email from the requestor" |
| CLOSY (975K+) | 1555555555 | 1★ "App requires you to give a five star review before any features become available" |
| PerformFlow (1M+) | 5555555453 | 1~2점 없음 |

**불만 상위 3 (위 표에서 센 것, 표본 60개 중 1~2점 13개)**
1. **돈 벽이 늦게 나온다** — 설정·배포 끝난 뒤 유료 요구, 무료 등급 폐지, 별점 강요(CAPY 2, CLOSY 1). → 3건
2. **제한이 조용히 안 걸린다 / 설정 메뉴가 안 보인다** — 지워야 할 선택지가 그대로 선택됨, configure 없음, 수량 허용 기능 사라짐(Choice Eliminator Lite 7, CAPY 1★은 1번과 겹침). → 7건(+겹침 1)
3. **사용법·지원 부족** — 튜토리얼 없음, 이메일 지원만(Form Publisher 2), 알림 메일 안 옴(Form Approvals 1). → 3건
- 표본 한계: Helpful 정렬 첫 10개만. 'Recent' 정렬·더 보기는 화면에서 바뀌지 않아 확인 안 함. 레딧 등 외부 불만은 확인 안 함.
- 기획서 2장 '다른 한 가지' 후보 재료: ①·② 둘 다 **첫 사이드바에서 '무엇이 무료이고 지금 제한이 걸려 있는가'를 보이는 것**으로 묶일 수 있으나, 고르는 것은 기획자·예술가 몫(여기선 정하지 않음).

## ④ Marketplace 공개 심사 기간
- 원문: "App review typically takes several days." 요건: OAuth 검증 통과, 링크가 모두 작동, "fully functional and not meant for testing purposes", Google 상표·로고 미사용 (developers.google.com/workspace/marketplace/about-app-review).
- 정확한 일수: 원문에 없음 → 확인 안 함. OAuth 검증(민감 범위면 영업일 10일)이 앞에 붙는다.
- 개인정보처리방침: 브랜드 검증 요구 항목에 포함(②). Marketplace 단독 필수 여부 문구는 확인 안 함.

## 결재 관련(사실만)
- Google Cloud 프로젝트·Marketplace SDK 등록·개발자 계정: 계정 생성 = 사장님 결재 대상. Marketplace 개발자 등록비는 확인 안 함.
- CASA는 제한 범위를 안 쓰면 해당 없음(②의 원문 요건). 비민감 범위로만 구성하면 검증 자체가 필요 없는지는 `forms.currentonly` 분류 미확인이라 **확인 안 함**.
