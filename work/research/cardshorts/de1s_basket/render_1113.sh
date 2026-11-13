# de1s_basket c1clip 11/13 22:4x PD: h4s_rank/render_1113.sh 사본(토막 2개·캐시 1GB, 띄우기 전 빈 메모리 2GB↑) · k1s_fix 번들 public에 audio/de1s_basket 복사
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr; D=$R/work/research/cardshorts/de1s_basket; OUT=$R/work/video/out
cd $R/work/video
B=$R/work/research/cardshorts/k1s_fix/bundle   # 11/12 PD: k1s_fix 번들 다시 씀(디스크 37G, 새 번들 7.7G) — bg/h3/cut만 넣음
[ -f $B/index.html ] || npx remotion bundle src/c1s_index.ts --out-dir=$B > $D/bundle.log 2>&1 || { echo BUNDLE_FAIL; exit 1; }
END=$(( $(PYTHONIOENCODING=utf-8 py -3.12 -c "import json;p=json.load(open('de1s_basket.json',encoding='utf-8'));print(sum(s['frames'] for s in p['scenes']))") - 1 ))
LIST="0-459 460-$END"
for rg in $LIST; do
  [ -f out/de1b_part_$rg.mp4 ] && { echo "skip $rg"; continue; }
  for t in 1 2 3; do   # 회의 11/12: 3번 연속 실패면 멈춤
    npx remotion render $B C1S out/de1b_part_$rg.mp4 --props=de1s_basket.json --frames=$rg --pixel-format=yuv420p --concurrency=1 --timeout=120000 --offthreadvideo-cache-size-in-bytes=1073741824 --offthreadvideo-video-threads=1 > $D/render_part_${rg}_$t.log 2>&1 && break
    rm -f out/de1b_part_$rg.mp4; echo "retry $rg $t"
  done
  [ -f out/de1b_part_$rg.mp4 ] || { echo "PART_FAIL $rg"; exit 1; }
  echo "part $rg $(date +%H:%M)"
done
: > out/de1b_parts.txt; for rg in $LIST; do echo "file 'de1b_part_$rg.mp4'" >> out/de1b_parts.txt; done
cd out && $R/work/video/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe -y -hide_banner -loglevel error -f concat -safe 0 -i de1b_parts.txt -c copy de1s_basket_c1.mp4 && echo "CONCAT OK"
cd .. && PYTHONIOENCODING=utf-8 py -3.12 $R/work/video/deess.py out/de1s_basket_c1.mp4 out/de1s_basket_c1_ds.mp4 --chirp-short > $D/deess_1113.log 2>&1; tail -3 $D/deess_1113.log
echo "DE1B_DONE $(date +%H:%M)"
