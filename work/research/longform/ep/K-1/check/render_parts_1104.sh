# K-1 11/4 02시 PD: J-1 render_parts_1103.sh 사본(빈 메모리 2.7GB — 통째 렌더는 No frame found 위험). 15,668프레임 → 4천 토막 4개
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr
EP=$R/work/research/longform/ep/K-1
OUT=$R/work/video/out
END=$(PYTHONIOENCODING=utf-8 py -3.12 -c "import json;p=json.load(open('$R/work/video/k1.json',encoding='utf-8'));print(sum(s['frames'] for s in p['scenes'])-1)")
for rg in ${PARTS:-12000-$END 0-3999 4000-7999 8000-11999}; do
  if [ -f $OUT/k1_part_$rg.mp4 ]; then echo "skip $rg"; continue; fi
  PYTHONIOENCODING=utf-8 py -3.12 -u $R/work/lfrender.py render $EP --concurrency=${CONC:-2} --timeout=120000 --offthreadvideo-cache-size-in-bytes=268435456 --frames=$rg > $EP/check/render_part_$rg.log 2>&1
  if [ ! -f $OUT/k1.mp4 ] || [ $(stat -c %Y $OUT/k1.mp4) -lt $(stat -c %Y $EP/check/render_part_$rg.log) ] && ! grep -q "Rendered" $EP/check/render_part_$rg.log; then echo "FAIL $rg"; touch $EP/check/parts_done_1104; exit 1; fi
  [ -f $OUT/k1.mp4 ] || { echo "FAIL $rg (h3.mp4 없음)"; touch $EP/check/parts_done_1104; exit 1; }
  mv -f $OUT/k1.mp4 $OUT/k1_part_$rg.mp4
  echo "part $rg $(date +%H:%M)"
done
LIST="0-3999 4000-7999 8000-11999 12000-$END"
: > $OUT/k1_parts.txt; for rg in $LIST; do echo "file 'k1_part_$rg.mp4'" >> $OUT/k1_parts.txt; done
cd $OUT && $R/work/video/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe -y -hide_banner -loglevel error -f concat -safe 0 -i k1_parts.txt -c copy k1.mp4 && echo "CONCAT OK $(date +%H:%M)"; touch $EP/check/parts_done_1104
touch $EP/check/parts_done_1104
