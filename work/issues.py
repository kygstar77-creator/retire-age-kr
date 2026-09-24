# 오늘 터진 이슈를 찾는다 — 예정된 일정 말고, 지금 사람들이 보고 있는 것.
#   py -3.12 work/issues.py            → work/research/issues.md (우리 축에 걸리는 것만)
#
# 사장님 2026-09-24: "이슈가 되고 사람들이 클릭할 만한 내용으로 우리가 기획한 시리즈든
#                    글 카테고리 분야에서 잘 찾아서 잘 기획해서 쓰고 있는 거야?"
#
# 그때까지 이슈를 찾는 경로는 세 가지였다.
#   calendar.json  — 마감·실적·지표. **예정된 것**이다.
#   topics.json    — 월 검색수. 평소 수요라 오늘 일은 안 보인다.
#   topic-ideas.md — 유튜브 키워드 추세. 그마저 전날 21시가 마지막이었다(20시간 묵음).
# 오늘 갑자기 터진 일을 보는 자는 없었다. 그래서 이슈 글을 쓸 수가 없었다.
#
# 무키로 되는 것만 쓴다(2026-09-24 실측): 구글 트렌드 KR RSS · 연합뉴스 경제 · 한국경제.
# 매경은 403이라 안 쓴다.
import sys, os, re, json, time, html, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, 'research')
OUT = os.path.join(R, 'issues.md'); LOG = os.path.join(HERE, 'issues_log.json')
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36'}

SRC = [('구글 트렌드 KR', 'https://trends.google.com/trending/rss?geo=KR'),
       ('연합 경제', 'https://www.yna.co.kr/rss/economy.xml'),
       ('한국경제', 'https://www.hankyung.com/feed/economy')]

# 우리 네 축. 이 말이 걸리는 것만 남긴다 — 연예·스포츠 이슈는 우리 글감이 아니다.
AXES = {
    '부동산': r'부동산|아파트|집값|전세|월세|분양|청약|재건축|재개발|주담대|LTV|DSR|임대|오피스텔|전셋값',
    '세금·연금': r'세금|세액|공제|연말정산|종부세|양도세|취득세|상속|증여|건강보험|국민연금|퇴직연금|연금저축|IRP|ISA',
    '주식·ETF': r'코스피|코스닥|나스닥|S&P|증시|주가|상장|실적|배당|ETF|반도체|삼성전자|공모주|외국인|기관',
    '금리·환율': r'금리|환율|원달러|기준금리|한국은행|연준|FOMC|물가|CPI|인플레|국채',
}

def fetch(u):
    try:
        raw = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=20).read()
    except Exception as e:
        print('가져오기 실패', u[:40], repr(e)[:50]); return []
    for enc in ('utf-8', 'euc-kr'):
        try: s = raw.decode(enc); break
        except Exception: s = raw.decode('utf-8', 'ignore')
    out = []
    for it in re.findall(r'<item>(.*?)</item>', s, re.S):
        m = re.search(r'<title>\s*(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?\s*</title>', it, re.S)
        if not m: continue
        t = html.unescape(re.sub('<[^>]+>', '', m.group(1))).strip()
        l = re.search(r'<link>\s*(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?\s*</link>', it, re.S)
        if t: out.append((t, (l.group(1).strip() if l else '')))
    return out

def axis_of(t):
    for name, pat in AXES.items():
        if re.search(pat, t, re.I): return name
    return None

def main():
    seen = set()
    try: seen = set(json.load(open(LOG, encoding='utf-8')).get('titles', []))
    except Exception: pass

    rows, fresh = [], 0
    for name, u in SRC:
        for t, link in fetch(u)[:60]:
            ax = axis_of(t)
            if not ax: continue
            key = re.sub(r'[\s\W]+', '', t)[:40]
            rows.append({'src': name, 'axis': ax, 'title': t, 'link': link, 'new': key not in seen})
            if key not in seen: fresh += 1
            seen.add(key)
        time.sleep(0.3)

    json.dump({'at': time.strftime('%Y-%m-%d %H:%M'), 'titles': sorted(seen)[-2000:]},
              open(LOG, 'w', encoding='utf-8'), ensure_ascii=False)

    byax = {}
    for r in rows: byax.setdefault(r['axis'], []).append(r)
    lines = ['# 오늘 이슈 (issues.py 자동 수집 — 우리 네 축에 걸리는 것만)', '',
             f'수집 {time.strftime("%Y-%m-%d %H:%M")} · 걸린 것 {len(rows)}건(처음 보는 것 {fresh}건)', '',
             '예정된 일정(calendar.json)이 아니라 **오늘 나온 것**이다.',
             '회차는 편성표 슬롯을 지키되, 그 슬롯 주제와 여기 이슈가 맞물리면 그 각도로 쓴다.',
             '제목을 베끼지 않는다 — 무슨 일이 있었는지만 보고 1차 출처로 다시 확인한다.', '']
    for ax in AXES:
        rs = byax.get(ax) or []
        if not rs: continue
        lines += [f'## {ax} ({len(rs)}건)', '']
        for r in rs[:8]:
            mark = '**새** ' if r['new'] else ''
            lines.append(f"- {mark}{r['title'][:70]} — {r['src']}" + (f" {r['link']}" if r['link'] else ''))
        lines.append('')
    os.makedirs(R, exist_ok=True); open(OUT, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print(f'[이슈 {time.strftime("%H:%M")}] {len(rows)}건 · 처음 보는 것 {fresh}건')
    for ax in AXES:
        rs = byax.get(ax) or []
        if rs: print(f'  {ax} {len(rs)}건 · ' + rs[0]['title'][:46])
    print(' 저장', OUT)

if __name__ == '__main__': main()
