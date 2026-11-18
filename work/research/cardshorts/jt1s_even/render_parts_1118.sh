# jt1s_even 11/18 PD: n3s_family/render_parts_1116.sh 사본
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr; D=$R/work/research/cardshorts/jt1s_even; OUT=$R/work/video/out
cd $R/work/video
B=$D/bundle2  # 11/18 23시 컷 바꿈 → 새 bundle
[ -f $B/index.html ] || npx remotion bundle src/c1s_index.ts --out-dir=$B > $D/bundle.log 2>&1 || { echo BUNDLE_FAIL; exit 1; }
END=$(( $(PYTHONIOENCODING=utf-8 py -3.12 -c "import json;p=json.load(open('jt1s_even.json',encoding='utf-8'));print(sum(s['frames'] for s in p['scenes']))") - 1 ))
LIST="0-449 450-899 900-$END"
for rg in $LIST; do
  [ -f out/jt1e_part_$rg.mp4 ] && { echo "skip $rg"; continue; }
  for t in 1 2 3 4 5 6 7 8; do
    npx remotion render $B C1S out/jt1e_part_$rg.mp4 --props=jt1s_even.json --frames=$rg --pixel-format=yuv420p --concurrency=1 --timeout=120000 --offthreadvideo-cache-size-in-bytes=67108864 --offthreadvideo-video-threads=1 > $D/render_part_${rg}_$t.log 2>&1 && break
    rm -f out/jt1e_part_$rg.mp4; echo "retry $rg $t"
  done
  [ -f out/jt1e_part_$rg.mp4 ] || { echo "PART_FAIL $rg"; exit 1; }
  echo "part $rg $(date +%H:%M)"
done
: > out/jt1e_parts.txt; for rg in $LIST; do echo "file 'jt1e_part_$rg.mp4'" >> out/jt1e_parts.txt; done
cd out && $R/work/video/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe -y -hide_banner -loglevel error -f concat -safe 0 -i jt1e_parts.txt -c copy jt1s_even_c1.mp4 && echo "CONCAT OK"
cd .. && PYTHONIOENCODING=utf-8 py -3.12 $R/work/video/deess.py out/jt1s_even_c1.mp4 out/jt1s_even_c1_ds.mp4 --chirp-short > $D/deess_1118.log 2>&1; tail -3 $D/deess_1118.log
echo "JT1E_DONE $(date +%H:%M)"
