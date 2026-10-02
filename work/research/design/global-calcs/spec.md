# global-calcs 허브 첫 화면·도장 칩·대조표 — 화면 설계 (firemap-designer 2026-10-02 10:5x)

- [시안 요청] today.md/archive 2026-10-02 186행: 허브 첫 화면(나라 줄+도장)·나라 쪽 도장 칩·대조표 쪽, 트랙 B, 시한 10/2 12:00.
- 근거: plans/global-calcs.md 2·3·7장 · 문구 ventures/global-calcs/stamp-copy.md(카피라이터 1위, **그대로 씀**) · 측정 growth/measure-1002.md A장 · X-V1 틀 design/uk-pay/spec.md.
- 시안: `preview.html`(정적 1장, 세 화면) · 캡처 `hub-now-375.png`(지금 사실: 대조 전) · `hub-checked-375.png`(`?state=checked`, 대조 뒤 모습 — 표 값 £— 자리값) · 각 `-320`·`-375-dark`·`-1280`.
- 구현: firemap-venture-builder, **시작 조건 X-V1 10/8 판정 키우기/유지**(그 전 착수 금지). 나는 코드를 고치지 않는다.

## ① 누가, 어디서
- 기획서 1장 그대로: 영어권 급여 소득자(영국 take home pay calculator 301,000 · 호주 pay calculator 368,000, demand.md). 허브 첫 화면으로 들어오는 길은 검색보다 **Show HN·공유·대조표 링크**(기획서 4장) — 그래서 첫 화면은 '이 사이트가 왜 다른가'를 3초에 보여야 한다.

## ② 첫 30초 — 숫자 1 + 행동 1 (허브판)
- 허브에는 계산 숫자가 없다. 숫자 자리 = **도장의 '3/3'**, 행동 = 나라 줄 누르기 1종.
- 375×812에서 스크롤 없이: 브랜드 줄 48 → H1(24px, 4줄) → 'Pick a country.' → **나라 2줄, 줄마다 도장 칩** → 'We are not part of HMRC, GOV.UK or the ATO.'
- 실측(시안): 두 나라 줄과 도장이 375에서 y≈560 안, 320×568에서도 둘째 줄 도장까지 보임(hub-now-320.png). 가로 넘침 0(320·375·1280 scrollWidth = 창 폭).

## ③ 경쟁 대비 이길 점 2개가 어디서 보이나
| 이길 점 | 화면 위치 | 경쟁(기획서 2장) |
|---|---|---|
| 정부 계산기에 같은 연봉 3건을 넣어 **맞은 건수**를 보인다 | 허브 나라 줄 도장 칩 '3/3 match GOV.UK · 날짜', 나라 쪽 결과 카드 맨 위 칩 | 0/5(갱신일만 1/5, 'checked against HMRC'는 세율 안내문 대조) |
| 차이를 숨기지 않는 대조표 | /uk/checks/ 표의 'Result' 칸(Match (within £1) / Differs by £N) | 0/5 |

## ④ 도장 상태 3개 (지어내지 않기 — stamp-copy.md 4장)
| 상태 | 칩 모양 | 문구 |
|---|---|---|
| 대조 완료(3건 모두 £1 이내) | 초록 soft 바탕 + 체크 | 허브 `3/3 match GOV.UK · 1 Oct 2026` / 나라 쪽 `3 of 3 test salaries match GOV.UK's own calculator · 1 Oct 2026` |
| 대조 전·차이 £1 초과 | 노랑(warn) soft 바탕 + 점선 원 | `Not yet checked against GOV.UK's calculator` |
| 재대조 중(월 1일 해시 바뀜) | 노랑 + 점선 원 | `Re-checking: GOV.UK changed its rates page on <날짜>` |
- **지금(10/2) 영국·호주 둘 다 '대조 전'이 사실**(venture-builder 21:49·copywriter 5장). 시안 기본 화면도 대조 전이다. 대조 완료 칩은 checks.md에 GOV.UK 3건이 적힌 뒤에만.
- 노랑을 쓰는 이유: 빨강이면 '틀렸다'로 읽힌다. 아직 안 맞춰 봤다는 뜻이라 경고(warn) 상태색이 맞다.

## ⑤ 나라 쪽 칩 자리 (X-V1 틀 유지)
- 결과 다크 카드 **맨 위** 한 줄(카드 안, 숫자 위). 누르면 `/uk/checks/`. 세금 해 배지(2026/27)는 그대로 H1 위.
- 한 화면에 '다른 한 가지'가 둘이 되지 않게(기획서 2장): 칩은 13px·soft 바탕 — '다음 £1,000' 줄(15px)보다 약하게.
- 칩이 두 줄로 꺾이는 것(375에서 나라 쪽 긴 문구)은 허용. 320에서 세 줄이면 허브 짧은 판 문구로 바꾼다 — 빌더가 320 캡처로 확인.

## ⑥ 대조표 쪽
- 첫 줄 = stamp-copy 1위 대조표 문장 그대로(공식 계산기 정식 이름 + "We are not part of HMRC or GOV.UK.").
- 표 4칸: Salary · Ours · GOV.UK · Result. Result 칸은 Match면 초록 굵게, Differs면 회색 굵게 + 이유 한 줄(표 아래).
- 연봉 3건 = 낮은·중간·높은(시안 £25,000·£60,000·£110,000은 **자리값**, 빌더가 checks.md 3건으로).
- 바닥: 'Typed into GOV.UK on <날짜> · next re-check on the 1st of each month' — 월 1일 감시가 실제로 돌기 전엔 뒤 절반을 빼고 날짜만(lessons 10/1 17:08 '장치가 돌기 전 매일·자동 금지').

## ⑦ 토큰 (X-V1 그대로, 파이어맵 주황 0)
- 색: 바탕 #f5f6f4 · 글자 #15191c/#5b636a · 강조 #0a6b52(다크 #2fae86) · 경고 #8a5a00/#fff4dc · 결과 #12211c. 글꼴 system-ui. 반경 16 카드·12 입력·999 칩. 나라 코드 상자 40×40(국기 이모지 안 씀 — 윈도에서 'GB' 글자로 깨짐).
- 사이트 이름은 미정(중립 도메인 결재 대기, 기획서 3장) → 시안 '[site name TBD]'.

## 측정 (growth/measure-1002.md A장 이름 그대로 — 붙이는 건 빌더)
- `check_open{country, from: hub|result}` — 허브 도장·나라 쪽 칩 누름. `country_switch{from,to}`. `calc_submit` · `share_done`.
- 판정: **도장 클릭률 = check_open ÷ calc_submit, 3% 미만이면 다른 한 가지가 안 먹은 것**(기획서 6장).

## 사전 부검 ("4주 뒤 아무도 도장을 안 눌렀다, 왜?")
1. 대조 전 노랑 칩만 오래 떠 있었다 → 허브 공개 조건에 '영국 3건 대조 완료'를 넣는다(빌더 backlog 1순위와 같음).
2. 'match'를 정부 인증으로 읽어 신고·불신 → 'We are not part of …'를 허브 바닥·대조표 첫 줄 두 곳에 둔다(시안 반영).
3. 칩이 결과 숫자보다 눈에 띄어 계산을 안 했다 → 칩 13px·soft, 숫자 40px 유지(시안 반영).

## 사용자 관점 반론
(아래 second_opinion 결과)
- `py -3.12 work/second_opinion.py spec.md 사용자` → spec_사용자.md (gemini-3-flash-preview 10:45). 참모 인물이 '한국 35세 파이어족'으로 고정돼 영국·호주 급여 사용자 관점이 아니다(X-V1 때와 같은 한계).
- **받아들인 것:** ① 대조 전 노랑 칩만 가득한 허브는 '준비 안 된 사이트'로 읽힌다 → 사전 부검 1과 같음, **허브 공개 조건 = 영국 3건 대조 완료**를 빌더 [지시]에 넣는다. ② '[site name TBD]'로는 공개 금지(도메인 결재 뒤 이름). ③ 'GB/UK' 글자 상자가 낡아 보일 수 있다 → 코드 상자는 강조 soft 바탕·굵은 글자로 이미 처리, 국기 SVG(공개 도메인)로 바꿀지는 빌더 캡처 뒤 다시 본다.
- **안 받아들인 것:** '은퇴 시점 계산과 연결' — 영국 사이트에 파이어맵 이름·은퇴 연결 금지(uk-pay brief 6장), 기획서 2장이 3판 후보로 미룸. 'We are not part of…'가 책임 회피처럼 읽힌다 — ATO 저작권 고지('정부 보증처럼 보이면 안 됨') 때문에 뺄 수 없다.
- 심사(8점)는 **하지 않음**: 허브 비교 대상(talent.com·salaryaftertax 등 375 캡처)이 아직 없다. 빌더 첫 판(10/9) 캡처 때 경쟁 5와 나란히 judge-prompt.md 3명으로 [디자인 검수 요청]을 받는다.
