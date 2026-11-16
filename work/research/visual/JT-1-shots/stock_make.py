"""JT-1 실사 4줄 — Pexels 후보(stock_try/stock, pexelsvid.py)에서 고른 4편을 -bf 0 다시 인코딩해 video/public/bg/jt1/stock/에, 출처는 stock_credits.json. visual 2026-11-16.
고른 이유: 4장씩 4프레임 견본(sheet_*.jpg)에서 얼굴 안 보이는 것 · 손/뒷모습/빈 창가."""
import os, json, subprocess, sys, imageio_ffmpeg, datetime
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
FF = imageio_ffmpeg.get_ffmpeg_exe(); S = os.path.join(HERE, 'stock_try', 'stock'); OUT = os.path.join(WORK, 'video', 'public', 'bg', 'jt1', 'stock')
os.makedirs(OUT, exist_ok=True)
PICK = {6326847: ('jt1_handnote', '0 여는 말 — 나이 든 손이 공책에 적음(반지·손만)'),
        8420602: ('jt1_market', '4 생활비 — 장바구니 든 손(목 아래만, 얼굴 없음) · 11/16 새 심사관이 빵 진열대(4121749)는 생활비 말과 안 맞다고 해 바꿈'),
        8794903: ('jt1_walk', '5 돌아가신 뒤(쉼) — 노부부 뒷모습 산책'),
        35161057: ('jt1_window', '6 끝 — 햇살 든 커튼 창가, 사람 없음')}
cred = {c['id']: c for c in json.load(open(os.path.join(S, 'credits.json'), encoding='utf-8'))}
res = []
for vid, (name, why) in PICK.items():
    o = os.path.join(OUT, name + '.mp4')
    subprocess.run([FF, '-y', '-loglevel', 'error', '-i', os.path.join(S, f'{vid}.mp4'), '-an', '-r', '30', '-vf', 'scale=1920:-2',
                    '-c:v', 'libx264', '-bf', '0', '-g', '30', '-crf', '18', '-pix_fmt', 'yuv420p', o], check=True)
    subprocess.run([FF, '-y', '-loglevel', 'error', '-ss', '1.5', '-i', o, '-frames:v', '1', o[:-4] + '.jpg'], check=True)
    c = dict(cred[vid]); c['file'] = f'bg/jt1/stock/{name}.mp4'; c['used'] = True; c['why'] = why
    c['note'] = '얼굴·간판 없음 확인(4프레임 견본 sheet_*.jpg) · -bf 0 다시 인코딩(lessons 11/11)'; res.append(c); print(name, os.path.getsize(o))
json.dump(res, open(os.path.join(HERE, 'stock_credits.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
