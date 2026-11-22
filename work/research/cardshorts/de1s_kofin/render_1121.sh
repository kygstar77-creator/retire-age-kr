# de1s_kofin 11/21 v2 PD: render_1120.sh 사본 — SOL 56.5%·출처 줄 운용사(prepub_1121) 바꾼 props로 다시, 로그 이름만 _v2
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr; D=$R/work/research/cardshorts/de1s_kofin; OUT=$R/work/video/out
cd $R/work/video
. $R/work/video/bundle_lib.sh
B=$(fm_bundle $D src/c1s_index.ts) || { echo BUNDLE_FAIL; exit 1; }
END=$(( $(PYTHONIOENCODING=utf-8 py -3.12 -c "import json;p=json.load(open('de1s_kofin.json',encoding='utf-8'));print(sum(s['frames'] for s in p['scenes']))") - 1 ))
LIST="0-299 300-$END"
for rg in $LIST; do
  [ -f out/de1k_part_$rg.mp4 ] && { echo "skip $rg"; continue; }
  for t in 1 2 3 4 5 6; do
    npx remotion render $B C1S out/de1k_part_$rg.mp4 --props=de1s_kofin.json --frames=$rg --pixel-format=yuv420p --concurrency=1 --timeout=120000 --offthreadvideo-cache-size-in-bytes=67108864 --offthreadvideo-video-threads=1 > $D/render_v2_part_${rg}_$t.log 2>&1 && break
    rm -f out/de1k_part_$rg.mp4; echo "retry $rg $t"
  done
  [ -f out/de1k_part_$rg.mp4 ] || { echo "PART_FAIL $rg"; exit 1; }
  echo "part $rg $(date +%H:%M)"
done
: > out/de1k_parts.txt; for rg in $LIST; do echo "file 'de1k_part_$rg.mp4'" >> out/de1k_parts.txt; done
cd out && $R/work/video/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe -y -hide_banner -loglevel error -f concat -safe 0 -i de1k_parts.txt -c copy de1s_kofin_c1.mp4 && echo "CONCAT OK" && fm_bundle_done $B
cd .. && PYTHONIOENCODING=utf-8 py -3.12 $R/work/video/deess.py out/de1s_kofin_c1.mp4 out/de1s_kofin_c1_ds.mp4 --chirp-short > $D/deess_1121.log 2>&1; tail -3 $D/deess_1121.log
echo "DE1V_DONE $(date +%H:%M)"
