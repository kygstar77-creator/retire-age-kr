# 파이어맵 개편 기여 가이드 (dev 브랜치 · 2026-09-11)

이 레포는 firemap.kr(파이어맵) 전용이다. 다른 프로젝트(스꾸)의 Supabase·Cloudflare·GitHub는 절대 건드리지 않는다.
Supabase 프로젝트는 `cvhskxdwqubmshdgkzhj` 하나뿐이며, 클라이언트 접속은 `src/utils/supabaseClient.js`의 `SUPABASE_URL / SUPABASE_KEY / sbHeaders / sbGet / sbRpc`만 쓴다(URL·KEY를 파일에 다시 적지 않는다).

## 1. 절대 규칙
- 화면 파일에 `style={{}}` 인라인 스타일 0, hex 색 0, `!important` 0, `window.alert/confirm` 0(→ `toast`, `Dialog`).
- 컴포넌트는 `src/ui/index.js`에서만 import: `Button IconButton BottomCTA Card SectionHead ListGroup ListRow Stat StatTiles ProgressBar Chips Chip Badge Tabs Sheet Dialog toast Notice EmptyState Skeleton Spinner TopBar StatHero Fold LeverList RangeField RuleChips PotCard`.
- 화면 루트: `<main className="fm-screen fm-scroll fm-has-tabbar ds-screen-gap">` (탭 없는 화면은 fm-has-tabbar 생략). 첫 자식은 `<TopBar title="…" onBack={onBack} />` 또는 `<TopBar onHome={() => onMove('home')} actions={…} />`.
- 날짜는 `src/utils/dates.js`(todayStr·monthStr·ymdOf) 1벌. 포맷은 `src/firemap-v2/formatters.js`의 `formatWon`(억/만), 기간은 `dailyData.fmtAdvance`.
- 새 CSS는 `src/ui/screens/<파일이름>.css`에 `.ds-*` 또는 `.sc-<화면>-*` 접두로만 추가한다(다른 파일의 CSS는 만지지 않는다). 토큰만 사용: `var(--ds-bg|surface|surface-2|line|line-strong|ink|ink-2|ink-3|accent|accent-strong|accent-soft|accent-ink|good|good-soft|warn|warn-soft|bad|bad-soft|r-sm|r-md|r-lg|r-xl|r-pill|sp-1..8|fs-*)`.
- 다른 사람이 맡은 파일은 열어보되 수정하지 않는다. `src/ui/fm-ds.css`, `src/ui/index.js`, `FireMapMVP.jsx`, `screens.js`는 수정 금지(필요하면 보고서에 "요청" 항목으로 적는다).
- 커밋하지 않는다. 빌드 확인은 `npx vite build --logLevel error` (에러 0이어야 함).
- 렌더 검사: 390px에서 가로 넘침 0, 숫자 줄바꿈 0(`.num` + `white-space:nowrap`), 긴 한글은 `word-break: keep-all`.

## 2. DS 컴포넌트 API 요약
- `Button variant=primary|secondary|ghost|tint|dark|danger size=lg|md|sm full loading disabled onClick` · `IconButton label size=sm plain`
- `Card variant=hero|soft|flat|tint|dark padding=md|lg onClick as` · `SectionHead kicker title desc action size=sm`
- `ListGroup label` > `ListRow lead title desc trail chevron size=S|M|L accent href external onClick`
- `Stat label value unit delta{text,dir:up|down} size=display|title|md|sm center` · `StatTiles items=[{label,value,unit,onClick}]` · `ProgressBar value max left right thin tone=good`
- `StatHero tone=dark|light label value unit sub delta tiles size children` — 화면의 "숫자 하나"
- `Fold icon title hint defaultOpen onOpen` — 접힘(열 때만 렌더)
- `LeverList items=[{key,tag,label,gain,off,onApply}]`
- `RangeField label value min max step money format chips=[가산액] required hint onChange` — 슬라이더+직접입력 Sheet
- `Tabs items=[{key,label}] value onChange variant=segmented|pill` · `Chips > Chip on onClick`
- `Sheet open title onClose` · `Dialog open title desc primary{label,onClick} secondary onClose` · `toast(msg)` `toast.good/bad`
- `Notice tone=accent|good|warn|bad icon title` · `EmptyState icon title desc action`
- 3숫자 가로 카드: `<div className="ds-three"><Stat…/><Stat…/><Stat…/></div>`
- 유틸 클래스: `.num .ds-caption .ds-body-sm .ds-p .ds-link .ds-stack .ds-row .ds-grid-2 .ds-grid-3 .ds-mt-2/3/4 .ds-textcenter .ds-list .ds-row-item.ds-row-item--S/M.ds-row-item--static`

## 3. 한글 카피 규칙 (6차 디자인시스템 결정서 §7 · 3차·4차 조사)
1. 어미는 해요체로 통일(-예요/-해요/-돼요). "~합니다/~하세요/~하십시오" 금지. 느낌표는 화면당 1개 이하.
2. 한 문장 25자 안팎, 한 블록 2문장 이하. 설명은 제목 아래 desc 한 줄로.
3. 숫자가 주인공: 문장 속 숫자는 `<b className="num">`로 감싸고 단위를 붙인다(56세·12.0억·월 140만). "약·대략·추정"은 캡션에만.
4. 사용자 관점 단어: "내 파이어 나이", "필요 자산", "오늘 한 걸음", "파이어 통", "같은 구간". 시스템 용어 금지: "시뮬레이션·파라미터·프리셋·모드·세그먼트·보드·컴포넌트·모듈·샌드박스·RPC·동기화" → "계산·조건·예시·화면·랭킹·기록 이어지기".
5. 전문용어는 첫 등장에 한 번만 풀어쓴다: 4%룰 → "1년 생활비의 25배(필요 자산)", 코스트파이어 → "더 안 모아도 굴리기만 하면 되는 상태", 지역가입자 → "회사 없이 혼자 내는 건강보험", 배당락 → "이 날 전에 사야 배당을 받는 날".
6. CTA는 동사로 끝나는 명령형 명사구: "기록하기" "계산하기" "인증 카드 만들기" "적용". 이모지는 CTA 앞에 1개까지, 본문에는 안 쓴다(섹션 kicker에는 허용).
7. 금액: 억·만 단위(formatWon). 원 단위 나열 금지. 퍼센트는 정수. 나이는 "56세".
8. 경고·면책은 회색 캡션 한 줄: "참고용 계산이에요 · 투자 자문이 아니에요".
9. 커뮤니티: "카페"(네이버 카페)·"방명록"(앱 안 한마디)·"인증 카드". "커뮤니티·라운지·오픈채팅·피드" 금지.
10. 부정 표현은 다음 행동과 함께: "아직 파이어 나이가 안 나와요 · 생활비를 낮춰보세요".
11. 괄호·슬래시·중점 남발 금지. 보조 정보는 중점(·) 하나로 잇거나 캡션으로 뺀다.

## 4. 데이터·사실 (조사에서 확정된 것 — 카피에 쓸 때 이 숫자만)
- 통계청 2025 가계금융복지조사 기준 또래 순자산 비교. 카카오뱅크 26주적금 800만 좌. 토스뱅크 이자받기 650만 명.
- 미국 ETF 배당은 Yahoo chart(events=div)로 과거만 확정, 향후 배당락은 "예상"으로 표기. 국내 ETF 분배금은 공식 소스 없음("예상" 표기).
- 파이어맵 카페: https://cafe.naver.com/firemap (links.js CAFE_URL). 게시판: 인증·봐주세요·파이어 후 하루·어디서 살까·오늘 한마디·소식.
