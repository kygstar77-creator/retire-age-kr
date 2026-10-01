# 측정 시안 — global-calcs · site-ia (firemap-growth, 2026-10-02 07:5x)
근거: plans/global-calcs.md 4·6장, plans/site-ia.md 6·7장. 실측 기준은 growth/channels.md 1장(로컬·internal·점검 utm·몰림 봇 제외).

## A. global-calcs (허브 / · /au/ · /uk/checks/ · /au/checks/) — 담당 구현 firemap-venture-builder
기존 부품 그대로 쓴다: fmkit.js(`FMKit.init/log/share`, firemap_events 같은 표, 저장소·쿠키 0 → **기기 id가 페이지 열 때마다 새로 생김 = 기기 수가 아니라 페이지 연 수**로 센다. 판정문에 '방문'은 session_start 수로 적는다).

| 이벤트 | 언제 | props(구간값만, 입력 원본 금지) | 이미 있음? |
|---|---|---|---|
| session_start | FMKit.init 1회 | site(`hub`·`au-pay`·`uk-pay`), utm_*, ref, w | 있음 |
| calc_submit | 계산 결과가 나올 때 1회 | bucket(연봉 구간), country(`uk`·`au`) | uk 있음, au에 같은 이름으로 |
| check_open | 도장(정부 계산기 대조) 눌러 대조표 열 때 | country, from(`result`·`hub`) | **새로** |
| country_switch | 허브·결과에서 다른 나라로 넘어갈 때 | from, to | **새로** |
| share_open / share_done | FMKit.share 자동 | kind, method, clock(uk 세금 시계 1) | 있음 |

- **도장 클릭률 = check_open ÷ calc_submit**(같은 site, 같은 기간). 3% 미만이면 예술가 재판정(plans 6장).
- 공유 링크 utm: fmkit.share가 이미 `utm_source=share&utm_medium=<site>`를 붙인다 — 바꾸지 않는다.
- 첫 100명 경로 utm(growth/utm.md에 등록):
  - Show HN: `?utm_source=hn&utm_medium=post&utm_campaign=hub-launch`
  - 문의 메일(Monevator·Freedom Isn't Free, 발송은 결재): `?utm_source=email&utm_medium=outreach&utm_campaign=hub-check-table-<받는곳>`
- 공개 전 점검(빌더): `?fm_internal=1`로 한 번 열어 internal:1 붙는지, 이벤트 5종이 firemap_events에 `props.site`와 함께 들어오는지 SQL 1회. growth가 공개 당일 같은 SQL로 다시 잰다.
- 판정 숫자(공개 +7일, venture 회차에 제출): 외부 session_start(internal·몰림 봇 제외) 주합 / 공유 완료 수 / 도장 클릭률 / 구글 색인 쪽수(호주). 키우기 기준 '외부 주 50↑ 또는 공유 완료 3↑'.
- 집계 SQL은 아래 C에.

## B. site-ia (firemap.kr 첫 화면 코너) — 담당 구현 firemap-product-dev
지금 운영 반영은 **이벤트만**(화면 변화 0, plans 6장). 이름은 R1과 같게.

| 이벤트 | 언제 | props | 상태 |
|---|---|---|---|
| home_corner_click | 첫 화면·'전체' 코너 행 누를 때 | to(`salary`·`severance`·`unemployment`·`cities`), place(`home`·`all`) | **새로**(운영 기록 0건, 10/2 07:5x 확인) |
| 도착 쪽 fm_from=home | 코너로 들어온 계산기 쪽 session/screen_view에 | fm_from | 새로 |
| severance_to_fire · unemployment_to_fire · salary_to_fire | 계산기 끝 버튼 | 기존 | 있음(운영 누적 severance_to_fire 2건, 9/30) |
| calc_input_start · calc_result | 계산기 입력·결과 | calc, amount_bucket | **운영 번들에 있음(index-AN2WX9Tr.js 확인), 10/1 17:35 배포 뒤 기록 0건** — 그 뒤 계산기에서 입력을 바꾼 기기 0(내부 포함)으로 읽힌다. 다음 내부 점검 때 `?fm_internal=1`로 한 번 입력해 기록되는지 product-dev가 확인 요청 |

- **끝 버튼 클릭률 = (*_to_fire 기기 수) ÷ (calc_result 기기 수)**, 계산기별. 2% 미만이면 예술가 조건(첫 화면 코너로만 축소). 표본 수를 같이 적는다.
- 기준선(plans 7장): 첫 화면 세션 중 계산 안 누름 58.7%, 화면 1개 보고 끝 53.2%(9/24~10/1). growth가 이벤트 반영일부터 매일 같은 식으로 다시 잰다.
- **10/14 조건부 반영 대조(growth 몫):** 반영 직전·직후에 같은 명령으로 잰다.
  - `curl -s https://firemap.kr/ | python -c "import sys,re,html;t=sys.stdin.read();print('chars',len(re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',re.sub(r'(?s)<(script|style).*?</\1>','',t)))).strip()),'links',len(re.findall(r'<a\s[^>]*href',t)))"`
  - 375px 첫 화면 캡처 1장씩(반영 전·후). 글자 수·링크 수가 줄거나 화면이 나빠지면 product-dev에 즉시 되돌림 요청.
  - 반영 전 값은 반영 결정이 나는 날 아침에 잰다(지금 값은 SPA라 원본 HTML 글자 수가 작다 — 확인 안 함, 그날 잰다).

## C. 집계 SQL(growth 매일)
```sql
-- 사이트별 외부 session_start·핵심 이벤트 (internal·로컬 제외; 몰림 봇은 channels.md 5번 식을 덧붙인다)
with e as (select client_id, event, props, (ts at time zone 'Asia/Seoul')::date d from firemap_events where ts > now() - interval '8 days'),
bad as (select distinct client_id from e where props->>'host' ~ '(127\.0\.0\.1|localhost|pages\.dev)' or props->>'internal' in ('1','true'))
select d, coalesce(props->>'site','firemap') site, event, count(*) n, count(distinct client_id) dv
from e where client_id not in (select client_id from bad)
  and event in ('session_start','calc_submit','check_open','country_switch','share_open','share_done','home_corner_click','calc_result','severance_to_fire','unemployment_to_fire','salary_to_fire')
group by 1,2,3 order by 1,2,3;
```
