# H-4 11/12 10:5x PD: No frame found가 무작위 프레임에서 남(남은 메모리 3GB, remotion 문서 '캐시 메모리 부족'이 1순위 원인) → 1천 프레임 토막 + 토막마다 3번까지 다시
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr
EP=$R/work/research/longform/ep/H-4
OUT=$R/work/video/out
LIST=""
for s in 0 1000 2000 3000 4000 5000 6000 7000 8000 9000 10000 11000; do LIST="$LIST $s-$((s+999))"; done
for rg in $LIST; do
  [ -f $OUT/h4_part_$rg.mp4 ] && { echo "skip $rg"; continue; }
  for t in 1 2 3; do
    rm -f $OUT/h4.mp4
    PYTHONIOENCODING=utf-8 py -3.12 -u $R/work/lfrender.py render $EP --concurrency=1 --timeout=120000 --offthreadvideo-cache-size-in-bytes=${CACHE:-1073741824} --frames=$rg > $EP/check/render_b_$rg.log 2>&1
    if [ -f $OUT/h4.mp4 ] && [ $(stat -c %Y $OUT/h4.mp4) -ge $(stat -c %Y $EP/check/render_b_$rg.log) ] || ( [ -f $OUT/h4.mp4 ] && ! grep -q "An error occurred" $EP/check/render_b_$rg.log ); then
      mv -f $OUT/h4.mp4 $OUT/h4_part_$rg.mp4; echo "part $rg try$t $(date +%H:%M)"; break
    fi
    echo "retry $rg try$t $(date +%H:%M)"; cp $EP/check/render_b_$rg.log $EP/check/render_b_${rg}_fail$t.log
  done
  [ -f $OUT/h4_part_$rg.mp4 ] || { echo "FAIL $rg"; exit 1; }
done
: > $OUT/h4_parts.txt; for rg in $LIST 12000-15430; do echo "file 'h4_part_$rg.mp4'" >> $OUT/h4_parts.txt; done
cd $OUT && $R/work/video/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe -y -hide_banner -loglevel error -f concat -safe 0 -i h4_parts.txt -c copy h4.mp4 && echo "CONCAT OK $(date +%H:%M)"
