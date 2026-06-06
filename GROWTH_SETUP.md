# 퇴사나이 운영 설정 가이드

이 문서는 사용자에게 보이는 화면이 아니라 운영자가 보는 체크리스트입니다.

## 1. 유입과 전환 보기

권장 조합은 아래 2개입니다.

- Cloudflare Web Analytics: 방문자 수, 유입 경로, 국가, 페이지뷰를 빠르게 확인합니다.
- Google Analytics 4: 입력 시작, 결과 확인, 링크 복사 같은 전환 행동을 이벤트로 봅니다.

현재 앱에는 GA4 이벤트 코드가 준비되어 있습니다. 단, 개인정보 보호를 위해 사용자가 입력한 금융자산, 부동산, 대출금, 생활비 같은 원금 숫자는 보내지 않습니다.

수집 준비 이벤트:

- `input_started`: 사용자가 입력을 시작함
- `input_change`: 어떤 입력 항목을 만졌는지 확인
- `result_view`: 결과 화면을 확인함
- `share_link_copy`: 계산 링크 복사
- `share_summary_copy`: 결과 요약 복사
- `inputs_reset`: 초기화
- `input_panel_open`: 입력 수정 열기
- `mobile_share_tap`: 모바일 공유 버튼 누름

## 2. GA4 켜는 방법

1. Google Analytics에서 GA4 속성을 만듭니다.
2. 웹 데이터 스트림을 만들고 측정 ID를 확인합니다. 예: `G-XXXXXXXXXX`
3. `work/build-deploy.mjs` 안의 아래 값을 채웁니다.

```js
gaMeasurementId: 'G-XXXXXXXXXX'
```

그 다음 GitHub에 반영하면 Cloudflare Pages가 다시 배포합니다.

## 3. 광고 켜는 방법

Google AdSense는 코드만 넣는다고 바로 돈이 들어오는 구조가 아닙니다. 먼저 AdSense 계정과 사이트 승인이 필요합니다.

승인 후 필요한 값:

- AdSense client ID: `ca-pub-...`
- 광고 단위 slot ID: 숫자 형태의 슬롯 ID

`work/build-deploy.mjs` 안의 아래 값을 채웁니다.

```js
adsEnabled: true,
adsenseClientId: 'ca-pub-XXXXXXXXXXXXXXXX',
adsenseSlotId: '1234567890'
```

광고 위치는 결과 화면 아래쪽에 1개만 준비되어 있습니다. 초기에는 UX를 해치지 않기 위해 입력 화면에는 광고를 넣지 않는 것이 좋습니다.

## 4. 먼저 봐야 할 지표

초기에는 돈보다 아래 숫자가 더 중요합니다.

- 방문자 중 몇 %가 입력을 시작하는지
- 입력 시작자 중 몇 %가 결과까지 보는지
- 결과를 본 사람 중 몇 %가 링크를 복사하는지
- 모바일 이탈이 PC보다 높은지
- 카카오톡 공유 후 다시 들어오는 사용자가 있는지

이 숫자가 잡히면 광고보다 먼저 “유료 상세 리포트”, “PDF 저장”, “부부/가구 버전”, “연금/건보 정밀 계산” 같은 유료 기능으로 확장할 수 있습니다.
