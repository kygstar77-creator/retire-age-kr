# 글자 카드 쇼츠(5~7초) — 2026-09-28 사장님 "쇼츠 제대로 못 만들었잖아 … 제대로 조사해서 올려"
#   py -3.12 work/cardshort.py <spec.json> [출력.mp4]
#
# 왜 이 틀인가(vidIQ 실측 2026-09-28, work/research/shorts-research.md):
#   - '어른의금융수업'(구독 1.2만) 최근 쇼츠 50편 전부 5~7초 글자 카드, 편당 1,500~9만 회.
#     재테크 주제 "500만원씩 쪼개서 넣었는데, 국세청이 다 안다고요?" 7.9만 회.
#     목소리 없음 · 카드 한 장(큰 제목 + 번호 3개 + 숫자 비교 상자) · 아래는 움직이는 화면 · 배경음악.
#     짧은 시간에 글이 많아 멈추거나 다시 보게 된다(시청 지속률이 100%를 넘는다).
#   - 우리가 전에 만든 쇼츠(shorts.py, 45초 목소리)는 거의 멈춘 카드 여러 장에 작은 차트라 휴대폰에서 안 읽혔다.
# 우리 규칙: 숫자는 facts에 있는 것만, '사라·사지 마라' 없음, 겁주는 제목 없음(질문 + 숫자).
import sys, os, json, math, subprocess, wave, struct, random
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg
HERE = os.path.dirname(os.path.abspath(__file__)); FD = os.path.join(HERE, 'fonts'); FF = imageio_ffmpeg.get_ffmpeg_exe()
W, H, FPS = 1080, 1920, 30
BG = (16, 18, 24); WHITE = (246, 246, 250); YELLOW = (255, 208, 0); GREY = (150, 156, 170)
BLUE = (120, 190, 255); GREEN = (140, 225, 120)

def font(name, size): return ImageFont.truetype(os.path.join(FD, name), size)
BHS = lambda s: font('BlackHanSans.ttf', s)      # 제목 — 가운뎃점(·)이 없다
NOTO = lambda s: font('NotoSansKR-Black.ttf', s)
PD7 = lambda s: font('pd700.ttf', s); PD5 = lambda s: font('pd500.ttf', s)

def runs(text):
    """'{…}' 안은 노란 강조. [(글자, 색)] 로 편다."""
    out, hi = [], False
    for ch in text:
        if ch == '{': hi = True; continue
        if ch == '}': hi = False; continue
        out.append((ch, YELLOW if hi else WHITE))
    return out

def wrap_runs(d, rs, f, maxw):
    """강조 색을 유지한 채 줄바꿈 — 띄어쓰기에서 끊는다."""
    lines, cur = [], []
    for c in rs:
        cur.append(c)
        if d.textlength(''.join(x for x, _ in cur), font=f) > maxw:
            txt = ''.join(x for x, _ in cur); cut = txt.rfind(' ')
            if cut > 0: lines.append(cur[:cut]); cur = cur[cut + 1:]
            else: lines.append(cur[:-1]); cur = cur[-1:]
    if cur: lines.append(cur)
    return lines

def draw_runs(d, x, y, line, f):
    for ch, col in line:
        d.text((x, y), ch, font=f, fill=col); x += d.textlength(ch, font=f)

# 유튜브 쇼츠 화면은 위 약 140px(검색·메뉴), 아래 약 380px(제목·채널·음원), 오른쪽 약 150px(좋아요·댓글 버튼)을 가린다.
# 읽혀야 할 것은 전부 x 64~930, y 150~1540 안에 넣는다(2026-09-28 첫 시안에서 막대·카페 주소가 가려질 자리에 있었다).
SAFE_R, SAFE_B = 930, 1540

def card(spec):
    """정지 카드. 막대 자리(bars_top)를 돌려준다."""
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im); M = 64; y = 150
    d.rounded_rectangle((M, y, M + 190, y + 58), 12, fill=(255, 107, 0)); d.text((M + 22, y + 8), '파이어맵', font=PD7(36), fill=WHITE)
    chip = spec['chip']; cw = d.textlength(chip, font=PD7(32)) + 40
    d.rounded_rectangle((M + 210, y, M + 210 + cw, y + 58), 12, fill=YELLOW); d.text((M + 230, y + 10), chip, font=PD7(32), fill=BG)
    y += 96
    for ln in spec['title']:
        d.text((M, y), ln, font=BHS(100), fill=WHITE); y += 116
    for ln in spec.get('sub', []):
        d.text((M, y + 4), ln, font=PD7(56), fill=YELLOW); y += 80
    y += 26
    for i, p in enumerate(spec['points'], 1):
        d.text((M, y - 2), str(i), font=BHS(58), fill=YELLOW)
        for ln in wrap_runs(d, runs(p), PD7(44), SAFE_R - M - 62):
            draw_runs(d, M + 62, y + 4, ln, PD7(44)); y += 60
        y += 18
    return im, y + 20

def rank_frame(base, spec, top, t):
    """순위 줄: 이름 왼쪽, 숫자 오른쪽 크게. 줄이 0.15초 간격으로 차례로 나타난다."""
    im = base.copy(); d = ImageDraw.Draw(im); M = 64; y = top
    for k, (label, v, unit) in enumerate(spec['bars'][:5]):
        if t < 0.15 * k: break
        col = YELLOW if k == 0 else WHITE
        d.rounded_rectangle((M, y, SAFE_R, y + 92), 16, fill=(30, 33, 42))
        d.text((M + 22, y + 22), label, font=PD7(40), fill=col)
        val = f'{v:,}{unit}'  # 사실표에 적힌 자릿수 그대로(4.29를 4.3으로 반올림하지 않는다)
        d.text((SAFE_R - 22 - d.textlength(val, font=BHS(52)), y + 16), val, font=BHS(52), fill=col)
        y += 108
    y = top + 108 * min(5, len(spec['bars'])) + 6
    for ln in wrap_runs(d, [(c, GREY) for c in spec['source']], PD5(27), SAFE_R - M):
        draw_runs(d, M, y, ln, PD5(27)); y += 38
    # 쇼츠 화면의 카페 주소는 뺀다(쇼츠 설명란 링크도 안 눌린다 — yt-policy-algorithm.md, 2026-09-30)
    d.text((M, y + 14), spec.get('foot', '파이어맵'), font=PD7(34), fill=(255, 150, 70))
    return im, y + 60

def bars_frame(base, spec, top, t):
    """비교 막대. 0.9초 동안 자라고 머문다 — 영상이 반복될 때마다 다시 자란다."""
    im = base.copy(); d = ImageDraw.Draw(im); M = 64
    items = spec['bars']; mx = max(v for _, v, _ in items)
    g = min(1.0, t / 0.9); g = 1 - (1 - g) ** 3
    y = top
    for k, (label, v, unit) in enumerate(items):
        d.text((M, y), label, font=PD7(38), fill=WHITE if k == 0 else GREY)
        bw = int((SAFE_R - M - 250) * v / mx * g); col = YELLOW if k == 0 else (110, 116, 130)
        d.rounded_rectangle((M, y + 54, M + max(bw, 8), y + 108), 12, fill=col)
        d.text((M + bw + 16, y + 50), (f'{v:,}{unit}' if g >= 1 else f'{v * g:,.1f}{unit}'), font=BHS(54), fill=YELLOW if k == 0 else GREY)
        y += 136
    y += 6
    for ln in wrap_runs(d, [(c, GREY) for c in spec['source']], PD5(27), SAFE_R - M):
        draw_runs(d, M, y, ln, PD5(27)); y += 38
    # 쇼츠 화면의 카페 주소는 뺀다(쇼츠 설명란 링크도 안 눌린다 — yt-policy-algorithm.md, 2026-09-30)
    d.text((M, y + 14), spec.get('foot', '파이어맵'), font=PD7(34), fill=(255, 150, 70))
    return im, y + 60

def music(path, sec, seed=''):
    """배경음악을 직접 만든다(저작권 문제 없게). 부드러운 코드 + 뜯는 소리 반복, 작게.
    2026-09-30: 예전엔 모든 쇼츠가 같은 Cmaj7·Am7 96bpm이라 음원이 똑같았다. 유튜브 스팸 정책 예시 원문
    "Channels that use the exact same background music ... across many videos"(research/longform/yt-policy-algorithm.md)에
    그대로 걸린다 → 영상마다 seed(제목)로 조·코드 진행·빠르기·아르페지오 모양을 바꾼다."""
    import hashlib
    h = int(hashlib.md5(seed.encode('utf-8')).hexdigest(), 16)
    sr = 44100; n = int(sr * sec); buf = [0.0] * n
    bpm = 78 + h % 37; beat = 60 / bpm                                   # 78~114bpm
    key = 2 ** (((h >> 8) % 12 - 5) / 12)                               # 조 옮김(반음 -5~+6)
    progs = [[(0, 4, 7, 11), (-3, 0, 4, 7)], [(0, 4, 7, 11), (5, 9, 12, 16), (-3, 0, 4, 7), (7, 11, 14, 17)],
             [(-3, 0, 4, 7), (5, 9, 12, 16), (0, 4, 7, 11), (7, 11, 14, 17)], [(2, 5, 9, 12), (7, 11, 14, 17), (0, 4, 7, 11)],
             [(0, 3, 7, 10), (5, 8, 12, 15), (-2, 2, 5, 9)], [(0, 4, 7, 9), (-5, -1, 2, 5), (-3, 0, 4, 7), (5, 9, 12, 14)]]
    prog = progs[(h >> 16) % len(progs)]
    chords = [[261.63 * key * 2 ** (s / 12) for s in c] for c in prog]
    pat = [(0, 1, 2, 3), (0, 2, 1, 3), (3, 2, 1, 0), (0, 2, 3, 1)][(h >> 24) % 4]
    for i in range(n):
        tt = i / sr; ch = chords[int(tt / (beat * 4)) % len(chords)]
        pad = sum(math.sin(2 * math.pi * f * tt) + 0.5 * math.sin(2 * math.pi * f * 1.003 * tt) for f in ch) / 12
        buf[i] += pad * 0.35
    for b in range(int(sec / (beat / 2))):          # 8분음표 아르페지오
        t0 = b * beat / 2; ch = chords[int(t0 / (beat * 4)) % len(chords)]; f = ch[pat[b % 4]] * 2
        s0 = int(t0 * sr)
        for j in range(int(sr * 0.35)):
            if s0 + j >= n: break
            e = math.exp(-j / (sr * 0.09))
            buf[s0 + j] += 0.22 * e * (math.sin(2 * math.pi * f * j / sr) + 0.3 * math.sin(4 * math.pi * f * j / sr))
    fade = int(sr * 0.25)
    for i in range(fade): buf[i] *= i / fade; buf[n - 1 - i] *= i / fade
    peak = max(abs(x) for x in buf) or 1
    with wave.open(path, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(b''.join(struct.pack('<h', int(x / peak * 0.5 * 32767)) for x in buf))

def cover_frame(spec):
    """표지 전용 첫 화면(2026-10-02 firemap-shorts): 카드 한 장이 표지를 겸하면 168px 목록에서 읽히지 않는다(a1_need100 1초 시험 4.2).
    spec "cover": ["줄1", "{강조}줄2", ...] 2~4줄, 큰 글자만. 기본 꺼짐 — "cover"가 없으면 예전과 같다."""
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im); M = 64
    d.rounded_rectangle((M, 150, M + 190, 208), 12, fill=(255, 107, 0)); d.text((M + 22, 158), '파이어맵', font=PD7(36), fill=WHITE)
    if spec.get('cover_chart'): return cover_chart_frame(spec, im, d, M)
    lines = spec['cover']; maxw = SAFE_R - M
    fs = []
    for ln in lines:
        txt = ln.replace('{', '').replace('}', ''); s = 190
        while s > 60 and d.textlength(txt, font=BHS(s)) > maxw: s -= 4
        fs.append(s)
    total = sum(int(s * 1.18) for s in fs); y = max(300, (SAFE_B + 150) // 2 - total // 2)
    for ln, s in zip(lines, fs):
        draw_runs(d, M, y, runs(ln), BHS(s)); y += int(s * 1.18)
    return im

def cover_chart_frame(spec, im, d, M):
    """표지 + 종가선 낙폭 그림(2026-10-03 firemap-shorts, e1_hynix_dd 표지 6.7 → '글자만·시점 없음' 지적).
    spec "cover_chart": {"prices": 네이버 일별 시세 txt, "from","to","peak","trough": YYYYMMDD, "big": "{-54.7%}", "span": "6/22 → 7/30 · 종가"}
    가격 숫자는 그리지 않는다(선 모양만) — 화면에 나오는 숫자는 spec 글자뿐이라 check가 그대로 잡는다."""
    import re
    c = spec['cover_chart']
    rows = re.findall(r'\["(\d{8})",\s*[\d.]+,\s*[\d.]+,\s*[\d.]+,\s*([\d.]+)', open(c['prices'], encoding='utf-8').read())
    s = sorted({dt: float(v) for dt, v in rows if c['from'] <= dt <= c['to']}.items())
    maxw = SAFE_R - M; y = 250
    for ln in spec['cover']:
        txt = ln.replace('{', '').replace('}', ''); sz = 130
        while sz > 60 and d.textlength(txt, font=BHS(sz)) > maxw: sz -= 4
        draw_runs(d, M, y, runs(ln), BHS(sz)); y += int(sz * 1.18)
    x0, x1, y0, y1 = M + 6, SAFE_R - 10, y + 90, y + 560
    lo, hi = min(v for _, v in s), max(v for _, v in s)
    px = lambda i: x0 + (x1 - x0) * i / (len(s) - 1)
    py = lambda v: y1 - (y1 - y0) * (v - lo) / (hi - lo)
    ip = [k for k, (dt, _) in enumerate(s) if dt == c['peak']][0]; it = [k for k, (dt, _) in enumerate(s) if dt == c['trough']][0]
    RED = (255, 84, 84)
    d.polygon([(px(ip), y1 + 20)] + [(px(k), py(s[k][1])) for k in range(ip, it + 1)] + [(px(it), y1 + 20)], fill=(70, 26, 30))
    pts = [(px(k), py(v)) for k, (_, v) in enumerate(s)]
    d.line(pts[:ip + 1], fill=GREY, width=8, joint='curve')
    d.line(pts[it:], fill=WHITE, width=10, joint='curve')          # 저점 뒤 회복 구간 — '지금 폭락 중' 오해 막기(10/3 심사 지적)
    d.line(pts[ip:it + 1], fill=RED, width=12, joint='curve')
    md = lambda dt: dt[4:6].lstrip('0') + '/' + dt[6:].lstrip('0')
    for k, lab, dy in ((ip, md(c['peak']), -80), (it, md(c['trough']), 24)):
        X, Y = pts[k]; d.ellipse((X - 18, Y - 18, X + 18, Y + 18), fill=WHITE, outline=RED, width=8)
        f = PD7(56); tw = d.textlength(lab, font=f); d.text((min(max(X - tw / 2, M), x1 - tw), Y + dy), lab, font=f, fill=WHITE)
    if c.get('end'):
        X, Y = pts[-1]; d.ellipse((X - 16, Y - 16, X + 16, Y + 16), fill=YELLOW)
        f = PD7(52); tw = d.textlength(c['end'], font=f); d.text((X - tw, Y - 90), c['end'], font=f, fill=YELLOW)
    y = y1 + 60
    if c.get('big_label'): d.text((M, y), c['big_label'], font=PD7(66), fill=RED); y += 84
    big = c['big'].replace('{', '').replace('}', '')
    d.text((M, y), big, font=BHS(190), fill=RED if c.get('big_red') else YELLOW); y += int(190 * 1.12)
    d.text((M, y), c['span'], font=PD7(58), fill=WHITE)
    if y + 70 > SAFE_B: print(f'경고: 표지 그림이 가려지는 자리까지(y={y + 70})')
    return im

def build(spec, out):
    base, top = card(spec); sec = spec.get('seconds', 6)
    frame = rank_frame if spec.get('layout') == 'rank' else bars_frame
    _, bottom = frame(base, spec, top, 2)
    if bottom > SAFE_B: print(f'경고: 글이 가려지는 자리까지 내려갔다(y={bottom} > {SAFE_B}) — 글을 줄인다')
    tmp = out + '_frames'; os.makedirs(tmp, exist_ok=True)
    csec = spec.get('cover_sec', 1) if (spec.get('cover') or spec.get('cover_png')) else 0
    if csec:
        # cover_png: 비주얼 디자이너가 심사 통과시킨 표지 그림을 그대로 첫 화면에(2026-10-03 visual, 기본 꺼짐). 표지 숫자는 그림 안이라 check가 못 잡는다 → 사실 대조는 표지 review에서.
        cov = Image.open(spec['cover_png']).convert('RGB').resize((W, H)) if spec.get('cover_png') else cover_frame(spec)
        cov.save(out.replace('.mp4', '_cover.png'))
        for i in range(int(csec * FPS)): cov.save(os.path.join(tmp, f'{i:04d}.png'))
    off = int(csec * FPS)
    for i in range(int(sec * FPS)):
        frame(base, spec, top, i / FPS)[0].save(os.path.join(tmp, f'{i + off:04d}.png'))
    sec = sec + csec
    wav = out + '.wav'
    if spec.get('music', True):   # 2026-09-30 사장님 "배경음악을 안 깔면 되는 거 아니야?" → 음악 있음/없음을 실험(experiments.md)으로 가린다
        music(wav, sec, spec.get('yt_title', '') + spec.get('facts', ''))
        subprocess.run([FF, '-v', 'error', '-y', '-framerate', str(FPS), '-i', os.path.join(tmp, '%04d.png'), '-i', wav,
                        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-c:a', 'aac', '-b:a', '160k', '-shortest', out], check=True)
    else:
        open(wav, 'wb').close()
        subprocess.run([FF, '-v', 'error', '-y', '-framerate', str(FPS), '-i', os.path.join(tmp, '%04d.png'),
                        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-an', out], check=True)
    frame(base, spec, top, 2)[0].save(out.replace('.mp4', '_card.png'))
    for f in os.listdir(tmp): os.remove(os.path.join(tmp, f))
    os.rmdir(tmp); os.remove(wav)
    print(out)

if __name__ == '__main__':
    spec = json.load(open(sys.argv[1], encoding='utf-8'))
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(sys.argv[1])[0] + '.mp4'
    build(spec, out)
