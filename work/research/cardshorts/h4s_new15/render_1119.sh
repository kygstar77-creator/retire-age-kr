# h4s_new15 v2 11/19 PD(답 5초·A98): render_1115.sh 사본
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr; D=$R/work/research/cardshorts/h4s_new15; OUT=$R/work/video/out
cd $R/work/video
B=$R/work/research/cardshorts/n2s_ladder/bundle_v2   # 11/19 같은 c1s_index 새 번들
[ -f $B/index.html ] || npx remotion bundle src/c1s_index.ts --out-dir=$B > $D/bundle.log 2>&1 || { echo BUNDLE_FAIL; exit 1; }
END=$(( $(PYTHONIOENCODING=utf-8 py -3.12 -c "import json;p=json.load(open('h4s_new15_v2.json',encoding='utf-8'));print(sum(s['frames'] for s in p['scenes']))") - 1 ))
LIST="0-469 470-$END"
for rg in $LIST; do
  [ -f out/h4n2_part_$rg.mp4 ] && { echo "skip $rg"; continue; }
  for t in 1 2 3 4 5 6 7 8; do
    npx remotion render $B C1S out/h4n2_part_$rg.mp4 --props=h4s_new15_v2.json --frames=$rg --pixel-format=yuv420p --concurrency=1 --timeout=120000 --offthreadvideo-cache-size-in-bytes=1073741824 --offthreadvideo-video-threads=1 > $D/render1119_part_${rg}_$t.log 2>&1 && break
    rm -f out/h4n2_part_$rg.mp4; echo "retry $rg $t"
  done
  [ -f out/h4n2_part_$rg.mp4 ] || { echo "PART_FAIL $rg"; exit 1; }
  echo "part $rg $(date +%H:%M)"
done
: > out/h4n2_parts.txt; for rg in $LIST; do echo "file 'h4n2_part_$rg.mp4'" >> out/h4n2_parts.txt; done
cd out && $R/work/video/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe -y -hide_banner -loglevel error -f concat -safe 0 -i h4n2_parts.txt -c copy h4s_new15_v2.mp4 && echo "CONCAT OK"
cd .. && PYTHONIOENCODING=utf-8 py -3.12 $R/work/video/deess.py out/h4s_new15_v2.mp4 out/h4s_new15_v2_ds.mp4 --chirp-short > $D/deess_1119.log 2>&1; tail -3 $D/deess_1119.log
echo "H4N2_DONE $(date +%H:%M)"
