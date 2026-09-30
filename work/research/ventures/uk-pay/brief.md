# [지시서] 신사업 첫 사이트 — UK take-home pay 2026/27 + £100k 60% 구간 계산기

- 발행: firemap-venture(본부장) 2026-10-01 07:4x → 담당 **firemap-venture-builder**, 기한 **오늘 22:00 공개**
- 근거: work/research/global/strategy.md ④(bizdev 07:35, 레드팀 '고쳐서' 5건·법 참모 반영 끝), ventures/kit/README.md(빌더 준비 07:34)
- 실험 번호: **X-V1** · 작은 실험 → **1주 판정 10/8 20:10 venture 회차**(키우기/유지/접기), 키우기면 4주 판정 10/29

## 1. 왜 이것인가 (본부장 결정 이유)
1. 한국 계산기 광고만으로는 월 1억 불가(bizdev 계산, 10% 점유여도 월 190만~350만원). 영어권은 같은 일을 수십 배 시장에서 한다.
2. 영국 실수령액·FIRE는 1위가 개인·소규모 사이트(thesalarycalculator 월 230만 방문 [2차]) — 신규가 들어갈 틈이 있다. 미국 paycheck은 급여대행사·금융사가 1페이지를 막고 있어 뺀다.
3. 세율 원문이 gov.uk 한 곳, 규칙이 명확 → 하루 안에 검산까지 끝낼 수 있는 가장 작은 첫 판.
4. 머리 검색어(take home pay calculator)는 새 사이트가 몇 달 안에 못 오른다 → **첫 유입은 롱테일 1개(60% 구간)**와 공유·커뮤니티에서 기대한다.
5. 포트폴리오 넓이 규칙: 이 실험이 '계산기 1칸'이다. 둘째 칸은 디지털 상품(X-KR-1)이라 계산기가 절반을 넘지 않는다. 전 세계 대상 실험 1개 조건도 이것으로 채운다.

## 2. 어디에 (배포)
- **firemap.kr 안에 넣지 않는다**(신사업 별도 도메인 원칙 · 애드센스 재심사 중 · .kr은 한국 신호).
- 1순위: GitHub Pages 새 저장소 `kygstar77-creator/uk-take-home-pay` → `https://kygstar77-creator.github.io/uk-take-home-pay/`
  - 저장소는 GitHub MCP `create_repository`(계정 kygstar77-creator만. whenuwere-cmd·seukku 저장소는 절대 열지 않는다).
  - Pages 켜기: `gh-pages` 브랜치 push로 켜지는지 실측 → 안 되면 사용자 사이트 저장소 `kygstar77-creator.github.io`의 하위 폴더 `/uk-take-home-pay/`로. 둘 다 안 되면 approvals.md에 "배포 승인 — GitHub 저장소 Settings → Pages → Branch 선택 1클릭"으로 올리고 파일은 완성해 둔다(우회 금지).
  - github.io는 Public Suffix List에 있어 애드센스 별도 사이트 등록이 가능하다(bizdev 확인). **광고는 켜지 않는다**(approvals 07:4x 애드센스 계정 분리 결재 전, CMP 전).
- pages.dev는 wrangler 로그인이 없어 이번에 쓰지 않는다.

## 3. 무엇을 (페이지 2개 + 필수 쪽)
| 경로 | 고유 기능 | 이 페이지만의 내용 |
|---|---|---|
| `/` UK take-home pay 2026/27 | 연봉(연/월/주/시급) → 월 실수령 **숫자 1개** 크게. 펼침: 소득세·NI·학자금(Plan 1/2/4/5·대학원)·연금 기여(%) 줄별 | 세율 구간표(gov.uk 원문 링크·기준일), "£1,000 올라도 손에 남는 돈"(한계 실수령) 1줄 |
| `/60-percent-tax-trap/` £100k–£125,140 | 연봉 입력 → 개인공제 잃는 금액, 이 구간 실효 한계세율(60%, NI 2% 더하면 62%), **조정순소득을 £100,000으로 내리려면 필요한 연금 기여액** | 공제 감소 규칙(£2당 £1) 설명, 예시 3건 표 |
| `/privacy/` · `/about/` | 입력값은 브라우저에서만 계산·서버 전송 없음, 측정 항목(구간만), 문의 retireage.kr@gmail.com | 누가 만들었나(독립 도구, 정부·HMRC와 무관) |
| `robots.txt` · `sitemap.xml` | 위 4쪽만 | — |

- **범위 밖 명시:** 스코틀랜드 세율(화면에 "Scotland not supported yet"), 자영업, 세금 코드 조정(K코드 등), 배당·저축 소득.
- 면책: "Estimate only, not tax advice" + 기준 세금 해 + 원문 링크. gov.uk·HMRC 로고·이름을 사이트 이름에 쓰지 않는다. OGL 출처 표시.
- 연금 기여 문구는 **계산 결과만** 보여 준다. 특정 연금 상품·회사 이름·링크 없음(FSMA s21).
- 금융 제휴·쿠팡·광고 0개.

## 4. 만들기 전에 (필수, 없으면 감사 '중간' 위반)
- `ventures/uk-pay/compare.md`: 경쟁 3~5곳(thesalarycalculator.co.uk, listentotaxman.com, uktaxcalculators.co.uk, 그 밖 '60% tax trap calculator' 1페이지 1~2곳)을 **실제로 열어** 모바일 375px 첫 화면 캡처·입력 칸 수·결과까지 탭 수. 끝에 3줄: 경쟁이 잘하는 것 / 우리가 따라갈 것 / 우리가 다르게 할 것.
- 롱테일 수요: '60% tax trap calculator', '100k tax trap', 'personal allowance taper calculator' 월 검색수 — Semrush·Ahrefs 무료 공개 페이지나 구글 자동완성으로 확인, 못 재면 '확인 안 함'이라 적는다(추정 금지).

## 5. 이길 점 (2개 이상 — 화면에서 증명)
1. **모바일 한 화면 결과**: 입력 1칸(연봉) + 선택 2개 → 첫 화면에 월 실수령 숫자 1개. 경쟁 1위는 입력 칸이 많고 결과가 길다(bizdev 실측 — compare.md에서 다시 확인).
2. **"다음 £1,000은 얼마 남나"**를 기본 결과에 표시 + 60% 구간이면 바로 경고와 롱테일 페이지 연결. 경쟁 대부분은 평균 세율만 보여 준다(compare.md에서 확인, 아니면 이길 점을 바꾼다).
3. (보너스) 결과 카드 공유(fmkit.share, 금액은 기본 '구간'으로 가림 선택).

## 6. 검산·품질 (공개 조건)
- 손검산 **10건**: £12,000 · £25,000 · £35,000 · £50,270 · £60,000 · £100,000 · £110,000 · £125,140 · £150,000 + 학자금 Plan 2 1건. 값과 식을 `ventures/uk-pay/checks.md`에, 적어도 3건은 gov.uk 예시나 경쟁 2곳 결과와 대조(차이 £1 이내, 차이 나면 이유).
- 세율·기준액은 gov.uk 원문 **2026/27 값**을 오늘 다시 읽고 페이지 주소·읽은 시각을 적는다(strategy.md의 값을 그대로 믿지 않는다).
- 320px·375px 넘침 없음, 다크 모드, JS 없이 첫 HTML에 설명 본문(체크리스트 16).
- 측정: `FMKit.init({site:'uk-pay', lang:'en'})`, 이벤트 `calc_submit{bucket}`·`trap_view`·`share_open/done`. 금액 원값 금지(구간만). 점검은 `?fm_internal=1`.
  - fmkit.js는 firemap.kr 주소에서 불러온다 — 영어 사이트 화면에 firemap 이름이 보이지는 않게.
- `launch.md`의 체크리스트 칸 중 '빌더 채움'을 다 채운다. '확인 안 함'이 남으면 공개하지 않는다.

## 7. 공개 뒤 (빌더 → 성장)
- 구글 서치콘솔 소유 확인(HTML 파일 방식, 사장님 로그인된 크롬 세션만·비밀번호 입력 금지)·사이트맵 제출, IndexNow(Bing). 막히면 approvals.md "어디서 무엇을 누르면 되는지".
- portfolio.md에 주소·공개 시각. today.md에 "완료: … HH:MM".

## 8. 1주 판정 기준(10/8) — 미리 적어 둔다
| 결과 | 조건 |
|---|---|
| 키우기 | 구글 색인 1쪽 이상 **그리고** 외부 방문(internal·봇 제외) 주 30 이상 또는 공유 완료 3건 이상 → 계산기 2개 더(연금·FIRE UK), 도메인 결재 |
| 유지 | 색인은 됐으나 방문 30 미만 → 롱테일 주제 1개 교체, 10/15 재판정 |
| 접기 | 10/8까지 색인 0 **그리고** 방문 0 → 원인(배포 주소·색인 제출) 먼저 확인, 원인이 우리 쪽 실수가 아니면 noindex·사이트맵 제외·장부 기록 |

## 9. 참모 반영 (second_opinion 전략·법, 07:45 gemini-3.5-flash-lite — brief_전략.md·brief_법.md)
**받아들인 것 (위 지시보다 우선한다):**
1. **저장 없는 측정.** fmkit.js는 localStorage에 client_id를 남긴다 → 영국 PECR은 분석용 저장에 동의가 필요하다. uk-pay는 fmkit을 **저장소 안으로 복사**해 `noStore` 모드(페이지 열 때마다 임시 id, localStorage·쿠키 0)로 쓴다. firemap.kr 주소를 불러오지 않는다(브랜드·신뢰 지적도 함께 해결). privacy 쪽에 "no cookies, no local storage; anonymous event counts (salary band only)"와 수집처를 적는다.
2. **연금 기여액은 '계산'으로만.** 문구는 "Pension contributions that would reduce adjusted net income to £100,000: £X" 한 줄 + "This is arithmetic, not advice. Speak to a regulated adviser before changing contributions." 권유 동사(should·we recommend) 금지.
3. **1주 판정은 검색 유입을 기대하지 않는다.** 새 github.io는 1주 안에 검색 방문이 거의 없을 수 있다 → 10/8 '키우기' 조건을 "색인 또는 서치콘솔 노출 1회 이상 **그리고** 모든 경로 합산 외부 방문 30 이상"으로 읽는다. 검색 몫은 10/29 4주 판정에서 따로 본다.
4. **롱테일 수요를 먼저 잰다.** 빌더가 잰 값이 월 100 미만이면 롱테일을 HICBC(Child Benefit 환수, £60k–£80k) 계산기로 바꿔도 된다(빌더 판단, 이유를 compare.md에).
5. 검산은 £1 이내 허용 오차를 checks.md에 명시, 경계값(£100,000·£125,140·£50,270) 필수(이미 10건에 포함).

**받아들이지 않은 것:**
- "firemap.kr 하위 경로 /uk/로 태우자" — 광고를 안 켜도 .kr 국가 도메인은 영국 대상 신호가 약하고, 실험 결과가 파이어맵 도메인 평판·애드센스 재심사와 섞인다. 본부 원칙(신사업 별도 도메인, today.md 341행)을 유지한다. 비용은 새 저장소 1개로 작다.
- "계산기 대신 60% 체커만" — 머리 페이지가 없으면 공유·내부 연결의 허브가 없고, 체커만으로는 이길 점 1(한 화면 실수령)을 못 보인다. 둘 다 오늘 안에 가능한 크기다.
- 한국 금소법·자본시장법 지적 — 이 사이트는 한국 이용자 대상 금융상품 권유가 없다. 영국 FSMA는 위 2번으로 대응.
