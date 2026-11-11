# 사이트 유입 출처 11/1~11/10 (firemap_events session_start, 11/11 20:3x 측정)
표본: session_start 205건(KST 11/1 00:00~11/11 00:00). 칸: props.utm_source·props.ref(referrer)·props.bot.

| 출처 | 세션 | 기기(client_id) |
|---|---|---|
| ref 없음(직접·앱 내 브라우저·북마크) | 113 | 80 |
| 봇(bot 칸) | 70 | 69 |
| 검색(ref 네이버·구글·다음) | 7 | 7 |
| 카페(utm cafe) | 4 | 4 |
| 디시(m.dcinside.com) | 4 | 4 |
| PWA(utm pwa) | 3 | 3 |
| 토스(viva.republica.toss) | 2 | 1 |
| ChatGPT(utm) | 1 | 1 |
| 더쿠 | 1 | 1 |
| 유튜브(utm·ref 둘 다) | 0 | 0 |

- 카페·유튜브·검색으로 나누면: 카페 4 · 유튜브 0 · 검색 7. 사람 세션 135건 중 83.7%(113)는 출처를 모른다.
- K-1(H9Lv281MaLs, 11/10 11:30 공개) 뒤 24시간+ utm youtube 세션 **0**(11/10 11:30~11/11 20:3x 전체 utm 이벤트는 pwa 1건뿐).
- 확인 안 함: ref 없음 113건의 실제 출처. 재는 방법: 카페 앱·유튜브 앱 내 브라우저는 referrer를 안 넘기므로, 카페 글·유튜브 설명란·고정 댓글 링크에 전부 utm_source를 달았는지부터 확인(유튜브 설명란 링크 utm 유무는 이번 회차에 안 봄).
