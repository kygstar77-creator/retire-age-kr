# 미국 주식 히트맵(수페TV·핀비즈 화면처럼 빨강·초록 네모) — 우리가 직접 그린다. 사장님 2026-09-23.
# 자료: Nasdaq 스크리너(무키, 7,100여 종목: 섹터·시총·등락률). 그림: PIL + squarify(시총 비례 면적, 등락률 색).
#   python work/heatmap.py                    → 시총 상위 110개, 섹터별 묶음 → work/research/_shots/heatmap_<날짜>.png + 요약 출력
#   python work/heatmap.py 60                 → 상위 60개
#   python work/heatmap.py --list NVDA,AAPL,MSFT,...  → 지정 종목만(예: 매그7, 배당주 20)
#   python work/heatmap.py --nobl [개수]      → 배당귀족(NOBL) 비중 상위 종목만. 티커를 손으로 적지 않아도 된다
#   python work/heatmap.py --out <경로.png>
import sys, os, re, json, time, urllib.request, collections
sys.stdout.reconfigure(encoding='utf-8')
import squarify
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); FD = os.path.join(HERE, 'fonts'); OUT = os.path.join(HERE, 'research', '_shots')
H = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) Chrome/126', 'Accept': 'application/json'}
KO = {'Technology': '기술', 'Finance': '금융', 'Health Care': '헬스케어', 'Consumer Discretionary': '경기소비재', 'Consumer Staples': '필수소비재',
      'Industrials': '산업재', 'Energy': '에너지', 'Utilities': '유틸리티', 'Real Estate': '부동산', 'Telecommunications': '통신', 'Basic Materials': '소재', 'Miscellaneous': '기타', '': '기타'}

def font(sz, bold=True):
    p = os.path.join(FD, 'pd700.ttf' if bold else 'pd500.ttf')
    return ImageFont.truetype(p, sz) if os.path.exists(p) else ImageFont.truetype(r'C:\Windows\Fonts\malgunbd.ttf' if bold else r'C:\Windows\Fonts\malgun.ttf', sz)

def fetch():
    d = json.load(urllib.request.urlopen(urllib.request.Request('https://api.nasdaq.com/api/screener/stocks?tableonly=false&limit=3000&offset=0&download=true', headers=H), timeout=90))
    rows = []
    for r in d['data']['rows']:
        try:
            cap = float(r['marketCap'] or 0); pct = float((r['pctchange'] or '0').replace('%', ''))
        except ValueError: continue
        if cap <= 0 or r['symbol'].endswith(('^', '.')) or '^' in r['symbol']: continue
        rows.append({'sym': r['symbol'], 'name': r['name'], 'cap': cap, 'pct': pct, 'sector': r['sector'] or '', 'price': r['lastsale']})
    return rows

def color(p):
    # -3% 이하 진한 빨강 … 0 회색 … +3% 이상 진한 초록 (핀비즈 색 계열)
    t = max(-3.0, min(3.0, p)) / 3.0
    if t >= 0: r, g, b = int(64 + (48 - 64) * t), int(64 + (168 - 64) * t), int(72 + (84 - 72) * t)
    else: t = -t; r, g, b = int(64 + (200 - 64) * t), int(64 + (48 - 64) * t), int(72 + (56 - 72) * t)
    return (r, g, b)

def draw(rows, out, title):
    W, Hh = 1600, 1000; PAD = 6; TOP = 70
    img = Image.new('RGB', (W, Hh), (18, 18, 22)); dr = ImageDraw.Draw(img)
    dr.text((24, 18), title, font=font(30), fill=(240, 240, 240))
    by = collections.defaultdict(list)
    for r in rows: by[r['sector']].append(r)
    sectors = sorted(by.items(), key=lambda kv: -sum(x['cap'] for x in kv[1]))
    sizes = [sum(x['cap'] for x in v) for _, v in sectors]
    rects = squarify.squarify(squarify.normalize_sizes(sizes, W - 2 * PAD, Hh - TOP - PAD), PAD, TOP, W - 2 * PAD, Hh - TOP - PAD)
    for (sec, items), rc in zip(sectors, rects):
        x, y, w, h = rc['x'], rc['y'], rc['dx'], rc['dy']
        dr.rectangle([x, y, x + w, y + h], outline=(70, 70, 78), width=2)
        items.sort(key=lambda r: -r['cap'])
        inner = squarify.squarify(squarify.normalize_sizes([r['cap'] for r in items], w - 4, h - 22), x + 2, y + 20, w - 4, h - 22)
        for r, ir in zip(items, inner):
            ix, iy, iw, ih = ir['x'], ir['y'], ir['dx'], ir['dy']
            dr.rectangle([ix + 1, iy + 1, ix + iw - 1, iy + ih - 1], fill=color(r['pct']), outline=(18, 18, 22), width=1)
            if iw > 44 and ih > 30:
                fs = max(12, min(34, int(min(iw / max(3, len(r['sym'])) * 1.5, ih / 2.6))))
                f1 = font(fs); tw = dr.textlength(r['sym'], font=f1)
                dr.text((ix + (iw - tw) / 2, iy + ih / 2 - fs * 0.95), r['sym'], font=f1, fill=(245, 245, 245))
                if ih > 48:
                    # 칸에 찍을 값 — 부동산 히트맵처럼 색(편차)과 보여 줄 숫자(실제값)가 다를 때 label을 쓴다
                    f2 = font(max(11, int(fs * 0.62)), False); s2 = r.get('label') or f'{r["pct"]:+.2f}%'; tw2 = dr.textlength(s2, font=f2)
                    dr.text((ix + (iw - tw2) / 2, iy + ih / 2 + fs * 0.15), s2, font=f2, fill=(235, 235, 235))
        dr.rectangle([x, y, x + w, y + 18], fill=(40, 40, 46))
        dr.text((x + 6, y + 1), KO.get(sec, sec), font=font(14, False), fill=(220, 220, 220))
    img.save(out); return out

def nobl_holdings(top=25):
    """배당귀족 ETF(NOBL)의 비중 상위 종목. 편성표가 '배당귀족 N종목'이라고만 적어 두어도
    티커를 손으로 옮겨 적지 않도록 여기서 받아 온다. 반환: [(티커, 이름, 비중%)] 비중 내림차순."""
    u = 'https://stockanalysis.com/etf/nobl/holdings/'
    h = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    html = urllib.request.urlopen(urllib.request.Request(u, headers=h), timeout=30).read().decode('utf-8', 'ignore')
    rows = re.findall(r'<a href="/stocks/[a-z\.\-]{1,6}/" >([A-Z\.]{1,6})</a>.{0,120}?<td class="shr[^"]*">([^<]+)</td>.{0,80}?<td class="svelte-[^"]*">([\d\.]+)%</td>', html, re.S)
    if not rows: raise SystemExit('NOBL 보유 목록을 읽지 못했다 — 페이지 구조가 바뀌었는지 확인할 것')
    return [(a, b.replace('&amp;', '&'), float(c)) for a, b, c in rows][:top]

def main():
    args = sys.argv[1:]; n = 110; only = None; out = None
    i = 0
    def need(flag):
        if i + 1 >= len(args): raise SystemExit(f'{flag} 뒤에 값이 필요하다. 예: --list NVDA,AAPL,MSFT / --out out.png')
        return args[i + 1]
    while i < len(args):
        if args[i] == '--list': only = [s.strip().upper() for s in need('--list').split(',')]; i += 2
        elif args[i] == '--nobl':
            top = int(args[i + 1]) if i + 1 < len(args) and args[i + 1].isdigit() else 25
            only = [s for s, _nm, _w in nobl_holdings(top)]
            print(f'NOBL 비중 상위 {len(only)}종목:', ','.join(only))
            i += 2 if (i + 1 < len(args) and args[i + 1].isdigit()) else 1
        elif args[i] == '--out': out = need('--out'); i += 2
        else: n = int(args[i]); i += 1
    rows = fetch()
    asof = time.strftime('%Y-%m-%d')
    if only:
        sel = [r for r in rows if r['sym'] in only]
        miss = [s for s in only if s not in {r['sym'] for r in rows}]
        if miss: print('스크리너에 없는 티커(그림에서 빠짐):', ','.join(miss))
        if not sel: raise SystemExit('지정한 티커가 스크리너에 하나도 없다 — 티커 철자를 확인할 것')
        title = f'미국 주식 {len(sel)}종목 등락 ({asof} 기준, 자료 Nasdaq)'
    else:
        sel = sorted(rows, key=lambda r: -r['cap'])[:n]; title = f'미국 시총 상위 {len(sel)}개 등락 ({asof} 기준, 자료 Nasdaq)'
    os.makedirs(OUT, exist_ok=True); out = out or os.path.join(OUT, f'heatmap_{asof}.png')
    draw(sel, out, title)
    by = collections.defaultdict(list)
    for r in sel: by[r['sector']].append(r)
    print('저장', out)
    print('섹터별(시총가중 등락, 종목수):')
    for sec, items in sorted(by.items(), key=lambda kv: -sum(x['cap'] for x in kv[1])):
        cap = sum(x['cap'] for x in items); wp = sum(x['pct'] * x['cap'] for x in items) / cap
        print(f'  {KO.get(sec, sec):6s} {wp:+.2f}%  {len(items)}개  ' + ' '.join(f"{x['sym']}{x['pct']:+.1f}" for x in sorted(items, key=lambda r: -r['cap'])[:5]))
    up = sorted(sel, key=lambda r: -r['pct'])[:5]; dn = sorted(sel, key=lambda r: r['pct'])[:5]
    print('상승 상위:', ', '.join(f"{r['sym']} {r['pct']:+.2f}%" for r in up)); print('하락 상위:', ', '.join(f"{r['sym']} {r['pct']:+.2f}%" for r in dn))

if __name__ == '__main__': main()
