# h5s_half 11/25 PD 끝 줄 뺀 렌더 — h2s_banpo/render_1120b.sh 사본
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr; D=$R/work/research/cardshorts/h5s_half; OUT=$R/work/video/out
cd $R/work/video
B=$D/bundle
[ -f $B/index.html ] || npx remotion bundle src/c1s_index.ts --out-dir=$B > $D/bundle.log 2>&1 || { echo BUNDLE_FAIL; exit 1; }
END=$(( $(PYTHONIOENCODING=utf-8 py -3.12 -c "import json;p=json.load(open('h5s_half.json',encoding='utf-8'));print(sum(s['frames'] for s in p['scenes']))") - 1 ))
LIST="0-$END"
for rg in $LIST; do
  [ -f out/h5h_part_$rg.mp4 ] && { echo "skip $rg"; continue; }
  for t in 1 2; do
    npx remotion render $B C1S out/h5h_part_$rg.mp4 --props=h5s_half.json --frames=$rg --pixel-format=yuv420p --concurrency=1 --timeout=120000 --offthreadvideo-cache-size-in-bytes=536870912 > $D/render1125b_part_${rg}_$t.log 2>&1 && break
    rm -f out/h5h_part_$rg.mp4; echo "retry $rg $t"
  done
  [ -f out/h5h_part_$rg.mp4 ] || { echo "PART_FAIL $rg"; exit 1; }
  echo "part $rg $(date +%H:%M)"
done
: > out/h5h_parts.txt; for rg in $LIST; do echo "file 'h5h_part_$rg.mp4'" >> out/h5h_parts.txt; done
cd out && $R/work/video/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe -y -hide_banner -loglevel error -f concat -safe 0 -i h5h_parts.txt -c copy h5s_half_c1.mp4 && echo "CONCAT OK"
cd .. && PYTHONIOENCODING=utf-8 py -3.12 $R/work/video/deess.py out/h5s_half_c1.mp4 out/h5s_half_c1_ds.mp4 --chirp-short > $D/deess_1125.log 2>&1; tail -3 $D/deess_1125.log
echo "H5H_DONE $(date +%H:%M)"
