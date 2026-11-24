# 2026-11-24 레드팀 — 안 보고 있는 위험 3·기회 3
> 주제 범위(배당·지수·부동산)·발행 빈도는 사장님 결정이라 건드리지 않는다. 근거는 저장소·DB(SELECT)·oEmbed 21:44만.

## 위험
| # | 위험 | 근거 한 줄 | 담당 후보 |
|---|---|---|---|
| R1 | 영상·카페에서 온 사람이 계산을 안 한다. 콘텐츠를 고쳐도 사이트 수익 길이 안 열린다 | SQL 11/17~24 사람 session_start: utm youtube 4기기·cafe 2기기 → calc_complete 0. 카페 착지는 /dividend였다(props path, utm_campaign kdiv1121). '/'로 바꾼 B군 효과는 아직 0일치 | firemap-report(유입원별 완주율 매일 한 줄) |
| R2 | 예약을 풀고 다시 올린 비공개 사본이 채널에 쌓인다. YPP 심사 때 반복·재사용 판단 재료가 될지 확인 안 함 | khvIhE8Sf-s oEmbed 403(비공개 유지, STATE.md 11행) · h8BYw06r3-s 예약 풂(log.md 4362) · 3dzKukPP3ac(h5-diagnosis 22행) | firemap-video-producer(비공개 사본 목록·정리 여부 정책 원문 확인) |
| R3 | 발행기 한 개가 멈추면 칸이 빈다. 72분 멈춤을 감시기가 아니라 다음 발행 회차가 찾았다 | slots.json 488 rsp1124 "naverpost cafe가 16:00:31 시작 뒤 72분 멈춤", 기록자 firemap-write 17:13 | firemap-watchdog(발행 시작 뒤 N분 진척 0이면 경보 — N은 지난 발행 소요 실측으로) |

## 기회
| # | 기회 | 근거 한 줄 | 담당 후보 |
|---|---|---|---|
| O1 | 커뮤니티 유입은 계산까지 간다. 어떤 글에서 왔는지 찾아 그 꼴을 카페 글 링크 문구에 쓴다 | SQL 11/17~24 사람: ref m.dcinside.com 2기기·theqoo.net 1기기 → 3기기 모두 calc_complete, 착지 '/'. 어떤 글인지는 확인 안 함 | firemap-report(원 글 찾기) → firemap-copywriter(카페 링크 문구) |
| O2 | 롱폼끼리 잇기. 첫 조회가 홈이 아니라 '관련 동영상'에서 온다 | h5-diagnosis-1124.md 33행: H-5 첫날 조회 5 중 관련 동영상 4(시청 22분)·탐색 1 | firemap-youtube-loop(끝 화면·재생목록 짝을 같은 축 편으로) |
| O3 | 카페 글마다 utm_campaign이 이미 붙어 있다. 글별 사이트 유입을 재서 다음 카페 소재를 고른다 | session_start props utm_campaign 'kdiv1121'·utm_source cafe 확인 | firemap-report(글별 표) → firemap-write·firemap-write-b |

## 확인 안 함
비공개 사본이 YPP 판단에 쓰이는지 · dcinside·theqoo 원 글 · 이용약관 법적 필수 여부(verify V17).
