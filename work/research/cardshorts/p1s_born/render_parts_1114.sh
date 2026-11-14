# p1s_born 11/14 PD: k1s_fix/render_parts_1111.sh 사본 — 빈 메모리 2GB↑ 회차만 돌린다(11/13 No frame found 3번)
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr; D=$R/work/research/cardshorts/p1s_born; OUT=$R/work/video/out
cd $R/work/video
B=$R/work/research/cardshorts/p1s_born/bundle
[ -f $B/index.html ] || npx remotion bundle src/c1s_index.ts --out-dir=$B > $D/bundle.log 2>&1 || { echo BUNDLE_FAIL; exit 1; }
END=$(( $(PYTHONIOENCODING=utf-8 py -3.12 -c "import json;p=json.load(open('p1s_born.json',encoding='utf-8'));print(sum(s['frames'] for s in p['scenes']))") - 1 ))
LIST="0-299 300-599 600-$END"
for rg in $LIST; do
  [ -f out/p1b_part_$rg.mp4 ] && { echo "skip $rg"; continue; }
  for t in 1 2 3 4 5 6 7 8; do
    npx remotion render $B C1S out/p1b_part_$rg.mp4 --props=p1s_born.json --frames=$rg --pixel-format=yuv420p --concurrency=1 --timeout=120000 --offthreadvideo-cache-size-in-bytes=67108864 --offthreadvideo-video-threads=1 > $D/render_part_${rg}_$t.log 2>&1 && break
    rm -f out/p1b_part_$rg.mp4; echo "retry $rg $t"
  done
  [ -f out/p1b_part_$rg.mp4 ] || { echo "PART_FAIL $rg"; exit 1; }
  echo "part $rg $(date +%H:%M)"
done
: > out/p1b_parts.txt; for rg in $LIST; do echo "file 'p1b_part_$rg.mp4'" >> out/p1b_parts.txt; done
cd out && $R/work/video/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe -y -hide_banner -loglevel error -f concat -safe 0 -i p1b_parts.txt -c copy p1s_born_c1.mp4 && echo "CONCAT OK"
cd .. && PYTHONIOENCODING=utf-8 py -3.12 $R/work/video/deess.py out/p1s_born_c1.mp4 out/p1s_born_c1_ds.mp4 --chirp-short > $D/deess_1114.log 2>&1; tail -3 $D/deess_1111.log
echo "K1F_DONE $(date +%H:%M)"
