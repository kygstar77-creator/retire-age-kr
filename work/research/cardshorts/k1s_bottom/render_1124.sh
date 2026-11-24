# k1s_bottom 11/24 PD 렌더 — h5s_jeonse/render_1121.sh 사본
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr; D=$R/work/research/cardshorts/k1s_bottom; OUT=$R/work/video/out
cd $R/work/video
. $R/work/video/bundle_lib.sh   # 11/22 렌더 끝나면 bundle 지움(public 통째 복사 약 11GB)
B=$(fm_bundle $D src/c1s_index.ts) || { echo BUNDLE_FAIL; exit 1; }
END=$(( $(PYTHONIOENCODING=utf-8 py -3.12 -c "import json;p=json.load(open('k1s_bottom.json',encoding='utf-8'));print(sum(s['frames'] for s in p['scenes']))") - 1 ))
LIST="0-$END"
for rg in $LIST; do
  [ -f out/k1b_part_$rg.mp4 ] && { echo "skip $rg"; continue; }
  for t in 1 2 3 4 5 6 7 8; do
    npx remotion render $B C1S out/k1b_part_$rg.mp4 --props=k1s_bottom.json --frames=$rg --pixel-format=yuv420p --concurrency=1 --timeout=120000 --offthreadvideo-cache-size-in-bytes=67108864 --offthreadvideo-video-threads=1 > $D/render_part_${rg}_$t.log 2>&1 && break
    rm -f out/k1b_part_$rg.mp4; echo "retry $rg $t"
  done
  [ -f out/k1b_part_$rg.mp4 ] || { echo "PART_FAIL $rg"; exit 1; }
  echo "part $rg $(date +%H:%M)"
done
: > out/k1b_parts.txt; for rg in $LIST; do echo "file 'k1b_part_$rg.mp4'" >> out/k1b_parts.txt; done
cd out && $R/work/video/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe -y -hide_banner -loglevel error -f concat -safe 0 -i k1b_parts.txt -c copy k1s_bottom_c1.mp4 && echo "CONCAT OK" && fm_bundle_done $B
cd .. && PYTHONIOENCODING=utf-8 py -3.12 $R/work/video/deess.py out/k1s_bottom_c1.mp4 out/k1s_bottom_c1_ds.mp4 --chirp-short > $D/deess_1124.log 2>&1; tail -3 $D/deess_1124.log
echo "K1R_DONE $(date +%H:%M)"
