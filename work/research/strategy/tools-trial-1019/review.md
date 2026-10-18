# 영상 도구 시험 — HyperFrames · OpenMontage (10/19 영상 도구 담당)

계기: 신영선의 AI탐구 「영상 제작 100% 자동화 클로드 모션그래픽부터 영상 편집 올인원 가이드」(youtu.be/57IVfvXqUVs). 사장님 10/19 00:1x "그래 설치해".
시험 편: R-1 쇼츠 r1s_fx '달러로 산 미국 ETF, 환율만으로 1억에서 330만원 줄었다'(공개본 k1hsFpaLDH0 = work/video/out/r1s_fx_ds.mp4, 45.06초).

## 파일 (이 폴더, 커밋은 review.md만)
- `compare.mp4` — 왼쪽부터 지금 공개본 · HyperFrames 판 · OpenMontage 판. 소리는 OpenMontage 판(말+음악).
- `r1s_fx_hyperframes.mp4` — HyperFrames 판(음악 없음)
- `r1s_fx_openmontage.mp4` — OpenMontage 판(음악·스톡 포함)

## 세 판 공통 조건
- 말소리: 공개본 소리를 그대로 뽑아 썼다(새 녹음 0). 자막 조각 시각은 work/video/r1s_fx.json 줄 프레임 + 소리 크기로 맞췄다.
- 숫자: facts.txt 값만 썼다. 1,406.0원(2025.10.2) · 1,359.6원(2026.10.2) · −3.30% · −330만원(3,300,142원) · 1,554.4원(7/2) · 1,337.9원(9/10) · 1억 2,304만원(123,037,245원) · 1억 776만원(107,755,946원) · −1,528만원(15,281,299원) · 달러 가격 +1.75%. 원 단위 숫자는 화면에 안 썼다.
- 배경: OpenMontage `pexels_video` 도구가 고른 첫 결과 11개(아래 출처). HyperFrames 판은 같은 영상의 1080×1920 파일을 따로 받아 썼다(도구가 360×640을 골라서, 아래 '도구 결함' 1).
- 디자인: design-spec-1016 쇼츠 기준(제목 2줄 흰 글자+검은 테두리·'환율' 노랑, 자막 한 줄 가운데 y 1168·흰 글자+검은 테두리 6px·상자 없음·숫자 노랑, 출처 줄 22px y 1216, 글자는 x 48~888 안).

## 디렉터 평가 (숫자 말고 말로)

### HyperFrames 판
좋아진 점
1. **숫자가 '묻고, 쉬고, 연다'.** 판에 줄 이름과 '?'가 먼저 서 있고, 목소리가 그 숫자를 말하는 순간 값이 튀어 오른다. 답(−330만원·−1,528만원)에는 주황 손 동그라미가 한 번 그려진다. 공개본은 숫자가 미리 다 깔려 있어 귀보다 눈이 먼저 끝났다.
2. **한 화면 한 문장.** 판 하나가 한 가지 질문(작년 vs 올해, 1억 기준 얼마, 최고 vs 최저, SPY 1억, 끝날 하루 vs 그 사이)만 다룬다. 공개본처럼 아래에 '환율만 −330만원' 띠가 45초 내내 붙어 있지 않아 같은 숫자 되풀이가 없다.
3. **끝이 숨을 쉰다.** 마지막 막대(−330만원 짧은 회색, −1,528만원 긴 주황)로 '끝날 하루와 그 사이 길'이 한눈에 보이고, 판과 제목이 빠진 뒤 맑은 하늘 3초로 닫힌다. 공개본은 판이 그대로 멈춘 채 끝났다.

어색한 점
1. **배경이 말을 못 받는 곳이 있다.** 5~11초 '환율' 대목에 폴란드 즐로티 지폐, 24~31초 '가장 높았던/낮았던 날'에 코인 차트가 나온다. 원/달러 이야기에 남의 나라 돈·코인은 '분위기용'이다(디렉터 기준 탈락).
2. **물음표가 너무 오래 기다린다.** 18~24초 '1년 안' 판, 31~34초 'SPY 1억' 판은 '?'만 2~3줄 서 있는 시간이 3초 넘는다. 비어 보이고 글자가 작다(판 아래 3분의 1이 빈칸).
3. **판이 너무 하얗고 반듯하다.** 흰 카드·그림자가 웹 화면처럼 보인다. '노트 같아야 한다'(design-spec 10절)에는 아직 못 미친다. 음악도 없어 쉼에서 소리가 빈다.

### OpenMontage 판
좋아진 점
1. **소리가 비지 않는다.** 말 밑에 잔잔한 음이 깔리고, 말이 나오면 자동으로 내려갔다가(더킹) 쉼과 끝 하늘 장면에서 올라온다. 세 판 중 '말 밑엔 늘 잔잔한 음'(design-spec 10절)을 지킨 것은 이것뿐이다.
2. **화면이 계속 움직인다.** 배경 영상 11개가 3~6초마다 바뀌고 큰 숫자 하나만 가운데 떠서, 공개본의 흰 판 45초보다 훨씬 '영상'처럼 보인다.
3. **조립이 빠르다.** 장면 목록(edit_decisions) 하나로 렌더 → 자막 → 제목 → 소리까지 붙었다. 스스로 검사(ffprobe·프레임 4장·소리)도 돌린다.

어색한 점
1. **숫자가 다 주황이다.** 틀(Explainer StatCard)이 모든 큰 숫자를 같은 주황 128px로 찍어, 답(−330만원)과 그냥 사실(1,406.0원, 1,554.4원)이 구별이 안 된다. 숫자 밑 설명은 36px 회색이라 실사 위에서 거의 안 읽힌다.
2. **세로 영상에 가로 틀을 눌러 담은 티가 난다.** 1차 렌더에서 비교 카드(ComparisonCard)는 작게 쪼그라들고 '1억 2,304 / 만원', '−1,528만 / 원'처럼 줄이 깨졌다. 그래서 2차는 큰 숫자 카드만 쓰도록 장면을 나눴다(그래도 18~24초 글 판은 흐려서 안 보인다). 기본 자막은 6낱말·42px·흰 상자라 우리 기준과 달라 끄고, 자막·제목은 OM의 burn_subtitles·overlay로 따로 얹었다.
3. **도구가 고른 그림이 엉뚱하다.** 즐로티 지폐, 코인 차트, 뉴욕증권거래소 앞 영국 국기. 첫 결과를 그냥 집는 방식이라 말과 그림이 어긋난다. 스스로 검사도 이걸 못 잡고 'pass'를 줬다.

### 공개본과 견주어 한 줄
공개본은 '엑셀 표를 읽어 주는 영상'이고, 두 시험판은 '실사 위에서 숫자를 보여 주는 영상'이 됐다. 숫자 보여 주는 맛은 HyperFrames 판, 소리와 화면 바뀜은 OpenMontage 판이 낫다. 다만 두 판 다 '배경이 말을 받는가'는 실패다.

## 관문 결과 (렌더본 그대로)
| | 공개본 | HyperFrames 판 | OpenMontage 판 |
|---|---|---|---|
| bgcheck(배경 실사·자막) | (10/16 전 판) | 통과 — 실사 98% · 자막 94% | 통과 — 실사 96% · 자막 78% |
| safezone(글자 안전 영역) | 걸림 45/45초 · 상자 394 | 걸림 15/46초 · 상자 94 | 걸림 20/46초 · 상자 108 |
| 길이·규격 | 45.06초 1080×1920 | 45.1초 1080×1920 30fps | 45.07초 1080×1920 30fps |
| 소리 크기(통합) | −19.7 LUFS | −19.7 LUFS(공개본 소리 그대로) | −16.3 LUFS(OM 목표 −14) |
- safezone 걸림의 대부분은 **스톡 영상 속 글자**(지폐 글씨 'DOLLARS'·송장 서류·증권 화면 숫자)다. `safezone.py --draw`로 4초·3초를 그려 보니 우리가 얹은 글자(제목·판·자막·출처)는 전부 안전 영역 안이었다. 다만 HyperFrames 판 19·22초 출처 줄 근처 상자 몇 개는 화면 배경 글자와 겹쳐 우리 글자인지 확인 안 함. → 스톡을 고를 때 '읽히는 글자가 많은 영상'을 거르는 단계가 없으면 이 관문을 못 넘는다.
- 귀로 들어 보지 않았다(음악 크기·어울림 확인 안 함). OM 판 끝 하늘 장면(42.8~44.8초) 평균 −26.4dB.

## 설치 기록
| | HyperFrames | OpenMontage |
|---|---|---|
| 위치 | C:\Users\강영준\Documents\tools\hyperframes | C:\Users\강영준\Documents\tools\openmontage |
| 받은 판 | git clone --depth 1, 커밋 01adadb(10/18) | git clone --depth 1, 커밋 c806645(10/16) |
| 라이선스 | Apache-2.0 | AGPL-3.0 |
| 설치 | README '직접 CLI' 순서: npm `hyperframes@0.8.171`을 tools/hyperframes/_cli에 고정 설치 → `hyperframes init r1s-fx --resolution portrait` | README Windows 순서 그대로: py -3.12 venv → requirements.txt → remotion-composer npm install(Remotion 4.0.484) → piper-tts 1.8.0 → .env.example 복사(키 0개) |
| 읽은 것 | README, packages/cli package.json(설치 스크립트 없음), 텔레메트리·브라우저 경로 코드 | README, Makefile, requirements, setup.py, remotion-composer package.json, 음악·스톡·합성 도구 코드 |
| 멈춤 조건 | 관리자 권한·시스템 설정·모르는 실행 파일·유료 키 필수 — 해당 없음 | 해당 없음(유료 키는 전부 선택) |
| 안 한 것 | Claude 플러그인·스킬 설치(`HYPERFRAMES_SKIP_SKILLS=1`, ~/.claude 안 건드림), Git LFS, Docker | `make`(Windows에 없음), GPU 설치, Backlot 보드, MusicGen(torch 수 GB) |
| 바깥 프로그램 | 새로 받지 않음: ffmpeg=imageio_ffmpeg 7.1, ffprobe·Chrome=work/video의 Remotion 것을 환경변수로 연결 | ffmpeg는 tools/openmontage/_bin/ffmpeg.exe(imageio_ffmpeg 복사본)를 그 실행에서만 PATH 앞에. Remotion이 처음 렌더 때 chrome-headless-shell을 자기 node_modules에 받음 |
| 끈 것 | `HYPERFRAMES_NO_TELEMETRY=1` · `DO_NOT_TRACK=1` · `HYPERFRAMES_NO_UPDATE_CHECK=1` · `HYPERFRAMES_NO_AUTO_INSTALL=1` | — |
| 키 | 없음 | Pexels 키는 C:\Users\강영준\Documents\pexels_key.txt에서 읽어 실행 중 환경변수로만 넘김. .env·설정 파일에 안 씀, 출력 안 함 |
| 렌더 시간 | 45초 쇼츠 1 worker 5~8분 | 45초 쇼츠 Remotion 9분(1차 기본 동시성) |
| 디스크 | tools/hyperframes 1.9GB(시험 프로젝트 포함) | (확인 안 함) · C 남은 용량 02:22 기준 20.6GB |

설정 파일 하나: `tools/openmontage/remotion-composer/remotion.config.ts`에 `Config.setConcurrency(2)`(2차 렌더부터 CPU 덜 쓰게).

## 도구 결함 (이 PC에서 직접 겪음)
1. OM `pexels_video`: Pexels 새 영상은 파일 quality 값이 비어 있어 'hd'를 못 찾고 목록 첫 파일(360×640)을 집는다. 11개 중 5개가 360×640.
2. OM `pixabay_music`: Pixabay가 403으로 막음(긁어 오기 차단). 우회는 하지 않았다.
3. OM `video_compose._mux_external_audio`: `-af apad -shortest` + 영상 copy 조합이 ffmpeg 7.1에서 끝나지 않음(10분 넘게 CPU 점유 → 내가 끔). 같은 내용을 apad 없이 직접 붙였다.
4. OM `burn_subtitles`: force_style로 글꼴·크기·정렬을 늘 덮어써서, ASS 파일 안 정렬은 `\an5` 태그를 줄마다 넣어야 지켜진다. Windows에서 하위 프로세스 출력 읽기가 cp949로 깨짐(PYTHONUTF8=1로 피함).
5. OM final_review: 줄 깨진 카드·주황 남발·엉뚱한 배경을 못 잡고 'pass'.
6. OM `video_compose` 상태표: ffmpeg가 PATH에 없으면 'ffmpeg false · hyperframes false'로 나옴.

## 음악 출처·라이선스
- OM 무료 음악 길 셋 다 막힘: `pixabay_music` 403, `freesound_music` 키 없음(우리 무료 자원 목록에 없음), `music_gen`은 유료 API 또는 로컬 MusicGen(torch 수 GB·메모리 부족).
- 그래서 OM 판 음악은 **직접 합성한 패드**다: Cmaj7–Am7–Fmaj7–G6 사인파 화음, 46.5초, 숫자로 만든 소리(외부 음원 0) → `tools/openmontage/music_library/firemap_pad_selfmade.wav`(OM의 '내 음악 폴더' 경로). 상업 사용·출처 표기 문제 없음. 섞기·더킹·크기 맞춤은 OM `audio_mixer full_mix`(말 나올 때 음악 0.15배, 목표 −14 LUFS).
- 출처가 확인 안 된 음악은 하나도 넣지 않았다.

## 스톡 영상 출처 (Pexels License https://www.pexels.com/license/ — 상업 사용 가능, 출처 표기 의무 없음)
| 칸 | Pexels ID | 올린 사람 | 무엇 |
|---|---|---|---|
| bg01 0~5.1초 | 6590515 | Sergei Starostin | 10달러 지폐 |
| bg02 5.1~11.0초 | 29587251 | SHOX ART | 폴란드 지폐·동전 (말과 어긋남) |
| bg03 11.0~14.1초 | 34993441 | Jakub Zerdzicki | 즐로티 세는 손 (말과 어긋남) |
| bg04 14.1~18.2초 | 7688135 | Kindel Media | 계산기 든 손 |
| bg05 18.2~24.0초 | 8480284 | ArtHouse Studio | 증권 화면 |
| bg06 24.0~27.3초 | 37676204 | Jakub Zerdzicki | 코인 차트 (어긋남) |
| bg07 27.3~30.9초 | 35606045 | Jakub Zerdzicki | 코인 하락 차트 (어긋남) |
| bg08 30.9~34.0초 | 13801277 | Mizuno K | 뉴욕증권거래소(영국 국기) |
| bg09 34.0~37.2초 | 7578620 | Tima Miroshnichenko | 노트북 앞 지친 사람 |
| bg10 37.2~41.2초 | 20728400 | sabir salam | 흙길 달리는 지프 |
| bg11 41.2~45.1초 | 30098016 | Mohit Singh | 맑은 하늘 |

## 그 밖 라이선스
- HyperFrames Apache-2.0: 우리 코드에 섞어도 문제 없음(고지 유지).
- OpenMontage AGPL-3.0: 도구로 돌려 만든 **영상**에는 의무 없음. 다만 OM 코드를 우리 저장소에 **복사해 넣으면** 그 부분은 AGPL 조건(소스 공개 등)을 따라야 한다 → 들인다면 코드 복사 말고 같은 방법을 우리가 새로 짠다.
- OM의 remotion-composer는 Remotion을 쓴다(우리 영상 파이프라인과 같은 라이선스 조건).
- HyperFrames 판 애니메이션은 GSAP 3.14.2(CDN, 무료 라이선스)로 움직였다.

## 지킨 것 / 어긴 것
- 업로드 0. 시험판·compare는 커밋 안 함(이 폴더 mp4는 .gitignore에 안 걸리니 `git add .` 금지).
- 렌더는 한 번에 하나씩 했다. 다만 **01:09~01:18 OM 1차 렌더(Remotion 기본 동시성)가 01:04에 다시 시작된 C-2 렌더와 겹쳤다** — 시작 전 C-2 렌더가 끝난 것으로 봤는데 다시 돌고 있었다. 그 뒤 렌더(HF 2차·OM 2차·후처리)는 낮은 우선순위(BelowNormal)·동시성 1~2로 돌렸다. C-2 렌더는 02:22 기준 계속 도는 중.
- C 남은 용량 10GB 아래로 안 내려감(최저 20.6GB).

## 들일 것 제안 — 하나
**음악 깔기(더킹 믹스)만 들인다. OpenMontage `audio_mixer full_mix` 방식을 우리 렌더 뒤 단계로.**
- 이유: 세 판을 나란히 보면 가장 크게 다른 것이 '소리가 비는가'다. 우리 파이프라인(Remotion·lfrender·ytlong 관문)에는 지금 음악 단계가 아예 없고, design-spec 10절('말 밑에는 늘 잔잔한 음')을 못 지키고 있다. 화면 쪽(물음표→열기·손 동그라미·끝 하늘)은 HyperFrames 없이도 지금 Remotion 부품으로 옮길 수 있어서 도구를 새로 들일 이유가 약하다. OM의 스톡 고르기·틀·스스로 검사는 위 결함 때문에 그대로 쓰면 품질이 내려간다.
- 방법: OM 코드를 복사하지 않고(AGPL) 같은 ffmpeg 방식(사이드체인 더킹: 말 나올 때 음악 0.15배, attack 200ms·release 500ms → loudnorm −14 LUFS)을 우리 스크립트 몇 줄로 새로 짠다. 음원은 직접 합성 또는 출처·라이선스를 적은 것만. deess 뒤, safezone·bgcheck 앞에 둔다.
- 먼저 할 것: PD가 compare.mp4를 소리 켜고 들어 보고 음악 크기(지금 말 아래 0.15배)를 정한다 — 이 담당은 귀로 확인 안 함.
