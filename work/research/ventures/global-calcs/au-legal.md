# 호주 첫 판 법 근거 — 금융상품 조언·세무대리·ATO 저작권 (au-legal.md)

- 요청: today.md [기획 요청·조사 요청] global-calcs, 시한 10/8 20:00 (plans/global-calcs.md 8장 "호주 원문 확인 안 함" 칸).
- 조사: firemap-venture-research-global, 2026-10-02 14:27~14:40 KST. 로그인 없음. 법률 자문 아님 — 원문 문구와 그 조건만 옮김.

## ① ATO 저작권 (원문 직접 확인, 내장 브라우저 — curl·WebFetch는 403)
- 주소: https://www.ato.gov.au/about-ato/using-our-website/copyright-notice · 쪽 표기 "Last updated 27 August 2012", QC17043.
- 원문 핵심(짧은 인용): "free to copy, adapt, modify, transmit and distribute this material as you wish" — 단 ATO나 연방정부가 **우리 또는 우리 서비스를 보증하는 것처럼 보이는 방식은 금지**.
- 로고·문장(紋章) 예외 문구는 이 쪽에 **없음**(확인함). 그래도 plans 7장 금지(ATO 이름·로고를 사이트 이름에) 그대로 두면 충분.
- 할 일: 대조표 쪽 문구 "Checked against the ATO Tax withheld calculator on <날짜>" = 사실 서술 → 가능. "ATO-approved/official" → 금지.

## ② 금융상품 조언(AFS 면허) — ASIC 일반 계산기 면제 (원문 확인)
- 원문: ASIC Corporations (Generic Calculators) Instrument **2026/41**, https://www.legislation.gov.au/F2026L00271/latest/text (as made 2026-03-18). 2016/207을 이어받음, **2031-04-01 폐지 예정**(s9). 근거 조항 Corporations Act s926A(2)(a)·s951B(1)(a).
- 대상 정의: "financial calculator" = 금융상품에 관한 수치 계산 도구, **superannuation calculator는 제외**.
- 면제 조건(s8) 요약: ① 특정 금융상품을 광고·홍보하지 않음 ② 법정 가정 외 가정은 사용자가 바꿀 수 있음 ③ 기본 가정이 합리적 ④ 화면에 목적·한계 설명, 가정 설명, 2년 넘는 기간이면 현재가치 표시, 그리고 "not intended to be relied on for the purposes of making a decision in relation to a financial product" 경고 ⑤ 결과를 인쇄·저장할 수 있음 ⑥ 기록 7년 보관.
- **우리 실수령 계산기에 대한 읽기:** 소득세·Medicare·HELP는 '금융상품'이 아니므로 이 면제가 꼭 필요한지부터 확실치 않다(원문에 세금 계산기 언급 없음 — 판단은 확인 안 함). 그러나 조건이 싸므로 **조건 ①·④·⑤를 그냥 지키는 것**을 권함: 상품 링크 0, 한계·가정·경고 문구 1줄, 결과 인쇄/복사 버튼. ⑥ '기록 7년'은 우리가 사용자 입력을 저장하지 않으면 남길 기록이 없음 — 저장 안 함을 쪽에 명시.
- **연금(super) 줄 주의:** 고용주 SG 12% 같은 법정 금액 한 줄 표시는 계산 결과 일부지만, '은퇴 때 super 잔액 예측'을 붙이면 별도 Instrument 2022/603(super 계산기·은퇴 추정, 기본 가정 법정, 2027-07-01 폐지 예정 — 2차 출처 ASIC 뉴스·로펌 글, 원문 조건 표는 확인 안 함) 대상. → **호주 첫 판에는 super 잔액 예측 칸을 넣지 않는다.** (compare.md의 '은퇴·연금 0/5' 차별점을 호주에 적용하려면 2022/603 원문 조사가 먼저.)

## ③ 세무대리(Tax Agent Services Act 2009) — TPB 지침 (원문 확인)
- s50-5 위반 요건(TPB 요약·AustLII): 세무대리 서비스이고 + **수수료나 다른 보상을 받고** + 미등록. s90-5 정의는 세법상 의무·권리를 산정·조언하는 서비스로, **"reasonably be expected to rely"** 상황에서 제공될 것.
- TPB(GS) 44/2023 https://www.tpb.gov.au/tpb-gs-44-2023-what-is-tax-agent-service 의 판단 요소(원문 목록 중): 개인 사정에 법을 적용하는가, 의뢰인이 요청·결제했는가, 다른 전문가를 권했는가, **효과적인 면책 문구가 있는가(단 문구만으로 자동 면제 아님)**.
- 읽기: 무료·익명·일반 계수표 계산은 개인 맞춤 조언·결제가 없어 위 요소 대부분에 걸리지 않는다. 다만 광고 수익이 'other reward'인지는 TPB(I) 40/2023에 있을 수 있음 — **확인 안 함**(PDF 미열람).
- 할 일: 결과 아래 "Estimate only, based on ATO Schedule 1 (2026–27). Not tax advice — for your situation, use the ATO calculator or a registered tax agent." + ATO 계산기 링크. 개인 상담·질문 답변 기능(챗봇 등) 넣지 않음.

## 한 줄
호주 첫 판은 **상품 링크 0 · 경고/가정/한계 문구 · 인쇄 버튼 · super 예측 없음 · '보증' 표현 없음**이면 원문상 막히는 곳 없음. 남은 '확인 안 함' 2개: 광고 수익이 TASA 'reward'인지(TPB(I) 40/2023), 2022/603 원문 조건.

## 출처
- ATO copyright: https://www.ato.gov.au/about-ato/using-our-website/copyright-notice
- ASIC 2026/41 원문: https://www.legislation.gov.au/F2026L00271/asmade/2026-03-18/text/original/epub/OEBPS/document_1/document_1.html · ASIC 뉴스 https://www.asic.gov.au/about-asic/news-centre/news-items/asic-updates-relief-instrument-for-generic-financial-calculators/
- TASA s50-5: https://www.austlii.edu.au/cgi-bin/viewdoc/au/legis/cth/consol_act/tasa2009197/s50.5.html · TPB(GS) 44/2023 위 주소
- 2022/603(2차): https://www.asic.gov.au/about-asic/news-centre/news-items/asic-updates-superannuation-forecasts-relief-instrument/
