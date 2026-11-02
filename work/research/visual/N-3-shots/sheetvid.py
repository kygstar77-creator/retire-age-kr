# 후보 스톡 영상 한 줄당 가운데 프레임 3장 → sheet_qN.jpg (visual 11/2, N-3 스톡 고르기)
import sys, os, glob, subprocess, json, re
import imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
D = sys.argv[1]; F = ImageFont.truetype(r'C:\Windows\Fonts\malgunbd.ttf', 18)
rows = sorted(glob.glob(os.path.join(D, 'q*')), key=lambda p: int(os.path.basename(p)[1:]) if os.path.basename(p)[1:].isdigit() else 0)
rows = [r for r in rows if os.path.isdir(r)]
bd = Image.new('RGB', (3 * 400, len(rows) * 240), 'white'); dr = ImageDraw.Draw(bd)
for ri, r in enumerate(rows):
    for ci, mp in enumerate(sorted(glob.glob(os.path.join(r, 'stock', '*.mp4')))[:3]):
        m = re.search(r'Duration: (\d+):(\d+):([\d.]+)', subprocess.run([FF, '-i', mp], capture_output=True, text=True, errors='ignore').stderr)
        dur = int(m[1]) * 3600 + int(m[2]) * 60 + float(m[3]) if m else 4
        jp = mp[:-4] + '_mid.jpg'
        subprocess.run([FF, '-y', '-v', 'error', '-ss', str(dur / 2), '-i', mp, '-frames:v', '1', '-vf', 'scale=400:-2', jp])
        im = Image.open(jp).convert('RGB'); im.thumbnail((400, 225)); bd.paste(im, (ci * 400, ri * 240))
        dr.text((ci * 400 + 4, ri * 240 + 2), f'{os.path.basename(r)} {os.path.basename(mp)[:-4]} {dur:.0f}s', fill='yellow', font=F, stroke_width=2, stroke_fill='black')
bd.save(os.path.join(D, 'sheet.jpg'), quality=80); print(os.path.join(D, 'sheet.jpg'))
