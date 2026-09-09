# 파이어맵 앱(iOS·Android) 출시 준비 — 코드 쪽은 끝, 계정 쪽은 사장님 몫

6차 조사 결정: **Capacitor**로 같은 웹 코드를 앱으로 감싼다(TWA·Expo 대신). App Store 4.2(최소 기능)를 넘기려면 네이티브 기능 3개가 있어야 한다 — 푸시, 위젯, 공유 시트. 코드는 `src/platform/index.js` 한 곳만 바꾸면 된다.

## 1. 사장님이 만들어야 하는 계정
| 순서 | 계정 | 어디에 쓰나 |
|---|---|---|
| 1 | Apple Developer Program($99/년) | TestFlight·App Store, 위젯(App Group) |
| 2 | Google Play Console($25 1회) | 내부 테스트·출시 |
| 3 | AdMob(사장님 Google 계정) | 보상형 광고 — **부가 콘텐츠에만**(결과 자체는 무료 유지) |
| 4 | 카카오 개발자 콘솔 → 앱 플랫폼에 iOS·Android 추가 | 카카오 로그인·공유가 앱에서도 되게 |

## 2. 개발 순서(계정 준비 뒤 1~2주)
```bash
npm i @capacitor/core @capacitor/cli @capacitor/ios @capacitor/android
npm i @capacitor/share @capacitor/haptics @capacitor/push-notifications @capacitor/preferences
npx cap add ios && npx cap add android
npm run build && npx cap sync
```
- `src/platform/index.js`: `share()`→`@capacitor/share`, `haptic()`→`@capacitor/haptics`, `widgetSync()`→App Group(iOS)·SharedPreferences(Android)에 `fm_widget` JSON 저장.
- 위젯(위젯 규격은 5차 조사): iOS WidgetKit small(숫자 1개: D-day) · medium(D-day·연속일·%) · Lock Screen accessoryCircular(%) ; Android 2×2·4×1·4×2, 48dp 셀. 데이터는 `buildWidgetState()` 결과 그대로 `{earliestAge, dday, streak, progressPct, updatedAt}`.
- 푸시: 기존 웹푸시(`send-fire-clock`)를 FCM/APNs로 확장 — Edge Function이 `push_subs`에 `platform` 컬럼을 보고 분기.
- 보상형(AdMob): `@capacitor-community/admob`. `showRewarded()`는 유형 테스트 심화·도시 리포트 같은 **부가 콘텐츠** 잠금 해제에만. 옵트인·비금전 보상·사전 고지(정책 검증 결과 §결정표 E).

## 3. 스토어 심사 체크리스트(App Store 4.2 · 2.5.6 · 3.1.1 · 5.1.1)
- 웹과 다른 네이티브 가치 3개: 위젯 · 푸시(파이어 시계) · 공유 시트/햅틱 ✔ 코드 준비
- 로그인 없이 핵심 기능 사용 가능 ✔ (계산·기록·랭킹 전부 익명)
- 보상형 광고는 부가 콘텐츠에만, 결과 숫자는 광고 없이 ✔
- 개인정보: 이름·연락처·계좌 수집 없음 ✔ `privacy.html`
- 오프라인: 앱 번들이 정적 자산을 가짐(폰트 로컬 `public/fonts`) ✔
