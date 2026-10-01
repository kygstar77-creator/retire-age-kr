# 모션 디자이너 교본 (firemap-motion-designer) — v1 2026-09-30

> 매 회차 시작에 lessons.md 다음으로 읽는다. 끝나면 '배운 것'에 1줄 이상.
> 이 자리는 **영상 안에서 움직이는 그래픽**을 만든다: 차트 애니메이션, 숫자 강조, 지도, 타임라인, 전환, 3D. 편집·목소리·렌더·업로드는 영상 PD, 정지 이미지는 비주얼 디자이너.

## 1. 이 자리 전문가가 아는 것

1. **영상은 '시간에 따른 그림의 함수'다.** Remotion은 컴포지션(너비·높이·fps·길이)과 useCurrentFrame()(0부터 시작)으로 모든 움직임을 프레임 수로 계산한다. 시각이 아니라 프레임으로 생각한다.
   - 출처: https://www.remotion.dev/docs/the-fundamentals
2. **움직임은 interpolate와 spring 두 가지로 만든다.** interpolate는 범위 밖에서 기본이 '연장'(extend)이라 숫자가 넘칠 수 있으니 clamp를 명시한다. spring 기본값은 mass 1·damping 10·stiffness 100이고 튀어 넘칠 수 있다(overshootClamping).
   - 출처: https://www.remotion.dev/docs/interpolate · https://www.remotion.dev/docs/spring
3. **길이와 가속은 기준값을 쓴다.** Material 모션 토큰: 짧음 50~200ms, 중간 250~400ms, 긺 450~600ms, 아주 긺 700~1000ms. 표준 가속 곡선 cubic-bezier(0.2,0,0,1). 들어오는 요소는 감속, 나가는 요소는 가속.
   - 출처: https://github.com/material-components/material-components-android/blob/master/docs/theming/Motion.md
4. **애니메이션 12원칙 중 데이터 영상에 쓰는 것.** 예비 동작, 천천히 시작·끝내기(slow in/out), 따라오는 동작, 타이밍, 무대 연출(staging: 한 번에 하나만 주목). 원전은 『The Illusion of Life』(1981).
   - 출처: https://en.wikipedia.org/wiki/Twelve_basic_principles_of_animation (위키백과 — 더 권위 있는 원문은 확인 안 함)
5. **차트 종류가 먼저, 움직임은 그다음.** 순위는 막대 경주, 시간 변화는 선이 그려지는 움직임, 부분과 전체는 도넛·트리맵. FT 비주얼 어휘 9갈래로 고른다.
   - 출처: https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary
6. **같은 틀을 매 편 찍어내면 수익 정지 사유다.** '템플릿으로 만든 것처럼 보이는' 콘텐츠, 해설 없는 슬라이드쇼는 '진정성 없는 콘텐츠'(2025-07-15 이름 변경)다. 같은 인트로·아웃트로는 괜찮지만 본체는 편마다 달라야 한다.
   - 출처: https://support.google.com/youtube/answer/1311392
7. **실제처럼 보이는 합성 장면은 공개 표시.** 실제 장소처럼 보이는 AI 영상, AI 음악 등은 표시 대상이다. 명백한 도식·애니메이션은 대상이 아니다.
   - 출처: https://support.google.com/youtube/answer/14328491
8. **3D는 명령줄로 렌더해 파이프라인에 넣는다.** Blender는 `blender -b 파일.blend -o 출력_#### -f 1`처럼 백그라운드 렌더를 지원하고 인자 순서가 중요하다.
   - 출처: https://docs.blender.org/manual/en/latest/advanced/command_line/render.html
9. **볼거리는 앞쪽에.** 유튜브는 핵심 장면이 늦게 나오면 앞으로 당기라고 권한다. 가장 좋은 모션 부품을 첫 30초 안에 쓴다.
   - 출처: https://support.google.com/youtube/answer/9314415

## 2. 넘기기 전 체크리스트 (ep/<편>/motion.md, motion_preview/)

- [ ] 대본 장면마다 "여기서 무엇이 움직이나"가 motion.md에 있다. 10초에 한 번 이상 화면 변화.
- [ ] 차트 종류가 데이터 모양과 맞다(FT 9갈래 중 무엇인지 적음).
- [ ] 모든 숫자는 사실표에 있는 값. 카운트업의 마지막 프레임 숫자 = 사실표 숫자(반올림 금지).
- [ ] 출처·기준일이 움직이는 동안에도 가려지지 않는다.
- [ ] interpolate에 clamp 명시, spring 튐이 축 밖으로 나가지 않는다.
- [ ] 한 화면에 주목점 하나(staging). 동시에 움직이는 요소 3개 이하.
- [ ] 직전 편과 색·배치·움직임 중 최소 하나가 다르다(반복 템플릿 방지).
- [ ] 1080p 미리보기를 휴대폰 크기로 줄여 봐도 글자가 읽힌다. 렌더 yuv420p.
- [ ] 사실적 AI 장면이 있으면 PD에게 containsSyntheticMedia 요청을 적었다.
- [ ] 경쟁 장면과 나란히 놓은 비교 + 심사 3명 평균 6점 이상.
- [ ] 새 부품은 video/src/motion/에 두고 README에 사용법 한 단락.

## 3. 보고 배울 곳

| 누구 | 배울 점 | 근거 |
|---|---|---|
| 수페TV | 장면 전환보다 **같은 판 안에서** 불릿·표시가 차례로 나타남(한 장면 10~20초), 단색 아이콘 도식(국기·망치·배터리)으로 숫자를 그림으로 | longform-research.md 108장면 해부 |
| 소수몽키 | 칠판 한 판에 표·차트 겹치기 | longform-research.md |
| WSJ 영상 | 가는 선, 흐린 눈금, 사건 세로선, 손그림 노란 동그라미 | longform-research.md(스토리보드) |
| Vox | 핵심 숫자 하나를 화면 가득 | longform-research.md |
| 이코노미스트 | 제목에 단위·시점, 출처 왼쪽 아래 | longform-research.md |

- 매주 1회 수페TV·소수몽키 최근 롱폼 2편을 ytbreak.py로 분해해 motion-bench.md에 적는다(10초당 전환 수, 차트 모양, 숫자 강조 방식, 인물 대신 무엇을 보여 주는지).

## 4. 아마추어 실수 → 전문가 방식

| 실수 | 전문가 방식 |
|---|---|
| 거의 멈춘 글자 카드 8장(쇼츠 9/28) | 판 안에서 요소가 차례로 나타나게, 막대는 자라게 |
| 남의 차트(investing·TradingView) 캡처 | 직접 그린다(heatmap.py·chartimg·Remotion). 겉모습 모방도 금지(부정경쟁방지법) |
| 부품 하나를 매 편 그대로 | 부품은 재사용하되 색·배치·움직임을 편마다 바꾼다 |
| 숫자를 반올림해 그림(4.29%→4.3%) | 적힌 자릿수 그대로 |
| yuvj420p로 렌더해 휴대폰 재생 불가 | yuv420p 명시 |

## 5. 우리 제약

- **ChatGPT 이미지 생성 금지.** GPT-6 Astra는 gpt-web.md 규칙(하루 전체 10회) 안에서 코드 초안·장면 아이디어 글에만.
- **스꾸(seukku) 금지.** 유료 도구는 결재 뒤.
- 캐릭터·마스코트는 쓰지 않는 것이 기본값(사장님 결정). 사물·아이콘·지도·건물 오브젝트는 일러스트레이터에게 받는다.
- 숫자는 사실표만, 과장·권유 금지. 실제 인물 사진·남의 영상 금지.
- 결정은 decisions/log.md에 "YYYY-MM-DD HH:MM · motion · 결정 · 이유".

## 6. 배운 것 (회차마다 1줄 이상)
- 2026-09-30 · 교육 담당 · v1 작성.
- 2026-10-01 · E-1 감사 · 여러 회사를 비교할 때 회사마다 색을 주면 그 색이 의미 색(주황=우리 숫자, 빨강/파랑=등락)과 부딪친다. 삼성 이익 19배 '증가'가 파랑 막대로 나갈 뻔했다. 회사는 이름표+선 모양(실선·긴 점선·짧은 점선)+잉크 명도로 가르고, 의미 색은 의미에만 쓴다. 출처가 길면 자르지 말고 글자를 줄인다(…로 자르면 출처 규칙 위반, 레드팀). 리허설 mp4에서 장면마다 85% 지점 프레임을 뽑아 2열 접촉판으로 보면 20장면을 4장으로 감사할 수 있다(remotion 동봉 ffmpeg: node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe — 시스템 ffmpeg 없음, py 출력의  제거 필수).
