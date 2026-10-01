# calc-3 퇴직금 숫자 줄·버튼 자리 — 디자인 검수 (firemap-designer, 2026-10-01 14:12~)

근거: build/severance-A-real-375.png(숫자 줄 있음) · severance-B-new-375.png(없음) · severance-A-real-desktop.png · src/components/firemap/SeveranceCalc.jsx · src/ui/fm-ds.css 672~675행

## 판정: 디자인 통과 (막지 않는 메모 2)

| 항목 | 결과 |
|---|---|
| spec 1 위치 | StatHero children, 타일 아래 1px `--ds-line` + 위 16px(`--ds-sp-4`) — 맞음 |
| spec 1 글자 크기 | lead 13/600/ink-2 · line 17/700/ink · N년 20px `.num`(tabular) — preview.html `<style>`과 한 글자도 다르지 않음. 주황 0 |
| 숫자 1개 | 히어로 22px(`--ds-fs-title-2`) > N년 20px > 타일 — 히어로가 여전히 가장 큼 |
| spec 2 행동 1 | 주황 버튼 1개, 결과 카드 바로 아래, 연봉과 같은 글자·모양. 다크 은퇴 카드 없음 → 행동 1개 |
| spec 3 조건 | `gainYears >= 1`일 때만 그림, 아니면 자리 비움·'0년' 없음(B 캡처 확인). 버튼·caption은 항상 같은 자리 |
| spec 4 375 실측 | 버튼 아래 끝 A 436px · B 355px(812 첫 화면 안), 높이 56, 가로 넘침 0 — 캡처로 확인 |
| 색 4 | 흰·잉크·회색·주황만 |
| 우리만 다른 한 수가 첫 화면에 | A: 'N년 앞당겨져요'가 첫 화면 안. B(저장 입력 없음): 없음 — spec '한계' 1 그대로(비율 측정 뒤 후보 ③) |
| 데스크톱 | 같은 순서, 넘침 없음 |

## spec과 다른 점 1 — 받음
차이를 `retirementAge` 대신 `earliestRetirementAge`로. retirementAge는 파이어 불가 때 목표 나이로 떨어져 가짜 차이가 날 수 있다(product-dev 13:43). 둘 다 있을 때만 그리므로 '안 그림' 쪽으로만 틀린다 → 화면 원칙(남의 숫자·가짜 숫자 금지)에 더 맞음. spec.md 3을 고쳐 둠.

## 심사 3명
| 심사 | 점수 |
|---|---|
| 제미나이 3.5-flash-lite(3-flash·3.8은 429) build/judge-gemini.txt | 6 |
| Claude sonnet | 6 |
| 내 채점 | 6.5 |
| **평균** | **6.17** (기준 6 이상) |

심사 지적 중 안 받은 것(모두 spec에서 이미 판정한 것):
- 'N년'을 주황으로 / 이득줄을 별도 배너로 — 주황은 버튼 하나(색 4·행동 1). spec 사용자 반론 ④ 안 받음과 같음.
- 버튼 아래 caption 삭제 — 근거 문장이라 숫자 줄과 떼지 않는다(spec 사용자 반론 ① 받음 조건).
- B 상태에 '자산 연결하세요' 자리 채움 — 자리 비움·대체 문구 금지(spec 3), 새로 짓는 말이 된다.

## 막지 않는 메모 (다음 조각 때)
1. 실업급여 조각도 같은 .fm-gain·같은 버튼 자리로. 실업급여 타일 '상한 · 하한'은 375에서 꽉 차므로 `ds-hero--compact-tiles` 붙이기(spec 한계 2).
2. 다크 모드 구현 캡처는 이번 근거에 없음(확인 안 함) — 토큰만 써서 D안과 같을 것으로 보이나, 실업급여 조각 검수 때 다크 375 1장 같이 내 주세요.

## 320px 타일 '원' 판정 (2026-10-01 16:33, editor-web 14:15 메모)
- 본 것: build/severance-editor-320.png — 가운데 타일 '97,826원'의 '원'이 오른쪽 칸 선(1px)에 닿는다. 칸 폭 약 93px, 값 20px(title-3).
- 판정: **고친다.** 새 부품·새 값 없이 연봉 결과(SalaryCalc.jsx 44행)와 같은 기존 수식어 `ds-hero--compact-tiles`(값 15px)를 퇴직금·실업급여 StatHero에 붙인다. 기준 하나: 원 단위 값이 들어가는 3칸 타일은 모두 compact.
- 확인 방법: 구현 뒤 320·375 캡처에서 타일 값과 칸 선 사이 여백 ≥ 4px.
