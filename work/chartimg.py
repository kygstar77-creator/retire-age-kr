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

def bar_chart(title, pairs, out, unit='', hi=3, short=False, source=''):
    W, H = (1080, 1350) if short else (1280, 720)
    n = len(pairs); pad = int(W * 0.06)
    im = Image.new('RGB', (W, H), BG); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 8], fill=YELLOW)
    ft = f_disp(int(W * 0.052)); dr.text((pad, int(H * 0.045)), title[:26], font=ft, fill=WHITE)
    top = int(H * 0.045) + int(ft.size * 1.7); bottom = H - int(H * 0.085)
    rowh = (bottom - top) / max(1, n); bh = int(rowh * 0.62)
    # 음수가 섞이면 0을 가운데 두고 왼쪽으로 뻗는다. 안 그러면 마이너스 막대가 아예 안 그려진다
    # (2026-09-24 섹터 등락률 차트에서 확인 — 마이너스 섹터가 값만 찍히고 막대가 없었다).
    vs = [v for _, v in pairs]
    neg = min(vs) < 0
    mx = max(abs(v) for v in vs) or 1
    RED = (232, 72, 72)
    lblw = max(dr.textlength(k, font=f_body(int(rowh * 0.42), True)) for k, _ in pairs) + 18
    x0 = pad + lblw; barw = W - pad - x0 - int(W * 0.13)
    zero = x0 + (barw * 0.45 if neg else 0)
    half = barw * 0.52 if neg else barw
    if neg: dr.line([(zero, top - 6), (zero, bottom)], fill=(70, 74, 88), width=2)
    for i, (k, v) in enumerate(pairs):
        y = top + rowh * i
        c = (YELLOW if v >= 0 else RED) if (i < hi or v < 0) else BAR
        fl = f_body(int(rowh * 0.42), i < hi)
        dr.text((pad, y + (bh - fl.size) / 2), k, font=fl, fill=WHITE if i < hi else DIM)
        w = max(6, int(half * abs(v) / mx))
        if v >= 0: box = [zero, y, zero + w, y + bh]
        else:      box = [zero - w, y, zero, y + bh]
        dr.rounded_rectangle(box, radius=int(bh * 0.28), fill=c)
        fv = f_disp(int(rowh * 0.5)); s = f'{v:,.2f}'.rstrip('0').rstrip('.') + unit
        tw = dr.textlength(s, font=fv)
        tx = (zero + w + 14) if v >= 0 else (zero - w - 14 - tw)
        # 막대가 길면 값이 왼쪽 이름과 겹친다(2026-09-24 확인) → 겹치면 막대 안쪽에 적는다
        inside = v < 0 and tx < pad + lblw
        if inside: tx = zero - w + 12
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
