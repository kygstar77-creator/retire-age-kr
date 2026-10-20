# T-1 10/20 PD(H-2 render_parts.sh 복사): 한 번에 렌더하면 17,800프레임쯤에서 브라우저가 그림을 못 풀어(paper.png decode) 죽는다 — lfrender render를 세 토막으로 돌리고 이어 붙인다(C-2 10/19 06:25와 같은 방식)
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr
EP=$R/work/research/longform/ep/T-1
OUT=$R/work/video/out
for rg in 0-8999 9000-17999 18000-26149; do
  PYTHONIOENCODING=utf-8 py -3.12 -u $R/work/lfrender.py render $EP --concurrency=2 --timeout=120000 --offthreadvideo-cache-size-in-bytes=536870912 --frames=$rg > $EP/check/render_part_$rg.log 2>&1
  if [ ! -f $OUT/t1.mp4 ] || [ $(stat -c %Y $OUT/t1.mp4) -lt $(stat -c %Y $EP/check/render_part_$rg.log) ] && ! grep -q "Rendered" $EP/check/render_part_$rg.log; then echo "FAIL $rg"; exit 1; fi
  mv -f $OUT/t1.mp4 $OUT/t1_part_$rg.mp4
  echo "part $rg $(date +%H:%M)"
done
printf "file 't1_part_0-8999.mp4'\nfile 't1_part_9000-17999.mp4'\nfile 't1_part_18000-26149.mp4'\n" > $OUT/t1_parts.txt
cd $OUT && $R/work/video/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe -y -hide_banner -loglevel error -f concat -safe 0 -i t1_parts.txt -c copy t1.mp4 && echo "CONCAT OK $(date +%H:%M)"
