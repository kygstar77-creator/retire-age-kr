# T-1 10/20 PD: 셋째 토막(18000-26149)만 다시 — 맺는 말 뒤 23초 자막 남던 것(소리 없는 빈 줄). 끝나면 세 토막 이어 붙임
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr
EP=$R/work/research/longform/ep/T-1
OUT=$R/work/video/out
rg=18000-26149
mv -f $OUT/t1_part_$rg.mp4 $OUT/t1_part_$rg.old1020.mp4.bak
PYTHONIOENCODING=utf-8 py -3.12 -u $R/work/lfrender.py render $EP --concurrency=2 --timeout=120000 --offthreadvideo-cache-size-in-bytes=536870912 --frames=$rg > $EP/check/render_part_${rg}_redo.log 2>&1
grep -q "Rendered" $EP/check/render_part_${rg}_redo.log || { echo "FAIL $rg"; exit 1; }
mv -f $OUT/t1.mp4 $OUT/t1_part_$rg.mp4
echo "part $rg redo $(date +%H:%M)"
printf "file 't1_part_0-8999.mp4'\nfile 't1_part_9000-17999.mp4'\nfile 't1_part_18000-26149.mp4'\n" > $OUT/t1_parts.txt
cd $OUT && $R/work/video/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe -y -hide_banner -loglevel error -f concat -safe 0 -i t1_parts.txt -c copy t1.mp4 && echo "CONCAT OK $(date +%H:%M)"
