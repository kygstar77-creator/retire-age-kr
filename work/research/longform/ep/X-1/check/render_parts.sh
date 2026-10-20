# X-1 10/20 PD(T-1 render_parts.sh 복사): 세 토막 렌더 후 이어 붙임
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr
EP=$R/work/research/longform/ep/X-1
OUT=$R/work/video/out
for rg in 0-8999 9000-17999 18000-25870; do
  PYTHONIOENCODING=utf-8 py -3.12 -u $R/work/lfrender.py render $EP --concurrency=2 --timeout=120000 --offthreadvideo-cache-size-in-bytes=536870912 --frames=$rg > $EP/check/render_part_$rg.log 2>&1
  if [ ! -f $OUT/x1.mp4 ] || [ $(stat -c %Y $OUT/x1.mp4) -lt $(stat -c %Y $EP/check/render_part_$rg.log) ] && ! grep -q "Rendered" $EP/check/render_part_$rg.log; then echo "FAIL $rg"; exit 1; fi
  mv -f $OUT/x1.mp4 $OUT/x1_part_$rg.mp4
  echo "part $rg $(date +%H:%M)"
done
printf "file 'x1_part_0-8999.mp4'\nfile 'x1_part_9000-17999.mp4'\nfile 'x1_part_18000-25870.mp4'\n" > $OUT/x1_parts.txt
cd $OUT && $R/work/video/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe -y -hide_banner -loglevel error -f concat -safe 0 -i x1_parts.txt -c copy x1.mp4 && echo "CONCAT OK $(date +%H:%M)"
