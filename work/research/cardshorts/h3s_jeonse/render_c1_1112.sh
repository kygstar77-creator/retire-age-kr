# h3s_jeonse c1clip 11/12 PD: k1s_fix/render_parts_1111.sh 사본
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr; D=$R/work/research/cardshorts/h3s_jeonse; OUT=$R/work/video/out
cd $R/work/video
B=$R/work/research/cardshorts/k1s_fix/bundle   # 11/12 PD: k1s_fix 번들 다시 씀(디스크 37G, 새 번들 7.7G) — bg/h3/cut만 넣음
[ -f $B/index.html ] || npx remotion bundle src/c1s_index.ts --out-dir=$B > $D/bundle.log 2>&1 || { echo BUNDLE_FAIL; exit 1; }
END=$(( $(PYTHONIOENCODING=utf-8 py -3.12 -c "import json;p=json.load(open('h3s_jeonse.json',encoding='utf-8'));print(sum(s['frames'] for s in p['scenes']))") - 1 ))
LIST="0-449 450-899 900-$END"
for rg in $LIST; do
  [ -f out/h3c_part_$rg.mp4 ] && { echo "skip $rg"; continue; }
  for t in 1 2 3 4 5 6 7 8; do
    npx remotion render $B C1S out/h3c_part_$rg.mp4 --props=h3s_jeonse.json --frames=$rg --pixel-format=yuv420p --concurrency=1 --timeout=120000 --offthreadvideo-cache-size-in-bytes=67108864 --offthreadvideo-video-threads=1 > $D/render_part_${rg}_$t.log 2>&1 && break
    rm -f out/h3c_part_$rg.mp4; echo "retry $rg $t"
  done
  [ -f out/h3c_part_$rg.mp4 ] || { echo "PART_FAIL $rg"; exit 1; }
  echo "part $rg $(date +%H:%M)"
done
: > out/h3c_parts.txt; for rg in $LIST; do echo "file 'h3c_part_$rg.mp4'" >> out/h3c_parts.txt; done
cd out && $R/work/video/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe -y -hide_banner -loglevel error -f concat -safe 0 -i h3c_parts.txt -c copy h3s_jeonse_c1.mp4 && echo "CONCAT OK"
cd .. && PYTHONIOENCODING=utf-8 py -3.12 $R/work/video/deess.py out/h3s_jeonse_c1.mp4 out/h3s_jeonse_c1_ds.mp4 --chirp-short > $D/deess_1112c1b.log 2>&1; tail -3 $D/deess_1112c1b.log
echo "H3C_DONE $(date +%H:%M)"
