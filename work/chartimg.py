# 자료 화면 생성 — 숏폼·블로그에 들어갈 차트. 글자만 있는 화면을 금지하기 위해 만든다(사장님 2026-09-23 "관련 자료가 없으면 아무도 안 본다").
#   py -3.12 work/chartimg.py bar <제목> <출력.png> "이름=값" "이름=값" ... [--unit %] [--hi 3] [--short]
#   py -3.12 work/chartimg.py rank <제목> <출력.png> <json파일> [--key 이름필드] [--val 값필드] [--top 8]
# 규칙(경쟁 화면 실측): 어두운 바탕, 막대는 굵게, 값은 막대 끝에 큰 숫자, 상위 몇 개만 노랑 강조, 출처 한 줄.
import sys, os, re, json
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); FD = os.path.join(HERE, 'fonts')
YELLOW = (255, 214, 10); WHITE = (238, 240, 246); DIM = (150, 154, 166); BG = (14, 15, 20); BAR = (58, 64, 84)

def f_disp(sz):
    p = os.path.join(FD, 'BlackHanSans.ttf')
    return ImageFont.truetype(p, sz) if os.path.exists(p) else ImageFont.truetype(os.path.join(FD, 'pd700.ttf'), sz)

def f_body(sz, bold=False):
    p = os.path.join(FD, 'pd700.ttf' if bold else 'pd500.ttf')
    return ImageFont.truetype(p, sz) if os.path.exists(p) else ImageFont.truetype(r'C:\Windows\Fonts\malgun.ttf', sz)

# 표시용 글꼴(BlackHanSans)에 없는 글자는 **아무 자리도 안 차지하고 조용히 사라진다**.
# 2026-09-24 화면 검증에서 확인: '전용 53.16㎡ 실거래' 가 '전용 53.16  실거래' 로 나왔다.
# 값·제목은 전부 이 글꼴로 그리므로, 없는 글자는 읽을 수 있는 글자로 바꿔 둔다.
DISP_SUB = {'㎡': 'm2', '㎥': 'm3', '²': '2', '³': '3', '℃': 'C', '№': 'No',
            # 2026-09-26 화면 검증에서 또 걸렸다. 제목 '배당률 — 버라이즌과 미국 리츠 11곳'의
            # em대시가 통째로 사라져 '배당률    버라이즌과'로 나왔다.
            # 글꼴에 있는지 폭(textlength)으로는 알 수 없다 — 없는 글자도 .notdef 폭을 돌려준다.
            # 실제로 그려 보고(getbbox) 판정해 아래 표를 만들었다. 중점(·)도 안 그려진다.
            '—': '-', '–': '-', '―': '-', '─': '-', '‐': '-', '‑': '-',
            '…': '...', '·': '.', '±': '+-', '→': '>', '←': '<', '↑': '^', '↓': 'v',
            '≥': '>=', '≤': '<=', '≒': '=', '～': '~', '％': '%', '￦': 'W', '°': '도',
            '※': '*', '★': '*', '☆': '*', '◆': '*', '●': '*', '■': '*', '▲': '^', '▶': '>', '◀': '<'}

# 표에 없는 글자가 또 조용히 사라지는 것을 막는다. 실제로 그려 보고 비어 있으면 알린다.
_MISS_CACHE = {}

def warn_missing(text, font, where=''):
    """표시용 글꼴에 없어 안 그려질 글자를 찾아 알린다(그리지는 않는다)."""
    bad = []
    for ch in set(str(text)):
        if ch.isspace() or ch in _MISS_CACHE and not _MISS_CACHE[ch]:
            continue
        if ch not in _MISS_CACHE:
            im = Image.new('L', (160, 160), 0)
            ImageDraw.Draw(im).text((30, 30), ch, font=font, fill=255)
            _MISS_CACHE[ch] = im.getbbox() is None
        if _MISS_CACHE[ch]:
            bad.append(ch)
    if bad:
        print('경고: 글꼴에 없어 안 그려지는 글자 %s %s — DISP_SUB에 넣어라'
              % (''.join(sorted(bad)), ('(' + where + ')') if where else ''))
    return bad


def disp_safe(t, where=''):
    t = str(t)
    for a, b in DISP_SUB.items(): t = t.replace(a, b)
    try:
        warn_missing(t, f_disp(40), where)      # 치환하고도 남은 글자가 있으면 알린다
    except Exception:
        pass
    return t


def bar_chart(title, pairs, out, unit='', hi=3, short=False, source=''):
    W, H = (1080, 1350) if short else (1280, 720)
    title = disp_safe(title); n = len(pairs); pad = int(W * 0.06)
    im = Image.new('RGB', (W, H), BG); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 8], fill=YELLOW)
    # 제목은 26자에서 무조건 잘랐다 — 출처·조건이 붙은 제목이 "…5,000만원  5.2" 처럼 끊겨 나갔다
    # (2026-09-24 dsr40 숏폼 프레임에서 확인). 이제 폭에 맞게 글자를 줄이고, 그래도 넘칠 때만 줄임표로 자른다.
    tsz = int(W * 0.052)
    while tsz > int(W * 0.030) and dr.textlength(title, font=f_disp(tsz)) > W - pad * 2: tsz -= 2
    ft = f_disp(tsz); t = title
    while len(t) > 4 and dr.textlength(t, font=ft) > W - pad * 2: t = t[:-1]
    dr.text((pad, int(H * 0.045)), t if t == title else t[:-1] + '…', font=ft, fill=WHITE)
    top = int(H * 0.045) + int(ft.size * 1.7); bottom = H - int(H * 0.085)
    rowh = (bottom - top) / max(1, n)
    # 2026-09-24 화면 검증: 두 줄짜리 차트는 rowh 가 화면 절반이 돼 막대 둘이 위아래 끝에 따로 떨어져 보였다
    # (도봉 신동아 고점/현재 비교). 줄 간격에 상한을 두고 남는 자리는 위아래로 나눠 가운데로 모은다.
    cap = (H - top) * 0.22
    if rowh > cap:
        top += (bottom - top - cap * n) / 2
        rowh = cap
    bh = min(int(rowh * 0.62), int(H * 0.11))   # 줄이 두셋뿐이면 rowh 가 커져 막대가 세로 덩어리로 보인다(2026-09-24)
    # 음수가 섞이면 0을 가운데 두고 왼쪽으로 뻗는다. 안 그러면 마이너스 막대가 아예 안 그려진다
    # (2026-09-24 섹터 등락률 차트에서 확인 — 마이너스 섹터가 값만 찍히고 막대가 없었다).
    vs = [v for _, v in pairs]
    neg = min(vs) < 0
    mx = max(abs(v) for v in vs) or 1
    RED = (232, 72, 72)
    # 값 글자와 이름 글자가 들어갈 자리를 먼저 재고, 남는 곳에 막대를 그린다.
    # 2026-09-24 실측 고침: 이름이 길면(예: '마곡 대명투웨니퍼스트') lblw 가 폭을 다 먹어 barw 가 음수가 됐다.
    # 그래서 막대가 사라지고 값이 화면 밖으로 잘려 나갔다 — 자료 화면이 장식이 되던 두 번째 원인이다.
    # 줄 수가 적을수록 rowh 가 커져 글자가 터무니없이 커지는 것도 절대 상한으로 막는다.
    vstrs = [disp_safe(f'{v:,.2f}'.rstrip('0').rstrip('.') + unit) for _, v in pairs]
    vsz = min(int(rowh * 0.5), int(W * 0.075))
    fvm = f_disp(vsz); vw = max(dr.textlength(t, font=fvm) for t in vstrs) + 28
    lbl_room = W - pad * 2 - vw - int(W * 0.22)          # 막대에 최소 22%는 남긴다
    lsz = min(int(rowh * 0.42), int(W * 0.055))
    while lsz > int(W * 0.026) and max(dr.textlength(k, font=f_body(lsz, True)) for k, _ in pairs) > lbl_room:
        lsz -= 2
    keys = []
    for k, _ in pairs:                                    # 그래도 넘치면 줄임표로 자른다
        while len(k) > 3 and dr.textlength(k, font=f_body(lsz, True)) > lbl_room: k = k[:-1]
        keys.append(k if k == pairs[len(keys)][0] else k[:-1] + '…')
    lblw = max(dr.textlength(k, font=f_body(lsz, True)) for k in keys) + 18
    x0 = pad + lblw; barw = max(int(W * 0.18), W - pad - x0 - int(vw))
    zero = x0 + (barw * 0.45 if neg else 0)
    # 0.52 는 0선 위치(0.45)보다 커서, 가장 긴 음수 막대가 0선 왼쪽 x0 를 넘어 이름 글자를 덮었다
    # (2026-09-24 화면 검증 — '도봉'의 '봉'이 막대에 가렸다). 이름 자리를 침범하지 않게 0.42로 줄인다.
    half = barw * 0.42 if neg else barw
    if neg: dr.line([(zero, top - 6), (zero, bottom)], fill=(70, 74, 88), width=2)
    for i, (k, v) in enumerate(pairs):
        y = top + rowh * i
        c = (YELLOW if v >= 0 else RED) if (i < hi or v < 0) else BAR
        fl = f_body(lsz, i < hi)
        dr.text((pad, y + (bh - fl.size) / 2), keys[i], font=fl, fill=WHITE if i < hi else DIM)
        w = max(6, int(half * abs(v) / mx))
        if v >= 0: box = [zero, y, zero + w, y + bh]
        else:      box = [zero - w, y, zero, y + bh]
        dr.rounded_rectangle(box, radius=int(bh * 0.28), fill=c)
        fv = fvm; s = vstrs[i]
        tw = dr.textlength(s, font=fv)
        tx = (zero + w + 14) if v >= 0 else (zero - w - 14 - tw)
        # 막대가 길면 값이 왼쪽 이름과 겹친다(2026-09-24 확인) → 겹치면 막대 안쪽에 적는다.
        # 2026-09-24 화면 검증에서 또 찾음: '막대 안쪽'은 값 글자가 막대보다 짧을 때만 성립한다.
        # 예전에는 길이를 안 보고 무조건 안쪽(배경색 글자)으로 적어서, 막대보다 긴 값은 막대를 넘어
        # 검은 바탕 위에 검은 글씨로 나가 아예 안 보였다 — 구별 하락률 차트에서 강북 -2.8% 가 통째로,
        # 도봉 -11.9% 는 '%'가 사라졌다. 안 들어가면 0선 오른쪽(음수 막대는 그쪽이 비어 있다)에 적는다.
        fits = tw + 24 <= w
        inside = False
        if v < 0 and tx < pad + lblw:
            if fits: inside = True; tx = zero - w + 12
            else: tx = zero + 14
        elif v >= 0 and tx + tw > W - pad:               # 오른쪽으로 삐져나가면 막대 안쪽에 적는다
            if fits: inside = True; tx = max(zero + 12, zero + w - tw - 12)
            else: tx = W - pad - tw
        dr.text((tx, y + (bh - fv.size) / 2 - 2), s, font=fv,
                fill=(14, 15, 20) if inside else (c if c != BAR else WHITE))
    if source: dr.text((pad, H - int(H * 0.062)), source[:60], font=f_body(int(W * 0.024)), fill=DIM)
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True); im.save(out)
    print('차트', out, f'{W}x{H}', f'{n}개 항목')
    return out

if __name__ == '__main__':
    a = sys.argv[1:]; mode = a[0]; title = a[1]; out = a[2]
    short = '--short' in a; unit = ''; hi = 3; src = ''
    for i, x in enumerate(a):
        if x == '--unit': unit = a[i + 1]
        if x == '--hi': hi = int(a[i + 1])
        if x == '--source': src = a[i + 1]
    items = [x for x in a[3:] if '=' in x and not x.startswith('--')]
    pairs = [(x.split('=')[0], float(x.split('=')[1])) for x in items]
    bar_chart(title, pairs, out, unit, hi, short, src)
