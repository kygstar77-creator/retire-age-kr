# 숏폼(9:16, 45~60초) 자동 제작 — 유튜브 쇼츠·인스타 릴스·틱톡·네이버 클립 공용 파일. 사장님 2026-09-23 "숏폼 다 만들어봐".
#   py -3.12 work/shorts.py <대본.json> [출력.mp4]
# 대본 형식: {"title": "...", "scenes": [{"label": "위 작은 글", "head": "큰 제목(한 줄~두 줄)", "lines": ["줄1", "줄2"], "image": "선택 png/jpg", "say": "읽을 문장(없으면 head+lines)"}], "outro": "마지막 한 줄"}
# 그림: PIL(1080x1920, 검정 바탕·흰 큰 글자·숫자 강조), 음성: edge-tts(무료), 합치기: imageio-ffmpeg. 자막은 화면에 이미 큰 글자로 박혀 있어 무음 재생에도 읽힌다.
import sys, os, re, json, asyncio, subprocess, shutil, time
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image, ImageDraw, ImageFont
import edge_tts, imageio_ffmpeg
HERE = os.path.dirname(os.path.abspath(__file__)); FD = os.path.join(HERE, 'fonts'); FF = imageio_ffmpeg.get_ffmpeg_exe()
W, H = 1080, 1920; VOICE = 'ko-KR-SunHiNeural'
TMP = os.path.join(os.environ.get('TEMP', 'C:/Temp'), 'shorts_' + str(int(time.time()))); os.makedirs(TMP, exist_ok=True)

def font(sz, bold=True):
    p = os.path.join(FD, 'pd700.ttf' if bold else 'pd500.ttf')
    return ImageFont.truetype(p, sz) if os.path.exists(p) else ImageFont.truetype(r'C:\Windows\Fonts\malgunbd.ttf' if bold else r'C:\Windows\Fonts\malgun.ttf', sz)

def wrap(dr, text, f, maxw):
    lines, cur = [], ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if dr.textlength(t, font=f) <= maxw: cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def draw_num(dr, x, y, text, f, fill=(255, 255, 255), accent=(255, 214, 10)):
    """숫자·%·억·원은 노란색으로 강조해서 한 줄 그리기"""
    for tok in re.split(r'(\d[\d,.]*\s?(?:%|억|만원|원|달러|배|세대|㎡|층|년|월|일|개|편|건|회)?)', text):
        if not tok: continue
        dr.text((x, y), tok, font=f, fill=accent if re.match(r'\d', tok) else fill); x += dr.textlength(tok, font=f)

def scene_png(sc, idx, total, title, out):
    im = Image.new('RGB', (W, H), (14, 14, 18)); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 8], fill=(255, 214, 10)); dr.rectangle([0, 8, int(W * (idx + 1) / total), 16], fill=(255, 214, 10))   # 진행 바
    dr.text((60, 60), title[:40], font=font(36, False), fill=(160, 160, 170))
    y = 200
    if sc.get('label'): dr.text((60, y), sc['label'], font=font(44, False), fill=(255, 214, 10)); y += 80
    f = font(92)
    for l in wrap(dr, sc.get('head', ''), f, W - 120)[:3]: draw_num(dr, 60, y, l, f); y += 112
    y += 30
    img = sc.get('image')
    if img and os.path.exists(img):
        pic = Image.open(img).convert('RGB'); r = min((W - 80) / pic.width, 700 / pic.height); pic = pic.resize((int(pic.width * r), int(pic.height * r)))
        im.paste(pic, ((W - pic.width) // 2, y)); y += pic.height + 40
    f2 = font(54, False)
    for line in sc.get('lines', [])[:6]:
        for l in wrap(dr, line, f2, W - 120)[:2]:
            draw_num(dr, 60, y, l, f2, fill=(230, 230, 235)); y += 72
        y += 12
    dr.text((60, H - 120), '파이어맵 · cafe.naver.com/firemap', font=font(34, False), fill=(120, 120, 130))
    im.save(out)

def tts(text, mp3): asyncio.run(edge_tts.Communicate(text, VOICE, rate='+8%').save(mp3))

def build(script, out):
    scenes = script['scenes']; parts = []
    if script.get('outro'): scenes = scenes + [{'head': script['outro'], 'say': script['outro']}]
    for i, sc in enumerate(scenes):
        png = os.path.join(TMP, f's{i:02d}.png'); scene_png(sc, i, len(scenes), script.get('title', ''), png)
        say = sc.get('say') or ' '.join([sc.get('head', '')] + sc.get('lines', []))
        mp3 = os.path.join(TMP, f'a{i:02d}.mp3'); tts(say, mp3)
        seg = os.path.join(TMP, f'p{i:02d}.mp4')
        subprocess.run([FF, '-y', '-loglevel', 'error', '-loop', '1', '-i', png, '-i', mp3, '-c:v', 'libx264', '-tune', 'stillimage', '-r', '30', '-c:a', 'aac', '-b:a', '128k', '-pix_fmt', 'yuv420p', '-af', 'apad=pad_dur=0.4', '-shortest', seg], check=True)
        parts.append(seg)
    lst = os.path.join(TMP, 'list.txt'); open(lst, 'w', encoding='utf-8').write(''.join(f"file '{p.replace(chr(92), '/')}'\n" for p in parts))
    tmp_out = os.path.join(TMP, 'final.mp4')
    subprocess.run([FF, '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', tmp_out], check=True)
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True); shutil.copy(tmp_out, out)
    dur = float(subprocess.run([FF.replace('ffmpeg', 'ffprobe'), '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', tmp_out], capture_output=True, text=True).stdout or 0) if os.path.exists(FF.replace('ffmpeg', 'ffprobe')) else -1
    print('완성', out, os.path.getsize(out), 'bytes', f'{dur:.0f}초' if dur > 0 else '')
    shutil.copy(os.path.join(TMP, 's00.png'), os.path.splitext(out)[0] + '_thumb.png')

if __name__ == '__main__':
    script = json.load(open(sys.argv[1], encoding='utf-8'))
    build(script, sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'research', 'shorts', re.sub(r'[^\w가-힣]+', '_', script.get('title', 'shorts'))[:40] + '.mp4'))
