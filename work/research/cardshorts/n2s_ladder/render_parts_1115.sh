# n2s_ladder 11/15 PD: x1s_even/render_parts_1114.sh 사본
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr; D=$R/work/research/cardshorts/n2s_ladder; OUT=$R/work/video/out
cd $R/work/video
B=$R/work/research/cardshorts/n2s_ladder/bundle
[ -f $B/index.html ] || npx remotion bundle src/c1s_index.ts --out-dir=$B > $D/bundle.log 2>&1 || { echo BUNDLE_FAIL; exit 1; }
END=$(( $(PYTHONIOENCODING=utf-8 py -3.12 -c "import json;p=json.load(open('n2s_ladder.json',encoding='utf-8'));print(sum(s['frames'] for s in p['scenes']))") - 1 ))
LIST="0-299 300-599 600-$END"
for rg in $LIST; do
  [ -f out/n2l_part_$rg.mp4 ] && { echo "skip $rg"; continue; }
  for t in 1 2 3 4 5 6 7 8; do
    npx remotion render $B C1S out/n2l_part_$rg.mp4 --props=n2s_ladder.json --frames=$rg --pixel-format=yuv420p --concurrency=1 --timeout=120000 --offthreadvideo-cache-size-in-bytes=67108864 --offthreadvideo-video-threads=1 > $D/render_part_${rg}_$t.log 2>&1 && break
    rm -f out/n2l_part_$rg.mp4; echo "retry $rg $t"
  done
  [ -f out/n2l_part_$rg.mp4 ] || { echo "PART_FAIL $rg"; exit 1; }
  echo "part $rg $(date +%H:%M)"
done
: > out/n2l_parts.txt; for rg in $LIST; do echo "file 'n2l_part_$rg.mp4'" >> out/n2l_parts.txt; done
cd out && $R/work/video/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe -y -hide_banner -loglevel error -f concat -safe 0 -i n2l_parts.txt -c copy n2s_ladder_c1.mp4 && echo "CONCAT OK"
cd .. && PYTHONIOENCODING=utf-8 py -3.12 $R/work/video/deess.py out/n2s_ladder_c1.mp4 out/n2s_ladder_c1_ds.mp4 --chirp-short > $D/deess_1115.log 2>&1; tail -3 $D/deess_1114.log
echo "N2L_DONE $(date +%H:%M)"
