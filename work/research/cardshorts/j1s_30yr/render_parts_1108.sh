# j1s_30yr 11/8 PD: j1s_couple/render_parts_1104.sh 사본(새 묶음, 토막 3개·concurrency 1·재시도 8번)
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr; D=$R/work/research/cardshorts/j1s_30yr; OUT=$R/work/video/out
cd $R/work/video
B=$R/work/research/cardshorts/j1s_30yr/bundle
[ -f $B/index.html ] || npx remotion bundle src/c1s_index.ts --out-dir=$B > $D/bundle.log 2>&1 || { echo BUNDLE_FAIL; exit 1; }
END=$(( $(PYTHONIOENCODING=utf-8 py -3.12 -c "import json;p=json.load(open('j1s_30yr.json',encoding='utf-8'));print(sum(s['frames'] for s in p['scenes']))") - 1 ))
LIST="0-299 300-599 600-$END"
for rg in $LIST; do
  [ -f out/j1y_part_$rg.mp4 ] && { echo "skip $rg"; continue; }
  for t in 1 2 3 4 5 6 7 8; do
    npx remotion render $B C1S out/j1y_part_$rg.mp4 --props=j1s_30yr.json --frames=$rg --pixel-format=yuv420p --concurrency=1 --timeout=120000 --offthreadvideo-cache-size-in-bytes=67108864 --offthreadvideo-video-threads=1 > $D/render_part_${rg}_$t.log 2>&1 && break
    rm -f out/j1y_part_$rg.mp4; echo "retry $rg $t"
  done
  [ -f out/j1y_part_$rg.mp4 ] || { echo "PART_FAIL $rg"; exit 1; }
  echo "part $rg $(date +%H:%M)"
done
: > out/j1y_parts.txt; for rg in $LIST; do echo "file 'j1y_part_$rg.mp4'" >> out/j1y_parts.txt; done
cd out && $R/work/video/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe -y -hide_banner -loglevel error -f concat -safe 0 -i j1y_parts.txt -c copy j1s_30yr_c1.mp4 && echo "CONCAT OK"
cd .. && PYTHONIOENCODING=utf-8 py -3.12 $R/work/video/deess.py out/j1s_30yr_c1.mp4 out/j1s_30yr_c1_ds.mp4 --chirp-short > $D/deess_1108.log 2>&1; tail -3 $D/deess_1108.log
echo "J1Y_DONE $(date +%H:%M)"
