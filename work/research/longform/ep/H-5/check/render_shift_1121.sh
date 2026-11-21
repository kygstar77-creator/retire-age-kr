# H-5 11/21 14:1x PD: 토막 9000 시작 7프레임 뒤 문장(57e3)에서 50ms 소리 끊김(두 번 렌더해도 같음) → 경계를 9500으로 옮겨 8000-9499·9500-9999 다시
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr
mkdir -p C:/fm_render_tmp; export TEMP=C:/fm_render_tmp TMP=C:/fm_render_tmp
EP=$R/work/research/longform/ep/H-5; OUT=$R/work/video/out
for rg in 8000-9499 9500-9999; do
  [ -f $OUT/h5s_part_$rg.mp4 ] && { echo "skip $rg"; continue; }
  for t in 1 2 3; do
    rm -f $OUT/h5.mp4
    PYTHONIOENCODING=utf-8 py -3.12 -u $R/work/lfrender.py render $EP --concurrency=1 --timeout=120000 --offthreadvideo-cache-size-in-bytes=1073741824 --frames=$rg > $EP/check/render_s_$rg.log 2>&1
    if [ -f $OUT/h5.mp4 ] && ! grep -q "An error occurred" $EP/check/render_s_$rg.log; then mv -f $OUT/h5.mp4 $OUT/h5s_part_$rg.mp4; echo "part $rg try$t $(date +%H:%M)"; break; fi
    echo "retry $rg try$t $(date +%H:%M)"
  done
  [ -f $OUT/h5s_part_$rg.mp4 ] || { echo "FAIL $rg"; exit 1; }
done
cd $OUT && sed -e "s#file 'h5_part_8000-8999.mp4'#file 'h5s_part_8000-9499.mp4'#" -e "s#file 'h5_part_9000-9999.mp4'#file 'h5s_part_9500-9999.mp4'#" h5_parts.txt > h5s_parts.txt && cat h5s_parts.txt | head -12 && $R/work/video/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe -y -hide_banner -loglevel error -f concat -safe 0 -i h5s_parts.txt -c copy h5.mp4 && echo "CONCAT OK $(date +%H:%M)"
cd $R/work/video && PYTHONIOENCODING=utf-8 py -3.12 -c "
import clickscan
a,sr=clickscan.load('out/h5.mp4'); print('bursts',[round(b[0]/sr,2) for b in clickscan.bursts(a,sr)], 'len', len(a)/sr)"
