# cloud/ai-study-1003 — AI 활용 유튜버 스터디 요약 (2026-10-03)

## 무엇을 했나
- cloud-prompts-1003.md ③을 했다. 6분야(디자인·영상 제작·네이버·에이전트 운영·차트·제휴)에서 출처 34행을 모아 도구·명령·순서만 뽑았다. 분야별로는 ① 6, ② 7, ③ 6, ④ 6, ⑤ 4, ⑥ 5다.
- 방법 30개마다 담당·바꿀 것·효과·비용·위험을 적었다. 교본·workflow.md·radar·today.md와 대조해 '이미 함(배제 포함)' 6개, '일부 이미 함' 2개, '진행 중' 3개, '보류·탈락' 4개를 표시했다.
- 결과 본문: `work/research/ai-lab/study-2026-10-03-youtubers.md`
- 코드는 바꾸지 않았다. 그래서 테스트도 없다.

## 근거와 출처 (본문을 직접 연 것)
- code.claude.com/docs/en/costs: `/usage`의 스킬·서브에이전트·MCP·예약 작업별 비중, `/clear` 비용 0, CLAUDE.md 200줄 이하, 훅으로 출력 필터.
- code.claude.com/docs/ko/claude-code-on-the-web: `claude --cloud`, `claude -p "…" --cloud <id>`, `--teleport`. **클라우드 세션은 계정의 다른 사용과 속도 제한을 공유한다.**
- claude.com 블로그(2026-09-30 갱신): `/design-sync`·`/design`. Claude Design은 Claude Code와 한도를 공유한다.
- GitHub에서 연 것: dembrandt(플래그 `--dtcg --wcag --compare --dark-mode --mobile`, MCP 명령), remotion-dev/skills(`npx skills add remotion-dev/skills`), longform-to-shorts.
- 그 밖의 블로그·언론·유튜브는 네트워크 차단으로 **검색 요약문만** 봤다. 08-03 이후 날짜가 확인된 것은 11건이다. 그중 숫자가 있는 것: AI 브리핑 인용의 49.3%가 상위 10위 밖(원포인트), 네이버 메이트 월 3,000명·연 200억(파이낸셜뉴스 8/7), 쿠팡 약관 9/3 시행(이데일리 8/4).

## 확인 안 함
- 유튜브 영상 자막 전부(vidIQ 크레딧 0, youtube.com 차단). 한국어 영상 게시일 대부분.
- 클라우드 크레딧 $250 조건 원문. **공식 문서('한도 공유')와 지시문('PC 주간 사용량 안 씀')이 어긋난다.**
- 쿠팡 9/3 약관 원문, 그 조항이 파트너스에도 적용되는지.
- Opus 5.5 한도 리셋 1회(10/22 만료). Dembrandt `--compare` 출력 형식. 네이버 AI 브리핑 인용수를 어디서 보는지.

## 담당이 적용할 것 (상위 10 중 바로 할 일)
1. 순돌이·총무: 오늘 '시작 전 85%'와 이 세션들이 끝난 뒤 주간 %를 비교해 클라우드가 주간 한도를 쓰는지 decisions/log.md에 기록한다.
2. firemap-write·editor: 글 체크리스트에 '첫 문단 숫자 답·질문형 소제목 2개 이상·FAQ 2~3·표 1·1인칭 계산'을 넣는다. 관문 코드를 고치면 test_*.py도 함께 넣는다.
3. 총무·growth: 쿠팡 9/3 약관의 자동화 금지 조항을 revenue_daily.py(크롬 MCP 리포트 읽기)·f2_coupang.py 방식과 대조한다.
4. 총무: 사용량 보고에 `/usage` 상위 3개 소비처(예약 작업 포함)를 넣는다.
5. 비주얼·모션: 차트 전에 `/dataviz` 팔레트 검증기로 우리 의미색을 검사한다.
6~10. Dembrandt 회귀 관문(A2) · 교본 슬림+훅(D5·D6) · Remotion 스킬(B1) · 롱폼→쇼츠 자르기(B5, 결재 필요) · Claude Design 재시험(A4). 자세한 내용은 본문 3장에 있다.
