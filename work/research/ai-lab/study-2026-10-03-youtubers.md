# AI 활용 유튜버·글 스터디 — 6분야 (2026-10-03, 클라우드 작업실, 브랜치 cloud/ai-study-1003)

지시: work/research/cloud-prompts-1003.md ③. 2026-08-03 이후 'AI 활용법을 가르치는' 유튜브·글에서 도구·명령·순서만 뽑는다. 한국어를 먼저 본다.

## 0. 먼저 알아 둘 한계 (읽는 사람이 꼭 볼 것)
- **유튜브 영상 본문(자막)은 한 편도 못 봤다.** vidIQ는 크레딧이 0이었다(`Not enough credits`, 5크레딧 필요, 청구 0). 이 작업실 네트워크는 youtube.com도 막는다(EGRESS_BLOCKED). 그래서 영상은 **검색 결과에 뜬 제목·설명 요약만** 근거로 쓴다. 영상 속 단계는 모두 '확인 안 함'이다.
- **열 수 있던 곳:** code.claude.com(공식 문서), claude.com 블로그, github.com.
- **막힌 곳:** gpters·브런치·위키독스·oppadu·daleseo·dembrandt.com·remotion.dev·substack·venturebeat 등 대부분의 블로그와 언론. 이런 곳은 **웹 검색 요약문에 나온 문장만** 옮겼다. 표에는 `요약만`이라고 적는다.
- **게시일:** 주소나 검색 요약에 날짜가 있을 때만 적었다. 날짜가 없으면 '확인 안 함'이다. 08-03보다 이른 자료는 `기간 밖(참고)`로 표시했다.
- 이미 하는 일은 교본(work/research/playbooks/*.md), workflow.md, ai-lab/radar.md, meeting/today.md를 grep해서 표시했다.

표기: **본문 봄** = 원문을 직접 열어 읽음 · **요약만** = 검색 요약문만 봄 · **이미 함** = 교본·기록에 이미 있음 · **진행 중** = 다른 세션이나 결재에서 진행 중

---

## 1. 분야별 출처와 뽑은 것

### ① 디자인·웹 화면 (Claude Design · 디자인 토큰 · Dembrandt) — 출처 6
| # | 출처 | 게시일 | 본 정도 | 뽑은 도구·명령·순서 |
|---|---|---|---|---|
| 1-1 | [Claude Design now stays on brand for daily work](https://claude.com/blog/claude-design-stays-on-brand-for-daily-work) (Anthropic 공식) | 2026-06-17, **2026-09-30 갱신** | 본문 봄 | 디자인 시스템을 **GitHub 저장소·디자인 파일·직접 업로드** 중 하나 이상에서 가져온다. Claude Code 안에서 `/design-sync`는 디자인 시스템을 Claude Code로 동기화하고, `/design`은 디자인을 만들고 고치고 동기화한다. **Claude Design은 이제 Claude Code와 사용 한도를 같이 쓴다.** |
| 1-2 | [Claude Design MASSIVE Update: September 2026](https://www.youtube.com/watch?v=OVrJePt-4bs) (유튜브) | 2026-09-20(검색 요약) | 요약만 | 별도 앱이 없어지고 Claude 안의 Design 탭으로 들어왔다. 디자인 시스템은 새로 만들어졌다(DESIGN.md를 Claude Design 형식으로 다시 짓는다). |
| 1-3 | [magicpatterns: Claude Design now lives inside Claude](https://www.magicpatterns.com/blog/claude-design-now-lives-inside-claude) | 9/16 발표(요약) | 요약만 | 채팅에서 바로 디자인을 요청하거나 Artifacts 탭에서 Design을 고르거나 Claude Code에서 부른다. 기존 디자인 시스템은 Settings > Design systems로 옮겨졌다. **옮기다 실패해 처음부터 다시 만든 사용자 보고가 있다.** |
| 1-4 | [GitHub dembrandt/dembrandt](https://github.com/dembrandt/dembrandt) | 릴리스 날짜 확인 안 함(Action v0.37.0) | 본문 봄 | `npm install -g dembrandt` → `dembrandt install-browser` → `dembrandt <주소>` (또는 `npx dembrandt <주소>`, Node 18+). 내보내기 플래그: `--dtcg`(W3C 토큰), `--tailwind`, `--shadcn`, `--html`. 분석 플래그: `--wcag`(명도 대비), `--compare <기준>`(토큰이 바뀌었는지 감지). 범위 플래그: `--crawl n`, `--dark-mode`, `--mobile`. MCP 연결: `claude mcp add --transport stdio dembrandt -- npx -y --package dembrandt dembrandt-mcp`(도구 `get_design_tokens`·`get_color_palette`). |
| 1-5 | [brightcoding: Dembrandt — extract design tokens from any website](https://www.blog.brightcoding.dev/2026/09/20/dembrandtdembrandt-extract-design-tokens-from-any-website) | 2026-09-20(주소) | 요약만 | Playwright로 실제 브라우저에서 화면을 그린다. 계산된 스타일을 읽어 토큰마다 신뢰도를 매긴다. 로그인 없이 100% 로컬에서 돈다. |
| 1-6 | 한국어 유튜브: [왕초보도 가능! 클로드 디자인 활용법 총정리](https://www.youtube.com/watch?v=qGL7LJGPlec) · [클로드 디자인 초보자도… '시스템' 없이 접근](https://www.youtube.com/watch?v=gNgHnkJc29M) · [클로드 디자인 + 코드 최강 조합 홈페이지](https://www.youtube.com/watch?v=vHmJg8VQW5c) · [오빠두엑셀 Claude Design PPT·웹사이트](https://www.oppadu.com/lesson/claude-design-tutrial/) | 전부 확인 안 함 | 요약만 | 참고 스타일 화면 하나를 캡처해 랜딩 페이지를 뽑는다. 회사 브랜드 디자인 시스템을 먼저 등록한 뒤 만든다('시스템 먼저'). 다 만든 디자인은 Claude Code로 넘겨 움직임을 붙인다. |

### ② 롱폼·쇼츠 제작 (대본 · 썸네일 · 코드 모션그래픽 · TTS) — 출처 7
| # | 출처 | 게시일 | 본 정도 | 뽑은 것 |
|---|---|---|---|---|
| 2-1 | [GitHub remotion-dev/skills](https://github.com/remotion-dev/skills) | 확인 안 함(커밋 86개) | 본문 봄 | `npx skills add remotion-dev/skills`. 들어 있는 규칙: 마크업·애니메이션·타이포·오디오·폰트·타이밍, 자막, 지도 애니메이션, 스튜디오·렌더. |
| 2-2 | 한국어 유튜브: [클로드 코드 X remotion 미친 조합](https://www.youtube.com/watch?v=uQPegX8CiyA) · [클로드 코드로 유튜브 영상을 자동화](https://www.youtube.com/watch?v=UM9FmXJQ3yg) · [Claude Code 영상 제작 기능 써봤는데](https://www.youtube.com/watch?v=S-foS0vfqIg) · [Remotion + Opus 5.5](https://www.youtube.com/watch?v=6_rCyryA6hg) | 확인 안 함(Opus 5.5 영상은 9/22 출시 뒤 것으로 추정되나 확인 안 함) | 요약만 | 리모션 스킬을 설치하고 "영상 만들어줘"라고 말하면 글자·도형 모션그래픽(인트로·홍보)이 나온다. |
| 2-3 | Threads @seize.more [쇼츠 자동화 글](https://www.threads.com/@seize.more/post/DWBXH9uEiU_) | 확인 안 함 | 요약만 | Remotion + Claude Code + edge-tts 조합이다. **씬 템플릿을 React로 만들어 두고 주제만 바꾼다.** 순서는 주제 → 대본 → TTS → 자막 타이밍 → 렌더. |
| 2-4 | [GitHub scalemaker-ship-it/longform-to-shorts](https://github.com/scalemaker-ship-it/longform-to-shorts) (Claude Code 스킬) | 확인 안 함(커밋 1개) | 본문 봄 | `git clone … ~/.claude/skills/longform-to-shorts` + Pillow + ffmpeg. "이 영상으로 숏폼 4개 만들어줘" 또는 `python3 scripts/make_short.py --config my_shorts.json`. 순서: 자막을 읽는다 → 후킹 구간을 고른다 → 2줄 제목을 단다 → ffmpeg로 9:16 크롭·강조색 → 채널 라벨·말풍선. |
| 2-5 | HyperFrames(HeyGen, HTML→MP4): [kitpa](https://kitpa.org/news/1440) · [silenceper](https://silenceper.com/en/article/2026-05-02-hyperframes-html-video-rendering/) · 한국어 유튜브 [클로드 코드로 영상 만드는 법 하이퍼프레임](https://www.youtube.com/watch?v=WofSIoEj_CQ) | 2026-05-02(silenceper) = **기간 밖(참고)**, 유튜브 날짜는 확인 안 함 | 요약만 | `npx hyperframes init` → `preview` → `render`. Node 22+와 FFmpeg가 필요하다. 헤드리스 Chrome으로 프레임을 캡처한다. |
| 2-6 | 썸네일: [캐럿 블로그 나노바나나 썸네일](https://carat.im/blog/youtube-thumbnail-creation-nanobanana) · [네이트 '유튜브 쇼츠 맞춤 썸네일·애스크 스튜디오'](https://m.news.nate.com/view/20260726n02071) | 캐럿 확인 안 함 · 네이트 2026-07-26 = **기간 밖(참고)** | 요약만 | 나노바나나 2는 한글 글자를 바로 쓸 수 있는 수준이라고 한다. 유튜브는 YPP 창작자에게 쇼츠 맞춤 썸네일을 열었고, '애스크 스튜디오'에 썸네일 생성이 들어갔다. |
| 2-7 | TTS: [캐럿 블로그 구글 TTS 가이드](https://carat.im/blog/google-tts-guide) · [Google Gemini-TTS 문서](https://docs.cloud.google.com/text-to-speech/docs/gemini-tts) | 확인 안 함 | 요약만 | AI Studio의 generate-speech 화면에서 무료로 만든다. Cloud TTS의 Neural2를 권한다. Gemini 3.1 Flash TTS는 4/15에 나왔다(기간 밖). |
| (대본) | [ChatGPT 유튜브 롱폼 대본 작성법 7프롬프트](https://junetapa.com/blog/dev/posts/ai-tools/chatgpt-%EC%9C%A0%ED%8A%9C%EB%B8%8C-%EB%8C%80%EB%B3%B8-%EC%9E%91%EC%84%B1%EB%B2%95.html) · [브런치 '클로드를 썼더니 유튜브가 떡상'](https://brunch.co.kr/@melanie-jg/304) | 확인 안 함 | 요약만 | 순서는 개요 → 섹션별 집필 → 제목·썸네일 문구다. 첫 15초 후킹과 챕터를 쓴다. (새것이 없어서 출처 수에 넣지 않음.) |

### ③ 네이버 글·검색 노출 — 출처 6
| # | 출처 | 게시일 | 본 정도 | 뽑은 것 |
|---|---|---|---|---|
| 3-1 | [원포인트: 네이버 AI 브리핑에 인용되는 콘텐츠 설계법](https://1point.kr/blog/insights/naver-ai-briefing-content-design/) | 확인 안 함 | 요약만 | **인용의 49.3%가 검색 상위 10위 밖 문서**에서 나왔다. 출처는 블로그 158건, 외부 웹 45건, 네이버 DB 44건, 카페 19건이다. 할 일: **첫 문단에서 질문에 바로 답하기, 질문형 소제목과 FAQ 구조, 직접 경험·자체 데이터.** |
| 3-2 | [파이낸셜뉴스: AI 브리핑 도입 후 창작자 지원 2배](https://www.fnnews.com/news/202608071146444762) · [AI타임스](https://www.aitimes.com/news/articleView.html?idxno=213684) | 2026-08-07(주소) | 요약만 | 네이버 메이트는 **AI 브리핑 인용 횟수**·주제 전문성·활동성으로 매달 약 3,000명을 뽑는다. 활동지원금은 연 약 200억 원이다. 5월 대비 7월 인용은 114% 늘었다. |
| 3-3 | [서울경제: 다시 힘준 블로그…AI 브리핑 인용 2배](https://www.sedaily.com/article/20084959) ([네이트](https://m.news.nate.com/view/20260830n12848)) | 2026-08-30(주소) | 요약만 | 블로그가 AI 브리핑 인용의 중심이다(3-1과 같은 흐름). |
| 3-4 | Threads @blog.oppa [AI 브리핑 인용수](https://www.threads.com/@blog.oppa/post/DZJZOCWEwpi/) | 확인 안 함 | 요약만 | 인용수는 2026년 1월부터 누적으로 센다. 인용수가 높을수록 메이트에 뽑힐 확률이 오른다. |
| 3-5 | [moneyroan: 네이버 AI 글 노출 안 되는 이유(2026)](https://moneyroan.com/naver-ai-blog-not-exposed-reason-2026/) · [AI 블로그 저품질 체크리스트](https://moneyroan.com/ai-blog-low-quality-checklist-2026/) | 확인 안 함 | 요약만 | '매끄럽지만 어디서나 보는 표현'은 독창성이 낮다고 판정된다. 체류 시간이 짧은 글이 반복되면 저품질로 간다. 1인칭 경험이 독창성 신호가 된다. |
| 3-6 | [ranketai: 2026 네이버 AI 검색 정리](https://www.ranketai.com/ko/blog/explainer-ranketai-guide-09-naver-ai-search-vs-google-ai-overview-2026-05-20) | 2026-05-20(주소) = **기간 밖(참고)** | 요약만 | AI 탭은 4/28 베타를 거쳐 6/26에 정식으로 열렸다. 블로그·카페 탭은 통합탭(피드형)으로 바뀌었다. |
| (유튜브) | 2026-08 이후 네이버 AI 브리핑을 다룬 한국어 **유튜브 영상은 검색에서 못 찾았다** | — | — | 확인 안 함 |

### ④ 에이전트 운영 (사용량 아끼기 · 클라우드 세션) — 출처 6
| # | 출처 | 게시일 | 본 정도 | 뽑은 것 |
|---|---|---|---|---|
| 4-1 | [Claude Code Docs: Manage costs effectively](https://code.claude.com/docs/en/costs) (공식) | 문서라 게시일 없음(2026-10-03 열람) | 본문 봄 | `/usage`는 Pro·Max에서 **스킬·서브에이전트·플러그인·MCP 서버별 사용 비중**, 비중 10% 이상인 행동(긴 맥락·캐시 미스), **무거운 `/loop`·예약 작업 순위**를 보여 준다(`d`/`w`로 24시간/7일 전환). `/clear`는 작업 사이에 쓰고 비용이 0이다(`/compact`는 그 자체가 큰 요청). CLAUDE.md는 200줄 아래로 두고 업무별 지침은 스킬로 옮긴다(필요할 때만 읽힘). 기본 모델은 Sonnet, 단순 서브에이전트는 `model: haiku`. 안 쓰는 MCP는 `/mcp`에서 끄고 `gh` 같은 CLI를 우선한다. PreToolUse 훅으로 테스트 출력을 실패 줄만 남긴다. `/effort`로 노력 수준을 낮춘다(Opus 5.5·Sonnet 5.5는 생각을 끌 수 없음). **예약 작업은 쉬는 동안에도 맥락 전체를 보낸다.** 캐시 수명은 구독이면 1시간, 사용 크레딧으로 넘어가면 5분이다. `/insights`는 습관 보고서다. |
| 4-2 | [Claude Code Docs: 클라우드에서 Claude Code 사용하기](https://code.claude.com/docs/ko/claude-code-on-the-web) (공식) | 문서(2026-10-03 열람) | 본문 봄 | `claude --cloud "<작업>"` 한 줄이 세션 하나다(여러 줄이면 병렬). **`claude -p "메시지" --cloud <session-id>`로 돌고 있는 클라우드 세션에 후속 메시지를 큐에 넣는다.** `claude --teleport`로 클라우드 세션을 터미널로 가져온다. 클라우드에서 `/clear`는 안 되고 `/compact`·`/context`는 된다. `/model sonnet`처럼 인수로 넘긴다. `.claude/agents/`의 서브에이전트를 자동으로 쓴다. **제한: 클라우드 세션은 계정의 다른 Claude·Claude Code 사용과 속도 제한을 공유한다. 병렬로 돌리면 그만큼 더 쓴다. VM 요금은 따로 없다.** |
| 4-3 | [위키독스 오픈위키: 클로드 코드 클라우드 세션 정식 출시, 크레딧 $100·$250](https://wikidocs.net/blog/@openwiki/31700/) | 2026-09-24 정식 출시(요약) | 요약만 | 리서치 프리뷰가 정식 기능이 됐다. 노트북을 꺼도 돈다. 크레딧 조건은 원문을 못 열어 확인 안 함. |
| 4-4 | [pasqualepillitteri: Opus 5.5와 사용량 리셋](https://pasqualepillitteri.it/en/news/17905/claude-free-usage-limit-reset-opus-5-5) · [buildthisnow: Opus 5.5 in Claude Code](https://www.buildthisnow.com/blog/guide/mechanics/claude-opus-5-5-in-claude-code) | Opus 5.5 9/22(요약) | 요약만 | 9/22에 5시간 한도가 올랐다. 9/14부터 주간 한도가 5월 전 기준보다 25% 높다. 구독자에게 **아무 때나 쓰는 한도 리셋 1회**가 주어졌고 만료는 **10/22**다(2차, 확인 안 함). 일상 작업은 effort medium을 기본으로 한다. |
| 4-5 | [인프런: 클로드 코드 토큰·사용량 절약법 10가지](https://www.inflearn.com/pages/claude-code-token-and-usage) · [gpters: 토큰 절약 10가지](https://www.gpters.org/nocode/post/claude-code-10-ways-oI1jGRGq1B15beN) | 확인 안 함 | 요약만 | 프롬프트를 하나로 합친다. 에러는 줄 번호와 메시지만 준다. CLAUDE.md를 쓰고 `/compact`를 쓴다. 5시간 롤링 창에 맞춰 작업을 나눈다. |
| 4-6 | 한국어 유튜브 [클로드 코드 2시간 마스터 통합본](https://www.youtube.com/watch?v=vxEvo2BLM6A) | 확인 안 함 | 요약만 | 커스텀 스킬, 서브에이전트 병렬, Hooks 자동화. |

### ⑤ 차트 시각화 — 출처 4
| # | 출처 | 게시일 | 본 정도 | 뽑은 것 |
|---|---|---|---|---|
| 5-1 | [claudecodehq: Claude Dataviz Skills](https://www.claudecodehq.com/blog/claude-dataviz-skills) · [getknack: /dataviz 스킬](https://getknack.ai/blog/claude-code-dataviz-skill) | 2026-09-26(요약) | 요약만 | Claude Code 내장 `/dataviz` 스킬(7월 변경 기록)은 차트 종류 고르기, 데이터 화면 배치, **실행 가능한 색 팔레트 검증기**를 담고 있다. 차트를 요청하면 자동으로 켜지고 `/dataviz`로 직접 부를 수도 있다. **이 작업실 세션의 스킬 목록에도 `dataviz`가 있다(직접 확인).** |
| 5-2 | [GitHub ThamJiaHe claude-code-handbook: 모션그래픽 Remotion 가이드](https://github.com/ThamJiaHe/claude-code-handbook/blob/main/docs/motion-graphics-claude-remotion-guide.md) · [gaga.art Remotion Skills](https://gaga.art/blog/remotion-skills/) | 확인 안 함 | 요약만 | JSON 값 배열을 받아 막대 너비가 데이터대로 움직이는 막대 차트 영상을 만든다. "월 매출 막대 차트를 부드러운 전환으로" 같은 문장이 Remotion 코드가 된다. |
| 5-3 | [GitHub indi256s/dataviz-skill](https://github.com/indi256s/dataviz-skill) | 확인 안 함 | 요약만 | ECharts 테마와 템플릿을 담은 대시보드 스킬이다. |
| 5-4 | 한국어 유튜브 [[클로드코드 AI 데이터시각화] 7. 첫번째 세션 실습](https://www.youtube.com/watch?v=NzxkIXYEZmY) (패스트캠퍼스 전서연 강의 관련, 요약) | 확인 안 함 | 요약만 | 강의 단계는 확인 안 함. |

### ⑥ 제휴 수익화 — 출처 5
| # | 출처 | 게시일 | 본 정도 | 뽑은 것 |
|---|---|---|---|---|
| 6-1 | [이데일리: 쿠팡 약관 개정 4가지](https://www.edaily.co.kr/News/Read?newsId=02784726645544040) ([다음](https://v.daum.net/v/20260804081652382)) | 2026-08-04(주소), **9/3 시행** | 요약만 | **로봇·스파이더·스크레이퍼 같은 자동화 프로그램으로 시스템에 접근하거나 데이터를 모으는 행위를 금지 대상으로 명확히 적었다.** 우회 계정 제재도 강화했다. 회원 게시물을 AI 학습에 쓸 수 있게 됐다. |
| 6-2 | [챌린지클래스: 2026 AI 자동화 블로그 수익화 강의(알파남 유튜브 라이브)](https://cclass.kr/product/2026-ai-%EC%9E%90%EB%8F%99%ED%99%94-%EC%9B%94-300%EB%A7%8C%EC%9B%90-%EB%B2%84%EB%8A%94-ai-%EB%B8%94%EB%A1%9C%EA%B7%B8-%EC%88%98%EC%9D%B5%ED%99%94-%EB%B9%84%EB%B0%80-%ED%95%B5%EC%8B%AC-%EB%85%B8%ED%95%98%EC%9A%B0-%ED%8F%AD%EB%A1%9C-%EA%B0%95%EC%9D%98/13/) | 라이브 2026-09-02(요약) | 요약만 | 강의 내용은 확인 안 함(유료 강의 홍보 페이지). |
| 6-3 | 유튜브 쇼핑 제휴(쿠팡 태그): [colosseum 입점 가이드(2026)](https://colosseum.global/market-trend/youtube-shopping-affiliate-guide/) · [viralpulse](https://viralpulse.net/blog/youtube-shopping-affiliate-guide) | 확인 안 함 | 요약만 | 한국 제휴사는 쿠팡이다. 영상에 제품을 태그하고 구매되면 수수료를 받는다. 조건은 YPP 기본 자격(구독자 500명 + 시청 3,000시간 또는 쇼츠 300만 회)이다. |
| 6-4 | [Medium: Claude AI로 제휴 마케팅(2026)](https://medium.com/write-a-catalyst/can-you-use-cloud-ai-for-affiliate-marketing-yes-i-did-2026-7322730c1353) · [유튜브 Claude AI + Pinterest 제휴](https://www.youtube.com/watch?v=oJa-YpcZBzA) | 확인 안 함 | 요약만 | 구매 의도가 높은 좁은 주제를 고른다. 비교·'best of'·리뷰 글을 Claude로 쓴다. |
| 6-5 | 대가성 문구(쿠팡 파트너스): [아이보스 토론](https://www.i-boss.co.kr/ab-6141-41877) | 확인 안 함 | 요약만 | '이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.' 문구가 빠지면 계정 정지 위험이 있다. |

**분야별 출처 수(표 행 기준, 묶음 행은 1로 셈):** ① 6 · ② 7 · ③ 6 · ④ 6 · ⑤ 4 · ⑥ 5 = 34행. 이 가운데 **2026-08-03 이후 게시가 확인된 것**은 ①1-1(9/30 갱신)·1-2(9/20)·1-3(9/16)·1-5(9/20), ③3-2(8/7)·3-3(8/30), ④4-3(9/24)·4-4(9/22), ⑤5-1(9/26), ⑥6-1(8/4)·6-2(9/2)다. 나머지는 날짜를 확인 안 함이거나 기간 밖이다.

---

## 2. 방법마다 담당·바꿀 것·효과·비용·위험

| ID | 방법 | 담당 | 바꿀 것 | 효과 | 비용 | 위험 | 상태 |
|---|---|---|---|---|---|---|---|
| A1 | Dembrandt로 레퍼런스(토스·뱅크샐러드·KRDS) 토큰 뽑기 `npx dembrandt <주소> --dtcg --mobile` | designer | design/tokens-ref/에 저장하고 ds-v2와 표로 비교 | 시안이 '레퍼런스 토큰 안'에서 나와 심사 점수 6.75→7 이상을 노림(today.md 목표) | 무료·로컬(MIT) | 남의 브랜드 토큰을 그대로 쓰면 겉모습 모방이 된다. 비교용으로만 쓴다 | **진행 중**(today.md 10/3, 클라우드 cloud/design-tokens-1003) |
| A2 | Dembrandt를 **우리 사이트에** 써서 회귀 관문으로: `dembrandt firemap.kr --dtcg` 기준본을 만들고 배포 전에 `--compare` + `--wcag` + `--dark-mode` | product-dev(+designer) | D트랙 배포 전에 자동 검사 1줄. 토큰이 기준본과 다르면 [디자인 검수 요청] | '화면 모양이 조금이라도 바뀌면 D가 아니다'(workflow.md)를 사람 대신 숫자로 잡는다. 다크 카드 대비 2.71 같은 사고(designer.md 10/1)를 미리 막는다 | 무료. Chromium 설치 1회 | 휴리스틱 오탐이 있을 수 있다. `--compare` 출력 형식은 확인 안 함 → 1회 시험 후 판정 | 새로 |
| A3 | Dembrandt MCP 연결 `claude mcp add --transport stdio dembrandt -- npx -y --package dembrandt dembrandt-mcp` | designer | 디자이너 세션에서 대화 중 토큰 조회 | CLI로도 같은 걸 얻는다 | 무료. MCP 정의만큼 맥락이 든다 | 공식 문서는 CLI가 MCP보다 맥락 효율이 낫다고 한다 → **CLI 우선, MCP는 보류** | 보류 |
| A4 | Claude Design 9월 개편 재시험: Claude Code에서 `/design-sync`(우리 저장소 디자인 시스템 동기화) → `/design` | designer | X-TOOL-1 판정에 '9월 개편 후 Claude Code 경로' 한 줄 추가 | 10/1 탈락 사유('무인 세션은 로그인 화면이라 열람 불가')가 Claude Code 경로로 풀리는지 본다 | 구독 안. **Claude Code와 한도 공유**(공식) | 마이그레이션 실패 보고(2차). 한도를 같이 쓴다 | 새로(10/1 판정 뒤 바뀜) |
| B1 | Remotion 공식 에이전트 스킬 `npx skills add remotion-dev/skills` | motion-designer · video-producer | 프로젝트에 스킬을 설치하고 자막·오디오·타이밍 규칙을 받는다 | 우리 교본(프레임·interpolate·yuv420p)과 겹치지 않는 규칙(자막·지도)을 얻는다 | 무료 | 스킬 규칙이 우리 규칙(색·출처 표시)과 부딪칠 수 있다 → 교본이 우선 | 새로(Remotion 자체는 **이미 함**) |
| B2 | 씬 템플릿 + 주제만 교체 | video-producer | — | — | — | — | **이미 함**(<편>props.py + <편>.tsx, firemap-video-producer.md) |
| B3 | edge-tts 내레이션 | — | — | — | — | 비공식 경로라 공개 영상 약관이 애매하다(longform-research.md) | **이미 배제** |
| B4 | Gemini TTS(AI Studio·API) | video-producer | — | — | — | — | **이미 함**(gemini-3.8-flash-tts, lfvoice readback) |
| B5 | 롱폼 → 쇼츠 하이라이트 자르기(longform-to-shorts 방식: 자막 → 후킹 구간 → 2줄 제목 → ffmpeg 9:16) | shorts | 롱폼 1편당 쇼츠 1~2편을 롱폼 장면에서 바로 뽑는 칸 추가. 스킬을 복제하지 말고 순서만 빌려 우리 Remotion 장면 번호로 자른다 | 쇼츠 → 롱폼 '관련 동영상' 연결(shorts.md 5)이 같은 장면이라 자연스럽다. 추가 TTS가 0이다 | 렌더 시간만 | 같은 사실표 두 번째 쇼츠 금지 규칙(firemap-shorts 10/3)과 부딪친다 → 롱폼 연결 쇼츠는 예외로 둘지 결재 | 새로 |
| B6 | HyperFrames(HTML→MP4) | — | — | Remotion이 있어 더 얻을 게 적다 | — | 도구가 둘로 갈린다 | 탈락(기간 밖 자료) |
| B7 | 나노바나나 2 한글 썸네일 | visual-designer | — | — | 장당 유료(radar: 무료 등급 0) | 제미나이 이미지 결재 '보류' | **보류**(radar 10/1과 같은 결정) |
| B8 | 첫 15~30초 후킹·챕터 | youtube-loop · PD | — | — | — | — | **이미 함**(도입 30초 원칙, chapters.py) |
| C1 | **AI 브리핑 인용 구조**: 첫 문단에서 검색 질문에 바로 답하기 + 질문형 소제목 + 끝에 FAQ 2~3문항 + 표 1개 + '내가 계산해 보니' 1인칭 한 줄 | firemap-write · firemap-editor | write.md 체크리스트에 4줄 추가. aitell/humanlike 관문에 '첫 문단에 숫자 답이 있나', '질문형 소제목 ≥2' 검사 추가(코드 변경 시 test_*.py 필수) | 인용의 49%가 상위 10위 밖에서 나온다(3-1). 검색 순위가 낮은 카페·블로그도 인용될 길이 생긴다 | 0(글 규칙 + 검사 코드) | 모든 글이 같은 틀이면 '같은 템플릿 대량 발행 = 스팸'(write.md 3)에 걸린다 → 틀은 고정하고 문장은 바꾼다. FAQ가 본문을 되풀이하지 않게 | **일부 이미 함**(경험·출처·구조는 write.md 1·2. 첫 문단 답·질문형 소제목·FAQ 검사는 없음) |
| C2 | AI 브리핑 인용수를 지표로 잰다 | growth | 주간 보고에 '인용된 글 수' 칸 추가(수집 방법은 확인 안 함: 네이버 창작자 화면에 인용수가 보이는지 원문 미확인) | C1의 효과를 판정할 숫자 | 0 | 측정 경로가 없으면 칸만 생긴다 | 새로 |
| C3 | 네이버 메이트(인용수 기반 월 3,000명, 연 200억) | growth → 순돌이 | 조건 확인만. 신청·가입이 필요하면 [결재 필요] | 지원금 수익 가능성 | 0 | 블로그는 지금 STOP_blog로 정지다. 카페가 대상인지 확인 안 함. 가입 금지 규칙 → 결재 | 새로(조사만) |
| C4 | 쇼츠를 네이버 클립에도 올려 AI 브리핑 인용 경로 추가 | shorts · growth | — | — | — | 업로드 자동화 가능 여부 확인 안 함 | **진행 중**(plan_2026-09-29, tools-wanted) |
| D1 | **클라우드 세션 사용량 사실 확인**: 공식 문서는 "클라우드 세션은 계정의 다른 사용과 속도 제한을 공유"라고 한다. 지시문은 "크레딧 $250에서 빠지고 PC 주간 사용량은 안 쓴다"라고 한다 | 순돌이 · admin(총무) | 오늘 10/3 '시작 전 85%' 실측(today.md)과 이 세션이 끝난 뒤 주간 %를 비교해 decisions/log.md에 기록. 크레딧 조건 원문(4-3)도 확인 | 맞다면 클라우드로 일을 옮기는 계획 전체가 성립한다. 틀리면 주간 한도를 두 배 속도로 쓴다 | 0 | 확인 전에 클라우드 병렬 투입을 늘리면 주간 한도가 바닥난다 | 새로(가장 급함) |
| D2 | `claude -p "메시지" --cloud <session-id>` — 돌고 있는 클라우드 세션에 PC에서 다음 일을 큐에 넣는다 | 순돌이 | 작업실 규칙 '일 받는 법'에 이 명령을 적는다(지금은 사장님이 세션을 열고 순돌이가 메시지를 보냄. 그 방식이 이 명령인지는 확인 안 함) | 사장님이 세션을 다시 열지 않아도 일을 보낸다 | 0 | 세션이 보관되면 실패한다(`archived`) → 실패 시 새 세션 | 새로(이미 쓰는지 확인 안 함) |
| D3 | `/usage` 사용 내역 분석(스킬·서브에이전트·MCP·**루프·예약 작업별 토큰 순위**, 24시간/7일) | admin(총무) · 운영실장 | 총무 07:4x 사용량 보고(workflow.md '하루 약 18%p')에 '상위 3개 먹는 곳' 줄을 추가 | 무엇이 한도를 먹는지 알아야 줄인다. 예약 작업은 쉬는 동안에도 맥락 전체를 보낸다(공식) | 0 | 이 기계의 로컬 기록만 센다(claude.ai·다른 기기는 빠짐) | 새로 |
| D4 | 모델 나눠 쓰기(Sonnet 기본, 단순 서브에이전트 Haiku) | 운영실장 | — | — | — | — | **진행 중**(bench/2026-10-01-model-tiers.md, Sonnet 1주 시험, Haiku는 탈락) |
| D5 | 교본·CLAUDE.md를 짧게 두고 업무별 지침은 스킬로(필요할 때만 읽힘). CLAUDE.md는 200줄 아래 | 운영실장 · improve | 직원 지시문이 매 회차 읽는 파일 크기를 재고(lessons.md·교본) 긴 부분을 '필요 시 읽기'로 나눈다 | 회차마다 반복해 읽는 토큰이 준다 | 정리 시간 | 규칙을 빠뜨릴 위험 → 체크리스트는 남기고 근거·사례만 옮긴다 | 새로 |
| D6 | PreToolUse 훅으로 테스트·로그 출력을 실패 줄만 남기기 | product-dev | .claude/settings.json 훅 + 스크립트(공식 예시 그대로) | 테스트 출력 수만 토큰을 수백으로 줄인다(공식) | 0 | 실패 맥락이 잘릴 수 있다(`grep -A 5`) | 새로 |
| D7 | `/effort` medium을 기본으로, 어려운 일만 high | 운영실장 | 투입 시 effort 지정(가능한 곳만) | 생각 토큰은 출력 요금이다(공식) | 0 | 품질 저하는 일감별로 비교해야 안다(D4 방식) | 새로 |
| D8 | Opus 5.5 출시 기념 **한도 리셋 1회(만료 10/22)** | 순돌이 | 있는지 claude.ai에서 확인하고 주간 한도가 바닥나는 날에 쓴다 | 막힌 하루를 살린다 | 0 | 2차 자료라 확인 안 함 | 새로(확인만) |
| E1 | **내장 `/dataviz` 스킬 + 팔레트 검증기**로 차트 색·종류 검사 | visual-designer · motion-designer · product-dev | 차트 만들기 전에 `/dataviz`를 부르고, 우리 의미색(주황=우리 숫자, 빨강/파랑=등락)을 검증기에 넣어 색맹·대비를 잰다 | E-1 감사의 '회사색이 의미색과 부딪침'(motion-designer.md 10/1) 같은 실수를 만들기 전에 잡는다 | 0(내장) | 스킬 기본 팔레트를 그대로 쓰면 우리 토큰과 어긋난다 → 우리 색으로 바꿔 넣는다 | 새로 |
| E2 | JSON 값 → 움직이는 막대·선 차트(Remotion) | motion-designer | — | — | — | — | **이미 함**(heatmap.py·chartimg·Remotion, FT 비주얼 어휘) |
| F1 | 대가성 문구를 제목이나 첫 부분에 | write · copywriter | — | — | — | — | **이미 함**(write.md 7, D-1 desc의 쿠팡 문구) |
| F2 | **쿠팡 약관(9/3 시행)의 자동화 금지 점검** | admin(총무) · growth | revenue_daily.py가 하는 '크롬 MCP로 쿠팡 리포트 읽기'와 f2_coupang.py가 쿠팡 쪽에 접근하는 방식을 약관 원문과 대조. 파트너스 약관이 일반 이용약관과 따로인지 확인 | 계정 정지(수익 0) 위험을 미리 막는다 | 0 | 원문을 못 봐서 우리 방식이 해당하는지 확인 안 함. 위반이면 수동 입력으로 바꾼다 | 새로 |
| F3 | 유튜브 쇼핑 제휴(쿠팡 태그) | growth · youtube-loop | YPP 자격(500명 등) 도달 시 영상 설명 링크 대신 제품 태그 | 쇼츠에서는 설명란 링크가 안 눌린다(shorts.md 5). 태그는 눌린다 | 0 | @firemapkr 자격 여부 확인 안 함 | 새로(자격 대기) |
| F4 | Claude로 구매 의도 높은 비교·'best of' 글 | — | — | 돈 글(YMYL)에 상품 비교를 섞으면 신뢰를 잃는다 | — | — | 탈락 |

---

## 3. 효과 순 상위 10

| 순위 | ID | 한 줄 | 담당 | 상태 |
|---|---|---|---|---|
| 1 | D1 | 클라우드 세션이 주간 한도를 쓰는지 오늘 실측으로 판정한다. 공식 문서는 '공유'라고 하고 지시문은 '안 씀'이라고 한다 | 순돌이·총무 | 새로 |
| 2 | C1 | 카페·블로그 글에 '첫 문단 답 + 질문형 소제목 + FAQ + 표 + 1인칭 계산'을 넣고 관문에서 검사한다(AI 브리핑 인용의 49%는 상위 10위 밖) | write·editor | 일부 이미 함 |
| 3 | F2 | 쿠팡 9/3 약관의 자동화·스크레이퍼 금지를 우리 쿠팡 리포트 수집·링크 생성 방식과 대조한다 | 총무·growth | 새로 |
| 4 | D3 | `/usage` 내역(스킬·서브에이전트·MCP·예약 작업별 순위)을 총무 사용량 보고에 붙인다 | 총무·운영실장 | 새로 |
| 5 | E1 | 차트를 만들기 전에 내장 `/dataviz` 스킬과 팔레트 검증기로 우리 의미색을 검사한다 | 비주얼·모션·제품 | 새로 |
| 6 | A2 | Dembrandt `--compare`·`--wcag`·`--dark-mode`로 firemap.kr 화면 토큰 회귀를 배포 전에 자동으로 잡는다 | 제품 개발·디자이너 | 새로(A1은 진행 중) |
| 7 | D5+D6 | 매 회차 읽는 교본·CLAUDE.md를 줄여 스킬로 나누고, 테스트 출력은 훅으로 실패 줄만 남긴다 | 운영실장·제품 개발 | 새로 |
| 8 | B1 | Remotion 공식 에이전트 스킬(`npx skills add remotion-dev/skills`)을 설치해 자막·오디오·타이밍 규칙을 받는다 | 모션·PD | 새로(Remotion은 이미 함) |
| 9 | B5 | 롱폼 장면에서 바로 쇼츠 1~2편을 자른다(후킹 구간 → 2줄 제목 → 9:16). 추가 TTS 0 | 쇼츠 | 새로(결재: 사실표 중복 규칙 예외) |
| 10 | A4 | Claude Design 9월 개편 뒤 Claude Code 경로(`/design-sync`·`/design`)로 10/1 탈락 사유가 풀리는지 다시 시험한다 | 디자이너 | 새로 |

차순위: D2(`claude -p --cloud <id>` 후속 메시지), C3(네이버 메이트 조건 확인), D8(한도 리셋 1회 10/22 만료 확인), D7(effort medium).

## 4. 확인 안 함 (모아 보기)
- 유튜브 영상 전부의 실제 단계(자막을 못 봄 — vidIQ 크레딧 0, youtube.com 접속 차단).
- 한국어 유튜브 영상들의 게시일(①1-6, ②2-2·2-5, ④4-6, ⑤5-4).
- 2026-08 이후 네이버 AI 브리핑을 다룬 한국어 유튜브 영상(검색에서 못 찾음).
- 클라우드 세션 크레딧 $100·$250 조건 원문(위키독스 차단). 공식 문서의 '속도 제한 공유'와 지시문의 '주간 사용량 안 씀' 중 무엇이 맞는지.
- Opus 5.5 한도 리셋 1회·10/22 만료(2차 자료).
- 쿠팡 9/3 약관 원문, 그리고 쿠팡 파트너스에도 그 조항이 적용되는지.
- Dembrandt `--compare`의 출력 형식과 종료 코드.
- 네이버 창작자 화면에서 AI 브리핑 인용수를 볼 수 있는지, 메이트에 카페가 대상인지.
- @firemapkr의 유튜브 쇼핑 제휴 자격.
- remotion-dev/skills·longform-to-shorts·dataviz-skill 저장소의 최근 커밋 날짜.
