# video/src/motion — 재사용 모션 부품 (firemap-motion-designer)

숫자는 props로만 받는다(spec·facts.txt 원문). 부품 안에 숫자를 쓰지 않는다. 편마다 `seed`(편 이름)를 바꿔 방향·간격·좌우가 달라진다 — 같은 틀 반복은 유튜브 '진정성 없는 콘텐츠' 신호.

| 부품 | 하는 일 | 근거 |
|---|---|---|
| `RollNumber` | 숫자 자리마다 **제 숫자만** 아래(또는 위)에서 올라와 임계 감쇠로 선다. 0프레임에도 숫자 70%가 보인다. 가짜 중간 숫자 없음 | 모션 475 'BUILD THE FLOOR' |
| `settle(frame,fps,stiffness)` | 튀지 않는 스프링(damping=2√k) | 같음 |
| `CardToBar` | 숫자 밑 바닥 선 → 차트 0 기준선, 숫자 → 제 막대 이름표, 비교 막대가 옆에 자람. 막대는 기준선에서만 자란다, 높이는 값 비례 | 모션 475 'Taxtello' 물체 전환 + dataviz |
| `ShortIntro` | 위 둘을 묶은 쇼츠 첫 2초(1080x1920). Root id `ShortIntro` | — |

## 쇼츠에 붙이는 법
1. props JSON을 만든다(예 `video/intro_e2_interest.json`): seed·chip·title(spec 제목 그대로)·hook·a·b·unit·source·numW(큰 숫자 폭 px, 스틸로 잼)·aFirst(카드 순서와 맞출 때).
2. `npx remotion render src/index.ts ShortIntro <out>.mp4 --props=<json> --codec=h264 --pixel-format=yuv420p`
3. 쇼츠 spec에 `"intro_mp4": "<절대경로>"` → `py -3.12 work/cardshort.py <spec> <out>`. 인트로가 있으면 표지(cover/cover_png) 대신 들어가고, 카드는 다 자란 상태(t=2)로 시작한다.
4. `py -3.12 work/video/motioncheck.py <out>`(정지 ≤15초) · 0초·0.5초·2.0초·2.1초 프레임에 사실표 밖 숫자 0 확인 · 심사 3명 평균 7.

## 편마다 바꿀 것(반복 방지 체크)
- seed 바꾸기(자동), 막대 좌우(aFirst), 비교 상대(값 2개가 아닌 경우 다른 부품), 강조색은 spec 카드 색 안에서.
- 매 편 '숫자→막대'만 쓰지 않는다: 다음 후보는 줌아웃(모션 475 #5), 계산 곡선(#3).
