# utm 규칙 — 채널에서 firemap.kr로 오는 링크 (2026-09-30 성장 담당)

모든 직원은 firemap.kr로 가는 링크를 만들 때 이 규칙만 쓴다. 규칙 밖 이름을 새로 만들지 않는다(집계가 쪼개진다).

## 형식
`https://firemap.kr/<경로>?utm_source=<채널>&utm_medium=<자리>&utm_campaign=<글·영상 id>`
- 모두 영문 소문자, 공백 대신 `-`. 한글 금지(인코딩되면 집계가 깨진다).
- 경로는 관련 계산기 1곳. 한 글·영상에 firemap.kr 링크는 **1개**(네이버 저품질 신호 회피, 같은 링크를 모든 글에 반복하지 않는다).

## utm_source (채널)
| 값 | 채널 |
|---|---|
| youtube | 유튜브 롱폼·채널 프로필 |
| shorts | 유튜브 쇼츠(롱폼과 나눠 잰다) |
| cafe | cafe.naver.com/firemap |
| blog | blog.naver.com/kygstar7777 |
| openchat | 카카오 오픈채팅 공지·봇 답변(링크 뿌리기 금지, 공지·질문 답변 자리만) |
| clip | 네이버 클립(보류 중, 쓸 때만) |
| share | 계산기 결과 공유(R6, 카카오 공유·링크 복사로 받은 사람이 연 링크). 사이트가 자동으로 붙인다 — 직원이 손으로 쓰지 않는다 (2026-10-01 등록) |

## utm_medium (자리)
| 값 | 자리 |
|---|---|
| profile | 채널 프로필·카페 대문·블로그 프로필 링크 |
| desc | 영상 설명란 첫 부분 |
| comment | 고정 댓글 |
| post | 글 본문 안 링크 |
| notice | 공지·대문 글 |
| kakao | (share 전용) 카카오톡 공유 버튼 |
| copy | (share 전용) 링크 복사 |

## utm_campaign (글·영상 id)
- 유튜브: 영상 id(11자). 업로드 전이면 작업 폴더 이름(예 `acn0930`), 업로드 뒤 영상 id로 바꾸지 않는다(처음 쓴 값 유지).
- 카페·블로그: 작업 폴더 이름(work/research/<폴더>). 발행 뒤 글 번호가 아니다.
- 프로필처럼 한 번 박아 두는 자리는 `profile`.
- share: 계산기 이름(`salary`·`severance`·`unemployment-benefit`). 이벤트 `calc_share`와 짝을 맞춘다.

## 예
- 롱폼 설명란: `https://firemap.kr/?utm_source=youtube&utm_medium=desc&utm_campaign=acn0930`
- 채널 프로필: `https://firemap.kr/?utm_source=youtube&utm_medium=profile&utm_campaign=profile`
- 카페 글: `https://firemap.kr/?utm_source=cafe&utm_medium=post&utm_campaign=apgu0930`
- 결과 공유: `https://firemap.kr/calc/severance?utm_source=share&utm_medium=kakao&utm_campaign=severance`

## 어디서 재나
- GA4(G-SYD7WCD35C)는 utm을 자동으로 받는다. 단 **성장 담당이 GA4를 읽을 권한이 아직 없다**(결재함 2026-09-30 참고).
- firemap_events(Supabase)의 session_start에는 지금 utm·referrer가 **안 남는다**(2026-09-30 확인: props가 `{}`, 14일간 utm/ref 포함 0건). 제품 개발 담당에게 첫 방문 utm·referrer 기록을 요청했다(today.md). 들어가기 전까지 채널별 칸은 '확인 안 함'.

- **(2026-10-01 16:46 갱신)** session_start props에 utm_source·utm_medium이 **이제 남는다**(9/29~10/1 실측: youtube profile 4·desc 3·comment 3, 그 밖 pwa·prodcheck·test·u2check는 내부 값). 위 '안 남는다'는 9/30 기준 기록이다. 점검용 utm(prodcheck·test·u2check 등)은 집계에서 뺀다 — 점검할 땐 utm 대신 ?fm_internal=1을 쓴다.

## 2026-10-02 추가 (firemap-growth 07:5x)
- B10 카페: `https://firemap.kr/?utm_source=cafe&utm_medium=post&utm_campaign=b10` · B10 쇼츠: `?utm_source=shorts&utm_medium=desc&utm_campaign=b10` (plans/sonpum.md의 yt_shorts를 shorts로 맞춤). 판정 10/9: utm_campaign=b10 외부 session_start 수.
- global-calcs: Show HN `?utm_source=hn&utm_medium=post&utm_campaign=hub-launch` · 문의 메일 `?utm_source=email&utm_medium=outreach&utm_campaign=hub-check-table-<받는곳>` · 공유는 fmkit이 자동 `utm_source=share&utm_medium=<site>`. 자세한 건 growth/measure-1002.md.
