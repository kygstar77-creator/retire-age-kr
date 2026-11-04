# j1s_cliff 11/4 PD: de1s_jepqhealth/render_parts_1103.sh 사본 — 새 묶음(bg/j1/stock/cut 포함)을 한 번 만들고 토막 4개·concurrency 1·재시도 4번
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr; D=$R/work/research/cardshorts/j1s_cliff; OUT=$R/work/video/out
cd $R/work/video
B=$D/bundle
[ -f $B/index.html ] || npx remotion bundle src/c1s_index.ts --out-dir=$B > $D/bundle.log 2>&1 || { echo BUNDLE_FAIL; exit 1; }
END=$(( $(PYTHONIOENCODING=utf-8 py -3.12 -c "import json;p=json.load(open('j1s_cliff.json',encoding='utf-8'));print(sum(s['frames'] for s in p['scenes']))") - 1 ))
LIST="0-349 350-699 700-1049 1050-$END"
for rg in $LIST; do
  [ -f out/j1c_part_$rg.mp4 ] && { echo "skip $rg"; continue; }
  for t in 1 2 3 4 5 6 7 8; do
    npx remotion render $B C1S out/j1c_part_$rg.mp4 --props=j1s_cliff.json --frames=$rg --pixel-format=yuv420p --concurrency=1 --timeout=120000 --offthreadvideo-cache-size-in-bytes=67108864 --offthreadvideo-video-threads=1 > $D/render_part_$rg.log 2>&1 && break
    rm -f out/j1c_part_$rg.mp4; echo "retry $rg $t"
  done
  [ -f out/j1c_part_$rg.mp4 ] || { echo "PART_FAIL $rg"; exit 1; }
  echo "part $rg $(date +%H:%M)"
done
: > out/j1c_parts.txt; for rg in $LIST; do echo "file 'j1c_part_$rg.mp4'" >> out/j1c_parts.txt; done
cd out && $R/work/video/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe -y -hide_banner -loglevel error -f concat -safe 0 -i j1c_parts.txt -c copy j1s_cliff_c1.mp4 && echo "CONCAT OK"
cd .. && PYTHONIOENCODING=utf-8 py -3.12 $R/work/video/deess.py out/j1s_cliff_c1.mp4 out/j1s_cliff_c1_ds.mp4 --chirp-short > $D/deess_1104.log 2>&1; tail -3 $D/deess_1104.log
echo "J1C_DONE $(date +%H:%M)"
