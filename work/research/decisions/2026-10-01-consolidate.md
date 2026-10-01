# 레드팀: 실험을 firemap.kr 한 사이트에 모을까 (2026-10-01 17:4x)

사장님 질문(17:2x): "한 사이트에 다 모으면 어떻게 되는데? 파이어맵 웹사이트에 새로운 화면을 만들어서 다 모으면 되는 거 아닌가."
대상: X-V1 영국 실수령(영어) · X-CN-1 시험 일정(한능검·토익) · 나라별 계산기 허브(global-calcs). 레드팀 참모(redteam-prompt.md 역할), 파일 읽기와 공개 원문 대조만 했다.

## 판정: 고쳐서 — 셋 다 firemap.kr 밖. 대신 사람 손을 "실험마다 1번"에서 "딱 1번"으로 줄인다

## 1. 사실 대조
| 주장 | 판정 | 근거 |
|---|---|---|
| 모으면 구글 '사이트 평판 남용'에 걸린다 | **틀림** | 이 정책은 **제3자 콘텐츠**만 대상이다. 원문: "applies where third-party content is published on a host site mainly because of that host's already-established ranking signals" ([spam-policies](https://developers.google.com/search/docs/essentials/spam-policies), 갱신 2026-08-28). 우리 실험은 우리가 만든 1자 콘텐츠다 |
| '대량 생성'은 모으면 위험, 나누면 안전 | **틀림(반쪽)** | 같은 원문 예시에 "Creating multiple sites with the intent of hiding the scaled nature"가 있다. 위치가 아니라 쪽의 모양(금액별 쪽 찍어내기)이 문제다. 모으든 나누든 금액별 쪽 금지 규칙은 그대로 |
| 모으면 도메인 신뢰가 쌓인다 | **대부분 틀림(지금 기준)** | firemap.kr 구글 site: 약 3쪽(/, /privacy, /disclaimer), 사이트맵 6/15 뒤 안 읽힘(growth/daily.md 10/1 07:4x). 빌려줄 신뢰가 거의 없다 |
| `/en/uk/...` + hreflang으로 영국 노출 | **틀림** | hreflang은 같은 쪽의 언어·지역판이 여럿일 때 쓴다("multiple versions of a page for different languages or regions", [localized-versions](https://developers.google.com/search/docs/specialty/international/localized-versions), 2026-09-21). 영국 계산기는 한국어 짝이 없다. 그리고 .kr은 국가 도메인이라 "strong signal ... explicitly intended for a certain country", 단점 "Single country only"([multi-regional](https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites), 2025-12-10) |
| 재심사 중 넣어도 따로 심사된다 | **틀림** | 애드센스는 "we may review all pages of your site"([81904](https://support.google.com/adsense/answer/81904)). 하위 도메인도 기존 사이트의 일부로 묶는다("subdomains that are part of an existing site", [12170421](https://support.google.com/adsense/answer/12170421)). 영어 쪽이든 시험 일정이든 넣으면 재심사 대상이 된다 |
| firemap.kr 껍데기에 영국 쪽을 얹으면 그대로 써도 된다 | **틀림** | 운영 firemap.kr 머리에 애드센스 코드가 들어가 있고(curl 17:4x, work/build-deploy.mjs 주입), CMP는 없다(fundingchoices 0). 영국 사용자 광고는 인증 CMP가 있어야 맞춤 광고 대상([13554116](https://support.google.com/adsense/answer/13554116)), 저장소 사용은 PECR 동의 문제(uk-pay/brief.md 9장 1번). 정적 HTML로 빼면 피할 수 있으나 그게 곧 '따로'다 |
| 한 번 제재되면 전부 피해 | **맞음(방향)** | 애드센스는 사이트·계정 단위로도 막는다(같은 계정 = 유튜브 수익 계정, memory firemap-monetization). 한 사이트 위반이 계정으로 번지는 조건 원문은 확인 안 함 |
| 새 저장소는 사람 손이 든다 | **맞음** | uk-take-home-pay·exam-dates-kr·kygstar77-creator.github.io 모두 404(curl 17:41). 결재함 17·18행, X-V1은 17:01 휴대폰 승인됐으나 PC 작업이라 미실행 |

## 2. 실험별 결론
- **X-V1 영국 실수령(금융·세금, 영어): 따로.** .kr 국가 신호·hreflang 부적합·CMP/PECR·재심사 오염 네 가지가 모두 불리, 이득은 저장소 1개 아낌뿐.
- **나라별 계산기 허브(금융·세금, 영어): 따로**(X-V1과 같은 집, plans/global-calcs.md 그대로). 예외 하나: '한국인이 보는 해외 실수령'(한국어, /fire-city 47쪽과 같은 결)은 파이어맵 주제와 맞으니 재심사 결과 뒤 product-dev 후보 — 수요 확인 안 함.
- **X-CN-1 시험 일정(비금융, 한국어): 따로.** .kr 문제는 없지만 ① 9/30 규칙 "firemap.kr에는 은퇴·노동·대출·세금만"(meeting/2026-09-30-decisions.md 83행) ② 실험 설계가 'firemap.kr 새 글 1편 = 대조군'이라 안에 넣으면 대조군이 사라진다(plans/content-network.md) ③ 재심사 중 새 주제 2쪽은 '미완성' 신호가 될 수 있다.

## 3. 재심사 중 지금 넣어도 되나
**안 된다.** 넣는다면 조건(재심사 결과 통지 뒤에만): 한국어 + 파이어맵 주제(은퇴·노동·대출·세금) + 쪽마다 직접 쓴 문장·계산 방법 HTML 미리 그림 + 금액별 쪽 0. 시험 삼아 넣을 거면 noindex·메뉴 미노출·sitemap 제외 — 단 noindex는 구글 검색만 막을 뿐 애드센스 검토 범위에서 빠지는지는 확인 안 함이라 재심사 중에는 이것도 하지 않는다.

## 4. 더 나은 대안(사람 손 1번으로 끝)
- **A(추천): 실험 마당 저장소 하나.** github.com/new에서 `kygstar77-creator.github.io` 한 개만 만든다 → `/uk-take-home-pay/`, `/exam-dates-kr/`, 이후 실험 전부 하위 폴더(uk-pay/brief.md 18행이 이미 적은 예비안). github.io는 공용 접미사 목록이라 firemap.kr·애드센스와 분리, 다음 실험부터 사람 손 0. 대가: GitHub Pages는 서버 301이 없어 졸업 때 새 도메인 이전이 메타 새로고침뿐(순위 이전 손실 정도 확인 안 함).
- B: 결재함 17·18행을 묶어 사장님 PC 1분(지금 계획 그대로).

## 5. 목표선 비판
두 실험 모두 10월 광고 0원 설계라 이번 달 목표(10/30 월 10만원)에 보탬 0. 어디에 둘지 회의에 시간을 더 쓰지 말고, 10월 돈은 firemap.kr 재심사 통과(콘텐츠 품질)에 집중한다. 모으기는 그 통과에 위험만 더한다.

## 판정을 바꿀 조건 1개
애드센스 재심사가 승인되고 firemap.kr 구글 색인이 계산기·가이드 30쪽 이상으로 올라가면(빌려줄 신뢰가 생기면), X-CN-1 같은 한국어 비금융 실험은 firemap.kr 하위 경로 시험을 다시 따져 본다. 영어·영국은 .kr이라 그때도 따로.
