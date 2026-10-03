# 클라우드 세션 지시문 (사장님이 claude.ai/code 또는 앱 Code 탭에서 '클라우드'로 새 세션 → 저장소 kygstar77-creator/retire-age-kr → 아래 하나씩 붙여 넣기)
크레딧 $250(11/5 16:59까지)에서 빠지고 PC 주간 사용량은 안 쓴다. 각 세션은 결과를 새 브랜치 `cloud/…`에 push하고 dev·main에는 직접 push하지 않는다. PC 쪽 work/cloudmerge.py가 발행 감시·카페 회차마다(하루 12번) 안전 검사 뒤 자동으로 dev에 합친다. 그러니 코드를 고쳤으면 work/tests/test_*.py에 테스트를 꼭 함께 넣는다. 스꾸(seukku)는 건드리지 않는다.

---

## ① 대본 검사기 보정 (대본이 사람 말처럼 들리게 — 실측 기반)

파이어맵 유튜브 롱폼 대본이 'AI가 읽는 글' 같다는 지적을 받았다. 저장소 work/research/longform/loop/speechcompare.py가 경쟁 사람 자막 12편(work/research/longform/loop/subs/*.ko-orig.json3)과 우리 대본 4편(work/research/longform/ep/{E-1,D-1,E-2,N-1}/voice.json의 say)을 비교한 결과가 있다. 숫자 밀도는 1,000단어당 경쟁 52(최대 91), 우리 187이다. 숫자 2개 이상 든 문장은 경쟁 11%, 우리 40%다. 반면 work/aitell.py 대본 점수는 6편 모두 0~3.5(기준 12)라 차이를 못 가린다.
할 일:
1) speechcompare.py를 늘린다. 추가 지표는 문장 길이 분포, 숫자 개수 분포, 문장마다 숫자 하나 이하 비율, 반복 표현, 접속사·추임새 종류, 질문형 비율이다. 경쟁 12편과 우리 4편을 가장 잘 가르는 지표 조합을 찾는다(leave-one-out 정확도 표).
2) 그 조합으로 aitell.py에 대본 모드 점수를 추가한다(`py aitell.py --script <파일>`). 경쟁 12편은 통과, 우리 4편은 실패가 나오도록 기준을 정하고 근거 표를 work/research/editor/script-gate.md에 쓴다. 근거 없는 규칙은 넣지 않는다.
3) N-1 대본(work/research/longform/ep/N-1/script.md)을 새 기준으로 고친 예시를 script.human-example.md로 쓴다. 숫자는 원문 그대로 두고, 말은 반올림한 숫자 하나만 남기며, 정확한 값은 [자막] 표시로 뺀다.
4) 브랜치 cloud/script-gate-1003에 커밋·push하고, 최종 답에 정확도 표와 기준을 적는다.

---

## ② 영상 화면 글자·목소리 관문 코드 (렌더 전에 막기)

사장님 지적 두 가지를 코드로 막는다.
- (a) 화면 글자(그래프 제목·부제·자막)가 편집을 거치지 않았다. 겹치는 집단(상위 1%와 상위 10%)을 나란히 그려 오해를 불렀다.
- (b) 녹음을 날을 나눠 해서 뒤쪽 목소리 높이가 바뀌었다(E-2 155→137Hz). 빠르기를 1.25배까지 바꿨다.
규칙 원문은 work/research/longform/loop/RULES.md의 '화면 글자·그래프 규칙'과 '목소리 한결같음'이다.
할 일:
1) work/video와 work/lf*.py(lfvoice·lfrender 등)를 읽고, 렌더 전에 화면 글자 전부를 ep/<편>/screen_text.txt로 뽑는 함수를 만든다. 그 파일의 편집 통과 표시(screen_text.edit.json — editgate.py 방식 해시)가 없으면 렌더를 거부하는 관문을 넣는다.
2) props에 같은 그래프 안 막대 이름이 '상위 N%'처럼 누적 구간이면 경고하고, '(포함)' 표시나 비누적 구간이 없으면 거부한다.
3) voice.json 검사: 줄마다 f0가 중앙값 ±12% 밖이거나, tempo가 1.0이 아니거나, 녹음 날짜가 두 날 이상이면 거부하고 다시 녹음할 줄 목록을 출력한다.
4) 테스트(가짜 voice.json·props 3종)를 work/tests/에 넣는다. 브랜치 cloud/render-gates-1003에 push하고, 최종 답에 바뀐 파일과 사용법을 적는다.

---

## ③ AI 활용 유튜버 스터디 (최근 1~2개월)

파이어맵은 한국 은퇴·돈 계산기 사이트에 네이버 카페와 유튜브 롱폼·쇼츠를 함께 운영하는 회사이고, 직원은 전부 Claude 에이전트다. 2026-08-03 이후 'AI 활용법을 가르치는' 유튜브·글을 찾아 바로 따라 할 방법을 뽑는다(한국어 우선). 분야는 6개다: 디자인·웹 화면(Claude Design·디자인 토큰·Dembrandt), 롱폼·쇼츠 제작(대본·썸네일·코드 모션그래픽·TTS), 네이버 글·검색 노출, 에이전트 운영(사용량 아끼기·클라우드 세션), 차트 시각화, 제휴 수익화. 분야마다 상위 3~5편에서 도구·명령·순서만 뽑고, 출처 링크를 단다. 확인 못 한 것은 '확인 안 함'이라고 쓴다. 방법마다 '담당·바꿀 것·효과·비용·위험'을 적고 효과 순 상위 10을 고른다. 저장소의 work/research/playbooks·workflow.md를 보고 이미 하는 것은 표시한다. 결과는 work/research/ai-lab/study-2026-10-03-youtubers.md에 쓰고 브랜치 cloud/ai-study-1003에 push한다.
