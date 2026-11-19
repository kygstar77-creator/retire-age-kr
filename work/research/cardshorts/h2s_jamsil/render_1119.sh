# h2s_jamsil 11/19 PD: h2s_jamsil/render_parts_1118.sh 사본 (bg/h2/cut 새 컷이라 새 bundle)
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr; D=$R/work/research/cardshorts/h2s_jamsil; OUT=$R/work/video/out
cd $R/work/video
B=$D/bundle
[ -f $B/index.html ] || npx remotion bundle src/c1s_index.ts --out-dir=$B > $D/bundle.log 2>&1 || { echo BUNDLE_FAIL; exit 1; }
END=$(( $(PYTHONIOENCODING=utf-8 py -3.12 -c "import json;p=json.load(open('h2s_jamsil.json',encoding='utf-8'));print(sum(s['frames'] for s in p['scenes']))") - 1 ))
LIST="0-499 500-999 1000-$END"
for rg in $LIST; do
  [ -f out/h2j_part_$rg.mp4 ] && { echo "skip $rg"; continue; }
  for t in 1 2 3 4 5 6 7 8; do
    npx remotion render $B C1S out/h2j_part_$rg.mp4 --props=h2s_jamsil.json --frames=$rg --pixel-format=yuv420p --concurrency=1 --timeout=120000 --offthreadvideo-cache-size-in-bytes=67108864 --offthreadvideo-video-threads=1 > $D/render_part_${rg}_$t.log 2>&1 && break
    rm -f out/h2j_part_$rg.mp4; echo "retry $rg $t"
  done
  [ -f out/h2j_part_$rg.mp4 ] || { echo "PART_FAIL $rg"; exit 1; }
  echo "part $rg $(date +%H:%M)"
done
: > out/h2j_parts.txt; for rg in $LIST; do echo "file 'h2j_part_$rg.mp4'" >> out/h2j_parts.txt; done
cd out && $R/work/video/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe -y -hide_banner -loglevel error -f concat -safe 0 -i h2j_parts.txt -c copy h2s_jamsil_c1.mp4 && echo "CONCAT OK"
cd .. && PYTHONIOENCODING=utf-8 py -3.12 $R/work/video/deess.py out/h2s_jamsil_c1.mp4 out/h2s_jamsil_c1_ds.mp4 --chirp-short > $D/deess_1119.log 2>&1; tail -3 $D/deess_1119.log
echo "H2J_DONE $(date +%H:%M)"
