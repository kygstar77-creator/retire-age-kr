# h4s_new15 c1clip 11/15 PD: h4s_ladder/render_1114.sh 사본(이름만 바꿈 — 1천 프레임 미만 토막·캐시 1GB, 띄우기 전 빈 메모리 2GB↑)
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr; D=$R/work/research/cardshorts/h4s_new15; OUT=$R/work/video/out
cd $R/work/video
B=$D/bundle
[ -f $B/index.html ] || npx remotion bundle src/c1s_index.ts --out-dir=$B > $D/bundle.log 2>&1 || { echo BUNDLE_FAIL; exit 1; }
END=$(( $(PYTHONIOENCODING=utf-8 py -3.12 -c "import json;p=json.load(open('h4s_new15.json',encoding='utf-8'));print(sum(s['frames'] for s in p['scenes']))") - 1 ))
LIST="0-469 470-$END"
for rg in $LIST; do
  [ -f out/h4n_part_$rg.mp4 ] && { echo "skip $rg"; continue; }
  for t in 1 2 3 4 5 6 7 8; do
    npx remotion render $B C1S out/h4n_part_$rg.mp4 --props=h4s_new15.json --frames=$rg --pixel-format=yuv420p --concurrency=1 --timeout=120000 --offthreadvideo-cache-size-in-bytes=1073741824 --offthreadvideo-video-threads=1 > $D/render_part_${rg}_$t.log 2>&1 && break
    rm -f out/h4n_part_$rg.mp4; echo "retry $rg $t"
  done
  [ -f out/h4n_part_$rg.mp4 ] || { echo "PART_FAIL $rg"; exit 1; }
  echo "part $rg $(date +%H:%M)"
done
: > out/h4n_parts.txt; for rg in $LIST; do echo "file 'h4n_part_$rg.mp4'" >> out/h4n_parts.txt; done
cd out && $R/work/video/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe -y -hide_banner -loglevel error -f concat -safe 0 -i h4n_parts.txt -c copy h4s_new15_c1.mp4 && echo "CONCAT OK"
cd .. && PYTHONIOENCODING=utf-8 py -3.12 $R/work/video/deess.py out/h4s_new15_c1.mp4 out/h4s_new15_c1_ds.mp4 --chirp-short > $D/deess_1115.log 2>&1; tail -3 $D/deess_1115.log
echo "H4L_DONE $(date +%H:%M)"
