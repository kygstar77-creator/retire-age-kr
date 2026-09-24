# 숏폼(9:16) 자동 제작 — 유튜브 쇼츠·릴스·틱톡·네이버 클립 공용. 경쟁 459편 실측 규칙 반영(2026-09-23).
#   py -3.12 work/shorts.py <대본.json> [출력.mp4]
# 대본은 shortscript.py(Gemini)가 쓴다. 내(클로드) 문장은 쓰지 않는다.
#
# 실측에서 가져온 규칙
#  - 길이: 경쟁 쇼츠 80편 중앙 42초(30~55초가 대부분) → 장면 4~5개 × 8~11초, 총 45초 안팎
#  - 글자: 제목체(Black Han Sans) 흰색 + 강조 줄 노란색, 검은 외곽선. 가로폭 88% 채움
#  - 화면: 정지 금지. 장면마다 천천히 확대/이동(Ken Burns)과 0.25초 밀어넣기 전환으로 속도감
#  - 첫 3초에 숫자가 보여야 한다(경쟁 쇼츠 제목 43%가 숫자)
import sys, os, re, json, asyncio, subprocess, shutil, time
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import edge_tts, imageio_ffmpeg
HERE = os.path.dirname(os.path.abspath(__file__)); FD = os.path.join(HERE, 'fonts'); FF = imageio_ffmpeg.get_ffmpeg_exe()
W, H = 1080, 1920; VOICE = 'ko-KR-SunHiNeural'; YELLOW = (255, 214, 10); WHITE = (245, 245, 250)
try: CFG = json.load(open(os.path.join(HERE, 'design.json'), encoding='utf-8')).get('video', {})
except Exception: CFG = {}
ZOOM = CFG.get('zoom', 0.0009)
TMP = os.path.join(os.environ.get('TEMP', 'C:/Temp'), 'shorts_' + str(int(time.time()))); os.makedirs(TMP, exist_ok=True)

def fit_bg(im, W, H):
    """자료 화면은 통째로 보이게 넣는다 — 잘라 채우지 않는다(사장님 2026-09-23 "자료 화면이 보여야 한다").
    2026-09-24 실측: chartimg --short 는 1080x1350 인데 1080x1920 에 max 배율로 맞춰 (0,0) 에서 자르면
    가로가 1536 으로 늘어나 오른쪽 30%가 잘려 나간다. 막대와 값이 통째로 사라지고 단지 이름만 남아서
    자료 화면이 장식이 돼 버렸다(영상 프레임·썸네일 둘 다 확인). 그래서 '덮기'가 아니라 '안에 맞추기'다.
    남는 자리는 원본 가장자리 색으로 채워 이어 붙인 티가 안 나게 한다."""
    # 0.92 는 천천히 확대(design.json video.zoom)가 먹는 자리다 — 딱 맞춰 넣으면 확대되면서 다시 가장자리 값이 잘린다
    r = min(W / im.width, H / im.height) * 0.92
    nw, nh = max(1, int(im.width * r)), max(1, int(im.height * r))
    sm = im.resize((nw, nh))
    if nw >= W and nh >= H: return sm.crop((0, 0, W, H))
    edge = im.resize((1, 1)).getpixel((0, 0))          # 원본 평균색 — 차트 바탕이 어두우면 어둡게 채워진다
    out = Image.new('RGB', (W, H), edge)
    out.paste(sm, ((W - nw) // 2, (H - nh) // 2))
    return out


def disp(sz):
    p = os.path.join(FD, 'BlackHanSans.ttf')
    return ImageFont.truetype(p, sz) if os.path.exists(p) else ImageFont.truetype(os.path.join(FD, 'pd700.ttf'), sz)

def body(sz, bold=False):
    p = os.path.join(FD, 'pd700.ttf' if bold else 'pd500.ttf')
    return ImageFont.truetype(p, sz) if os.path.exists(p) else ImageFont.truetype(r'C:\Windows\Fonts\malgun.ttf', sz)

def fit_lines(dr, text, maxw, maxsz=150, minsz=54):
    """제목을 1~2줄로 나누고, 폭을 꽉 채우는 크기를 찾는다"""
    words = text.split()
    for sz in range(maxsz, minsz - 1, -2):
        f = disp(sz); lines, cur = [], ''
        for w in words:
            t = (cur + ' ' + w).strip()
            if dr.textlength(t, font=f) <= maxw: cur = t
            else:
                if cur: lines.append(cur)
                cur = w
        if cur: lines.append(cur)
        if len(lines) <= 2 and all(dr.textlength(l, font=f) <= maxw for l in lines): return f, lines
    f = disp(minsz); return f, [text[:14], text[14:28]]

def draw_tokens(dr, x, y, text, f, base, sw):
    """숫자·단위는 노랑, 나머지는 base 색"""
    for tok in re.split(r'(\d[\d,.]*\s?(?:%|억|만원|원|달러|배|세대|㎡|층|년|월|일|개|편|건|회|위|퍼센트)?)', text):
        if not tok: continue
        col = YELLOW if re.match(r'\d', tok) else base
        dr.text((x, y), tok, font=f, fill=col, stroke_width=sw, stroke_fill=(0, 0, 0)); x += dr.textlength(tok, font=f)

def bg_base():
    """자료 화면이 없을 때 쓰는 바탕"""
    im = Image.new('RGB', (W, H), (11, 12, 16))
    top = Image.new('RGB', (W, H), (26, 30, 48)); mask = Image.new('L', (1, H))
    for y in range(H): mask.putpixel((0, y), int(70 * (1 - y / H)))
    return Image.composite(top, im, mask.resize((W, H)))

def scene_png(sc, idx, total, title, out):
    """글자와 자료 화면을 위아래로 나눈다(2026-09-24).
    전에는 자료 화면을 화면 전체에 깔고 그 위에 글자를 얹었다. chartimg 차트는 한가운데(y 339~1581)에
    들어가는데 글자도 y 300 부터 시작해서, 차트 제목과 값이 머리글 뒤에 그대로 겹쳤다
    (dsr40 1장면 실측: '만기별 대출 한도 (연소득 5,000만원  5.2' 가 잘린 채 '40년이면' 뒤에 깔림).
    게다가 겹침을 가리려고 화면 전체를 0.42로 어둡게 눌러서 막대가 아예 안 보였다.
    이제는 글자를 먼저 앉히고, 남은 아래 자리에 자료 화면을 통째로 넣는다. 겹치지 않으니 덜 어둡게 해도 된다."""
    im = bg_base()
    dr = ImageDraw.Draw(im); pad = 56; maxw = W - pad * 2

    # 1) 글자가 어디까지 내려오는지 먼저 잰다(아직 그리지 않는다)
    y0 = 150
    y = y0
    if sc.get('label'): y += 118
    f, lines = fit_lines(dr, sc.get('head', ''), maxw)
    y += int(f.size * 1.22) * len(lines) + 44
    y += 86 * len(sc.get('lines', [])[:4])
    text_bottom = y

    # 2) 자료 화면은 글자 아래 남은 자리에 '통째로' 넣는다 — 잘리지도, 글자에 깔리지도 않는다
    bgp = sc.get('image')
    if bgp and os.path.exists(bgp):
        box_t, box_b = text_bottom + 36, H - 150
        bw, bh = W - pad * 2, max(200, box_b - box_t)
        src = Image.open(bgp).convert('RGB')
        r = min(bw / src.width, bh / src.height) * 0.98
        nw, nh = max(1, int(src.width * r)), max(1, int(src.height * r))
        card = ImageEnhance.Brightness(src.resize((nw, nh))).enhance(0.82)
        cx, cy = (W - nw) // 2, box_t + (bh - nh) // 2
        dr.rounded_rectangle([cx - 12, cy - 12, cx + nw + 12, cy + nh + 12], 22, fill=(20, 22, 28))
        im.paste(card, (cx, cy))
        dr = ImageDraw.Draw(im)

    # 3) 이제 글자를 그린다
    dr.rectangle([0, 0, W, 10], fill=(60, 60, 70)); dr.rectangle([0, 0, int(W * (idx + 1) / total), 10], fill=YELLOW)
    y = y0
    if sc.get('label'):
        fl = body(46, True); tw = dr.textlength(sc['label'], font=fl)
        dr.rounded_rectangle([pad, y - 14, pad + tw + 44, y + 70], 16, fill=YELLOW)
        dr.text((pad + 22, y), sc['label'][:20], font=fl, fill=(10, 10, 12)); y += 118
    sw = max(5, f.size // 14)
    for l in lines:
        draw_tokens(dr, pad, y, l, f, WHITE, sw); y += int(f.size * 1.22)
    y += 44
    fb = body(56)
    for line in sc.get('lines', [])[:4]:
        dr.rectangle([pad, y + 16, pad + 8, y + 58], fill=YELLOW)
        seg = line if dr.textlength(line, font=fb) <= maxw - 30 else line[:int(len(line) * (maxw - 30) / max(1, dr.textlength(line, font=fb)))]
        draw_tokens(dr, pad + 30, y, seg, fb, (228, 228, 236), 3); y += 86
    dr.text((pad, H - 108), '파이어맵 · cafe.naver.com/firemap', font=body(34), fill=(130, 130, 142))
    im.save(out)

def tts(text, mp3): asyncio.run(edge_tts.Communicate(text, VOICE, rate='+10%').save(mp3))

def dur_of(path):
    pr = FF.replace('ffmpeg', 'ffprobe')
    if not os.path.exists(pr): return None
    r = subprocess.run([pr, '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path], capture_output=True, text=True)
    try: return float(r.stdout.strip())
    except ValueError: return None

def build(script, out):
    scenes = list(script['scenes'])
    if script.get('outro'): scenes.append({'head': script['outro'], 'say': script['outro']})
    parts = []
    for i, sc in enumerate(scenes):
        png = os.path.join(TMP, f's{i:02d}.png'); scene_png(sc, i, len(scenes), script.get('title', ''), png)
        say = sc.get('say') or ' '.join([sc.get('head', '')] + sc.get('lines', []))
        mp3 = os.path.join(TMP, f'a{i:02d}.mp3'); tts(say, mp3)
        d = (dur_of(mp3) or 6) + 0.5
        seg = os.path.join(TMP, f'p{i:02d}.mp4'); n = max(2, int(d * 30))
        # Ken Burns: 홀수 장면은 확대, 짝수는 축소 — 정지 화면이 아니게
        z = f"zoompan=z='min(zoom+{ZOOM},1.12)':d={n}:s={W}x{H}:fps=30" if i % 2 == 0 else f"zoompan=z='if(lte(zoom,1.0),1.12,max(1.001,zoom-{ZOOM}))':d={n}:s={W}x{H}:fps=30"
        subprocess.run([FF, '-y', '-loglevel', 'error', '-loop', '1', '-i', png, '-i', mp3,
                        '-filter_complex', f'[0:v]scale={W*2}:{H*2},{z},scale={W}:{H},setsar=1[v]', '-map', '[v]', '-map', '1:a',
                        '-c:v', 'libx264', '-r', '30', '-c:a', 'aac', '-b:a', '128k', '-pix_fmt', 'yuv420p',
                        '-af', 'apad=pad_dur=0.45', '-t', f'{d:.2f}', seg], check=True)
        parts.append(seg)
    lst = os.path.join(TMP, 'list.txt'); open(lst, 'w', encoding='utf-8').write(''.join(f"file '{p.replace(chr(92), '/')}'\n" for p in parts))
    tmp_out = os.path.join(TMP, 'final.mp4')
    subprocess.run([FF, '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', tmp_out], check=True)
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True); shutil.copy(tmp_out, out)
    total = dur_of(out)
    # 썸네일은 thumb.py 규칙으로 따로(첫 장면 재활용 금지)
    try:
        sys.path.insert(0, HERE); import thumb
        # 3줄 판형(2026-09-24)이 생겨 아랫줄에 자리가 늘었다. 글자 수로 뚝 자르지 않고 띄어쓰기에서 자른다.
        s0 = scenes[0]; thumb.make(thumb.clip_words(s0.get('head', script.get('title', '')), 20),
                                   thumb.clip_words((s0.get('lines') or [script.get('title', '')])[0], 30),
                                   os.path.splitext(out)[0] + '_thumb.png', s0.get('image'), short=True)
    except Exception as e: print('썸네일 실패', str(e)[:60])
    print('완성', out, f'{os.path.getsize(out):,} bytes', f'{total:.0f}초' if total else '')

if __name__ == '__main__':
    script = json.load(open(sys.argv[1], encoding='utf-8'))
    build(script, sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'research', 'shorts', re.sub(r'[^\w가-힣]+', '_', script.get('title', 'shorts'))[:40] + '.mp4'))
