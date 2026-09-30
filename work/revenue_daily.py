# -*- coding: utf-8 -*-
"""수익 계측 — 하루 한 줄 (성장 담당, 2026-10-01 신설. 레드팀: "이게 없으면 목표 대비 %도 실험 판정도 공회전")

한 번 실행하면 work/research/growth/revenue.md 에 오늘 날짜 줄을 쓴다(같은 날 다시 돌리면 그 줄을 바꾼다).
  py -3.12 work/revenue_daily.py                         # 입력 파일 + 유튜브 자동 → revenue.md 한 줄
  py -3.12 work/revenue_daily.py --set coupang_clicks=0 coupang_orders=0 coupang_rev=0 coupang_asof=2026-09-30
  py -3.12 work/revenue_daily.py --dry                   # 파일은 안 고치고 줄만 출력

칸마다 어디서 재나(2026-10-01 실측으로 확인한 길):
- 쿠팡 파트너스: 로그인은 사장님 크롬 세션에만 있다(비밀번호 입력 금지). 그래서 회차 담당이 크롬 MCP로
  partners.coupang.com 홈 '기간별 리포트 > 이번 달 집계'(클릭·구매 건수·수익, '최근 업데이트' 날짜)를 읽어 --set 으로 넣는다.
  리포트는 하루 늦게 갱신된다(10/1 07시에 '최근 업데이트 2026.09.30').
- 애드센스: 크롬 adsense.google.com/adsense/u/2/pub-3225798545626010/sites/list 의 firemap.kr 승인 상태.
  u/0 은 다른 계정(pub-6105…, 파이어맵 아님), u/1 은 스꾸 계정이다 — 쓰지 않는다. 승인 전에는 수익 0, 상태만 적는다.
- 카카오 애드핏: 9/30 제휴 제안 등록(초대제). 회신이 오기 전에는 상태만.
- 유튜브: work/ytanalytics.py 토큰(youtube.readonly)으로 구독자 수를 자동으로 읽는다. 구독 1,000 미만이면 YPP 전이라 광고 수익 0.
  수익 금액 자체는 monetary 권한이 없어 못 읽는다(YPP 들어가면 권한 추가 필요).
- 사이트 쿠팡 나감 클릭(firemap_events): Supabase c7cd8a90 MCP로 세어 --set fm_coupang_out=N (이벤트가 배포된 뒤부터).
못 잰 칸은 '확인 안 함'. 입력값이 오늘 것이 아니면 날짜를 붙여 오래된 값임을 드러낸다.
"""
import sys, os, json, re, datetime
sys.stdout.reconfigure(encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
INPUTS = os.path.join(HERE, 'research', 'growth', 'revenue_inputs.json')
OUT = os.path.join(HERE, 'research', 'growth', 'revenue.md')
TARGET_MONTH = 100_000          # 10월 목표 10만원(roadmap.md)
COUPANG_FINAL_APPROVAL = 150_000  # 파트너스 최종 승인 조건: 누적 판매(합산 금액) 15만원

HEADER = """# 수익 일지 — 하루 한 줄 (성장 담당, work/revenue_daily.py가 씀)
형식: 날짜 시각 · 애드센스 · 애드핏 · 쿠팡(이번 달 클릭/구매/합산 금액/수익, 리포트 기준일) · 유튜브 · 이번 달 합계 · 10월 목표 10만원 대비 %
- 금액은 세전, 플랫폼 몫을 뗀 '우리 수익'. 못 잰 칸은 '확인 안 함'.
- 쿠팡 '합산 금액'은 최종 승인 조건(누적 판매 15만원)을 보려고 같이 적는다.

"""

def load_inputs():
    d = json.load(open(INPUTS, encoding='utf-8')) if os.path.exists(INPUTS) else {}
    for a in sys.argv[1:]:
        if '=' in a and not a.startswith('--'):
            k, v = a.split('=', 1)
            d[k] = int(v) if re.fullmatch(r'-?\d+', v) else v
            d[k + '_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    return d

def youtube_subs():
    try:
        sys.path.insert(0, HERE)
        import ytanalytics
        from googleapiclient.discovery import build
        c = ytanalytics.creds()
        if not c: return None, '토큰 없음'
        r = build('youtube', 'v3', credentials=c).channels().list(part='statistics', mine=True).execute()
        return int(r['items'][0]['statistics']['subscriberCount']), None
    except Exception as e:
        return None, type(e).__name__

def stale(d, key, today):
    at = str(d.get(key + '_at', ''))[:10]
    return '' if at == today else (f' ({at} 값)' if at else '')

def won(n): return f'{n:,}원'

def main():
    now = datetime.datetime.now(); today = now.strftime('%Y-%m-%d')
    d = load_inputs()
    total = 0; unknown = []

    # 애드센스
    ads = d.get('adsense_status')
    if ads is None: ads_txt = '확인 안 함'; unknown.append('애드센스')
    elif ads in ('준비됨', '승인'):
        rev = d.get('adsense_rev')
        if isinstance(rev, int): total += rev; ads_txt = f'{won(rev)}(승인)'
        else: ads_txt = '승인·수익 확인 안 함'; unknown.append('애드센스 수익')
    else: ads_txt = f'{ads}·0원'
    ads_txt += stale(d, 'adsense_status', today)

    # 애드핏
    fit = d.get('adfit_status')
    fit_txt = (f'{fit}·0원' + stale(d, 'adfit_status', today)) if fit else '확인 안 함'
    if not fit: unknown.append('애드핏')

    # 쿠팡
    if isinstance(d.get('coupang_rev'), int):
        cr = d['coupang_rev']
        # 리포트가 하루 늦어 1일엔 지난달 집계가 보인다 → 이번 달 합계에 넣지 않는다
        if str(d.get('coupang_asof', ''))[:7] == today[:7]: total += cr
        cp_txt = (f"클릭 {d.get('coupang_clicks', '?')}/구매 {d.get('coupang_orders', '?')}/"
                  f"합산 {won(d.get('coupang_gmv', 0)) if isinstance(d.get('coupang_gmv'), int) else '?'}/수익 {won(cr)}"
                  f", 리포트 {d.get('coupang_asof', '기준일 확인 안 함')}"
                  f"{'' if str(d.get('coupang_asof', ''))[:7] == today[:7] else '(지난달 집계, 합계 제외)'}{stale(d, 'coupang_rev', today)}")
    else: cp_txt = '확인 안 함'; unknown.append('쿠팡')
    if isinstance(d.get('fm_coupang_out'), int): cp_txt += f", 사이트 쿠팡 나감 {d['fm_coupang_out']}"

    # 유튜브
    subs, err = youtube_subs()
    if subs is None: yt_txt = f'확인 안 함({err})'; unknown.append('유튜브')
    elif subs < 1000: yt_txt = f'0원(구독 {subs}, YPP 전)'
    else: yt_txt = f'구독 {subs}, 수익 확인 안 함(monetary 권한 없음)'; unknown.append('유튜브 수익')

    pct = total / TARGET_MONTH * 100
    tail = f' · 못 잰 칸: {", ".join(unknown)}' if unknown else ''
    line = (f"{today} {now:%H:%M} · 애드센스 {ads_txt} · 애드핏 {fit_txt} · 쿠팡 {cp_txt} · 유튜브 {yt_txt}"
            f" · 이번 달 합계 {won(total)} · 목표 대비 {pct:.1f}%{tail}")
    print(line)
    if '--dry' in sys.argv: return

    json.dump(d, open(INPUTS, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    body = open(OUT, encoding='utf-8').read() if os.path.exists(OUT) else HEADER
    lines = [l for l in body.split('\n') if not l.startswith(today + ' ')]
    body = '\n'.join(lines).rstrip('\n') + '\n' + line + '\n'
    open(OUT, 'w', encoding='utf-8').write(body)
    print('기록:', OUT)

if __name__ == '__main__':
    main()
