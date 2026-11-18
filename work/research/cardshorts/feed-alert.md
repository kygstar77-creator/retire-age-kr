# 쇼츠 피드 배포 경보 — 판정 줄

기준: 공개 48시간(공개일·다음날) 유튜브 분석 `insightTrafficSourceType=SHORTS` 조회 50 미만 → patrol 위반(`shortsdaily.feed_check`, 11/19 benchmark-loop 지시).
분석 API는 2~3일 늦게 차서 공개 3일 지난 편부터 본다. 분석이 0인데 공개 조회수가 50 이상이면 '측정 지연'으로 넘긴다.

## 2026-11-19 첫 판정 (youtube-loop, 2026-11-19 04:5x 실측)

| 편 | 공개(KST) | 길이 | 48시간 쇼츠 피드 / 전체 | 같은 롱폼에서 자른 형제 편 | 판정 |
|---|---|---|---|---|---|
| aW8HfeGCGgw SCHD 배당금 11%→2% | 11/05 19:20 | 28초 | 2 / 8 (누적 조회 9) | HFESFTAD8dU(D-ETF-1, 31초) 589 | 원인 확인 안 함 |
| 7bBwnLg86-Q 종부세 거주기간 공제 | 11/11 19:20 | 32초 | 0 / 1 (누적 2) | G5ofrC5Di4U·x1e7vUdFghg(J-1) 1,150·974 | 원인 확인 안 함 |
| jGtx9f6SZKA 정기예금 1억 이자 | 11/12 19:20 | 28초 | 0 / 2 (누적 2) | p1NgZhn5QUk(K-1, 33초) 989 | 원인 확인 안 함 |

Data API로 같은 주 잘된 c1clip 편과 견준 것 — 차이 없음:
- privacyStatus public · madeForKids False · license youtube · uploadStatus processed · licensedContent False · contentRating 없음 · regionRestriction 없음 · 카테고리 27 · 오디오 ko · 태그 5개 · 설명 570~800자 · 공개 시각 19:20 같음 · 목소리 같은 롱폼 wav 재사용(형제 편과 같은 방식).
- 길이: 막힌 3편은 28~32초로 짧은 쪽이지만 31초(HFES 589)·33초(p1Ng 989)도 잘됨 → 길이로 설명 안 됨.
- 세 편 모두 피드 첫 노출 자체가 거의 없음(전체 1~8) — 시청 반응이 나빠서 줄어든 모양(수백 노출 뒤 꺾임)이 아니라 처음부터 배포가 안 된 모양.

남은 확인(사장님 로그인 필요 — today.md 11/19 '결정 필요 ②'와 같은 일): 유튜브 스튜디오에서 세 편의 '제한'·저작권 표시·'적합성' 칸. Data API로는 이 표시를 읽을 수 없다.
다시 볼 것: 11/16~11/18 공개 3편(7_EkpkW09ec·yX3f9ESewcg·ISLXaS9Wa18)은 분석 아직 0(공개 조회 380~1,079라 배포는 됨) — 11/21 patrol이 자동으로 다시 잰다.
