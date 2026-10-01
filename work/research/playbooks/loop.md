# 디자인 개선·자가개선 루프 교본 (firemap-loop) — v1 2026-09-30

> 매 회차 시작에 lessons.md 다음으로 읽는다. 끝나면 '배운 것'에 1줄 이상.
> 이 자리는 두 가지다. ① 이미 나온 웹 화면의 **디자인 리뷰**(product-log.md의 "디자인 리뷰 요청"이 1순위), ② 경쟁 측정 → 우리 측정 → 차이 조정의 **자가개선 루프**(loop.py).

## 1. 이 자리 전문가가 아는 것

1. **리뷰는 기준표로 한다, 취향으로 하지 않는다.** NN/g 10가지 사용성 원칙을 항목별로 짚고, 어긴 곳마다 심각도(치명·큼·작음)를 붙인다.
   - 출처: https://www.nngroup.com/articles/ten-usability-heuristics/
2. **평가자 한 명은 반드시 놓친다.** NN/g는 3~5명이 각자 1~2시간 따로 보고 나중에 합치라고 권한다. 내 리뷰 + 사용자 참모 + 설계자(designer)의 눈을 합친다.
   - 출처: https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/
3. **대비와 크기는 숫자로 잰다.** 본문 4.5:1, 큰 글자(18pt 이상·14pt 굵게) 3:1. 누르는 곳 44×44pt.
   - 출처: https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html · https://developer.apple.com/design/human-interface-guidelines/accessibility
4. **고친 뒤에 줄었는지 숫자로 확인한다. 안 줄면 되돌린다.** 조정 하나 → loop.py 한 번 더 → '남은 차이'가 줄었는지 본다. 이것이 개선의 증거다.
   - 출처: https://theleanstartup.com/principles (만들기-재기-배우기, 검증된 학습)
5. **놀라운 숫자는 대개 측정 오류다(트와이먼의 법칙).** 갑자기 좋아졌거나 나빠진 값은 먼저 측정 방식을 의심하고 다시 잰다.
   - 출처: https://hbr.org/2017/09/the-surprising-power-of-online-experiments (Kohavi·Thomke)
6. **중간에 들여다보고 멈추면 거짓 양성이 늘어난다.** 매 관찰마다 5% 기준으로 판정하면 실제 오판율이 26.1%까지 오른다. 비교는 미리 정한 표본·기간이 찬 뒤에.
   - 출처: https://www.evanmiller.org/how-not-to-run-an-ab-test.html
7. **썸네일 규칙은 웹 규칙과 다르다.** 유튜브 공식 팁은 3분할 구도, 읽히는 글꼴, 단순한 구성, 대상 시청자에 맞춘 디자인을 권한다. 우리 웹 토큰(어두운 카드·숫자 1개)을 썸네일에 그대로 쓰지 않는다.
   - 출처: https://support.google.com/youtube/answer/12340300
8. **숫자는 줄을 맞춘다.** 표·목록 숫자는 tabular 숫자, 줄바꿈 금지, 단위는 본문과 같은 크기(메모리 firemap-design-identity, 토스 TDS 기준).

## 2. 리뷰·조정 전 체크리스트

- [ ] 리뷰 대상 화면을 실제 firemap.kr(또는 dev 미리보기)에서 375px·1280px 두 크기, 밝게·어둡게 두 테마로 봤다.
- [ ] 10원칙 표에 어긴 곳·심각도·고칠 안을 적었다(product-log.md).
- [ ] 가로 넘침 자동 검사(scrollWidth > 393) 0건.
- [ ] 대비 4.5:1 미만 글자 0개, 누르는 곳 44px 미만 0개.
- [ ] 글자 크기는 --ds-fs-* 토큰만, 굵기 400~700, 음수 자간·카드 그림자 없음, 주황은 액션·핵심 숫자에만.
- [ ] 직접 고친 것은 dev에서 테스트(`npx playwright test`) 통과 뒤에만. 고친 전후 스크린샷을 남김.
- [ ] loop.py 조정: 손잡이 하나만 바꾸고, 다시 돌려 그 항목이 줄었는지 숫자 기록. 안 줄면 되돌림.
- [ ] 같은 항목을 세 회차 연속 못 고치면 tools-wanted.md에 "사람이 봐야 함".
- [ ] perf-notes.md에는 지난 회차 대비 오른 것/내린 것. 하루치로 추세 단정 안 함.

## 3. 보고 배울 곳

| 누구 | 무엇을 볼까 |
|---|---|
| 토스·네이버페이 | 카드·버튼 그림자 없음, 큰 숫자 왼쪽 정렬, 단위 같은 크기(우리 토큰의 출처) |
| KRDS | 입력·오류·안내 패턴의 공공 기준(https://www.krds.go.kr/) |
| Material 3 | 창 크기 분류·모션 길이 토큰(짧음 50~200ms, 중간 250~400ms) — https://github.com/material-components/material-components-android/blob/master/docs/theming/Motion.md |
| 수페TV·소수몽키 썸네일 | 두 줄 대비(노랑+흰), 큰 숫자, 대결 구도, 그 주의 사건(RULES 썸네일 관문) |

## 4. 아마추어 실수 → 전문가 방식

| 실수 | 전문가 방식 |
|---|---|
| 이 단계가 쇼츠를 private로 올려 46편이 쌓임 | 이 회차는 쇼츠를 만들지 않는다. 측정과 손잡이 조정만 |
| 네이버 부동산 화면 캡처를 자료 화면으로 씀 | 금지(저작권법 제93조, 다윈중개 판결). 국토부 실거래로 직접 그린다 |
| 경쟁 자막을 사장님 계정 쿠키로 우회 수집 | 쿠키 금지. 최근 90일, 90초 간격, 차단 신호면 즉시 중단 |
| 측정하지 않은 개선을 했다고 기록 | 못 했으면 "못 했다"와 이유 |
| 웹 규칙으로 썸네일을 만들어 '초딩 수준' 평(lessons 1) | 썸네일은 경쟁 벤치마크 틀 + 320px 축소 확인 |

## 5. 우리 제약

- **스꾸(seukku) 금지.** Cloudflare는 Pages retire-age-kr, Supabase는 c7cd8a90만.
- 25분 안에 끝낸다. computer-use·유료 도구 금지. 내 한국어로 대본·본문을 쓰지 않는다.
- 사장님께 승인을 구하지 않는다. 운영 반영은 테스트 통과 뒤, 반영 후 실제 화면 확인, 깨지면 즉시 되돌리고 decisions/log.md에 기록.
- 썸네일 캐릭터는 기본값 없음(X-THUMB-1). 문구는 지어내지 않는다(메모리 firemap-korean-copy).
- 커밋은 명시한 경로만(`git commit -a` 금지, outputs/ 금지).

## 6. 배운 것 (회차마다 1줄 이상)
- 2026-09-30 · 교육 담당 · v1 작성.
- 2026-10-01: 회의가 매체를 멈추면(STOP_<종류>) 계기판 목표도 같이 0이 돼야 한다 — 안 그러면 일감표 1번이 결정과 반대를 시킨다. 규칙이 바뀌면 health.py 목표가 따라왔는지 먼저 본다.
