# J-1 10/22 14시 PD(H-3 render_parts_v5c.sh 복사): 25,956프레임 네 토막 — 끝 토막 먼저
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr
EP=$R/work/research/longform/ep/J-1
OUT=$R/work/video/out
END=$(PYTHONIOENCODING=utf-8 py -3.12 -c "import json;p=json.load(open('$R/work/video/j1.json',encoding='utf-8'));print(sum(s['frames'] for s in p['scenes'])-1)")
for rg in ${PARTS:-24000-$END 0-7999 8000-15999 16000-23999}; do
  if [ -f $OUT/j1_part_$rg.mp4 ]; then echo "skip $rg"; continue; fi
  PYTHONIOENCODING=utf-8 py -3.12 -u $R/work/lfrender.py render $EP --concurrency=${CONC:-2} --timeout=120000 --offthreadvideo-cache-size-in-bytes=536870912 --frames=$rg > $EP/check/render_part_$rg.log 2>&1
  if [ ! -f $OUT/j1.mp4 ] || [ $(stat -c %Y $OUT/j1.mp4) -lt $(stat -c %Y $EP/check/render_part_$rg.log) ] && ! grep -q "Rendered" $EP/check/render_part_$rg.log; then echo "FAIL $rg"; exit 1; fi
  [ -f $OUT/j1.mp4 ] || { echo "FAIL $rg (h3.mp4 없음)"; exit 1; }
  mv -f $OUT/j1.mp4 $OUT/j1_part_$rg.mp4
  echo "part $rg $(date +%H:%M)"
done
printf "file 'j1_part_0-7999.mp4'\nfile 'j1_part_8000-15999.mp4'\nfile 'j1_part_16000-23999.mp4'\nfile 'j1_part_24000-$END.mp4'\n" > $OUT/j1_parts.txt
cd $OUT && $R/work/video/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe -y -hide_banner -loglevel error -f concat -safe 0 -i j1_parts.txt -c copy j1.mp4 && echo "CONCAT OK $(date +%H:%M)"
