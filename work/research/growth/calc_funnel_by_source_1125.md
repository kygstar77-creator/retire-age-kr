# 유입처별 계산 완주 — 11/17~11/24(KST) 사람 기기 (firemap-report 11/25, 회의 11/24 21:47 지시)
출처: Supabase firemap_events. 기기(client_id) 단위, 기간 첫 session_start의 utm_source → 없으면 ref 호스트 → 없으면 direct. props.bot·internal이 한 번이라도 '1'/'true'인 기기 뺌. 완주 = calc_complete 또는 calc_result.

| 유입처 | 기기 | 계산 완주 | 쿠팡 | 랜딩 |
|---|---|---|---|---|
| direct | 60 | 5 | 0 | / · /calc/salary · /calc/severance · /guide/* · /ranking |
| youtube(utm) | 4 | 0 | 0 | / (h-5 2·kospi-1 2) |
| cafe(utm) | 2 | 0 | 0 | /dividend (둘 다 kdiv1121) |
| m.dcinside.com | 2 | 2 | 0 | / |
| theqoo.net | 1 | 1 | 0 | / |
| www.youtube.com(ref) | 1 | 1 | 0 | / |
| pwa·bing | 2 | 0 | 0 | / |

## 카페 utm_campaign 글별
- kdiv1121 2기기(11/22 12:40 m.cafe·15:11 cafe.naver.com) — 그 밖 글 0. /dividend는 계산 이벤트를 안 내는 화면이라 0은 측정 빈칸(11/23 표와 같음).

## 디시·더쿠 3기기는 어느 글에서 왔나
- 디시 11/18 01:57·11/24 00:40, 더쿠 11/22 20:58 — 셋 다 랜딩 '/'·셋 다 완주. **어느 글인지는 확인 안 함**: 사이트가 ref에 호스트만 남기고 경로를 버린다(props.ref='m.dcinside.com'). 우리가 디시·더쿠에 글을 올린 기록도 없음 → 남이 건 링크로 보임(확인 안 함).

## 주의
- youtube utm 4기기 전부 공개 시각 정각(11/22 11:30 h-5 2대·11/24 11:30 kospi-1 2대), 같은 시각 kospi-1 bot 1대 따로 있음 → 우리 공개 확인 회차가 bot 표시 없이 연 것일 수 있음(확인 안 함). 그러면 유튜브 사람 유입은 0~4.
- 원인 판단: 홈 '/' 외부 링크 유입(디시·더쿠·youtube.com) 4/4 완주, 카페(/dividend) 측정 빈칸 — 11/23 결론 그대로.
