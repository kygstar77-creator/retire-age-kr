# FireMap v3 UI 스펙 (디자인 잠금)

토큰: `src/firemap-v3-tokens.css` (색·반경·간격 단일 출처). 모든 v3 화면/컴포넌트는 하드코딩 대신 토큰 참조.

## 색
- 네이비(등수 히어로): --fm-navy / 라벨 --fm-navy-soft
- 액센트(주행동·차트·게이지): --fm-accent
- 성공/개선: --fm-success
- 텍스트: --fm-text / 보조 --fm-muted / 흐림 --fm-faint
- 표면: --fm-surface, 경계 --fm-border

## 공용 컴포넌트
- 카드: surface + --fm-border + radius-lg + padding 16.
- 단위 칩(돈 입력): +금액 가산, 상한 없음(직접입력=슬라이더 max 초과 가능). 나이·%는 슬라이더+스텝퍼.
- RankHero(네이비): "또래 상위 X%(통계)" + 등급 배지 + "함께 계산한 N명 중 K등(Supabase)" + 출처. **결과 최상단 히어로.**
- 진단 점수 게이지: accent 막대.
- Top 레버 2개 카드 / 다음행동 카드(비교=primary, 2px accent border).
- AssetCompareChart: 증권앱 영역 차트(현재 점선 vs 절감안 영역+그라데이션), 크로스헤어 툴팁.
- Header: 로고 탭→홈, '‹ 이전'. 의견 FAB(아이콘).

## 화면 레이아웃 (목업 확정본)
- Home: 브랜드 + "내 돈은 몇 살까지" + 신뢰 칩 + 시작 CTA + 정책 링크.
- Question: 1화면 1질문, 진행바, (돈=칩) 입력, 하단 이전/다음.
- Result: RankHero(히어로) → 요약(퇴사나이·자산수명) → 진단 점수 → 레버 2개 → 다음행동 → 광고 → 면책.
- Compare(Experiment): 전체 레버(자산·나이·저축·생활비·부업·수익률·절감안) + 증권앱 차트.
- City: 국내·해외 도시 생활비·FIRE 수명·정보(주기 갱신, 출처).
- Advanced: 건보료·해외체류·현금흐름·세금·환율 — 각 입력/가정/결과/적용.
- Community: 익명 한마디(Supabase), 금융 입력 미저장.
- Share: 등급 카드 이미지 + OG 후킹 + 조건 링크(Base64).

## 미해결(다음 보정)
- AssetCompareChart의 캔버스 색은 아직 하드코딩(canvas라 CSS var 직접 불가) → JS에서 토큰 읽어 적용 예정.
- 흩어진 v2 CSS(firemap-*.css 다수) 점진 통합(#9).
