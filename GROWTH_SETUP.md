# 퇴사나이 운영 설정 가이드

이 문서는 사용자에게 보이는 화면이 아니라 운영자가 보는 체크리스트입니다.

## 현재 준비된 것

- 메인 화면 하단의 개인정보처리방침, 이용약관, 문의 링크
- GA4 이벤트 수집 코드 준비
- Cloudflare Web Analytics 토큰 삽입 구조 준비
- AdSense 광고 코드 구조 준비
- 광고는 결과 화면 아래쪽에 1개만 붙도록 설계
- 사용자가 입력한 금융자산, 부동산, 대출금, 생활비 같은 원금 숫자는 분석 이벤트로 보내지 않도록 설계

## 1. Cloudflare Web Analytics 켜기

Cloudflare Pages 대시보드에서 Web Analytics를 켜는 방법이 가장 쉽습니다.

1. Cloudflare Dashboard에 로그인합니다.
2. Pages에서 `retire-age-kr` 프로젝트를 엽니다.
3. Analytics 또는 Web Analytics 메뉴에서 사이트 분석을 활성화합니다.
4. 대시보드에서 방문자 수, 페이지뷰, 국가, 유입 경로를 확인합니다.

Cloudflare가 별도 토큰을 제공하는 방식으로 설정할 경우, `work/build-deploy.mjs` 안의 아래 값을 채웁니다.

```js
cloudflareAnalyticsToken: '토큰값'
```

## 2. GA4 측정 ID 받아서 붙이기

GA4는 “사용자가 어디서 들어왔는지”뿐 아니라 “입력 시작, 결과 확인, 링크 복사” 같은 전환 행동을 보기 위해 사용합니다.

1. Google Analytics에서 GA4 속성을 만듭니다.
2. 웹 데이터 스트림을 만들고 측정 ID를 확인합니다. 예: `G-XXXXXXXXXX`
3. `work/build-deploy.mjs` 안의 아래 값을 채웁니다.

```js
gaMeasurementId: 'G-XXXXXXXXXX'
```

준비된 이벤트:

- `input_started`: 사용자가 입력을 시작함
- `input_change`: 어떤 입력 항목을 만졌는지 확인
- `result_view`: 결과 화면을 확인함
- `share_link_copy`: 계산 링크 복사
- `share_summary_copy`: 결과 요약 복사
- `inputs_reset`: 초기화
- `input_panel_open`: 입력 수정 열기
- `legal_link_click`: 약관/개인정보 링크 클릭

## 3. AdSense 신청

Google AdSense는 코드만 넣는다고 바로 돈이 들어오는 구조가 아닙니다. 먼저 AdSense 계정과 사이트 승인이 필요합니다.

승인 전 체크리스트:

- 개인정보처리방침 페이지 있음
- 이용약관 페이지 있음
- 문의 페이지 있음
- 사이트가 모바일에서 정상적으로 열림
- 광고가 버튼 바로 옆이나 입력 흐름 중간을 방해하지 않음

승인 후 필요한 값:

- AdSense client ID: `ca-pub-...`
- 광고 단위 slot ID: 숫자 형태의 슬롯 ID

`work/build-deploy.mjs` 안의 아래 값을 채웁니다.

```js
adsEnabled: true,
adsenseClientId: 'ca-pub-XXXXXXXXXXXXXXXX',
adsenseSlotId: '1234567890'
```

초기에는 UX를 해치지 않기 위해 입력 화면에는 광고를 넣지 않고, 결과를 확인한 뒤 아래쪽에만 광고를 표시하는 구성이 좋습니다.

## 4. 먼저 봐야 할 지표

초기에는 광고 수익보다 아래 숫자가 더 중요합니다.

- 방문자 중 몇 %가 입력을 시작하는지
- 입력 시작자 중 몇 %가 결과까지 보는지
- 결과를 본 사람 중 몇 %가 링크를 복사하는지
- 모바일 이탈이 PC보다 높은지
- 카카오톡 공유 후 다시 들어오는 사용자가 있는지

이 숫자가 잡히면 광고보다 먼저 “유료 상세 리포트”, “PDF 저장”, “부부/가구 버전”, “연금/건보 정밀 계산” 같은 유료 기능으로 확장할 수 있습니다.
