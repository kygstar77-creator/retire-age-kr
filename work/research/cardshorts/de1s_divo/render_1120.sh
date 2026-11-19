# de1s_divo 11/19 PD: h2s_jamsil/render_1119.sh 사본 — 같은 묶음(h2s_jamsil/bundle, d-etf-1 소리·bg/detf 있음)에 나눈 wav 3개만 복사해 씀
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr; D=$R/work/research/cardshorts/de1s_divo; OUT=$R/work/video/out
cd $R/work/video
B=$R/work/research/cardshorts/h2s_jamsil/bundle
END=$(( $(PYTHONIOENCODING=utf-8 py -3.12 -c "import json;p=json.load(open('de1s_divo.json',encoding='utf-8'));print(sum(s['frames'] for s in p['scenes']))") - 1 ))
LIST="0-359 360-$END"
for rg in $LIST; do
  [ -f out/de1v_part_$rg.mp4 ] && { echo "skip $rg"; continue; }
  for t in 1 2 3 4 5 6; do
    npx remotion render $B C1S out/de1v_part_$rg.mp4 --props=de1s_divo.json --frames=$rg --pixel-format=yuv420p --concurrency=1 --timeout=120000 --offthreadvideo-cache-size-in-bytes=67108864 --offthreadvideo-video-threads=1 > $D/render_part_${rg}_$t.log 2>&1 && break
    rm -f out/de1v_part_$rg.mp4; echo "retry $rg $t"
  done
  [ -f out/de1v_part_$rg.mp4 ] || { echo "PART_FAIL $rg"; exit 1; }
  echo "part $rg $(date +%H:%M)"
done
: > out/de1v_parts.txt; for rg in $LIST; do echo "file 'de1v_part_$rg.mp4'" >> out/de1v_parts.txt; done
cd out && $R/work/video/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe -y -hide_banner -loglevel error -f concat -safe 0 -i de1v_parts.txt -c copy de1s_divo_c1.mp4 && echo "CONCAT OK"
cd .. && PYTHONIOENCODING=utf-8 py -3.12 $R/work/video/deess.py out/de1s_divo_c1.mp4 out/de1s_divo_c1_ds.mp4 --chirp-short > $D/deess_1120.log 2>&1; tail -3 $D/deess_1120.log
echo "DE1V_DONE $(date +%H:%M)"
