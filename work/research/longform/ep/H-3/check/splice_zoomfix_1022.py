# H-3 10/22 PD: h3_ds.mp4(소리 그대로) 위에 다시 렌더한 지도 6장면을 그 프레임 자리에 덮어 h3_ds_v2.mp4
import imageio_ffmpeg, subprocess, os, sys
OUT = r'C:/Users/강영준/Documents/GitHub/retire-age-kr/work/video/out'
R = ['184-321', '2116-2268', '4001-4053', '5679-5922', '9057-9248', '23271-23523']
cmd = [imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-hide_banner', '-loglevel', 'error', '-i', f'{OUT}/h3_ds.mp4']
for r in R: cmd += ['-i', f'{OUT}/h3fix1022/seg_{r}.mp4']
fl, last = [], '0:v'
for k, r in enumerate(R, 1):
    a, b = map(int, r.split('-')); s, e = a / 30, (b + 1) / 30 - 0.001
    fl.append(f'[{k}:v]setpts=PTS-STARTPTS+{s}/TB[s{k}]')
    fl.append(f"[{last}][s{k}]overlay=enable='between(t,{s:.4f},{e:.4f})':eof_action=pass[o{k}]"); last = f'o{k}'
cmd += ['-filter_complex', ';'.join(fl), '-map', f'[{last}]', '-map', '0:a', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
        '-pix_fmt', 'yuv420p', '-r', '30', '-c:a', 'copy', '-movflags', '+faststart', f'{OUT}/h3_ds_v2.mp4']
sys.exit(subprocess.call(cmd))
