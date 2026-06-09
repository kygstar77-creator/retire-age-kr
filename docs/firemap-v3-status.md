# FireMap v3 — 진행 상태 / 아침 보고서 (최종)

브랜치 `firemap-v3` · 라이브 프리뷰: https://firemap-v3.retire-age-kr.pages.dev/
프로덕션(main, 구버전): https://retire-age-kr.pages.dev/ ← v3 미반영(의도적, 아래 참고)

## 대화 전체 재검토 후 반영한 기능 (FigJam/PRD 매핑)
- Home·질문(단위칩·상한제거 입력)·Result(등수 히어로)·Compare(증권앱 차트+전체 레버)·Advanced·City·Share·Community 전부 동작
- 코어 엔진 검증(8케이스 손계산 일치)
- 등수: 통계청 가계금융복지조사 백분위(즉시) + Supabase 익명 점수 실시간 등수
- 세제 모듈 4종(로직 검증): 건보료 피부양자 판정·해외주식 양도세(누진 27.5%)·배당 건보료/종합과세 경고·국민연금 조기수령
- 투자 수익률 벤치마크(예적금 대비, 교육용·컴플라이언스)
- 해외체류 직접조절 모듈(체류개월·환율·건보료 정지) + 도시 정보(비자/의료/기후)
- 공유 바이럴: 등급 카드 이미지(등수·등급, 금액 없음) + 조건 링크(계산값 포함) + 받은 링크 입력 자동 채움→결과 진입
- 데이터: 출처/기준일 레지스트리 + 환율 시드/갱신 스크립트(work/refresh-data.mjs) + City 환율 데이터 연동(fallback)
- 컴플라이언스: 1회 면책 동의 + 종목추천 차단 문구
- 은퇴 백과 6편(피부양자·양도세·배당·국민연금·동남아·4%룰), 홈 링크
- 디자인 토큰화 + UI 스펙 문서

## 남은 작업 / 수빈님 조치 필요
1. 프로덕션 배포(#7): 자동 머지 안 함. 프리뷰 확인 후 PR 머지(원클릭). → https://github.com/kygstar77-creator/retire-age-kr/pull/new/firemap-v3
2. 환율 주간 자동갱신 cron: `docs/snippets/refresh-data.workflow.yml`를 `.github/workflows/`로 넣어야 함(토큰 workflow 권한 없어 제가 못 올림). 또는 수동으로 `node work/refresh-data.mjs`.
3. 은퇴 백과 나머지 4편 + Google AdSense 계정 신청/승인.
4. 프리미엄 PDF·결제(#13): 배포 후 반응 보고 추가(토스페이먼츠 계정·키 필요).
5. 동적 OG 메타(공유 URL별 미리보기 이미지): 현재 정적 OG + 등급 카드 이미지로 대체. 완전 동적은 엣지 렌더 필요.
6. v2 CSS 깊은 통합(#9): 토큰화는 완료, 잔여 firemap-*.css 통합은 후순위.
7. 보안: 작업 끝났으니 GitHub fine-grained 토큰 revoke 권장.

## 프로덕션 배포 방법 (원클릭)
프리뷰를 폰에서 확인 → 위 PR 링크 → "Merge pull request" → Cloudflare가 main 자동 배포. 롤백은 머지 revert 또는 Cloudflare 이전 배포.

## 검증
개발 내내 자동 검증(시뮬레이터 회귀 + 세제/연금/피부양자/공유 왕복 단위검증 + esbuild 번들)으로 확인. 머지 전 프리뷰에서 라이브 통합 QA 1회 권장(특히 Advanced 계산기, Share 공유, City 해외체류, 조건링크 진입).
