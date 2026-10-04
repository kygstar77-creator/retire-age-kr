# cloud/audit-1003 — 공개물 전수 감사 + 바로 막을 관문 4개 (클라우드 ⑥, 2026-10-03)

전체 문제 목록: `work/research/cloud/audit-2026-10-03.md`. 근본 원인 상위 10과 네 영역(영상미·영상 퀄리티·자료 퀄리티·글짓기), 이미 알려진 것 6개가 들어 있다.

## 무엇을 했나
- 처음 보는 사람 눈으로 공개물을 봤다.
  - 롱폼 5편: 대본·props·meta·썸네일
  - 카드 쇼츠 7편: json·카드·표지·log
  - 카페 20편(#185~#204): 제목·본문·그림·order
  - 계산기 4화면(375px)
- 문제는 31개를 새로 찾았다(이탈 7·오해 12·신뢰 12). 이미 알려진 6개는 오늘 숫자로 다시 쟀다.
- 관문 4개를 새로 만들고, 테스트 34개(전부 통과)를 넣었다.
  - `work/audit_links.py`: utm.md 규칙·경로·글당 1개·카페 첫 화면 링크 검사
  - `work/audit_text.py`: 카페 글 숫자 밀도(경쟁 카페 18편과 같은 함수)·RULES 원문 용어·쉼표 제목 틀·글끼리 반복 문장 검사
  - `work/audit_thumb.py`: png에서 글자 줄 높이를 잼(썸네일 320·카드 375·카페 343px 기준 9px), 썸네일 영상 길이 자리 가림 검사
  - `work/audit_screen_collect.mjs` + `work/audit_screen.py`: 375px 넘침·잘림·대비(WCAG 1.4.3)·12px·24px 누르는 칸 검사
  - 테스트 파일: `work/tests/test_audit_{links,text,thumb,screen}.py`
- 실제 파일에 돌린 결과:
  - 링크: 거부 8곳(10/3 카페 6편 utm_medium 없음, D-1 설명 링크 2개·campaign 불일치, N-1 utm_medium 없음)
  - 카페 글: 14/20편 거부, 쉼표 없는 제목 0/20
  - 썸네일: 공개본 5/5 꼬리말 5.5~6.5px
  - 카페 그림: 61/65 거부
  - 계산기: 넘침 0, 대비 거부 79곳
- 계산기 화면 사진과 측정값: `work/research/cloud/audit-1003-shots/`(로컬 dev 719eadc9)

## 근거
- 비교 기준:
  - 경쟁 사람 자막 12편: 52/1000단어·숫자 2개+ 문장 11%(이웃 브랜치 script-gate.md)
  - 경쟁 카페 글 18편: 83/1000어절·20%(cafe_style/benchmark_*.json, `audit_text.baseline`)
  - 수페TV: 17분 108장면(RULES 1장)
- 규칙 근거:
  - RULES.md 3장 색 토큰
  - RULES.md 썸네일 관문 규칙 2
  - RULES.md 화면 글자 규칙 1·2·4
  - growth/utm.md
  - WCAG 2.2 1.4.3·1.4.10·2.5.8, Lighthouse 12px
- 이웃 브랜치에서 인용한 것(다시 만들지 않음):
  - `lfrender.py`: N-1 장면 8 누적 막대 거부, 다시 녹음할 줄 E-2 32/67·E-1 35/88·D-1 17/70·N-1 24/46, A-1 f0·tempo 기록 없음
  - `aitell --script`: 대본 148~197/1000단어

## 확인 안 함
- 프록시 CONNECT 403으로 못 연 것: firemap.kr·youtube.com·cafe.naver.com 실제 화면. 계산기는 로컬 dev로 대신 봤다.
- 렌더 영상: remotion이 없다. 그래서 장면 안 움직임·자막 가림·소리는 못 봤다.
- 쇼츠 8번째 편: 기록이 없다. 카드 png 4장도 저장소에 없다.
- 경쟁 쪽 값 가운데 저장소에 없는 것: 첫 30초 숫자·카드 글자 수·장면 길이·썸네일 글자 크기.
- 카페 숫자 대조 거짓 경보 30개 중 26개: 하나씩 보지 않았다(표본 4개는 사실표와 일치).
- 관문 기준 9px·보이는 폭은 근거를 적은 가정값이다. 경쟁 썸네일로 다시 맞추지는 않았다.

## 담당이 적용할 것
- **copywriter**: N-1 설명 첫 줄 '상위 몇 %인지 보기'를 10/4 19:30 공개 전에 고친다(/calc/salary에 백분위 칸이 없음).
- **growth**
  - 10/3 카페 6편의 utm을 고친다(`&utm_medium=post`).
  - N-1에 `utm_medium=desc`를 넣는다.
  - D-1 둘째 링크를 지운다.
- **firemap-write**
  - 발행 전에 `python3 work/audit_links.py <pkg>`·`python3 work/audit_text.py <오늘 pkg들>`·`python3 work/audit_thumb.py --kind cafe <img>`를 돌린다.
  - order.txt에서 `_orig` 그림을 뺀다.
  - blogimg.py 강조색을 RULES 3장 빨강·파랑으로 바꾼다.
- **video-producer**
  - 썸네일은 `python3 work/audit_thumb.py <thumb.png>` 통과본만 쓴다.
  - A-1 meta.json의 thumb를 실제 공개 파일로 고친다.
  - 장면 12초 안팎·첫 30초 숫자 0~1개를 지킨다.
- **제품 개발**
  - --ds-ink-3와 주 버튼의 대비를 4.5:1 이상으로 올린다.
  - 눈금을 12px 이상으로 키운다.
  - qa:mobile에 `node work/audit_screen_collect.mjs` → `python3 work/audit_screen.py`를 붙인다.
- **도구 담당**: scriptnum.py가 억·만 숫자를 읽고, 카페 글은 전 줄을 읽게 고친다.
- **PC에서 합친 뒤**: `python3 -m pytest work/tests/test_audit_links.py work/tests/test_audit_text.py work/tests/test_audit_thumb.py work/tests/test_audit_screen.py`를 돌린다. test_audit_thumb는 Pillow가 필요하고, 없으면 건너뛴다.
