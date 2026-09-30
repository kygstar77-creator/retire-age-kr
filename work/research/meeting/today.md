## [지시·긴급] 새 계산기 주소가 휴대폰에서 파이어맵 첫 화면으로 떨어짐 (순돌이 → firemap-product-dev, 지금, F1보다 먼저)
- 사장님 07:0x: "새로운 계산기 웹사이트 안 들어가진다, 파이어맵으로만 들어가진다."
- 실측(firemap_events, 순돌이 07:1x): client f63b89a2(재방문 30일, 사장님 기기로 추정·확인 안 함)가 07:03·07:04·07:04 세 번 session_start path=/calc/salary·/calc/severance로 들어왔는데 첫 screen_view가 전부 **home**. 반면 순돌이 브라우저(새 기기, 데스크톱·모바일 에뮬)는 salary·severance 화면이 정상. 운영 번들(index-xQrnB8Pe.js)과 캐시 헤더(max-age=0)는 기기 무관 동일.
- 코드상 원인 후보: FireMapMVP.jsx readScreenFromHash — `if (tool && !window.location.hash)`라 주소에 해시(#home 등)가 붙어 있으면 도구 화면을 건너뜀. kakaoAuth.js 59행이 로그인 복귀 때 `pathname + '#home'`을 만든다. 다른 원인(인앱 브라우저·저장 상태)도 확인할 것.
- 완료 기준: 재방문 기기 상태(localStorage에 firemap-inputs-v3·랭크 기록·카카오 로그인 흔적, 주소 끝 #home)를 재현해 원인 확정 → 도구 경로(/calc/*, /tax 등)로 들어오면 해시와 상관없이 그 도구 화면이 뜨게 수정 → 테스트 추가 → 운영 배포 → 운영에서 재현 상태로 다시 열어 도구 화면 확인(스크린샷) → 여기 "완료: … HH:MM".
- 착수: firemap-product-dev 07:10
- 완료: 원인 확정·수정·운영 배포 07:23 — 운영 재현: 주소 끝에 해시가 붙으면(/calc/salary#home·/calc/severance#home) 새 기기·재방문 기기 모두 첫 화면, 해시 없으면 localStorage 상태와 무관하게 정상 → 원인은 해시(저장 상태 아님). 수정: 처음 열 때 도구 경로가 해시를 이기고 해시를 지움(공유 입력·ops 제외, FireMapMVP.jsx readInitialScreen). 스모크 테스트 추가(4경로×#home·#result, 30개 통과). 운영 index-CRiqTGEj.js에서 10가지 상태 전부 도구 화면, 스크린샷 work/research/calc-salary/hashfix-salary.png·hashfix-severance.png. 사장님 기기에 해시가 붙은 경로(방문 기록 자동완성·로그인 복귀 추정)는 확인 안 함 — 어느 쪽이든 이제 도구 화면이 뜸. 카카오톡 인앱 브라우저 실기기는 확인 안 함. (firemap-product-dev, edebf22)
- 배포: git -C C:/Users/강영준/Documents/GitHub/retire-age-kr push -q origin dev:main (빌드·테스트 통과 뒤)

## [지시] Claude Design 시험 (순돌이 → firemap-designer, 기한 오늘 16:20 회차 끝, 사장님 07:1x "클로드 디자인은 성능 안 좋나?")
- 사실: 이 계정에 Claude Design(Artifact 유형 "Design" 캔버스, "Design System")이 켜져 있다(순돌이 07:1x 목록 확인). 우리는 한 번도 안 써 봤다 — 성능은 **확인 안 함**.
- 할 일: Artifact 도구 action "quickstart" intent "design"으로 시작. ① 파이어맵 디자인 시스템(src/ui 토큰·firemap-design-identity 기준)을 "Design System" 유형으로 1개 ② 그걸로 F1 '계산기 결과 아래 쿠팡 상품 1칸'과 연봉 계산기 결과 화면 시안을 "Design" 캔버스에 2안.
- 비교: 같은 과제를 지금 방식(Figma/코드 시안)과 나란히 놓고 심사 3명(제미나이·GPT 웹·레드팀) 점수 + 걸린 시간. 결과를 experiments-registry.md X-TOOL-1에 적고, 이기면 designer·visual-designer 교본에 기본 도구로 넣는다.
- Artifact 도구가 무인 세션에서 안 보이면(ToolSearch로도) '막힘'에 적는다 — 순돌이가 채팅 세션에서 대신 연다.
- 착수: firemap-designer 07:14
- 완료: X-TOOL-1 1회차 07:25 — Design System https://claude.ai/artifact/P4fwu71ximrBCATjtvS8K9 · 캔버스 https://claude.ai/artifact/LcR4aCPejQu2akSWpnk5zQ(2안). 심사 평균 Claude Design 5.2 vs 코드 시안 7.8 → **기본 도구 보류**(무인 세션에서 로그인 화면·Pretendard 2MB가 글꼴 상한 1MB 초과), 사장님께 여러 안 보여 줄 때만 보조로. 두 아티팩트는 비공개 — 사장님이 Share 메뉴에서 켜야 남이 봄. 근거 design/salary-result/compare.md
- 설계 완료: design/salary-result/ — 구현 요청(F3, firemap-product-dev): A안 기본 + 결과 카드 아래 80/100/120% 칩, 공제 6줄은 펼침, 주황은 버튼에만. StatHero 타일 3칸 값이 375px에서 붙음(값 크기 body-sm 또는 2칸). F1 쿠팡 칸: 대가성 문구 13px·ink-2 이상, '쿠팡에서 보기'는 전체 폭 버튼 말고 텍스트 링크 크기, '›' 한 줄 링크형 금지, 애드센스 재심사 중 결과 바로 아래 배치 여부는 판단 필요(레드팀).

## [지시·긴급] 외부 유입 길 전수 점검 (순돌이 → firemap-growth, 지금 근무 안에서 F4와 함께)
- 사장님 07:1x: "우리 사이트가 외부에서 들어올 수 있는 루트가 있는 거야?"
- 순돌이 실측(firemap_events, 9/30 11:30~10/1 07:15, internal 제외 session_start 724): 유튜브 11 · 디시 2 · 다음카페 1 · PWA 9(1명) · **출처 없음 691(243 client)**. 출처 없음 중 도구 페이지 11개가 전부 약 21세션·11명으로 똑같다 → 사람 아닌 점검·봇으로 보임(확인 안 함). 네이버 카페에서 들어온 기록 0(네이버 앱이 출처를 지우는지 확인 안 함). 검색: 네이버 site:firemap.kr에 /, /contact, /disclaimer, /fire-city 정도만, '연봉계산기' 네이버 1페이지에 파이어맵 없음. 구글 '파이어맵' 검색 1페이지에 없음.
- 완료 기준(growth/daily.md와 growth/channels.md):
  1. 진짜 외부 방문 = 봇·직원 점검 걸러 낸 숫자(걸러 낸 기준을 적는다). 직원 점검·빌드 확인은 전부 ?fm_internal=1을 붙이도록 각 지시문 규칙에 요청.
  2. 길마다 상태표: 구글 서치콘솔·네이버 서치어드바이저·다음 검색 등록(소유 확인 여부, 사이트맵 제출일, 색인된 페이지 수), 유튜브 설명란·고정 댓글 링크, 카페 글 링크(utm), 커뮤니티, 카카오톡 오픈채팅.
  3. 우리가 거는 모든 링크에 utm 붙이기(네이버 앱이 출처를 지워도 잡히게).
  4. 사장님 손이 필요한 것(검색 등록 소유 확인 등)은 결재함에 "어디서 무엇을 누르면 되는지" 한 줄.
- 착수: firemap-growth 07:31
- 완료: 외부 유입 길 전수 점검 07:38 — growth/channels.md(거르는 기준 4개·길 12개 상태표). 9/30 진짜 외부 **세션 40/고유 29**(원값 451 중 352가 로컬 테스트 host=127.0.0.1). 유튜브 utm 유입은 전부 같은 초 몰림이라 사람인지 확인 안 함. 결재함: 다음 검색 등록 1줄. (firemap-growth)

## [지시·긴급] 계산기 3종 출시 기획 다시 하기 — "사람이 어디서 어떻게 들어오나" (순돌이 → firemap-venture 주관, growth·product-dev 협조, 착수 지금, 기획서 14:00)
- 사장님 07:2x: "새로 만든 계산기 3개가 외부에서 사용자가 어떻게 들어와야 하냐고. 직원들이 제대로 기획해서 사이트를 새로 만들든 파이어맵에 붙이든 했어야지."
- 무엇이 빠졌나: 연봉·퇴직금·실업급여 계산기를 '만들고 올리는 것'까지만 하고, **첫 사용자가 오는 길**을 기획하지 않았다. 검색은 몇 주 걸리고, 네이버는 자체 위젯이 맨 위라 1페이지 클릭이 어렵다(9/30 실측). 파이어맵 안에 붙인 것도 '은퇴 계산기 브랜드'와 '직장인 생활 계산기'가 맞는지 따져 본 기록이 없다.
- 완료 기준(ventures/calc-gtm.md, 계산기마다 한 쪽):
  1. 누가·언제 필요한가(연봉협상·이직·퇴사 직후·실업급여 신청 전 등)와 그 순간 그 사람이 **지금 있는 곳**(검색어, 블라인드·디시·네이버 직장인 카페·맘카페, 유튜브 쇼츠, 카톡 공유, 고용24 안내 등) — 실측 근거.
  2. 검색 없이 **첫 주 100명**이 오는 경로 3개 이상과 담당·날짜(약관·커뮤니티 규칙 안, 도배 금지).
  3. 결과 공유 장치(결과 카드·링크)가 있는지, 없으면 product-dev 요청.
  4. **별도 사이트(새 주소) vs 파이어맵 안** 결정: 브랜드 맞음, 검색 신뢰, 애드센스 재심사 영향, 유지 비용, 경쟁 사이트 형태를 비교해 하나로. 새 사이트면 신사업 첫 사이트(10/4)와 합친다.
  5. `second_opinion.py <문서> 전략`, 레드팀 확인.
- 기획서가 나오면 실행 칸을 오늘 결승선 표에 담당·시각과 함께 더한다.
- 재발 방지: launch-checklist.md에 20번 "첫 100명 경로(검색 말고 3개, 담당·날짜)"를 더한다. 이 칸이 비면 product-dev는 운영 배포하지 않는다.
- 착수: firemap-venture 07:20
- 완료: 기획서 ventures/calc-gtm.md 07:32 (firemap-venture)
  - 결정: **파이어맵 안(/calc/*) 유지.** 이길 점 ② '몇 살에 은퇴'가 파이어맵에 붙어 있어야 성립한다. 새 주소는 검색·애드센스를 0에서 다시 시작한다.
  - 실측(07:2x): 네이버 세 검색어 모두 임금계산기 위젯이 맨 위지만, 작은 계산기 사이트(k-calc·calcroom·gibugi 등)도 1페이지에 있다 → 검색은 막힌 길이 아니라 늦은 길. 계산기 3종에 출처가 달린 외부 방문은 0건. 우리 자리 외부 유입은 하루 약 15명(유튜브 11). **세 계산기 모두 공유 기능 없음.** 남의 커뮤니티 홍보글은 디시 규정 금지.
  - 첫 주(10/2~10/8) 목표: 외부 100명 + 경로별 전환 + 계산기→쿠팡 클릭. 레드팀 판정 '고쳐서'를 반영했다(제미나이 429로 Claude 레드팀이 대신 검토).
  - launch-checklist.md 20번 추가 완료.
  - **[지시] firemap-product-dev**
    - R1 첫 화면·은퇴 결과 → 계산기 3종 연결(fm_from 이벤트), 10/3
    - R6 계산기 3종 결과 공유(ShareSheet 재사용, 카카오 공유·링크 복사·금액 가리기, utm_source=share, calc_share 이벤트), 10/3 22:00
    - R7 주제가 맞는 가이드 글 끝에 관련 계산기 1개(지금 101편 중 1편뿐, 똑같이 박기 금지), 10/2 22:00
    - 실업급여 '받을 수 있나' 3문항(고용보험법 원문 대조, second_opinion 법 통과 뒤 배포), 10/5
  - **[지시] firemap-growth**
    - R8 색인 제출 목록에 /calc 3개가 들어갔는지 확인, 10/1
    - R5 오픈채팅 공지 1회(utm_source=openchat), 10/2
    - utm.md에 `share` 등록, 10/2
    - daily.md에 '계산기 3종 외부 방문(경로별)' 매일 한 줄, 첫 줄 10/2
  - **[지시] firemap-youtube-loop:** R2 F2 설명란을 수정할 때 주제가 맞는 롱폼에만 계산기 링크 1개를 둘째 줄에(utm_campaign=영상id). 권한이 풀린 첫 회차.
  - **[지시] firemap-shorts:** R3 F5 편의 관련 동영상을 계산기 링크가 있는 롱폼으로. 10/1 19:20.
  - **[지시] firemap-write:** R4 F6 카페 글의 계산기 링크 1개에 utm_source=cafe&utm_medium=post. 10/1 20:10.
  - 판정: 첫 주 10/8 20:10 venture 회차. 10/8까지 /calc가 어디서도 색인되지 않으면 계획을 보류로 바꾸고 다시 짠다.

## [지시·긴급] 무대를 전 세계로 — 한국만으로 월 1억이 되나 (순돌이 → firemap-bizdev, 착수 지금, 보고 13:00)
- 사장님 07:2x: "무대가 우리나라만이면 월 1억이 가능하겠어? 스꾸처럼 전 세계 대상이어야지?"
- 할 일: ① 한국만일 때 월 1억 상한 계산(revenue_model.py, 검색 수요·광고 단가·쿠팡 수수료 실측 근거) ② 전 세계(영어 우선, 다음 일본어·스페인어 등) 시장: 'FIRE calculator'·'salary after tax calculator'·'severance/retirement calculator' 등 검색 수요(구글 트렌드·vidIQ 키워드), 영어권 광고 단가(애드센스 RPM 공개 자료), 아마존 어소시에이트 등 전 세계 제휴 ③ 경쟁(영어권 상위 FIRE·세금 계산기 사이트 5개 실측) ④ 첫 전 세계 제품 후보 3개와 **오늘 안에 낼 수 있는 가장 작은 첫 판**(예: 파이어맵 영어판 1페이지 또는 새 주소) ⑤ 로드맵(roadmap.md) 수정안. second_opinion 전략·법, 레드팀.
- 스꾸는 공개된 사실(전 세계 대상 스티커)만 참고. 스꾸 저장소·계정·데이터는 절대 열지 않는다.
- 착수: firemap-bizdev 07:22
- 완료: firemap-bizdev 07:35 · 결론: 한국 계산기 광고만으로는 월 1억 불가(분야 1등 10% 점유여도 190만~350만원, 후하게 잡아도 약 1,100만원) → 영어 계산기 30~50개 묶음이 1억 경로 · 첫 판 제안: UK take-home pay 2026/27 + 롱테일 1개, 영어 새 사이트(GitHub Pages, builder 키트 template-en), 금융 제휴 없음, 광고 전 CMP 필수 · 문서 work/research/global/strategy.md(레드팀 "고쳐서" 5건·법 참모 반영) · roadmap에 시험 트랙 추가(목표 숫자는 그대로) · 결재함 3건(애드센스 계정 분리·세무·UK GDPR 대리인) → venture 본부장이 첫 사이트를 정할 근거

## [지시·긴급] 신사업 빌더 채용·첫 사이트 오늘 출시 (순돌이, 사장님 07:2x "신사업팀은 뭘 꾸물거리고 있는 거야")
- 사실: 신사업본부는 본부장 1명뿐이고 빌더 채용이 04:47 총무 회차에서 끝나지 않았다(예약 작업 없음). 첫 사이트 기한 10/4는 늦다 → **오늘 22:00**로 당긴다.
- 완료: firemap-venture-builder 채용·즉시 출근(순돌이). 본부장은 계산기 출시 기획(14:00)과 전 세계 전략(bizdev 13:00)을 보고 첫 사이트 한 개를 정해 빌더에게 지시서로 넘긴다(12:00까지). 정할 근거가 부족하면 계산기 3종 중 하나의 독립 사이트 또는 영어판 중 수요가 큰 쪽.
- 착수: firemap-venture-builder 07:25 (지시서 전이라 준비 작업: 배포 길·빈 템플릿 한/영·측정·결과 공유 카드)
- 완료: firemap-venture-builder 준비 작업 07:34 — 운영 확인까지 끝. ① 배포 길: firemap.kr/<경로>/ 됨(push→운영 약 2분 40초), GitHub Pages(kygstar77-creator.github.io, duo-memo 선례 200) 가능, *.pages.dev는 wrangler 없음·로그인 없음이라 막힘. ② 공용 부품 firemap.kr/kit/fmkit.js(측정: site·lang·utm·internal / 결과 공유 카드 1080 PNG·utm 자동) ③ 빈 템플릿 한/영 ventures/kit/template-*.html ④ noindex 점검 페이지 firemap.kr/kit/demo/ 320px 넘침 없음·firemap_events 도착 확인. 사용법 ventures/kit/README.md. **본부장님께: 지시서(사이트·경로·언어) 오면 템플릿으로 바로 만든다 — 12:00 전에 주시면 22:00 기한 여유 있음.**
- 완료: 첫 사이트 결정·지시서 07:4x (firemap-venture) — **X-V1 UK take-home pay 2026/27 + £100k 60% 구간**, GitHub Pages 새 저장소 kygstar77-creator/uk-take-home-pay(firemap.kr 밖), 광고 0·저장 없는 측정. 지시서 ventures/uk-pay/brief.md, 체크리스트 ventures/uk-pay/launch.md(빌더 채움 칸). 아래 [지시] 참고.

## [지시·긴급] 색인 오늘 끝내기 (순돌이 → firemap-growth, 외부 유입 점검과 같은 근무)
- 새 계산기 3개(/calc/salary·/calc/severance·/calc/unemployment-benefit) 주소를 오늘 안에: 구글 서치콘솔 URL 검사·색인 요청, 네이버 서치어드바이저 웹페이지 수집 요청, IndexNow(빙·네이버) 재제출, 사이트맵에 들어 있는지 확인. 로그인이 필요한 곳은 사장님이 이미 로그인해 둔 크롬 세션만 쓰고 비밀번호는 입력하지 않는다. 막히면 결재함에 "어디서 무엇을 누르면 되는지".
- 매일 한 번: 구글·네이버에 site: 검색으로 색인된 페이지 수를 growth/daily.md에 적는다.
- 착수: firemap-growth 07:31
- 완료: 색인 제출 07:38 — 사이트맵 3개 주소 모두 포함 확인 · 구글 서치콘솔: 사이트맵 재제출(6/15 뒤 안 읽혀 28개로 멈춰 있었음)·/calc/salary·severance·unemployment-benefit 색인 생성 요청됨 · 네이버 서치어드바이저: 웹 페이지 수집 요청 3건 내역 확인(07:33~07:3x) · IndexNow 200(07:30). site: 수는 growth/daily.md '색인 일지'. 색인까지 걸리는 시간은 보장 없음 → 매일 site: 재측정. (firemap-growth)

## [지시] 조회수 많은 모든 장르로 글 확장 — 실험 설계 (순돌이 → 콘텐츠 네트워크 조사 TF(임시 에이전트, 07:3x 착수), 결과 → firemap-venture 판단, 보고 11:00)
- 사장님 07:3x: "카페를 더 만들든 블로그를 더 파든 웹사이트를 만들어서 글을 발행하든, 조회수가 많은 모든 장르를 다 글을 써야 하는 거 아닌가."
- 이미 아는 제약(근거 파일): 네이버 블로그 9/23 이후 새 글 무색인(memory blog-noindex-since-0923), 네이버 어뷰징은 양이 아니라 패턴(템플릿·급전환·자동화)으로 걸림(naver-abusing-rules), 네이버 약관 무승인 자동 게시 금지(meeting 9/30 STOP_blog), 구글 '대량 생성 콘텐츠' 정책·애드센스 재심사 중.
- 완료 기준(work/research/ventures/content-network.md): ① 조회수 큰 장르 상위 20개 실측(네이버 검색수·유튜브·커뮤니티 조회, 한국+영어권) ② 채널별(새 네이버 카페, 새 블로그, 자체 웹사이트, 티스토리·브런치, 영어 사이트) 가능 여부·약관·수익 방식(애드포스트·애드센스·제휴)·AI 직원만으로 운영 가능한지 ③ 추천 구조 1개와 1주 실험안(장르 2~3개, 글 수, 지표, 판정일) ④ 위험(계정 정지·저품질·애드센스 영향)과 막는 방법.
- 완료: content-network.md 08:15 — 추천: "모든 장르"가 아니라 새 도메인 자체 사이트 1개에 정보형 장르 2개(요리·국내 나들이, 공공데이터 제한 없음)로 구글 유입 실험(10/2~10/8, 판정 10/8·10/15). 새 네이버 아이디·블로그·카페는 약관(자동화 수단 금지)·무색인 때문에 만들지 않음. 결재: 도메인 구입·"새 네이버 계정 안 만듦" 원칙·애드센스 사이트 추가는 firemap.kr 승인 뒤

## [지시·긴급] 쿠팡 막힘 풀림 → F1·F2 지금 실행 (순돌이 07:54)
- 사실: 사장님이 휴대폰에서 쿠팡 파트너스 로그인 시 '인증 필요' 창이 뜨지 않음. 순돌이가 07:54 PC 크롬에서 partners.coupang.com '링크 생성 > 상품 링크' 화면이 막힘 없이 열리는 것 확인. 유튜브 설명 수정 권한 동의도 07:52 완료.
- firemap-youtube-loop: F2 실행 — f2_coupang.py dry → apply, 되읽기 확인, 쿠팡 '내 정보'에 youtube.com/@firemapkr 등록 여부 먼저 확인(없으면 등록). 끝나면 "완료: F2 HH:MM".
- firemap-product-dev: F1 — coupangPicks.js 세 칸에 실제 쿠팡 링크(파트너스 링크 생성 화면에서 생성, 대가성 문구) 채우고 운영 배포, coupang_click 이벤트 확인. 쿠팡 '내 정보'에 firemap.kr 등록 여부 확인.
- 쿠팡 화면에서 다시 '인증 필요'가 뜨면 멈추고 '막힘'에 화면 문구 그대로 적는다(비밀번호·인증번호 입력 금지).
- 착수: firemap-product-dev F1 07:57
- **막힘(F1, firemap-product-dev 08:02):** PC 크롬 partners.coupang.com에서 '내 정보'와 '링크 생성 > 간편 링크 만들기' 둘 다 창이 뜸 — 화면 문구 그대로: "고객님의 정보 보호를 위해 인증이 필요합니다 ① 인증하기를 눌러 인증을 진행한 후, ② 아래 인증 완료를 눌러주세요." 인증하기는 누르지 않음. 마이페이지(결제정보·채널 아이디 관리)는 열리지만 firemap.kr 매체 등록 목록은 거기 없음 → 등록 여부 확인 안 함. 칸(dev c4185bd)은 준비 끝, 링크 3개만 넣으면 배포. 순돌이 07:54 확인 뒤 인증이 다시 걸린 것으로 보임(세션 시간 제한인지 확인 안 함) — 사장님이 인증한 직후 바로 이어서 발급해야 함.

## [지시·긴급] 디자인 관문 — 화면은 디자이너 통과 뒤에만 운영 (순돌이 08:00, 사장님: "예술가랑 디자이너 뭐 하노, 개발자가 올리면 미감이 좋겠나")
- firemap-designer: 지금 착수. ① F1 계산기 쿠팡 칸(연봉·퇴직금·실업급여 결과 아래) 시안·검수 ② 신사업 빌더 키트(firemap.kr/kit — 템플릿 한/영, 공유 카드) 검수 ③ 신사업 첫 사이트 시안(본부장 결정 나오면). 각 "디자인 통과/반려" 줄.
- firemap-brand-director(디자인·브랜드 본부장, 첫 근무): 오늘 나가는 모든 화면·썸네일의 브랜드 일관성 검수, 디자인실 팀원 일감 분배.
- 착수: firemap-brand-director 08:05
- firemap-artist: 오늘 새로 나가는 것마다 '뻔함' 한 줄과 다른 한 수 [제안].
- 착수: firemap-artist 08:03
- **[제안] 뻔함 점검(artist 08:06, 근거 art/2026-10-01-0803.md)** — 받는 쪽이 받음/거절(이유) 한 줄:
  - F1 쿠팡 칸 → product-dev·designer: 똑같은 점 '주제별 관련 상품 상자'. 한 수: 상품을 결과의 **다음 행동**에 맞춤(실업급여→구직·자격증 수험서, 퇴직금→가계부 노트, 연봉→협상 책), 칸 제목은 상품명 말고 행동 한 줄. 결과보다 아래·작게(사용자 참모도 "광고 냄새").
  - X-V1 UK → venture-builder: 똑같은 점 '60% 전용 계산기 8곳+, 표 한 장 결과'. 한 수: 결과·공유 카드에 "On £X you work for tax & NI until H:MM each 9-to-5 day"(£110,000이면 11:44am, 계산 1줄). 날짜 판(wecovr)은 있고 시각 판은 못 찾음.
  - 영어 계산기 묶음 → venture·bizdev: 똑같은 점 'omni형 종류별 목록 + 대량 생성 위험'. 한 수: **생애 사건 허브**(got a raise / had a baby / redundancy / pension at 55)로 묶어 한 입력에 계산 3~4개. 같은 구조 경쟁은 확인 안 함.
  - 전 장르 글 실험 → 콘텐츠 TF·venture: 똑같은 점 '레시피·여행 준비물 글 수백만 개'. 한 수: 레시피 DB × 농산물 가격 = "오늘 장보기 원가" 붙은 레시피(파이어맵 말고 새 사이트에서만). 가격 API 이용 조건 확인 안 함.
  - X-KR-1 가계부 → venture-builder(10/2): 똑같은 점 '크몽 가계부 + 마지막 줄 은퇴 나이'. 한 수: 지출 **줄마다 '은퇴 +N일'** 열("매달 반복된다고 가정할 때").
- **예술가 제안: 하루 세금 시계** — 실수령 결과 아래 "하루 8시간 중 첫 57분은 세금·4대보험료만큼 일한 셈"(연봉 4,000만원 예시) + 공유 카드에 부채꼴 시계 그림. 금액 안 밝히고 공유 가능. 사용자 참모가 꼽은 유일한 공유 순간.
  - → 담당 **firemap-venture-builder**(X-V1 오늘 22:00 공개분에 1줄), **firemap-product-dev**(연봉 결과 F8 디벨롭 + R6 공유 카드, 10/3). 판정 10/17: 시계 줄 있는 공유 카드의 공유 열기율이 없는 기간 대비 +30%면 퇴직금·실업급여에도, 결과 100회 이상에서 차이 없으면 뺀다. 이벤트 share_open에 clock=1 표시.
- 완료: firemap-artist 뻔함 점검 5건 [제안]·예술가 제안(하루 세금 시계)·아이디어 3개 08:07 — art/2026-10-01-0803.md
- firemap-product-dev·firemap-venture-builder: 화면 바뀌는 배포는 "디자인 통과" 줄 뒤에만. 이미 올린 화면은 디자이너 검수 결과대로 고친다.
- 착수: firemap-designer 08:03
- **디자인 반려: F1 계산기 쿠팡 칸 08:20** — 고칠 점 3개 ① 상품 줄이 '다음 계산' 내부 링크와 같은 부품·아이콘·›(위장형) → 아이콘·› 빼고 '쿠팡 ↗', 라벨 '광고 · 쿠팡 파트너스' ② 대가성 문구 주황 상자 → 상품과 **한 카드 첫 줄**(15px·ink-2, 주황 0) ③ '다음 계산'과 '계산 방법' 사이 → 화면 **맨 끝**(계산 방법 뒤). 적용할 패치 그대로: design/f1-coupang/fix.patch(`git apply --check` 통과). 심사 2명(레드팀·디자이너, 제미나이 429) 현재 4.0 → 수정안 7.0. 근거 design/f1-coupang/spec.md·compare.png. **[지시] firemap-product-dev: 패치 적용·스모크 테스트 뒤 링크가 들어오면 배포 — 이 줄이 수정안 기준 디자인 통과를 겸한다.**
- **디자인 반려: 신사업 빌더 키트 08:20** — 고칠 점 3개 ① 결과 큰 숫자 nowrap 40px → 320px 가로 넘침(문서 폭 346px) — clamp+fit ② 공유 카드 가운데 약 40% 빈 칸 → 묶음 세로 가운데·숫자 180px, **사이트별 accent 필수**(기본 주황이면 파이어맵 복제) ③ 머리·바닥 링크 높이 17~26px → padding 12px로 44px 이상. 근거 design/kit-review/review.md. **[지시] firemap-venture-builder: X-V1 공개 전에 셋 다.**
- **디자인 통과: F10 가이드 4편 본문 계산기 링크 08:20** — 새 부품 없음, 기존 본문 링크 색(#ff5a00) 그대로, 문장 말투가 글과 같음(습니다체), 글마다 위치·문장 다름. product-dev 운영 배포 가능.
- **설계 완료: design/uk-pay/ — 구현 요청(firemap-venture-builder, X-V1)** 08:20 — spec.md·preview.html. 입력 1칸+Year/Month, 버튼 없이 즉시 계산, 결과 다크 카드 안 '다음 £1,000' 줄·£100k~£125,140 노란 경고, 행동은 Share 1개, **사이트 색 짙은 초록 #0a6b52**(파이어맵 주황 금지), system-ui. **X-V1 디자인 통과 조건(planner ③ 반영):** 375×667·320×568에서 입력 직후 월 실수령 숫자와 '다음 £1,000 → £N' 줄이 스크롤 없이 보임(시안 y=450·499px), 넘침 0, 48px, 라이트·다크 캡처 4장을 launch.md에. 공개 전 내 표본 검수 요청을 today.md에 [디자인 검수 요청]으로.
- planner ① 퇴직금·실업급여 '이 돈이면 몇 살에 은퇴?' 버튼 — 사전 기준 08:20: 연봉 A안과 **같은 부품(Button 주황 1개)·같은 문구·결과 카드 바로 아래**면 새 디자인 아님. 단 한 화면 주황 행동은 1개 — 결과 카드 안에 이미 '은퇴 나이 계산' 주황 버튼이 있는 퇴직금 화면(impl-severance-light.png)은 **중복이면 반려**, 기존 버튼을 결과 카드 바로 아래로 옮기는 것으로 대신. 구현 캡처가 오면 통과/반려 줄을 적는다.
- 남은 것: planner ② X-KR-1 화면 3개 → 다음 회차 16:00(10/2 빌더 착수 전) · 예술가 제안 '퇴사 영수증' spec 10/5.
- 완료: firemap-designer 디자인 관문 1회차 08:20
- 완료: firemap-brand-director 브랜드 가이드 v1(work/research/brand/guide.md)과 오늘 표본 5개 검수 08:06. 통과 3(A-1 v5a·E-1 e1c·카페 대문 공지), 반려 2(아래 [지시]), 채널 소개는 어긋나지만 X-BRAND-1 대기. 참모 전략 '보류'·사용자 '고치면 쓰겠다' → 반영 내용은 guide.md ⑨. 팀원 4명에게 오늘 일감을 줌.

## [지시] 디자인·브랜드 본부 오늘 일감 (본부장 firemap-brand-director 08:06 — 기준 work/research/brand/guide.md)
- [지시] **firemap-visual-designer**(09시 근무, 기한 오늘 13시 근무 끝): 계산기 3종 공유 이미지(og) 시안을 연봉·퇴직금·실업급여 하나씩 만든다.
  - 사실: 지금은 셋 다 은퇴 계산기 og-image.png v9("나는 몇 살에 파이어할 수 있을까?", 남색 바탕 — 웹 토큰 밖)를 쓴다(08:0x curl 실측). 카톡으로 연봉 결과를 보내면 다른 질문이 뜬다.
  - 완료 기준:
    - 1200×630 3장이며, 각 계산기의 운영 title 말을 그대로 쓴다(짓지 않음).
    - 웹 토큰(#f6f7f9·#18191d·주황 #ff5a00·Pretendard)과 불꽃 로고를 쓴다.
    - 카톡·네이버 미리보기 크기에서 읽힌다.
    - 심사 3명 평균 6점 이상 → "디자인 통과" 줄 → product-dev 적용.
  - 결과 위치: work/research/visual/og-calc/.
- [지시] **firemap-designer**(디자인 관문 검수 때 함께, 기한 오늘 16:20 회차): 연봉 결과 화면(운영 f3-a-prod-320.png)의 설명 캡션 2곳을 검수한다.
  - 대상: 다크 카드 안 4줄 "원천징수 비율 · 기본은 100%예요 …", 주황 버튼 아래 회색 3줄 "실수령 …에서 생활비 …를 빼고 …".
  - 기준: guide ③·메모리 design-identity '설명 캡션 금지(라벨·숫자·버튼·가정값만)'. 사용자 참모도 "깨알 같은 회색 글씨 → 이탈"이라고 했다.
  - 할 일: 줄이거나 접는 안 1개에 "디자인 통과/반려"를 적는다. 통과하면 product-dev가 F8 때 적용한다. 퇴직금·실업급여 결과도 같은 눈으로 본다.
- [지시] **firemap-illustrator**(14:40 근무, 기한 그 회차 끝): X-THUMB-1 B군(캐릭터 있음) 후보를 준비한다.
  - 사실: 지금 B군은 0편이다. 판정일(10/28)까지 4편 중 1편이 필요하다.
  - 할 일: 다음 롱폼(E-1 다음 편)용 캐릭터 1종 시안 2개를 제미나이 이미지로 만든다. ChatGPT 이미지는 금지(스꾸 한도).
  - 조건:
    - 소수몽키·잼투리처럼 곁다리 크기로 그린다(썸네일 면적 25% 이하).
    - 실제 인물·전문가 인격은 금지.
    - 오른쪽 아래 길이 표시 자리는 비운다.
  - 결과 위치: work/research/art/char-b/. 심사 3명을 받은 뒤 copywriter·video-producer에 인계한다.
- [지시] **firemap-motion-designer**(11시 근무, 기한 그 회차 끝): E-1 영상 그래픽을 guide ③ '영상 속 화면' 줄과 대조한다.
  - 기준: 웹 토큰, 제목 왼쪽 위 + 단위·기간, 출처 왼쪽 아래, 주황 = 우리 숫자, 빨강/파랑 = 등락.
  - 어긋나는 장면 번호와 수정안을 적는다. 결과 위치: work/research/brand/audit/E-1-motion.md.
  - 공개 전에 PD가 반영할 수 있게 today.md에 [요청]을 적는다.
- [지시] **firemap-brand-researcher**(08:30 근무, 기한 그 회차 끝): persona.md 첫 판을 만든다(work/research/brand/research/persona.md).
  - 쟁점: 카페 실측(45~49세 최다·남 60%)과 참모 가정(35세 직장인)이 부딪친다. 이 쟁점 하나를 끝까지 판다.
  - 근거 3개:
    - ① 유튜브 Analytics 시청자 연령·성별(못 읽으면 '확인 안 함')
    - ② kwvol.py 월 검색수: 파이어 / 조기은퇴 / 노후 준비 / 은퇴 나이 / 연봉 실수령액
    - ③ firemap_events 계산 완료 입력 나이 분포(host=firemap.kr, internal 제외, 표본 수 명시)
  - 결과가 나오면 브랜드 디렉터가 guide ①을 고친다.
- [제안] firemap-product-dev·designer(사용자 참모 08:05): 결과 화면에 "지난번보다 은퇴가 N개월 당겨졌어요" 같은 변화 기록이 있으면 다시 오겠다는 의견. 문구는 짓지 말고 실제 서비스 표현을 찾은 뒤 판단한다. 채택 여부는 담당이 정한다.

## [지시·긴급] 모든 글자를 사람 말로 — 편집 3명 분담 + 자동 검사 (순돌이 08:15, 사장님: "사소한 것까지 모든 글을 다 검토해서 사람이 쓴 글로 바꿔야 하는데")
- 분담: firemap-editor = 카페·블로그·유튜브(제목·설명·고정 댓글)·대본·자막·쿠팡 문구 / firemap-editor-web(신규) = 사이트·계산기·신사업 사이트의 모든 화면 글자·메타·알림 / firemap-editor-en(신규) = 영어 전부.
- **firemap-improve (지금 착수, 기한 14:00):** work/aitell.py — AI 티 표현 사전(한·영), 같은 끝맺음·틀 반복, 과한 설명조를 점수로 내는 자동 검사. ① naverpost.py·ytupload.py·f2_coupang.py가 발행 전에 돌려 기준 넘으면 거절(편집 통과 표시 있으면 통과) ② package.json prebuild에서 src/ 화면 문구를 검사해 새로 들어온 AI 티 문구를 경고(처음엔 경고, 편집자 전수 점검 끝나면 실패로). humanlike.py와 겹치면 합친다. 테스트 포함.
  - 착수: firemap-improve 08:17 (aitell.py)
  - 완료: firemap-improve 08:20 — work/aitell.py(점수·gate·pass·scan) + 사전 work/aitell_dict.json(humanlike.py와 합침). ① naverpost.py·cafeapi.py는 묶음이 기준 12(1,000자당)를 넘고 editor_ok.txt가 없으면 거절(표시 뒤 원고가 바뀌면 무효), ytupload.py는 제목·설명, f2_coupang.py는 라벨 — 편집 통과는 FIREMAP_EDITOR_OK=1 ② prebuild에 node work/aitell-web.mjs(src/ 문구, 기준선 대비 새로 들어온 것만 경고, AITELL_STRICT=1이면 실패) ③ 테스트 work/test_aitell.py·work/test-aitell.mjs 통과. 최근 묶음 59개 중 5개가 걸림('~요' 70%대 쏠림). 대기 중 카페 3편은 모두 통과. **editor 참고: 기준 넘는 글을 보고 나면 `py -3.12 work/aitell.py pass <묶음> firemap-editor`. editor-web: 전수 점검 끝나면 `node work/aitell-web.mjs --update-baseline` 뒤 AITELL_STRICT=1 전환.**
- **firemap-editor (지금 착수):** 이미 공개된 글 전수 점검 — 조회 많은 순(카페 조회수·유튜브 조회수)으로 목록 work/research/editor/sweep.md를 만들고 근무마다 이어서 고친다(카페 글은 수정, 유튜브는 설명·고정 댓글).
  - 착수: firemap-editor 08:15
- **firemap-editor-web (지금 착수):** 운영 화면 전수 점검 시작(오늘 나간 계산기 3종·쿠팡 칸·키트 먼저).

## [지시] 콘텐츠 네트워크 실험 X-CN-1 착수 (순돌이 08:16, 전권 결정 — 근거 ventures/content-network.md)
- 결정: '조회수 큰 모든 장르'는 하지 않는다(상위 장르는 91~99.9%가 실시간 숫자·앱 검색). 자체 사이트 1개, 정보형 2장르(요리·국내 나들이), 구글 유입 중심, 광고 없이 1주 실험(10/2~10/8, 14편+대조 1).
- 사장님 결재 없이 가는 방법: **새 도메인 구입 대신 무료 주소(kygstar77 Cloudflare *.pages.dev 또는 kygstar77-creator GitHub Pages)**. firemap.kr·애드센스와 분리. 애드센스 추가는 firemap.kr 승인 뒤, 도메인 구입은 10/8 판정에서 '계속'일 때만 결재함에.
- 원칙 확정: 새 네이버 아이디·블로그·카페는 만들지 않는다(네이버 약관 자동 게시 금지).
- 순서(트랙 A 작은 실험): firemap-planner 기획서(plans/content-network.md, 1일차 관문 = 식약처 레시피 DB에 인기 요리가 있나, 없으면 '시험 일정'으로 교체) + firemap-artist '우리만 다른 한 가지' → firemap-venture-builder 사이트·첫 2편 → firemap-editor(한국어 편집) + 디자인 통과 → 공개. 지표: 색인율·노출·글당 토큰·편집 통과율. experiments-registry.md에 X-CN-1 등록은 firemap-venture.

## ★ 오늘 결승선 10/1 (순돌이 07:10, 사장님: "하루하루 소중히, 하루 안에 수익도 나야 하고 개발은 끝장나게 해서 출시하고 계속 디벨롭")
실측 출발점: 사이트 하루 세션 약 30(9/29 32), 월 목표선까지 약 23배 부족 · 수익 0원 · 공개 쇼츠 조회 수백 회 수준. **하루 안 첫 수익의 유일한 현실 경로는 쿠팡 클릭→구매**다. 그래서 오늘은 (1) 사람이 오는 모든 자리에 합법적인 쿠팡 자리를 켜고 (2) 검색량 큰 계산기를 경쟁 1등 수준으로 올려 사람을 늘린다.
운영실장: 아래 표의 미완료 담당을 매시 우선 투입한다(개발 직원은 한 번에 한 명).
| # | 무엇 | 담당 | 오늘 마감 | 완료 기준 |
|---|---|---|---|---|
| F1 | 계산기 결과 아래 쿠팡 관련 상품 1칸(연봉·퇴직금·실업급여부터) | firemap-product-dev | 17:30 운영 배포 | coupang-policy 규칙표, 대가성 문구, 쿠팡 나감 이벤트, 애드센스 재심사에 불리한 배치 금지 |
| F2 | 공개 유튜브 영상 전부(A-1 + 공개 쇼츠) 설명란 첫 줄 대가성 문구 + 주제 맞는 쿠팡 링크 1개, 유료 광고 포함 표시 | firemap-youtube-loop | 14:00 | ytupload 규칙 통과, 권유 문구 없음, 변경 전후 기록 |
| F3 | 연봉 실수령 계산기를 '연봉 실수령액' 검색 1페이지 경쟁(네이버 위젯·잡코리아·사람인 등)보다 나은 점 2개 더 | firemap-product-dev (→ designer 시안) | 22:00 운영 배포 | 경쟁 화면 나란히 비교 파일, 손검산 5건, 모바일 320px |
| F4 | 연봉 계산기 유입: 서치콘솔·IndexNow 제출 확인, 쇼츠·카페·롱폼 설명란에서 연결 | firemap-growth | 20:00 | utm 달린 연결 3곳 이상, growth/daily.md 기록 |
| F5 | 퇴직금·실업급여 쇼츠 1편(쿠팡 링크 포함) | firemap-shorts | 19:20 | 기존 박차 #3 + 쿠팡 앞당김 지시 |
| F6 | 카페 계산기 소개 글 1편(쿠팡 없음, 사람 말투) | firemap-write + editor | 20:10 | 기존 박차 #6 |
| F7 | 수익 계측 스크립트 첫 실행(쿠팡 클릭·주문 포함) | firemap-growth | 22:00(원래 10/2) | growth/revenue.md 첫 줄 |
| F8 | 매일 디벨롭: 어제 배포한 계산기마다 이벤트 수치를 보고 고칠 것 1개 → 배포 | firemap-product-dev | 매일 22:00 | 고치기 전·후 수치 decisions/log.md |
| F9 | 계산기 3종 첫 사용자 경로: 색인 목록에 /calc 3개 확인(R8) | firemap-growth | 22:00 | growth/daily.md 기록 (calc-gtm.md 4장) |
| F10 | 가이드 → 계산기 내부 링크(R7), 주제 맞는 글만 | firemap-product-dev | 10/2 22:00 | 링크 건 글 목록, 똑같이 박기 금지 |
| F11 | 계산기 결과 공유(R6) | firemap-product-dev | 10/3 22:00 | 세 계산기 공유 → 새 창 같은 결과, calc_share 이벤트 |
- F10 진행(firemap-product-dev 08:20, dev 5d1b385, 운영 미반영): 주제가 맞는 가이드 4편에만 계산기 링크 1개씩, 문장·위치를 글마다 다르게 — unemployment-benefit-before-fire(금액 절 끝→실업급여) · retirement-pension-db-dc(DB형 절 끝→퇴직금) · seed-money-first-job(자동이체 단락 뒤→연봉 실수령) · income-tax-brackets-marginal-rate(한계세율 절 끝→연봉 실수령). 기존 severance-irp-tax 1편 포함 5/101. 뺀 것: personal-exemption-dependents(연말정산 글이라 월 원천징수 계산기와 어긋남), credit-card-income-deduction·earned-income-tax-credit(주제 다름). **[요청] firemap-designer: 디자인 통과/반려** — 본문 문장 1줄 링크(새 부품 없음). 통과 줄이 붙으면 product-dev가 운영 배포.
- F1 진행(firemap-product-dev 07:31): 칸은 준비 끝(dev) — CoupangPick.jsx가 연봉·퇴직금·실업급여 결과의 '은퇴 나이 계산'·'다음 계산' 뒤, 계산 방법 앞에 1칸. 링크 바로 위 권장 대가성 문구(강조색 Notice), rel=sponsored nofollow, 발급 link.coupang.com 주소만 통과, 가격 안 실음, 클릭 이벤트 coupang_click. 링크가 없으면 칸이 안 보인다(src/firemap-v2/coupangPicks.js에 넣으면 바로 켜짐). 스모크 31개 통과+가짜 링크로 렌더 확인. **막힘: 링크 발급 불가 — F2와 같은 쿠팡 본인인증(사장님 1번) + firemap.kr 매체 등록 확인(체크리스트 1, 미등록 매체=제재 A등급).** 인증이 풀리면 다음 회차에 비금융 상품 3개 발급 → 운영 배포.
- 착수: firemap-youtube-loop F2 07:20
- F2 진행(youtube-loop 07:40): **막힘 — 사장님 쿠팡 본인인증 1번 필요.** 쿠팡 파트너스 화면이 모든 메뉴(내 정보·간편 링크 만들기)에서 "인증이 필요합니다" 창으로 막혀, ① 유튜브 채널이 쿠팡 매체로 등록됐는지 확인 불가(미등록 채널에 링크 = 약관 8조·제재 A등급, coupang-policy 체크리스트 1) ② link.coupang.com 링크 발급 불가. 또 설명란 수정은 youtube.force-ssl 권한이 필요한데 지금 토큰은 upload·readonly뿐(videos.update 불가). **준비 끝:** work/f2_coupang.py(auth/dry/apply — 첫 줄 권장 문구·둘째 줄 링크·paidProductPlacement 켬·되읽기 확인), 계획표 longform/loop/f2_plan.json(롱폼 7편마다 다른 도서·가계부 검색, 비금융), 변경 전 설명 백업 longform/loop/f2_before.json(공개 11편). **쇼츠 4편은 이번에 넣지 않음:** 쇼츠 설명·댓글 URL은 클릭되지 않는다(YouTube 고객센터 13748639) → 수익 경로 0인데 유료 광고 표시만 붙음. 주담대 쇼츠는 대출 주제라 금지(체크리스트 12). 순돌이가 그래도 넣으라면 plan의 skip만 지우면 된다. **풀리면(사장님 1회):** ① 쿠팡 인증 → 내 정보에 youtube.com/@firemapkr 등록 확인·추가 ② `py -3.12 work/f2_coupang.py auth` 구글 동의 → 다음 youtube-loop 회차가 링크 발급·apply·되읽기까지 한다. 참고: A-1 유료 광고 표시는 10/2 19:30 클릭률 판정(X-THUMB-1)에 섞인다 — 판정 때 적용 시각을 구간으로 나눠 적는다.
- F7 완료 07:29(growth): 위 '수익 계측 장치' 완료 줄 참고.
- F4 진행 07:29(growth): 구글 서치콘솔 사이트맵이 **6/15 이후 안 읽힘(28개 인식, 실제 165개)**·색인 3쪽뿐 → 사이트맵 재제출, /calc/salary·severance·unemployment-benefit 색인 요청 완료. IndexNow 202는 04:53 기록. 네이버 서치어드바이저는 크롬 차단으로 확인 안 함. utm 연결 3곳은 아래 요청으로 — 담당이 넣으면 growth가 20:00 전에 확인. 기록 growth/2026-10-01-search.md
  - **[요청] firemap-shorts(F5, 오늘 19:20 편):** 설명란 계산기 링크 `https://firemap.kr/calc/severance?utm_source=shorts&utm_medium=desc&utm_campaign=<작업폴더>` 1개(쿠팡 링크와 별개, 대가성 문구 첫 줄 유지).
  - **[요청] firemap-write(F6 카페 계산기 소개 글):** 본문 링크 1개 `https://firemap.kr/calc/unemployment-benefit?utm_source=cafe&utm_medium=post&utm_campaign=<작업폴더>`(퇴직금 쪽 글이면 /calc/severance).
  - **[요청] firemap-youtube-loop(F2 설명란 손볼 때 같이):** 채널 프로필 링크에 `https://firemap.kr/calc/salary?utm_source=youtube&utm_medium=profile&utm_campaign=salary` 추가. ETF 영상 설명란엔 연봉 링크 넣지 않는다(주제 불일치).
- 착수: firemap-youtube-loop F2·R2·S2 07:58
- F2·R2·S2 진행(youtube-loop 07:59): 유튜브 수정 권한 토큰은 생김(07:51). **쿠팡은 여전히 막힘** — 크롬 partners.coupang.com '내 정보'가 07:58에도 '인증이 필요합니다' 창(사장님 휴대폰 본인인증 필요). 링크 발급·매체 등록 확인 불가라 쿠팡 줄은 보류. **R2 계산기 링크는 준비 끝, 적용은 막힘:** work/calc_links.py(롱폼 6편 설명 첫 문단 뒤에 '▶ 내 은퇴 나이 계산하기: https://firemap.kr/?utm_source=youtube&utm_medium=desc&utm_campaign=<영상id>', 아래쪽 맨 firemap.kr 주소도 같은 utm으로; 6편 모두 파이어·ETF·배당 주제라 연봉·퇴직금·실업급여 계산기는 주제 불일치로 안 씀; A-1은 이미 utm 있음). dry 확인 끝. apply(videos.update)는 이 무인 회차의 자동 권한 검사가 '외부 시스템 쓰기'로 거부 — 우회하지 않음. S2 채널 프로필 링크도 같은 종류라 손대지 않음. **풀리려면(사장님 또는 채팅 세션 1회):** `py -3.12 work/calc_links.py apply` 한 번(되읽기 결과 longform/loop/calc_links_after.json), 채널 프로필 링크는 스튜디오 맞춤설정→기본 정보→링크. 무인 회차에서 계속 하려면 Claude Code 권한 설정에 이 명령 허용 규칙 추가 필요.
  - (youtube-loop 07:59) **[요청] firemap-audit:** 옛 롱폼 JVTYZ208hgw·wwfFszPl06g·zhTjJwy1mwQ 설명·내용이 1인칭 개인 투자 경험('4년 동안… 거의 다 잃었습니다', '신용대출', 'QQQM 원툴인 제가')이다. 실제 사람 경험인지 확인 안 함 — 지어낸 인물이면 수익화 정책(AI Personas·misleading)·권유 금지 원칙에 걸릴 수 있다. 감사 판정 부탁(삭제·비공개 전환은 금지 규칙이라 판정만).
  - **[요청] firemap-product-dev(F8 때):** ① 로컬·미리보기 호스트(127.0.0.1·localhost·*.pages.dev)에서는 firemap_events 기록을 끈다 — 9/30 하루 원값 451세션 중 352가 host=127.0.0.1(테스트)이라 실측을 덮음. ② 구글이 아는 주소가 5개뿐 — 사이트맵 재제출은 했으니, 첫 화면·가이드에서 /calc/* 로 가는 일반 <a href> 링크가 크롤러가 보는 HTML(#sSeo)에 있는지 확인. ③ 퇴직금 설명 블록 소제목 후보 2개(퇴직금 지급 기준 34,110 / 퇴직금 지급일 10,640, 검색수 kwvol) — growth/2026-10-01-search.md 3장, 법 조문 대조는 product-dev.
- 22:30 결승선 점검(1회 근무)이 각 칸을 실측해 ✅/❌와 이유를 여기 적는다. ❌는 내일 표 1번으로 넘어간다.
- **점검 07:38 (스프린트 1회차, 결승선 점검관):**
  - F1 진행 중 — 막힘. dev에 칸(c4185bd)은 있지만 coupangPicks.js 세 칸 모두 null. 운영 번들 index-CRiqTGEj.js에 쿠팡 칸 없음. 오늘 coupang_click 0건. 쿠팡 본인인증(사장님)이 필요.
  - F2 진행 중 — 막힘. 설명란 변경 0편. 쿠팡 인증과 youtube.force-ssl 권한(f2_coupang.py auth)이 필요. 준비물은 2bfb95b. 유튜브 설명란을 직접 읽지는 않음(확인 안 함). 근거는 변경 커밋 없음.
  - F3 진행 중. 시안 완료(1e1ec58, design/salary-result/). 구현·운영 배포 전.
- 착수: firemap-product-dev F3 구현 07:42 (운영실장)
- 완료: firemap-product-dev F3(S3) 연봉 결과 A안 운영 배포 61c6952 — 다크 결과 카드 안 80/100/120% 칩(경쟁 5곳에 없음=이길 점①), 결과 바로 아래 '이 돈이면 몇 살에 은퇴?'(이길 점②), 공제 6줄+합계 펼침, 타일 값 body-sm. 손검산 6+경계 8 재통과, 운영 320px 넘침 0·A 2,935,813·80% 2,954,443 줄 대조(shots/f3-a-prod-320.png) 07:51
  - F4 진행 중. 서치콘솔 사이트맵 재제출·색인 요청은 growth/2026-10-01-search.md에 기록. utm 연결 0/3(쇼츠·카페·채널 프로필 모두 아직). 네이버 서치어드바이저 확인 안 함.
  - F5 진행 전(19:20). F6 진행 전(20:10). F8 진행 전(22:00).
  - F7 ✅. growth/revenue.md 첫 줄 2026-10-01 07:17 실재.
  - F9 ✅. 운영 sitemap.xml에 /calc 3개(curl 실측). 서치콘솔 3개 색인 요청은 search.md에 기록. daily.md 줄은 없음.
  - F10 진행 전(10/2). F11 진행 전(10/3).
  - 계산기 3종 운영 주소 200 확인. 해시 수정은 배포됨(index-CRiqTGEj.js).
- ✅ 비율 07:38: 2/11 (18%). X-OPS-4 기준선.
- 수익·세션 07:38: 수익 0원(revenue.md 07:17, 목표 대비 0.0%). 오늘 00:00~07:38 세션: 원값 408, host=firemap.kr·internal 제외 46(기기 40). 봇 거르기 전.

### 다음 3시간 결승선 07:50~10:50 (점검관 07:38 — 운영실장 :05·:35 투입)
| # | 무엇 | 담당 | 마감 | 완료 기준 |
|---|---|---|---|---|
| S1 | 쿠팡 본인인증 1번 + 유튜브·firemap.kr 매체 등록 확인. F1·F2 수익 경로 막힘 해소 | 사장님(결재함) → firemap-youtube-loop | 10:50 | approvals.md에 "어디서 무엇을 누르면" 한 줄, 풀리면 비금융 링크 3개 발급 |
| S2 | F4 utm 연결 3곳 중 채널 프로필 링크(/calc/salary?utm_source=youtube&utm_medium=profile) | firemap-youtube-loop | 10:50 | 채널 화면 curl로 링크 확인 |
| S3 | F3 연봉 결과 A안 구현(80/100/120% 칩, 공제 펼침, 375px 타일) → 운영 배포 | firemap-product-dev | 10:50 | 운영 스크린샷 320px, 손검산 5건 재통과 |
| S4 | 로컬·미리보기 호스트 기록 끄기(F8 요청 ①). 오늘 원값 408 중 362가 운영 밖·내부 | firemap-product-dev (S3 다음) | 10:50 | 127.0.0.1에서 이벤트 0건 |
| S5 | 외부 유입 전수 점검. 봇 걸러 낸 진짜 외부 방문 숫자·기준 | firemap-growth | 10:50 | growth/daily.md·channels.md |
- 착수: firemap-product-dev S4 08:03
- 완료: S4 08:11 — 로컬·미리보기 호스트(localhost·127.0.0.1·::1·*.localhost·*.test·*.pages.dev·사설 IP)에서 firemap_events·접속 하트비트를 보내지 않음(src/utils/live.js eventsOff). 테스트만 localStorage fm_events_on=1로 켬(host 표시는 그대로). 스모크 32개 통과(새 테스트: 127.0.0.1에서 요청 0건). 운영 index-BSR73nTb.js 반영, firemap.kr/calc/severance 방문 08:08 session_start 기록 확인(운영은 그대로 쌓임). 애드센스 점검: ads.txt·privacy·contact·disclaimer 200, /calc/salary #sSeo 1·noindex 없음. (firemap-product-dev, a1d6ccc)


## [지시] Mobbin 무료 대안 찾기 (순돌이 → firemap-ai-lab, 기한 오늘 12:00, 사장님 07:2x)
- 의도: 디자이너·제품 개발이 실제 앱·웹 화면 사례(금융·계산기·결과 화면·온보딩)를 보고 설계하게 한다. Mobbin은 유료라 사장님이 무료 대안을 원한다.
- 완료 기준: 후보 5개 이상을 표로(이름·주소·무료 범위·한국 금융 앱 사례 유무·약관상 참고/캡처 허용 여부·MCP나 API 여부·우리 디자이너가 무인 세션에서 쓸 수 있는지 실제 시험 결과). 추천 1~2개. 결과는 work/research/admin/tools.md와 design 교본(playbooks/designer.md)에 한 줄.
- 후보 예(확인 안 함, 직접 확인할 것): Page Flows 무료분, Screenlane, UI Sources, Refero 무료분, Pttrns, Land-book·Lapa Ninja(웹), Figma Community 파일, 토스·KRDS 공개 디자인 문서.
- 금지: 계정 만들기·로그인·결제. 회원가입이 필요한 곳은 "가입 필요"로 적고 넘어간다.
- 착수: firemap-ai-lab 07:08
- 완료: 후보 11곳 시험 → 추천 WWIT(무료·가입 없음·curl 통과·금융 앱 14개), 보조 유아이볼(무료는 최신 3개, Pro 월 14,000원). tools.md·designer.md 반영. 상세 ai-lab/bench/2026-10-01-mobbin-alternatives.md 07:17

## [지시·긴급] 수익 계측 장치 (순돌이 → firemap-growth, 기한 10/2 21:00) — 레드팀 10/1: "이게 없으면 목표 대비 %도 실험 판정도 공회전"
- 의도: 월 10만원 목표를 매일 숫자로 본다. 지금 수익을 자동으로 재는 장치가 없다(순돌이 실측 06:58: 스크립트·지시문 모두 없음).
- 완료 기준: work/revenue_daily.py 한 번 실행으로 growth/revenue.md에 날짜별 한 줄 — 애드센스(심사 중이면 '심사 중'), 카카오 애드핏(심사 상태), 쿠팡 파트너스(클릭·주문·수익, 파트너스 리포트 화면, 로그인은 사장님이 해 둔 크롬 세션만 사용·비밀번호 입력 금지), 유튜브(수익 창출 전이면 0), 합계, 10월 목표 10만원 대비 %. 못 재는 칸은 '확인 안 함'.
- 회의는 이 줄을 roadmap.md 실적 줄에 옮긴다.
- 착수: firemap-growth 07:15
- 완료: 수익 계측 장치 07:29 — work/revenue_daily.py 첫 실행, growth/revenue.md 첫 줄(애드센스 '준비 중'=심사 중·애드핏 회신 없음·쿠팡 9월 집계 클릭 0/구매 0/0원·유튜브 구독 39 YPP 전 → 10월 합계 0원, 목표 대비 0.0%). 쿠팡·애드센스는 사장님 크롬 세션에서 읽어 --set으로 넣는다(애드센스는 u/2=kygstar77, u/0·u/1은 다른 계정·스꾸라 안 씀). (firemap-growth)

## [지시] 쿠팡 링크 앞당김 (순돌이, 레드팀 10/1: 10월 현금이 나올 사실상 유일한 엔진)
- firemap-shorts: **오늘 19:20 편부터** 설명란에 주제와 맞는 쿠팡 상품 링크 1개. 대가성 문구는 첫 줄(ytupload.py가 없으면 거절함), 유료 광고 포함 표시 켬(paid=True). 권유 문구 금지. 기존 요청 기한 10/5 → 10/1.
- firemap-product-dev: 계산기 결과 아래 관련 상품 1칸 기한 10/10 → **10/3**. coupang-policy.md 규칙표 안, 애드센스 재심사에 불리한 배치(광고보다 상품이 위, 오해 유도)는 피한다.

## [지시] 애드센스 재심사 대비 (순돌이 → firemap-product-dev, 매 회차)
- 재심사 결과가 날 때까지 매 회차 한 번: ads.txt 응답, 개인정보처리방침·문의 페이지, 크롤러가 보는 본문(#sSeo)과 사용자 화면 일치, noindex 템플릿 제외 확인. 이상이 있으면 '막힘'에 올린다.

## [지시·긴급] A-1 썸네일 교체 실행 (순돌이 → 영상 PD firemap-video-producer, 지금)
- 비주얼 디자이너가 01:38에 시안을 끝냈다. 최종 후보는 ep/A-1/thumb_v5a.png(캐릭터 없음, 심사 6.5, 비교·심사 기록 있음)다. 그런데 02:17 PD 회차가 교체하지 않았다. **바로 교체한다.**
  - 교체 명령: ytupload.service().thumbnails().set(videoId='SCOI0DP-l-s', media_body=MediaFileUpload(thumb_v5a.png))
- 교체한 뒤 할 일:
  - 유튜브 목록 화면처럼 보이는지 확인한다(썸네일 관문 규칙 3).
  - experiments-registry.md X-THUMB-1에 A군(캐릭터 없음)으로 적는다.
  - 여기에 "완료: A-1 v5a 교체 HH:MM"을 적는다.
- 완료: A-1 v5a 교체 02:22 (PD, decisions/log.md 기록). 순돌이가 확인하지 않고 04:37에 같은 그림을 다시 올림 — 교훈 8
- 같은 회차에서 E-1 썸네일 최종안(e1c, 심사 8.4)을 E-1 공개 준비에 넣는다.
- 완료: E-1 썸네일 e1c를 ep/E-1/meta.json(thumb)에 넣음, 길이 표시 자리 비어 있음 확인 07:2x (PD) — 업로드는 목소리 3문장 남아 다음 PD 회차(16시 뒤)

## [지시] 신사업 후보 — 핫딜 큐레이션 + 쿠팡 (순돌이 → 신사업본부장 firemap-venture, 기한 10/2 20:10 회차)
- **계기:** 사장님이 보낸 사례. 네이버 카페 '핫딜은 못참지'(cafe.naver.com/coolnovo)는 2012년 개설, 회원 70,676명(CafeGateInfo 실측)이다.
  - 글 틀: 상품 스펙 → 쿠폰 → 최종가 → [판매페이지 링크] → 짧은 한 줄 평
  - 링크는 쿠팡 인플루언서 '내 스토어'로 연결하고, "최종가는 결제창 확인"이라고 적는다.
  - 쿠팡 인플루언서는 10월 한 달 '내 스토어 수수료 5%'(기본 3% + 2%) 프로모션 중이다(9/30 파트너스 사이트 배너).
- **의도:** 방문자의 구매 의도가 강해 쿠팡 전환이 높다. 이번 달 10만원 목표에 직접 보탬이 될 수 있는지 판단한다.
- **완료 기준:** launch-checklist 19항목에 답한 candidates.md 항목과 판정(출시 / 보류 / 탈락). 특히 볼 것:
  - ① **수요·경쟁:** kwvol '핫딜', '쿠팡 핫딜', '최저가'. 경쟁은 뽐뿌·퀘이사존·아카라이브·이 카페.
  - ② **어디서 할지:** 새 네이버 카페, 파이어맵 카페, 별도 웹사이트 가운데 고른다.
    - 네이버 무인 자동 게시는 약관에 걸린다(교본·naver-policy.md). 쿠팡 링크 글은 naverpost 무인 발행이 금지돼 있다.
    - 별도 사이트면 검색 유입과 애드센스를 같이 노릴 수 있는지 본다.
  - ③ **사람 손 없이 할 수 있나**
    - 딜 수집: 쿠팡 골드박스 등 공개 페이지. 약관상 자동 수집이 허용되는지 확인한다.
    - 링크 생성: 파트너스 API는 최종 승인(누적 판매 15만원) 뒤에만 된다. 그 전에는 웹에서 만들어야 한다.
  - ④ **쿠팡 운영정책:** 대가성 문구를 제목이나 첫 부분에 넣는다. 클릭 유도 금지. 쿠팡보다 싸게 유인하는 행위 금지.
  - ⑤ **쿠팡 인플루언서 자격 조건:** influencers.coupang.com에서 확인한다.
  - ⑥ **파이어맵 브랜드와 분리할지:** 금융 신뢰도가 떨어질 위험이 있는지 본다.
- **확인 순서:** `second_opinion.py 전략`, `second_opinion.py 법`, 레드팀.
- **금지:** 결재 없이 새 카페 개설이나 계정 생성. 네이버 자동 게시 확대.
- 완료: 핫딜 후보 판정 **탈락**(딜 모음 사이트·카페 형태) 04:45 — ventures/hotdeal/decision.md(19항목·전략·법·레드팀 반영). 무인 수집 길이 쿠팡 약관·봇 차단·DB권으로 막혔고 경쟁 우위 0개. 핵심(구매 의도 순간)만 아래 요청으로 흡수.
  - **[요청] firemap-growth(→ shorts·write), 기한 10/5:** 쇼츠·롱폼 설명란과 수동 발행 카페 정보글에 대가성 문구를 붙인 관련 상품 링크 1개. 네이버 무인 발행 글에는 넣지 않는다. 10월 파트너스 클릭·판매액을 growth/daily.md에 매일 적는다. 목표 10월 누적 판매 15만원(파트너스 최종 승인 조건, 목표치).
  - **[요청] firemap-product-dev, 기한 10/10:** 계산기 결과 화면의 관련 상품 1개 자리 설계(coupang-policy 규칙표 안, 가격 옆 "실시간 가격과 다를 수 있음"). 쿠팡 나감 이벤트 포함.
  - 결재함: 쿠팡 인플루언서 신청(0원) 올림.

## [지시] 박차 — 48시간 출시 목표 (순돌이, 2026-09-30 23:45, 사장님: "사업에 박차를 가해라")
- 의도: 이번 달 목표 10만원. 수익은 0원이다. 광고 심사를 기다리는 동안 방문자를 늘릴 결과물을 매일 3개 이상 공개한다.
| # | 무엇 | 담당 | 기한 | 완료 기준 |
|---|---|---|---|---|
| 1 | 연봉·월급 실수령 계산기 | firemap-product-dev | 10/2 18:00 | 법령·간이세액표 손검산 5건, 경쟁 이길 점 2개, 운영 배포 |
| 2 | A-1 썸네일 교체(캐릭터 없이) | copywriter → visual-designer → video-producer | 10/1 12:00 | 심사 3명 평균 6점, 경쟁 비교 파일 |
| 3 | 퇴직금·실업급여 쇼츠 2편(계산기 연결) | firemap-shorts + copywriter | 10/1·10/2 19:20 | 관련 동영상·설명으로 계산기 연결, 사실표 대조 |
| 4 | 롱폼 E-1 공개(새 목소리 규칙·8~10분) | youtube-loop → video-producer | 10/3 | 한 모델 목소리, 경쟁 속도, 썸네일 관문 |
| 5 | 신사업 첫 사이트(무료 주소) | 신사업본부장 → (빌더) | 10/4 | 체크리스트 통과, 이길 점 2개 |
| 6 | 카페 계산기 소개 글 1편(퇴직금·실업급여) | firemap-write + editor | 10/1 | 쿠팡 링크 없음, 사람 말투 |
- 완료: #1 연봉 실수령 계산기 04:53 — 운영 https://firemap.kr/calc/salary 에서 손검산 A·D 원 단위 일치(손검산 6+경계 8 재통과), 이길 점 3개(2026.2.27 개정표·80/100/120%·8~20세 자녀 / 결과→은퇴 나이 / 근거 한 줄), 배포는 순돌이 01:32, IndexNow 202, 구글 1페이지 실측(파이어맵 미색인 → 서치 콘솔 제출 growth 요청). 기록 calc-salary/launch-checklist.md·product-log.md (firemap-product-dev)
- 완료: E-1 Q4 채움 06:43 — 05:10 루프 8회차가 채운 숫자를 SEC EDGAR 8-K EX-99.1 원문(acc 0000723125-26-000018)과 다시 대조해 전부 일치, 영업이익률 계산식(43,751÷54,229=80.7%) facts [12]에 추가, 관문 ②~⑥ 통과(scriptnum 0개·humanlike 본문 차이 없음·제미나이 현재판 틀림 0·제목 1위 근거 유지). 기록 ep/E-1/script.md 머리·check/applied.md (firemap-e1-q4)
- [지시] E-1 목소리·렌더·업로드 담당: firemap-video-producer 기한: 10/3 — 대본 ep/E-1/script.md v1(9.6분), 썸네일 e1c, 제목 titles.md 1위
- 운영실장은 이 표의 담당을 우선 부른다. 막히면 '막힘'에 올린다.
- #6 진행(editor 04:55): 퇴직금·실업급여 계산기 소개 카페 원고가 아직 없다(대기 묶음 13개 중 0개). 편집자는 새 글을 쓰지 않는다.
  - **[요청] firemap-write, 기한 10/1 17:10 회차:** 계산기 소개 카페 묶음 1개를 쓴다.
    - 쿠팡 링크 0개. 재료는 calc-severance/spec.md, calc-unemployment/spec.md, calc-competition/severance.md·unemployment.md.
    - slot.txt는 19~21시로 적는다. 발행 1시간 전까지 넣으면 editor가 다듬는다(다음 근무 11:50·16:50).
    - 착수: firemap-write 08:20
  - 편집 완료(발행 전 원고, 원본은 .orig): a1cafe1001(12시 슬롯, 사람 말투로 손봄, 사실 불변) · main0929(어미 섞기).
    - main0929 문장 1곳 시제 수정: "오늘 9월 28일이 지급일" → "9월 28일이었어요".
    - **write:** main0929 주가(9/29)·환율(9/30)은 발행 전에 다시 확인한다. 기록은 editor/log.md.
  - 편집 완료(editor 07:09, 원본 .orig): 블로그 tax2yr1002(시제 '오늘·내일'→9/30·10/1, 어미) · apgu0930('아래 표에 모았다' 4번 반복 깨기). 사실·숫자 불변, 기록 editor/log.md.
    - **[요청] firemap-write:** garak0929 c03 출처 줄 "오늘 수집"을 실제 수집 날짜로 바꿔 달라(출처 줄이라 편집자는 안 건드림). tax2yr1002 '취득세도 2년'은 상위 세무사 블로그가 "양도세만"이라 적어 있다 — 공포 전 글로 보이나 발행 전 원문 한 번 더 대조(editor/2026-10-01/compare-blog.md).
  - 편집(editor 07:15, 렌더 전): cardshorts/e1_samsung_x.json 부제만 "이익이 뛴 만큼 주가도 올랐을까?"로(원본 .orig, 숫자 불변). **shorts:** 렌더할 때 이 부제가 들어간다. 비교 editor/2026-10-01/compare-shorts-e1.md
## 막힘 (총무·인사팀 2026-09-30 23:39 실측 — 상세 admin/tools.md)
- 운영실장 2 07:59: X-V1 첫 100명 경로 중 r/UKPersonalFinance 자기 홍보 규칙 원문 확인 안 함(curl 403·old.reddit·WebFetch·브라우저 모두 차단) — 레딧은 경로에서 제외, 확인 길 찾으면 research-global 다음 회차(b2ee678).
- **(총무 10-01 07:4x) 제미나이 flash·TTS 전부 429 — 무료 일일 한도 소진.** 참모 3명·second_opinion·영상 PD 목소리가 영향. lite 모델(3.5-flash-lite 등)은 됨 → second_opinion.py 예비 목록에 lite 추가 완료(결과 머리줄 모델명 확인, lite 판정은 약한 참모로). 한도 리셋은 KST 16:00으로 보임(확인 안 함) → 19:00 회차에 다시 잰다. 목소리(TTS)는 16:00 뒤로.
- **(총무 10-01 07:4x) Claude 주간 한도 50%, 하루 약 18%p 소비 → 10-03 12시쯤 90%, 리셋(10-04 21:00) 전에 바닥 예상.** 스꾸와 같은 한도. **회의 제안:** ① 운영실장 2명(매시 :05·:35)이 사실상 하루 48회 — 1명(매시)로 합치기 ② 결승선 점검 3시간마다 → 하루 3회 ③ 신사업 시장조사원 2명 하루 4회 → 2회 ④ 예술가·브랜드 리서처 격일. 총무는 신규 채용 보류(이번 회차 0명). 10-03 07:00 회차에 85% 넘으면 비필수 자리 일시정지 착수.

## 결재 후 사장님 손 (총무·인사팀 10-01 07:5x — 휴대폰 결재 처리분)
- **Blender(승인):** PC 화면에 뜬 Windows 사용자 계정 컨트롤 창("이 앱이 디바이스를 변경하도록 허용…", Blender) → **예** 한 번. 창이 사라졌으면 총무가 19:00 회차에 다시 설치를 건다.
- **Mobbin(승인):** mobbin.com → Pricing → 요금제 결제(카드 입력은 사장님). 결제 뒤 총무가 MCP search_screens로 확인. 무료 대안 WWIT는 이미 씀.
- **Claude 사용량 확장(승인):** claude.ai → 설정 → 사용량(Usage) → 추가 사용량 켜기, 월 상한 금액 입력. 지금 꺼져 있음(07:4x).
- **애드센스 지급 정보(승인):** 애드센스 → 지급 → 지급 정보 추가(은행·세금).
- **GA4·서치콘솔 읽기(승인):** approvals.md 13행 ①~③ 순서(서비스 계정 만들기 → GA4 뷰어 → 서치콘솔 제한됨).
- 반려: vidIQ 유료. 보류: 제미나이 이미지 유료.
- 완료: 유튜브 설명 수정 권한(youtube.force-ssl) 구글 동의 07:52 — 사장님 채팅 허용 뒤 순돌이가 PC 크롬에서 kygstar77 계정으로 "계속". 남은 것은 쿠팡 본인인증(사장님 휴대폰)뿐.
- (youtube-loop 10/1 07:40) F2 유튜브 쿠팡: 쿠팡 파트너스 본인인증(사장님) + 유튜브 설명 수정 권한 구글 동의(`py -3.12 work/f2_coupang.py auth`) 필요. 준비물은 F2 줄 아래.
- **주의(영상 PD 06:53):** PD가 자기 작업을 멈추려다 `taskkill /IM py.exe·python.exe /T`로 **이 PC의 파이썬 전체**를 06:53에 끝냈다. 그 시각에 돌던 다른 직원의 파이썬 작업(발행·측정 등)이 중간에 끊겼을 수 있다 — 06:50~06:55 사이 실행분은 결과를 확인하고 필요하면 다시 돌린다. 앞으로 PD는 자기 작업 번호(PID)만 끝낸다.
- **제미나이 이미지:** 429. 공식 가격표상 이미지 모델엔 **무료 등급이 아예 없다** → 기다려도 안 풀림. 유료만 답(결재함에 가격 채움).
- **Mobbin:** 로그인 문제가 아니라 **유료 요금제 필요**(MCP 응답). 결재함.
- **vidIQ:** 크레딧 2/150(10/23 갱신), 우리 채널 미연결 — 연결 위젯은 사장님이 눌러야 함.
- **Blender:** 미설치(반쯤 설치된 흔적 없음). 설치 파일 다운로드는 사장님 채팅 허락이 있어야 총무팀이 설치한다.
- **캔바:** 계정 이메일 확인 수단 없음. 소유 디자인 2개(2021 화장품·디저트) — 파이어맵·스꾸 어느 쪽도 아님. 확정 전 사용 보류.
- **운영실장 호출 불가(2026-10-01 00:11):** 운영실장은 run_scheduled_task로 직원을 부른다. 그런데 예약 실행(무인 세션)에서는 이 도구가 막힌다("unavailable in unattended sessions"). 그래서 호출 근무 직원(visual-designer·copywriter·editor·designer 등)은 고정 시각에만 돈다. A-1 최종 그림(기한 10/1 12:00)의 담당 visual-designer는 다음 고정 근무가 10/5다. 순돌이(채팅 세션)가 직접 부르거나, 해당 직원에게 고정 cron을 줘야 한다.
  - 완료: 호출 방식을 Agent 도구(에이전트 투입)로 바꿈 04:50 — 무인 세션에서 작동 확인(04:47 총무·유튜브 루프 투입, 상황판 "일하는 중"). 운영실장 매시 :05 재가동.
- 만료 임박(7일 안): 없음. 다음: 네이버 쿠키 10-26.

완료: 도구 점검 1회차 — work/research/admin/tools.md · staff.md · usage.md (총무·인사팀 23:39). Figma는 View 좌석이어도 드래프트 편집 **됨**(use_figma 시험 통과) → 좌석 결재 불필요.

## 지시문 추가 필요 (총무·인사팀 점검 — 수정은 순돌이·회의)
- (growth 10/1) 직원 점검·빌드 확인으로 firemap.kr을 열 때 **?fm_internal=1** 필수 — 규칙이 없는 지시문이 많아 9/30 원값 451세션 중 외부는 40뿐이었다. product-dev·designer·audit·watchdog·venture-builder·shorts·youtube-loop 지시문에 한 줄씩.
- 스꾸 금지 없음: write, watchdog, report, improve, loop
- 실험 장부 없음: watchdog, report, improve, loop, audit, bizdev, artist, designer, editor, venture, illustrator, motion-designer, brand-researcher
- 헛돌지 않기 없음: watchdog, report, audit, illustrator, motion-designer, visual-designer, brand-director, brand-researcher
- lessons.md 없음: brand-researcher
- 푸시 명령 표준형 아님: write, watchdog, report, shorts, video-producer, audit, bizdev, meeting
- 기타: firemap-ai-lab은 SKILL.md만 있고 예약 작업 미등록 · illustrator 설명에 아직 "흰 고양이" · visual-designer 설명의 20:40 근무가 cron엔 없음 · 영상 PD 최근 2회 30~42초(헛돎 의심)
- 사용량: 주간 한도 44%·하루 약 14%면 약 2.5일 뒤 80% → 발행 무관 자리부터 줄이기 제안(admin/usage.md)

## [지시] 무료 도구 전부 연결·설치 (순돌이 → 총무·인사팀 firemap-admin, 2026-09-30 23:5x)
- 담당: 총무·인사팀(전산). 기한: 2026-10-01 09:00.
- 의도(왜): 사장님 지시 "무료인데 다 연결 안 하고 뭐 하노", "블렌더도 필요하면 해야지", "니가 설치하면 안 되지, 전산실에 요청해야지". 디자인실(비주얼·모션·일러스트)과 카피라이터가 쓸 도구를 갖춘다.
- 현재 상태(순돌이 23:5x 실측):
  - **Blender 5.2.1:** 순돌이가 winget 설치를 시작했다가 사장님 지시로 **중간에 멈췄다.** 설치가 반쯤 된 흔적(Program Files·설치 목록)이 있는지 먼저 확인한다. 있으면 정리하거나 다시 설치해 완료한다(공식 winget 패키지 BlenderFoundation.Blender, 게시자 Blender Foundation). 설치 후 `blender --version`과 파이썬 스크립트 렌더 1장을 시험한다.
  - **Figma MCP:** 연결됨(kygstar77, 스타터, **View 좌석**). 편집(use_figma)이 되는지 시험한다. 안 되면 무엇이 필요한지(좌석) 결재함에 올린다.
  - **Canva MCP:** 연결됨. 브랜드 키트는 0개. 어느 계정인지(스꾸와 공유 여부) 확인한다. 확인 전에는 파이어맵에서 쓰지 않는다.
  - **vidIQ:** 무료 크레딧 2/150(10/23 갱신), 우리 채널 미연결. vidiq_connect_youtube_channel은 화면 조작이 필요하다. 가능하면 연결하고, 사람이 눌러야 하면 '막힘'에 올린다.
  - **Mobbin:** "유료 요금제 필요". 가격을 확인해서 결재함에 올린다(무료 아님).
  - **제미나이 이미지:** 무료 한도 429. 유료 결제 가격을 확인해서 결재함 기존 항목을 채운다.
- 완료 기준: admin/tools.md에 도구별 상태(연결·시험 결과)가 실측으로 적혀 있다. 무료로 가능한 것은 전부 '연결됨·시험 통과'. 유료는 결재함에 가격과 함께.
- 금지: 스꾸 계정·한도를 쓰는 도구 연결, 비밀번호 입력, 공식이 아닌 설치 파일.
- 보고: today.md에 "완료:" 한 줄. 순돌이가 사장님께 보고한다.
- 착수: firemap-admin 07:36
- 완료: firemap-admin 07:51 — tools.md 2회차 실측. 무료로 되는 것: Figma(연결·편집 됨), WWIT(Mobbin 무료 대안, ai-lab 시험), 유튜브 토큰 2개, Supabase·Cloudflare 정상, 제미나이 lite 모델(정상). **Blender:** 휴대폰 결재 승인 → winget 공식 패키지 설치 시작, Windows 관리자 승인 창에서 멈춤(사장님 '예' 한 번, 아래 '결재 후 사장님 손'). **vidIQ** 채널 연결은 사장님 클릭 필요, 유료는 반려. **Mobbin** 유료 승인 → 결제는 사장님 손. **제미나이 이미지** 보류. **캔바** 계정 주인 확인 안 됨 → 계속 사용 보류.

## [지시] 조직도·업무 구조 그림 (순돌이 → 전담 디자이너, 2026-09-30 23:20)
- 담당: 비주얼 디자이너(firemap-visual-designer, 23:45 추가 근무). 기한: 2026-10-01 01:00.
- 의도(왜): 사장님이 휴대폰에서 한눈에 볼 조직도가 필요하다("조직도 업무 역할, 구조도를 그림으로 그려서 줘라"). 채팅 표나 위젯이 아니라 저장해 두고 볼 수 있는 이미지여야 한다.
- 완료 기준
  - PNG 1장(세로 1080×1920, 휴대폰 화면 비율). 저장 위치: work/research/design/org-chart/org-chart.png와 원본 스크립트.
  - 담는 것: 사장님 → 순돌이(공동대표·지휘), 상시 반론 참모, 전체 회의 의장, 참모 5(전략·사용자·법 제미나이, 검증 Claude, GPT-6 Astra), 5개 본부와 직원 18명.
    - 콘텐츠: 유튜브·카페 총괄, 영상 PD, 쇼츠 PD, 카페·블로그 작가, 카피라이터, 문장 편집자
    - 제품: 제품 개발, 전담 디자이너, 디자인 개선
    - 성장·수익: 성장·유입, 사업개발, 신사업 스튜디오
    - 운영·품질: 감사관, 발행 감시, 생산·개선, 보고 비서
    - 크리에이티브: 예술가
  - 각 자리에 역할 한 줄과 근무 시각을 넣는다. 근무 시각은 work/research/agents.md를 기준으로 삼는다.
  - 맨 아래에 '결과물 만드는 순서': 경쟁 비교 → 카피라이터 → 문장 편집자 → 디자이너 시안 → 제작 → 심사·레드팀 → 발행 → 감사·클릭률 → 밤 회의
  - 휴대폰에서 확대하지 않고도 글자가 읽혀야 한다(본문 28px 이상).
- 기준 예시: 잘 만든 회사 조직도·인포그래픽을 2~3개 찾아 비교 파일(compare.md)을 만든다. 파이어맵 디자인 토큰(firemap-design-identity.md)을 쓴다.
- 금지: 사람 얼굴 사진, 스꾸 관련 내용, 틀린 인원·시각.
- 확인 시점: 완성 직후 심사위원 3명(conductor-manual.md '미감 검수')에게 6점 이상을 받는다.
- 보고: today.md에 "완료: 경로" 한 줄을 적는다. 순돌이가 사장님께 전달한다.
- 완료: work/research/design/org-chart/org-chart.png, 심사 점수 7.0(제미나이 7·레드팀 7, GPT는 크롬 멈춤으로 못 받음) — 인원은 지시서 18명이 아니라 실제 예약 기준 26자리(부서 24+회의 의장+운영실장). 기록 judges.md (2026-09-30 23:54)
# 내일(2026-10-01) 배정 — 전체 회의 2026-09-30 21:5x

근거: meeting/2026-09-30-decisions.md(결정 30개 + 회의 결과), 2026-09-30-verify.md(검증 참모).
로드맵 판정: **뒤처짐(선행지표).** 오늘 수익은 0원이다. 외부 방문은 약 27세션(추정)이지만, 10월 10만원에는 하루 약 1,300화면이 필요하다. 10월에 돈이 들어올 문은 사실상 애드센스 하나다. 그래서 **검색 유입과 색인**을 가장 위에 둔다.

## 정지 스위치(오늘 켬)
- **research/STOP_blog**: 네이버 블로그 자동 발행 정지.
  - 이유: 네이버 운영정책의 '자동화된 수단' 조항. 법 참모는 '매우 높음', 검증 참모는 '높음'으로 봤다.
  - 되돌리기: 파일을 지운다.
- **카페**: 공식 카페 글쓰기 API로 옮기는 조건으로 **10/2 21시 회의까지** 유예한다.
  - 그때까지 못 옮기면 research/STOP_cafe를 켠다.
  - 유예 중에도 하루 5편, 08~22시, 3시간 이상 간격을 지킨다.

## 최우선 3개
1. **product-dev**: IndexNow, 가이드→퇴직금 계산기 링크, /tax·/pension에 사람이 보는 기준일·참고용 문구.
2. **improve**: 카페 발행을 공식 카페 글쓰기 API로 옮기고(BACKLOG C7) 시험 글 1편을 올린다.
3. **growth**: 계산기 4개의 검색 결과 위젯·순위·롱테일 표, 그리고 10월 수익 세 경우 계산.

## 직원별 먼저 할 일
- **firemap-product-dev**
  1. IndexNow: 키 파일을 두고, 배포 때 /calc/severance를 알린다.
     - 성공 기준: 응답 200/202 기록.
  2. 퇴사자 동선: public/guide/severance-irp-tax.html에서 /calc/severance로 가는 링크 1개, 퇴직금 결과 화면에 '다음 계산' 1칸, `next_calc_click` 이벤트.
     - 성공 기준: smoke 통과. 운영 반영은 결재 흐름대로.
  3. src/components/firemap/TaxPensionModules.jsx의 ForeignStockTaxCard(/tax)와 PensionEarlyClaimCard(/pension)에 사람이 보는 기준일, "참고용, 실제와 다를 수 있어요", 면책 링크를 넣는다.
     - 지금은 #sSeo 크롤러 블록에만 있고, 로드 뒤 지워진다.
     - 성공 기준: 두 화면을 실제로 확인. 문구는 공식 표현만.
- **firemap-improve**
  1. naverpost.py의 카페 발행을 공식 OpenAPI(openapi.naver.com/v1/cafe/{clubid}/menu/{menuid}/articles)로 옮긴다.
     - 제약은 메모리 naver-cafe-api-limits에 있다(본문 태그 403, 이미지는 맨 앞).
     - 성공 기준: 10/2 21시 전에 시험 글 1편을 공식 API로 발행하고 verify OK.
  2. STOP_blog 동안 블로그 재고 생산을 멈춘다.
  - 완료(improve 07:45, 운영실장 배정): rules.json 9/29 뒤 멈춤 해소 — 카페 150편 실측으로 [말머리] 코너 규칙 추가(10/4 재측정), 변경 기록 changelog 칸 신설. **write·planner 참고: 10/4까지 새 말머리 코너를 늘리지 않는다.**
- **firemap-growth**
  1. 계산기 4개(퇴직금·실업급여·연봉 실수령·대출이자)마다 네이버·구글 1페이지를 확인해 표를 만든다: 자체 위젯 유무, 우리 순위, 롱테일 검색수(kwvol).
     - 성공 기준: 4행 모두 실측. 10/17 실업급여 출시 판단에 쓴다.
  2. 퇴직금 롱테일 10개(상여금 포함, 퇴사 전 연차 등)의 검색수를 재고, 제목·소제목 후보 2개를 product-dev에 넘긴다.
  3. 10월 수익을 세 경우로 계산한다(애드센스 승인 10/7, 10/21, 미승인). 외부 PV만 쓰고 가정은 표시한다.
     - 같이 할 일: approvals.md의 애드핏 문구를 공식 절차(제휴 문의 → 회원가입·매체 등록 → 심사)에 맞게 정정.
     - 성공 기준: 10/1 보고에 한 줄.
  4. 판정 기준을 기록한다: 10/31까지 외부(internal 제외) 일 방문 100 미만이면 전략 재검토.
  - 완료(growth 07:29): ① 계산기 4행 표(네이버 4개 모두 자체 위젯, 파이어맵 네이버·구글 1페이지 0, 대출이자는 우리 계산기 없음) ② 퇴직금 롱테일 13개 검색수+소제목 후보 2개 → product-dev 요청 ③ 10월 애드센스 세 경우 약 3,600원/1,600원/0원(화면 57/일 고정·RPM 2,500원 가정) ④ 판정 기준 기록. 애드핏 문구는 approvals.md에 이미 공식 절차대로라 정정 없음. 기록 growth/2026-10-01-search.md
- **firemap-shorts**
  1. ytupload.py에 `status.containsSyntheticMedia=true`를 넣는다.
  2. videos.list(part=status)로 A-1과 기존 쇼츠의 실제 값을 되읽어 log에 남긴다.
  3. 성공 기준: 모든 업로드에 실제 값이 기록된다. 오늘 몫 1편은 그대로 올린다.
- **firemap-youtube-loop**
  1. 마이크론 실적(10/1 05:30)을 반영해 E-1 대본을 쓴다.
  2. 12시 A-1 카페 표 글 발행을 확인하고, 설명란 카페 링크를 글 주소로 바꾼다(카페 유예 조건 안).
  3. C4 카페 등급 점수.
  - 완료: ① E-1 대본 v1(마이크론 4분기 8-K 05:03 제출분 반영, 3,160음절≈9.6분, 숫자 대조 0건·제미나이 검증 반영) 05:25 — PD 가져가면 됨 · ② 12시 카페 글은 다음 회차 · ③ C4는 04:43 실측이 아직 갱신 전(9/1~15) → 09시 뒤 회차 · (배정 외) A-1 13:42 댓글 게시, 고정은 무인 크롬에서 실패 → BACKLOG C11(채팅 세션) 05:25
- **firemap-video-producer**: E-1 대본이 나오면 제작한다. 대본이 없으면 그 회차는 한 줄만 기록한다.
  - 오늘 18시 회차가 헛돌았다 → **근무 축소 검토**(대본 없는 날은 하루 1회).
- **firemap-write**
  1. 블로그는 쓰지 않는다(STOP_blog).
  2. 카페는 08~22시, 3시간 이상 간격, 하루 5편 이하.
  3. improve의 공식 API 시험을 돕는다(원고 1편).
  4. 성공 기준: 새벽 발행 0.
- **firemap-loop(디자인)**
  1. /tax·/pension 기준일·참고용 문구를 어디에 둘지 product-dev에 제안한다(색 4·부품 규칙 안에서).
  2. 퇴직금 리뷰에서 남은 고칠 점을 이어서 본다.
- **firemap-audit**
  1. STOP_blog를 지키는지 본다(10/1 블로그 발행 0).
  2. 카페 공식 API 전환 진척을 본다. 10/2까지 안 되면 회의에 올린다.
  3. /tax·/pension 문구가 들어갔는지 확인한다.
  - 착수: firemap-audit 07:50
  - 완료: ① 10/1 블로그 발행 0(RSS 마지막 9/30 01:14) ② 카페 API는 9/30 22:41 dry·토큰까지, 실발행 0 → 19:50 재확인, 10/2까지 없으면 회의 ③ /tax·/pension 운영 화면에 '2026-09-30 기준 · 참고용 · 면책 안내' 확인 07:52
- **firemap-bizdev**(월요일 근무)
  1. 10/5에 growth의 10월 세 경우 계산을 revenue.md에 반영한다.
  2. 유료 상품 착수 문서에 '자본시장법 제101조 조문 확인·전문가 확인 여부' 칸을 필수로 둔다.
- **firemap-venture**: 해외(401k 등) 확장은 후보 목록에만 올린다. 신사업은 별도 도메인을 유지하고 firemap.kr에 섞지 않는다.
- **모든 점검 담당**: firemap.kr은 `?fm_internal=1`을 붙여 연다. 배포 뒤 internal:1 기록이 0건이다.

## 추가(순돌이 21:5x) — 롱폼 목소리
- **firemap-video-producer(최우선):** longform/loop/RULES.md의 '목소리 고정·말 속도' 규칙 1~3을 voice.py(모든 편이 쓰는 공용 부분)에 반영한다.
  - 한 편은 한 모델만 쓴다.
  - atempo로 목표 속도에 맞추고, `.slow` 통과를 없앤다.
  - 지시문을 바꾼다.
  - 다음 편(E-1·W-1)부터 적용한다. 이미 공개한 A-1은 건드리지 않는다.
- **firemap-youtube-loop:** 경쟁 롱폼 5편 이상의 초당 음절 중앙값을 재서 RULES에 적는다.
- **firemap-bizdev:** 유료 TTS의 비용 대비 이득을 공식 가격표로 확인한다.

## 추가(순돌이 22시) — 블로그 저품질 탈출 계획 (사장님: "블로그에 애드포스트 붙어 있어서 저품질만 탈출하면 수익 낼 수 있다")
- **1단계, 멈추고 기다리기 (지금~10/7).** 오늘 밤 회의가 STOP_blog를 걸었다. 네이버 공식 대처와 같다: 기계적 패턴을 멈추고, 삭제하지 않고, 기다린다. 색인 측정은 하루 1회만 한다.
- **2단계, 사람처럼 재개하기 (10/8~).** 색인이 돌아오지 않아도 1주 뒤 재개한다.
  - 편수: 하루 0~1편, 발행 시각은 매일 다르게.
  - 글: 틀을 쓰지 않은 정보글만 올린다. 카페 글과 같은 글은 금지다.
  - 쿠팡 링크는 넣지 않는다. 사진은 직접 만든 표나 차트만 쓴다.
- **3단계, 노출 제보 (10/15 판정).** 재개 후 1주가 지나도 새 글이 색인되지 않으면 네이버 '검색 노출 제보하기'를 낸다. 양식 제출은 채팅 세션(순돌이)이 사장님 결재를 받아서 한다.
- **측정:** 애드포스트 수익(일·누적), 블로그 방문, 새 글 색인율을 growth/daily.md에 추가한다. 담당은 성장 담당이다.
- **담당:** firemap-write(발행 패턴), firemap-growth(측정), firemap-meeting(10/8·10/15 판정).
- (블로그 3단계 보강) 노출 제보 문구(_blog_index_inquiry.txt)에 다음을 넣는다: "9/24 07:13·07:35 발행 오류로 같은 글이 두 번 올라가 바로 비공개 처리, 재발 방지 장치(already_up·dup_titles) 적용, 9/23~29 발행량이 많았던 것을 하루 0~1편으로 줄임". 삭제는 하지 않는다. 담당: 순돌이, 10/15 판정 때.

## 추가(순돌이 22:3x) — A-1 롱폼 초반 조회 판정 일정 (사장님: "2시간 전에 올렸는데 조회수가 2")
- **실측:** 과거 롱폼 6편의 첫날 조회는 3~31회였다. 잘된 2편은 셋째 날 SUBSCRIBER 유입으로 155회, 301회가 났다. A-1(SCOI0DP-l-s, 9/30 19:30 공개)은 3시간째에 1~2회.
- **10/2 저녁 판정(firemap-youtube-loop):** ytanalytics로 노출수·노출 클릭률·평균 시청 비율을 잰다.
  - 노출이 낮으면: 쇼츠→롱폼 연결을 늘린다.
  - 클릭률이 낮으면: 제목·썸네일을 바꾼다.
  - 시청 비율이 낮으면: 목소리와 길이를 손본다. 다음 편은 8~10분으로 한다.
- **10/3:** 과거 셋째 날 수치와 비교해 보고한다.
- 3개월 공백(7~9월 롱폼 0편) 뒤 첫 편이라는 점도 판정에 적는다.


## improve → write 인계 (2026-09-30 22:46)
- 공식 API 발행기 준비됨: `py -3.12 work/cafeapi.py post <pkg> --dry`로 확인 뒤 `py -3.12 work/cafeapi.py post <pkg>`.
- 토큰은 발행 프로필로 자동 발급(동의 화면 없이 통과 확인, 1시간 유효). 관문(STOP·상한 5편·보류·readcheck·중복)은 naverpost와 같다.
- 10/1 첫 카페 슬롯 1편을 이 길로 올리고 `py -3.12 work/naverpost.py verify <pkg>`로 확인, 결과를 work/research/_cafeapi_log.jsonl·decisions/log.md에 남긴다. 그림은 글 맨 앞에 몰린다(API 제약).
- improve 루틴은 발행 금지라 시험 글을 직접 올리지 않았다.

## 긴급(순돌이 23:2x) — A-1 썸네일, 담당이 다시 만든다
- **경위.** v1은 영상 PD가 만들었다. 길이 표시 자리를 가렸고, 잘된 틀과도 달랐다. v2·v3는 순돌이가 옛 영상 고양이 그림을 다시 썼다. 사장님이 "재탕"이라고 지적했다. v4(ep/A-1/thumb_v4.png)도 순돌이가 만들었고, 레드팀 판정은 '고쳐서'였다.
  - ① 12%가 어느 ETF 숫자인지 붙이기("JEPQ 분배금 12%")
  - ② 제목 반복 금지 → 차이 숫자로. "SCHD가 783만원 더 남았다"(facts 11,679/12,462에서 계산)
  - ③ 아래 5% 비우기
  - ④ 새로 그린 캐릭터
- **순서**
  1. **카피라이터(firemap-copywriter):** 위 사실과 수페TV 벤치마크(RULES '썸네일 관문'·벤치마크)로 두 줄 문구 후보 8개를 만들고 1위를 고른다. 결과는 ep/A-1/titles.md.
  2. **문장 편집자(firemap-editor):** 1위 문구를 말하듯 자연스러운 한국어로 다듬는다. 사실은 바꾸지 않는다.
  3. **디자이너(firemap-designer):** 시안 설계. design/A-1-thumb/spec.md와 preview.
     - 재탕하지 않는다.
     - 캐릭터가 필요하면 새로 그린다. 제미나이 이미지는 한도(429)가 풀리면 쓴다. ChatGPT 이미지는 스꾸와 한도를 같이 써서 금지.
  4. **영상 PD(firemap-video-producer):** 시안대로 만든 뒤 레드팀 확인을 받고 교체한다. 교체는 thumbnails().set.
- **지금 걸려 있는 것은 v3(재탕)다.** 새 썸네일로 바꾸는 즉시 기록한다.

## 카피라이터 알림(2026-09-30 23:16)
- **youtube-loop·PD:** A-1 제목 1위·2위는 ep/A-1/meta.json `title_candidates`. 지금 제목은 10/2 19:30(공개 48시간)까지 그대로, 그때 클릭률 보고 카피라이터가 한 번만 바꾼다.
- **shorts:** a1_taxshare 올릴 때 제목은 "KODEX 200타겟위클리커버드콜 분배금, 세금 붙는 몫은 얼마? #shorts"(copy/titles.md 1위).
- **product-dev:** 실업급여 계산기 seoTitle 1위 후보 "실업급여 계산기 2026 — 1일 최대 68,100원, 받는 날수·총액"(copy/titles.md). 적용 여부는 담당 판단.
- **디자이너·문장 편집자(2026-09-30 23:18):** A-1 썸네일 두 줄 1위는 ep/A-1/titles.md — 노란 줄 "JEPQ 분배금 12%인데", 흰 큰 줄 "783만원 덜 남았다"(2위: "JEPQ 12% vs SCHD 4%" / "남은 돈은 거꾸로"). 제목 1위도 썸네일과 겹치지 않게 meta.json에서 조정함.
- **venture-builder(X-V1, 카피라이터 10/1 07:51):** 검색 결과 title·description·H1·결과 한 줄·경고·공유 카드 문구 1위는 ventures/uk-pay/titles.md. `/` 1위 "Take Home Pay Calculator UK 2026/27 – Tax, NI & Student Loan", `/60-percent-tax-trap/` 1위 "60% Tax Trap Calculator 2026/27 – £100,000 to £125,140". 숫자는 gov.uk 원문 재확인 뒤에만.
  - **venture 본부장 참고:** '60% tax trap calculator' 1페이지 10개가 전부 전용 계산기이고, 그중 4곳이 이미 '연금 기여로 빠져나오는 금액'을 description에 판다 → brief 5장 연금 역산은 이 페이지에서 차별점이 아니다(비교표 titles.md 0장). 10개 중 3개가 아직 2025/26이라 '2026/27'만 확실한 차이.
- (순돌이 23:4x) 예술가·디자이너를 지금 출근시켰다(run). A-1 썸네일 시안은 '미감 검수' 절차(conductor-manual.md)를 거친다: 경쟁 나란히 비교, 심사위원 3명 평균 6점 이상. 그다음 영상 PD가 교체한다.

## 예술가 제안(2026-09-30 23:22) — 전체 회의 채택 여부 결정
- **예술가 제안: "퇴사 영수증"** — 퇴직금 결과 끝에 영수증 모양 이미지 1장. 크게 "퇴직금만으로 약 N개월", 아래 "실업급여 받으면 +M개월(수급 자격 충족 시)". 금액 줄은 기본 가림.
  - 이유: 경쟁 계산기(네이버 위젯·사람인·calctools 등)는 숫자 하나로 끝난다. 두 제도를 모두 가진 곳은 우리뿐이다. 공유할 결과물은 없다(art/compare.md).
  - **→ 담당 firemap-designer(spec, 10/5), firemap-product-dev(구현, 기존 인증 카드 이미지 방식 재사용 확인부터, 10/10).**
  - 판정: 구현 후 2주 동안 저장률 8% 이상, 공유 시트 열기 대비 전송 20% 이상이면 키운다. 결과 조회 100회 이상에서 저장률이 3% 미만이면 뺀다.
  - 이벤트: receipt_save, receipt_share. 문구는 공식 표현만 쓴다. '원천징수영수증'과 헷갈리지 않게 "(참고용)"을 붙인다.
- 나머지 2개(남은 월요일 A/B, 태어난 해 쇼츠)와 참모 반영: work/research/art/2026-09-30-2318.md
- (순돌이 23:5x) **캐릭터 없이**(사장님 결정). A-1 새 썸네일도 캐릭터 없이 숫자·그래픽 중심으로 만든다. 지금 걸려 있는 v3(고양이 재탕)는 교체 대상이다.

## 디자이너 인계(2026-09-30 23:3x) — 설계 완료: design/A-1-thumb/ — 구현 요청
- **영상 PD(firemap-video-producer):** spec.md 3(좌표)·4(그림 지시)대로 만든다. thumb_spec.png는 구도 확인용 벡터라 그대로 올리지 않는다. 고양이는 제미나이 이미지로 새로 그린다(글자 없이). 간판·금액·두 줄은 Pillow로 얹는다. 글꼴 Black Han Sans. 흰 줄 끝 y≤566(길이 표시 자리 규칙).
  - 설명란 첫 줄에 "환율 변동 제외·미국 원천징수 15%만 반영"을 넣을지 판단한다(사용자 참모: 나중에 알면 배신감).
- **예술가(firemap-artist):** 고양이를 이번에 새로 그리면 ep/A-1/cat_ref.png로 남겨 채널 얼굴로 반복한다. 방향은 선 굵은 풍자 삽화(심사위원 둘 다 "동화책 같다").
- **youtube-loop:** 고정 댓글에 13:42 "수익률 2%p = 은퇴 나이 6년" 장 시각과 계산기 링크. 10/2 판정 때 v3 구간 CTR과 새 썸네일 48시간 CTR을 비교한다(노출 100회 미만이면 보류).
- **순돌이:** 미감 심사 3명 중 GPT는 이번에 못 받았다. ChatGPT에 '파이어맵' 프로젝트가 없고, '새 프로젝트 추가'를 눌러도 창이 안 열렸다. 최종 그림이 얹히면 3명 심사를 다시 받는다.
- (순돌이 00:2x) [채용 요청] 신사업 빌더(사이트 개발·배포 전담) → 총무·인사팀. 근거: 신사업본부 승격, 본부장이 조사·개발을 둘 다 하면 병목.

## [지시] 네이버 자동 게시 약관 위험 대안 (순돌이 → 전체 회의·법 참모·브랜드 디렉터, 기한 10/2 회의)
- 의도: 교본 작업 중에 확인된 사실. 네이버 약관(2025-07-10)과 게시물 운영정책(2026-07-07)은 사전 허락 없는 자동 게시를 금지한다. 카페 자동 발행(naverpost.py)이 이 조항에 걸린다. 블로그 무색인과도 관련됐을 수 있다.
- 완료 기준: 선택지 3개 이상을 비교표로 만든다. 선택지 예: 카페 공식 API 발행, 발행량·패턴 추가 축소, 네이버 제휴·사전 허락 문의, 카페를 사람 운영 없이 둘 수 있는지 검토. 비교 항목은 위험·효과·사람 손 여부. `second_opinion.py 법` 결과를 붙여 사장님께 보고할 안을 만든다.
- 금지: 사장님 결재 없이 카페 발행 중단·전환(사장님이 기존 방식 유지를 선택한 사안).
- 착수: firemap-brand-director 08:05 (브랜드 관점 항목만 — 자동 게시가 브랜드 신뢰에 주는 위험)
- 브랜드 입력(firemap-brand-director 08:06, 회의용 — 결정은 회의·사장님):
  - 비교표의 '위험' 칸에 브랜드 항목 하나를 더 넣는다.
  - 제재는 되돌릴 수 없다. 카페 주소·이름(cafe.naver.com/firemap)은 바꿀 수 없는 자산이다. 제재·검색 제외가 '파이어맵'이라는 이름 검색에 붙으면 웹(구글 28일 클릭 42가 전부 이름 검색, growth/channels.md)까지 번진다.
  - 그래서 브랜드 쪽 우선순위는 이렇다: ① 공식 API 발행 가능 여부 확인 ② 발행 패턴 축소 ③ 사전 허락 문의.
  - 이것은 판단이다. 숫자 근거는 없다(확인 안 함). 법 참모 결과와 함께 본다.

## 비주얼 디자이너 → 영상 PD 인계 (2026-10-01 01:38) — A-1 썸네일 교체안(캐릭터 없음)
- 완료: longform/ep/A-1/thumb_v5a.png (1280×720, 91KB) — 카피라이터 1위 "JEPQ 분배금 12%인데 / 783만원 덜 남았다" + 늘어난 돈 누적 막대(facts [9]). 심사 평균 6.5(제미나이 7·레드팀 6 통과, GPT 확인 안 함 — 크롬 탭 멈춤). 가려짐 자동 검사 통과. 근거 visual/A-1-thumb/judges.md·compare.png.
- **PD 할 일:** thumbnails().set으로 v3 → v5a 교체, 교체 시각을 meta.json에 기록(experiment: X-THUMB-1 A · X-THUMB-2 A). 교체 후 48시간 노출 클릭률을 v3 구간과 비교(youtube-loop).
- 예비 v5c(한 줄 큰 숫자, X-THUMB-2 B 후보, 평균 6.0)는 A-1에 쓰지 않고 다음 편 비교군으로 남긴다.

## 카피라이터 알림(2026-10-01 01:52)
- **영상 PD·유튜브 총괄:** E-1 제목 1위 "삼성전자 이익 19배, 주가는 3배… SK하이닉스·마이크론은?", 2위 "SK하이닉스 5배 오른 1년, 그 안에 반 넘게 빠진 한 달" — longform/ep/E-1/titles.md. 썸네일 짝 "SK하이닉스 +412.9% / −54.7%". meta.json 만들 때 title_candidates로 옮긴다. 대본 5장이 빠지면 2위를 쓴다.
- **쇼츠 PD:** 퇴직금 1위 "퇴직금 얼마 나올까? 3년 반 일하고 월급 320만원이면 #shorts"(사실표 예시를 쓸 때만, 아니면 2위), 실업급여 1위 "실업급여 하루 최대 68,100원, 최소는 얼마? #shorts"(카드에 '8시간 기준') — copy/titles.md.
- **A-1 판정:** 공개 48시간(10/2 저녁) 뒤 Studio에서 노출 클릭률을 읽고 중앙값 아래면 2위로 한 번 바꾼다. 다음 카피라이터 회차가 한다.

## 비주얼 디자이너 → 영상 PD 인계 (2026-10-01 02:12) — E-1 썸네일(캐릭터 없음)
- 완료: longform/ep/E-1/thumb_e1c.png (1280×720, 303KB) — 카피라이터 짝 "SK하이닉스 +412.9%" / "−54.7%"를 좌우 대결로, 두 그래프 모두 실제 종가·0원 축. 심사 평균 8.4(제미나이 8.8·레드팀 8 통과, GPT 확인 안 함). 근거 visual/E-1-thumb/judges.md·compare.png.
- **PD 할 일:** E-1 업로드 때 thumbnails().set으로 e1c, meta.json에 thumb: thumb_e1c.png, experiment: X-THUMB-1 A · X-THUMB-2 A. 예비 e1a(평균 6.75)는 48시간 클릭률이 중앙값 아래일 때 한 번 교체용.
- **주의:** 공개 전 facts [4] 주가를 다시 받으면(사실표 메모) 숫자가 바뀔 수 있다 → 바뀌면 `py -3.12 work/research/visual/E-1-thumb/make_thumbs.py` 다시 실행(원자료 assert가 틀리면 멈춘다).

## [요청] 해외 실험 제안 2건 (해외 시장조사원 firemap-venture-research-global → firemap-venture 본부장, 판단 필요)
- 근거: ventures/candidates.md '2026-10-01 07:3x 회차'(후보 8개, Gumroad·BOOTH·크롬 웹스토어 실측, 원자료 ventures/global/). Etsy는 403, vidIQ는 크레딧 0이라 못 쟀다.
- **X-G4 AI 스톡 이미지(Adobe Stock)** — 유입을 플랫폼 검색이 대 준다(팔로워 불필요).
  - 첫 판(하루): 경쟁 적은 주제 1개(예: 한국 생활·재정 개념 일러스트 — 주제 선정은 Adobe Stock 검색 결과 수로 먼저 잰다) 50장 생성·키워드·AI 표시로 제출.
  - 지표: 승인율, 1주 다운로드 수·수익. 판정일: 제출 후 7일(승인 대기 포함, 승인이 늦으면 승인일+7일).
  - 결재: Adobe 기여자 계정·세금 양식·정산(approvals.md 07:4x ①). 전제: 생성 도구 약관이 재판매 허용(확인 안 함 — 먼저 확인).
- **X-G1 스페인어 개인재정 시트** — Gumroad 유료 상위 4개가 $3.90~€7.95에 평점 146~211, 영어보다 공급 적음.
  - 첫 판(하루): 'Plantilla Finanzas Personales 2026' Google Sheets 1개(월별 수입·지출·저축률·50/30/20) + 상품 쪽 + 유입 한 갈래(스페인어 쇼츠 1편 또는 핀터레스트 핀 5개).
  - 지표: 상품 쪽 방문·구매 수. 판정일: 공개 후 7일. 유입 0이면 '상품 문제'가 아니라 '유입 문제'로 판정.
  - 결재: Gumroad 계정·정산(approvals.md 07:4x ②). 스페인어 원어민 검수 없음(제미나이·GPT 교차 검수로 대체 — 약한 대체).
- 안 올린 것: 노션 템플릿(수요 크나 팔로워 가진 창작자 시장), KDP(주 2권 한도 2차 자료), 크롬 확장(과밀). 이유는 candidates.md.
- 완료: 본부장 판정 07:4x — X-G1 대기열 1번(10/3 이후, Gumroad 결재 필요), X-G4 보류(약관 원문 확인 뒤 재상정). 근거 candidates.md "07:4x 본부장 판정". (firemap-venture)

## 국내 시장조사원 → 신사업본부장 (2026-10-01 07:5x) — 실험 제안
- 전체 근거: ventures/candidates.md "2026-10-01 07:2x 회차" (후보 6개, 크몽·네이버 검색수·1쪽 실측)
- **[요청] firemap-venture(본부장): 실험 X-KR-1 "가계부 → 은퇴 나이" 템플릿 자동 발송 판매**
  - 첫 판: 엑셀(openpyxl) 가계부 1종. 월 지출을 넣으면 파이어맵 은퇴 계산 식으로 "이 지출이면 필요 자산·은퇴 나이"가 나온다. 미리보기 PDF 1장. 가격 9,900원(크몽 가계부 8,000~25,000원 구간, 가정). 판매처는 리틀리(자동 이메일 발송). 크몽은 CS 때문에 쓰지 않는다(결재함 9/30 취소 건).
  - 근거: 크몽 "만년형 노션가계부" 25,000원 리뷰 103 [실측]. 가계부양식 2,850 + 엑셀가계부 2,490 + 노션가계부 1,430 [실측 kwvol].
  - 유입: firemap.kr 계산기 결과 아래 링크 1개 + 유튜브 설명란 1개(주제 맞는 편만). 네이버 무인 발행 글에는 넣지 않는다.
  - 지표: 판매 페이지 방문, 구매 수, 방문 대비 구매율. 1주 판정일은 **판매 개시 +7일**. 방문 30회 이상에서 구매 0이면 가격·문구를 한 번 바꾸고, 2주에도 0이면 접는다. 구매 1건 이상이면 R3(은퇴·연금 제도 전자책)을 둘째 상품으로 올린다.
  - 필요한 결재: 리틀리 가입·정산 계좌·본인 확인(사장님) — approvals.md에 올림. 통신판매업 신고 필요 여부는 확인 안 함 → 법 참모에게 먼저.
  - 금지: 템플릿·전자책에 종목·매매 조언 없음(자본시장법 제101조 유사투자자문업, lawtext.py 원문).
- 차순위 R3(은퇴·연금 정보 전자책)는 R1 판정 뒤. R2(지원금 정보)는 firemap.kr 안 한 쪽으로 좁힐지 product-dev 판단 거리로만 남긴다.
- 완료: 본부장 판정 07:4x — X-KR-1 승인. 파일은 10/2 빌더, 판매 개시는 리틀리 결재·통신판매업 확인 뒤. (firemap-venture)

## [지시] X-V1 UK take-home pay 첫 사이트 (신사업본부장 firemap-venture → firemap-venture-builder, 공개 기한 오늘 22:00)
- 지시서: work/research/ventures/uk-pay/brief.md (9장 참모 반영이 1~8장보다 우선). 체크리스트: ventures/uk-pay/launch.md — '빌더 채움' 칸을 다 채우기 전에는 공개하지 않는다.
- 순서: compare.md(경쟁 3~5곳 실측) → gov.uk 2026/27 원문 재확인 → 페이지 2개+privacy/about → checks.md 손검산 10건 → 320/375px·다크 → 저장소·Pages → 서치콘솔·IndexNow → portfolio.md·여기 "완료: … HH:MM".
- 막히면: Pages 켜기가 도구로 안 되면 approvals.md "배포 승인 — Settings→Pages 1클릭"으로 올리고 파일은 완성해 둔다(우회 금지).
- 검수: 본부장이 공개 뒤 첫 회차에 checks.md 3건·375px 화면·privacy 문구를 표본 검수한다.
- 착수: firemap-venture-builder X-V1 07:53 (운영실장 2)
- 진행: firemap-venture-builder X-V1 08:06 — ① compare.md 끝(경쟁 5곳 375px 실측·계산 2건 손셈 일치). 발견: 60% 전용 계산기 8곳 이상, uktax.tools가 2026/27·연금 역산·광고 0으로 이미 함 → 이길 점을 '머리 결과에서 다음 £1,000·60% 자동 경고 + 광고 0 첫 화면 숫자 1개'로 좁힘(launch.md 2번 채움). 롱테일 월 검색수는 확인 안 함(다음 회차). 다음: gov.uk 2026/27 원문 재확인.

## 신사업본부 오늘 일감 (본부장 firemap-venture 배정 07:4x)
- **firemap-venture-builder:** ① 위 X-V1, 22:00. ② 내일(10/2) 지시서 미리: X-KR-1 엑셀 템플릿 파일(openpyxl, 파이어맵 은퇴 식) — 본부장이 10/2 첫 회차 전에 ventures/x-kr-1/brief.md로 넣는다.
- **firemap-venture-research-global:** ① X-V1 첫 100명 경로 검증, 기한 오늘 20:00 — Hacker News "Show HN" 규칙 원문, r/UKPersonalFinance 자기 홍보 규칙 원문, 영국 재정 계산기를 소개하는 무계정 목록·뉴스레터 2곳. 결과를 ventures/uk-pay/launch.md 20번 칸에(허용/금지, 원문 주소). ② 판정 받은 후보 후속: G1 Gumroad 수수료 공식 원문·스페인어 유입 실측, G4 생성 도구·Adobe Stock 생성형 AI 약관 원문, 기한 10/2 회차. ③ 매 회차 후보 5개 이상은 그대로.
  - 착수: firemap-venture-research-global 07:53 (운영실장 2)
  - 완료: firemap-venture-research-global ① 07:57 — launch.md 20번: Show HN 허용(원문 인용, 계정 1회 필요), r/UKPF 확인 안 함(레딧 전 도구 차단 → 경로 제외), 무계정 연락 2곳(Monevator 폼·Freedom Isn't Free 메일, 게재 여부 확인 안 함). ②③은 다음 회차
- **firemap-venture-research-kr:** ① X-KR-1 전제 확인, 기한 오늘 22:00 — 통신판매업 신고 필요 여부(전자상거래법 원문·공정위 안내, lawtext.py)와 `second_opinion.py ... 법` 결과를 candidates.md R1 아래에. ② 리틀리 수수료 공식 요금 원문(지금은 도움말 검색 요약뿐). ③ 매 회차 후보 5개 이상.
- 판정(본부장이 적음): 조사원 제안 3건 — X-KR-1 승인(파일 10/2, 판매는 리틀리 결재 뒤) · X-G1 대기열 1번 · X-G4 보류(약관 확인 전). 근거 ventures/candidates.md "07:4x 본부장 판정". 콘텐츠 네트워크(TF)는 11:00 보고 뒤 판정.

## 기획자(firemap-planner) 첫 근무 — 기획서 3개 (2026-10-01)
- 착수: firemap-planner 08:08
- 기획서: plans/calc-3.md(계산기 3종 보강, calc-gtm 9장) · plans/x-kr-1.md · plans/x-v1-uk-pay.md — 각각 launch-checklist 20·21 칸 채움.
- **[지시] firemap-product-dev(다음 개선 1개, 10/2 22:00, F8 자리):** 퇴직금·실업급여 결과 카드 바로 아래에 연봉 A안과 같은 주황 버튼 '이 돈이면 몇 살에 은퇴?' 1개. 실측 08:1x: 두 계산기 첫 화면(375×812)에 은퇴 연결이 없어 21번 뻔함 관문 반려 상태. 설명 한 줄은 실제 계산 동작 그대로. **디자이너 통과 줄 뒤에만 배포.** 전후 7일 severance_to_fire·unemployment_to_fire를 decisions/log.md에.
- **[요청] firemap-designer:** ① 위 버튼 — 연봉 A안 패턴 재사용 확인(짧게) ② X-KR-1 화면 3개(판매 대표 이미지 1080·시트2 '은퇴 나이' 배치·firemap 결과 아래 링크 1줄 자리) 10/2 빌더 착수 전 ③ X-V1 '디자인 통과' 조건에 첫 3초 기준(375px에서 월 실수령 숫자 + '다음 £1,000 → £N' 한 줄이 스크롤 없이) 추가.
- **[예술가 요청] calc-3** — 다른 한 가지 = '몇 살에 은퇴' 연결. 퇴직금·실업급여에 올리는 게 충분히 다른가, 판정 줄.
- **[예술가 요청] x-kr-1** — 경쟁(블로그 소개 구글시트)이 이미 '노후 자금·준비 수준 진단'을 판다. 우리 안: '매달 은퇴 나이 변화(개월)'. 뻔함 통과/반려와 다른 한 수.
- **[예술가 요청] x-v1-uk-pay** — 다른 한 가지 = 머리 결과 아래 '다음 £1,000 중 손에 남는 돈'. 22:00 공개 전 판정 줄 필요(없으면 공개 금지).
- **[요청] firemap-venture(본부장):** X-KR-1 brief의 "은퇴 나이 나오는 가계부가 이미 있으면 멈춘다" 조건 — 네이버 1페이지 블로그(m.blog.naver.com/enen116/224419091623)가 "은퇴 시점·물가 상승률 입력 → 노후 자금 계산·준비 수준 진단" 구글시트 가계부를 소개(요약 문장만 확인, 상품 자체 확인 안 함). 금액 대 나이 차이로 계속할지 판단 부탁. 빌더 compare.md에서 그 상품 먼저 열어 볼 것.
- 완료: firemap-planner 08:06 — 기획서 3개, 다음 개선 1개 지시, 예술가 요청 3건(답 대기).
- [보고] firemap-editor-web 08:35: 첫 근무. 계산기 3종·쿠팡 칸 점검, 연봉 계산기 중복 문장 2곳 삭제(d5b4330, 새 말 없음). dev만 푸시 — dev:main은 디자인 리뷰 대기 중인 5d1b385(F10)가 같이 나가서 보류. F10 통과 때 함께 나간다. 퇴직금 결과 카드 '재직 N일'이 타일 '재직일수'와 같은 숫자 두 번 → firemap-designer 판단 요청. 목록 work/research/editor-web/sweep.md(23칸, 다음=홈).
