# H-3 10/21 PD(X-1 render_parts.sh 복사): v5 29,4xx프레임 네 토막(10/21 18시 PD, 옛 v4 토막은 old_v4로 치움) 렌더 후 이어 붙임 — 끝 토막 먼저(화면 관문 미리 재기)
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr
EP=$R/work/research/longform/ep/H-3
OUT=$R/work/video/out
END=$(PYTHONIOENCODING=utf-8 py -3.12 -c "import json;p=json.load(open('$R/work/video/h3.json',encoding='utf-8'));print(sum(s['frames'] for s in p['scenes'])-1)")
for rg in ${PARTS:-27000-$END 0-8999 9000-17999 18000-26999}; do
  if [ -f $OUT/h3_part_$rg.mp4 ]; then echo "skip $rg"; continue; fi
  PYTHONIOENCODING=utf-8 py -3.12 -u $R/work/lfrender.py render $EP --concurrency=2 --timeout=120000 --offthreadvideo-cache-size-in-bytes=536870912 --frames=$rg > $EP/check/render_part_$rg.log 2>&1
  if [ ! -f $OUT/h3.mp4 ] || [ $(stat -c %Y $OUT/h3.mp4) -lt $(stat -c %Y $EP/check/render_part_$rg.log) ] && ! grep -q "Rendered" $EP/check/render_part_$rg.log; then echo "FAIL $rg"; exit 1; fi
  mv -f $OUT/h3.mp4 $OUT/h3_part_$rg.mp4
  echo "part $rg $(date +%H:%M)"
done
printf "file 'h3_part_0-8999.mp4'\nfile 'h3_part_9000-17999.mp4'\nfile 'h3_part_18000-26999.mp4'\nfile 'h3_part_27000-$END.mp4'\n" > $OUT/h3_parts.txt
cd $OUT && $R/work/video/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe -y -hide_banner -loglevel error -f concat -safe 0 -i h3_parts.txt -c copy h3.mp4 && echo "CONCAT OK $(date +%H:%M)"
