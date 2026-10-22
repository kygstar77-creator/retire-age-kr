# H-3 10/22 PD: 새 타임라인(4:26 '431채' +13프레임) 조립.
#   영상: h3_ds_v2 [0,8121) + 새 seg 8121-8384 + h3_ds_v2 [8372,29521)  → 그 위에 새 seg(s13·s45·s65·s71·s105)를 새 타임라인 자리에 덮음
#   소리: h3_full_v5b_1022(디에서 전 원 소리) [0,8121) + seg 8121-8384 소리 + [8372,끝) → deess.py가 편 전체를 한 번에 처리(음량 맞춤 포함)
import imageio_ffmpeg, subprocess, sys, json
OUT = r'C:/Users/강영준/Documents/GitHub/retire-age-kr/work/video/out'
FPS, A0, B0, SHIFT = 30, 8121, 8372, 13          # 옛 장면 47 시작 8121 · 옛 장면 49 시작 8372 · 새 seg는 8121-8384(264프레임)
OV = ['2985-3146', '7720-7988', '11324-11707', '12462-12692', '20570-20764']
n_new = json.load(open(r'C:/Users/강영준/Documents/GitHub/retire-age-kr/work/video/h3.json', encoding='utf-8'))
TOT = sum(s['frames'] for s in n_new['scenes'])
assert (8384 + 1 - A0) - (B0 - A0) == SHIFT and TOT == 29521 + SHIFT, TOT
ins = ['-i', f'{OUT}/h3_ds_v2.mp4', '-i', f'{OUT}/h3_full_v5b_1022.mp4', '-i', f'{OUT}/h3rt1022/seg_8121-8384.mp4']
for r in OV: ins += ['-i', f'{OUT}/h3rt1022/seg_{r}.mp4']
f = [f'[0:v]trim=start_frame=0:end_frame={A0},setpts=PTS-STARTPTS[v1]',
     f'[2:v]setpts=PTS-STARTPTS[v2]',
     f'[0:v]trim=start_frame={B0}:end_frame=29521,setpts=PTS-STARTPTS[v3]',
     '[v1][v2][v3]concat=n=3:v=1:a=0[vb]',
     f'[1:a]atrim=start=0:end={A0/FPS},asetpts=PTS-STARTPTS[a1]',
     f'[2:a]asetpts=PTS-STARTPTS[a2]',
     f'[1:a]atrim=start={B0/FPS},asetpts=PTS-STARTPTS[a3]',
     '[a1][a2][a3]concat=n=3:v=0:a=1[ab]']
last = 'vb'
for k, r in enumerate(OV, 3):
    a, b = map(int, r.split('-')); s, e = a / FPS, (b + 1) / FPS - 0.001
    f.append(f'[{k}:v]setpts=PTS-STARTPTS+{s}/TB[s{k}]')
    f.append(f"[{last}][s{k}]overlay=enable='between(t,{s:.4f},{e:.4f})':eof_action=pass[o{k}]"); last = f'o{k}'
cmd = [imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-hide_banner', '-loglevel', 'error', *ins, '-filter_complex', ';'.join(f),
       '-map', f'[{last}]', '-map', '[ab]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', '30',
       '-c:a', 'aac', '-b:a', '320k', '-ar', '48000', '-movflags', '+faststart', f'{OUT}/h3_rt.mp4']
rc = subprocess.call(cmd)
if rc == 0:
    p = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-i', f'{OUT}/h3_rt.mp4', '-map', '0:v', '-c', 'copy', '-f', 'null', '-'], capture_output=True, text=True, encoding='utf-8', errors='replace').stderr
    import re; fr = re.findall(r'frame=\s*(\d+)', p); print('h3_rt.mp4 프레임', fr[-1] if fr else '?', '/ 기대', TOT)
sys.exit(rc)
