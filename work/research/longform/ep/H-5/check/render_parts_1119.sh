# H-5 11/19 02:3x PD: JT-1 render_parts_1118.sh 사본(jt1→h5, JT-1→H-5만). TEMP C:/fm_render_tmp, 토막 1000프레임·concurrency 1
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr
mkdir -p C:/fm_render_tmp; export TEMP=C:/fm_render_tmp TMP=C:/fm_render_tmp
EP=$R/work/research/longform/ep/H-5
OUT=$R/work/video/out
LIST=""
for s in 0 1000 2000 3000 4000 5000 6000 7000 8000 9000 10000 11000 12000 13000 14000 15000; do LIST="$LIST $s-$((s+999))"; done; LIST="$LIST 16000-"
for rg in $LIST; do
  [ -f $OUT/h5_part_$rg.mp4 ] && { echo "skip $rg"; continue; }
  for t in 1 2 3; do
    rm -f $OUT/h5.mp4
    PYTHONIOENCODING=utf-8 py -3.12 -u $R/work/lfrender.py render $EP --concurrency=1 --timeout=120000 --offthreadvideo-cache-size-in-bytes=${CACHE:-1073741824} --frames=$rg > $EP/check/render_b_$rg.log 2>&1
    if [ -f $OUT/h5.mp4 ] && [ $(stat -c %Y $OUT/h5.mp4) -ge $(stat -c %Y $EP/check/render_b_$rg.log) ] || ( [ -f $OUT/h5.mp4 ] && ! grep -q "An error occurred" $EP/check/render_b_$rg.log ); then
      rm -rf C:/fm_render_tmp/remotion-* 2>/dev/null; mv -f $OUT/h5.mp4 $OUT/h5_part_$rg.mp4; echo "part $rg try$t $(date +%H:%M)"; break
    fi
    echo "retry $rg try$t $(date +%H:%M)"; cp $EP/check/render_b_$rg.log $EP/check/render_b_${rg}_fail$t.log
  done
  [ -f $OUT/h5_part_$rg.mp4 ] || { echo "FAIL $rg"; exit 1; }
done
: > $OUT/h5_parts.txt; for rg in $LIST; do echo "file 'h5_part_$rg.mp4'" >> $OUT/h5_parts.txt; done
cd $OUT && $R/work/video/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe -y -hide_banner -loglevel error -f concat -safe 0 -i h5_parts.txt -c copy h5.mp4 && echo "CONCAT OK $(date +%H:%M)"
