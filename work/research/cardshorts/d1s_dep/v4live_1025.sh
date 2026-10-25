# d1s_dep 10/25 23시 PD: v3(흰 판 100% — bgcheck ⑥ 10/21부터 거부) → 지금 C1S 기본 look=live(bg 11개)로 화면만 다시 렌더, 소리는 v3_ds 트랙 그대로(-c copy)
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr; D=$R/work/research/cardshorts/d1s_dep; V=$R/work/video
cd $V
T=C:/Users/Public/rtmp/d1s_dep_v4; mkdir -p $T
TEMP=$T TMP=$T npx remotion render src/c1s_index.ts C1S out/d1s_dep_v4.mp4 --props=_v3tmp_d1s_dep.json --muted --pixel-format=yuv420p --concurrency=3 --timeout=180000 > $D/render_v4.log 2>&1 || { echo RENDER_FAIL; exit 1; }
PYTHONIOENCODING=utf-8 py -3.12 -c "
import imageio_ffmpeg,subprocess,cv2
n=lambda p:int(cv2.VideoCapture(p).get(7))
a,b='out/d1s_dep_v4.mp4','out/d1s_dep_v3_ds.mp4'
print('frames',n(a),n(b)); assert n(a)==n(b)
subprocess.check_call([imageio_ffmpeg.get_ffmpeg_exe(),'-y','-loglevel','error','-i',a,'-i',b,'-map','0:v:0','-map','1:a:0','-c','copy','out/d1s_dep_v4_ds.mp4'])
" || { echo SPLICE_FAIL; exit 1; }
echo "V4_DONE $(date +%H:%M)"
