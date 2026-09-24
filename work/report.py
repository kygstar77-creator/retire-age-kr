# 보고문 — 숫자 부분을 코드가 찍는다.
#   py -3.12 work/report.py            → 화면에 보고문
#   py -3.12 work/report.py > out.txt  → 파일로
#
# 사장님 2026-09-24: "보고를 저렇게 하면 너무 줄글이 많아서 안 보고 싶어져."
# 그날 보고가 44줄 6,662자였고 그중 28줄이 글 제목·링크 나열이었다. 글 목록은 현황판에 있으니 뺀다.
# 매일 똑같이 반복되던 '확인 필요'(유튜브 공개·브이월드 권한 같은 것)도 한 줄로 묶는다.
#
# 회차(클로드)는 여기에 두 가지만 덧붙인다: 오늘 고친 것, 오늘 새로 생긴 확인 필요.
# 숫자를 사람이 옮겨 적지 않는다 — 옮기다 틀리면 사장님이 틀린 숫자를 보게 된다.
import sys, os, re, json, glob, time, statistics, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, 'research')
UA = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://cafe.naver.com/'}
BOARD = 'https://claude.ai/artifact/Xk9jFKPQiKzLTnfDo7wDAg'

def load(p, d=None):
    try: return json.load(open(p, encoding='utf-8'))
    except Exception: return d

def pct(a, b): return f'{round(a / b * 100)}%' if b else '—'

def delta(now, before, unit=''):
    """어제 대비. 같으면 아무것도 안 붙인다 — 변화 없는 줄에 괄호가 붙으면 읽을 게 늘기만 한다."""
    if before is None or now is None or now == before: return ''
    d = now - before
    return f' ({"+" if d > 0 else ""}{round(d, 1)}{unit})'

def cafe_reads(n=30):
    try:
        u = ('https://apis.naver.com/cafe-web/cafe2/ArticleListV2dot1.json?search.clubid=31789001'
             '&search.queryType=lastArticle&search.page=1&search.perPage=50')
        arts = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=20))['message']['result']['articleList']
        rs = [a.get('readCount', 0) for a in arts[:n]]
        return (statistics.median(rs), max(rs)) if rs else (None, None)
    except Exception: return None, None

def main():
    out = [f'[파이어맵 {time.strftime("%-m/%-d") if os.name != "nt" else time.strftime("%#m/%#d")}]']

    # 발행
    runs = (load(os.path.join(HERE, 'runs_today.json'), {'runs': []}) or {}).get('runs', [])
    nb = sum(1 for r in runs if (r.get('blog') or {}).get('url'))
    nc = sum(1 for r in runs if (r.get('cafe') or {}).get('url'))
    out.append(f'발행  블로그 {nb}/24 · 카페 {nc}/24')

    # 색인 — 하루 지난 글 기준. 당일 글은 색인될 시간이 없어 언제나 낮다.
    perf = load(os.path.join(HERE, 'perf_log.json'), {}) or {}
    days = sorted(perf)
    if days:
        last = perf[days[-1]]
        mt = last.get('mature')
        if not mt:                                   # 아직 안 쌓였으면 recheck에서 직접 센다
            rc = last.get('recheck') or []
            able = sum(1 for x in rc if x.get('indexed') is not None)
            got = sum(1 for x in rc if x.get('indexed'))
            mt = {'n': able, 'indexed': got, 'rate': got / able} if able else None
        if mt:
            out.append(f'색인  {pct(mt["indexed"], mt["n"])} (하루 지난 글 {mt["n"]}편 중 {mt["indexed"]}편)')
        else:
            out.append('색인  확인 불가 — 하루 지난 글을 다시 잰 기록이 없다')

    # 방문
    vis = load(os.path.join(HERE, 'visitors_log.json'), {}) or {}
    vd = sorted(vis)
    if vd:
        today_v = vis[vd[-1]].get('today')
        prev_v = vis[vd[-2]].get('today') if len(vd) > 1 else None
        out.append(f'방문  {today_v}명{delta(today_v, prev_v, "명")}')

    med, mx = cafe_reads()
    if med is not None: out.append(f'카페  조회 중앙 {med:.0f}회 · 최고 {mx}회')

    # 대기 묶음 — 0이면 다음 회차가 쓸 재료가 없다는 뜻이라 눈에 띄어야 한다
    pend = ''
    try:
        import subprocess
        pend = subprocess.run([sys.executable, os.path.join(HERE, 'naverpost.py'), 'pending'],
                              capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=300).stdout or ''
    except Exception: pass
    pb = len(re.findall(r'"kind": "blog"', pend)); pc = len(re.findall(r'"kind": "cafe"', pend))
    if pb < 3 or pc < 3: out.append(f'대기  블로그 {pb} · 카페 {pc}  ← 3편씩은 있어야 한다')

    # 계기판에서 지금 가장 나쁜 것 세 개만
    h = load(os.path.join(HERE, 'health.json'), {}) or {}
    bad = [i for i in (h.get('items') or []) if i.get('score', 0) >= 1][:3]
    if bad:
        out.append('')
        out.append('가장 벌어진 것')
        for i in bad: out.append(f'· {i["name"]} {i["value"]} (목표 {i["target"]})')

    # 매일 똑같이 반복되는 '확인 필요'는 한 줄로 묶는다
    tw = ''
    twp = os.path.join(R, 'tools-wanted.md')
    if os.path.exists(twp): tw = open(twp, encoding='utf-8').read()
    waiting = re.findall(r'^\|\s*([^|]{2,40}?)\s*\|[^|]*\|\s*대기\s*\|', tw, re.M)
    if waiting:
        out.append('')
        out.append(f'계속 대기 {len(waiting)}건: ' + ', '.join(w.strip() for w in waiting[:6]))

    out += ['', '오늘 고친 것', '· (회차가 채운다)', '', '손봐 주실 것', '· (없으면 이 두 줄을 지운다)', '', BOARD]
    print('\n'.join(out))

if __name__ == '__main__': main()
