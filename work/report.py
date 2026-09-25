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
    # 같은 글이 여러 회차 기록에 들어간다 — 발행한 회차와 그것을 확인한 회차가 둘 다 적는다.
    # 2026-09-25: law1001 하나가 10시·11시 기록에 겹쳐 블로그가 4편으로 나왔다(실제 3편,
    # verify today와 RSS로 확인). 편수는 회차가 아니라 서로 다른 주소를 센다.
    nb = len({(r.get('blog') or {}).get('url') for r in runs if (r.get('blog') or {}).get('url')})
    nc = len({(r.get('cafe') or {}).get('url') for r in runs if (r.get('cafe') or {}).get('url')})
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
        # 어제와 오늘을 잰 시각이 다르면 '오늘 방문'끼리 견주는 것이 뜻이 없다.
        # 2026-09-24는 19:58에, 9/25는 12:39에 쟀는데 보고에는 '-35명'만 나갔다(2026-09-25).
        at_now, at_prev = vis[vd[-1]].get('at'), (vis[vd[-2]].get('at') if len(vd) > 1 else None)
        same_hour = at_now and at_prev and at_now[:2] == at_prev[:2]
        line = f'방문  {today_v}명'
        if prev_v is not None and same_hour: line += delta(today_v, prev_v, '명')
        elif prev_v is not None:
            line += f' (어제 {prev_v}명 — 잰 시각이 달라 그대로 비교하지 않는다: 어제 {at_prev} · 오늘 {at_now})'
        out.append(line)

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
    # 표가 두 가지 모양이다: 상태칸이 맨 뒤인 줄(| 무엇 | 왜 | 절차 | 대기 |)과
    # 맨 앞인 줄(| 대기 | 무엇 ... |). 앞엣것만 세던 탓에 무엇이 대기인지 한 번도 안 보였다.
    waiting = []
    for ln in tw.splitlines():
        if '| 대기 |' not in ln: continue
        cells = [c.strip() for c in ln.strip().strip('|').split('|')]
        name = cells[1] if cells and cells[0] == '대기' else (cells[0] if cells else '')
        name = re.sub(r'\*\*|\(.*?\)', '', name).split('—')[0].strip()
        if name and name != '대기': waiting.append(name[:26])
    if waiting:
        out.append('')
        out.append(f'계속 대기 {len(waiting)}건 — 사장님 손이 필요합니다')
        for w in waiting[:6]: out.append(f'· {w}')

    out += ['', '오늘 고친 것', '· (회차가 채운다)', '', '손봐 주실 것', '· (없으면 이 두 줄을 지운다)', '', BOARD]
    print('\n'.join(out))

if __name__ == '__main__': main()
