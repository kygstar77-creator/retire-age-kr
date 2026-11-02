# de1s_jepqhealth 11/3 PD: 통째 렌더 4번 No frame found(빈 메모리 0.7GB, 클립 7118320·6343634·6343634·8661806 번갈아) → J-1 render_parts_1103.sh처럼 토막·concurrency 1·토막마다 재시도 2번
# 2판: 구간만 자른 클립(cut/, 25fps)으로 0-299·300-599 통과, 600-901이 8661806_10 1.23초에서 3번 실패 → 30fps로 다시 자른 cut30/, 끝 토막 150프레임씩(앞 두 토막은 그대로 씀 — 같은 그림)
# 5판(06:5x): 빈 메모리 0.45GB — 해독 스레드 1·캐시 64MB·재시도 4번
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr; D=$R/work/research/cardshorts/de1s_jepqhealth; OUT=$R/work/video/out
B=C:/Users/강영준/AppData/Local/Temp/remotion-webpack-bundle-4tnpX9
cd $R/work/video
for rg in 0-299 300-599 600-749 750-901; do
  [ -f out/de1q_part_$rg.mp4 ] && { echo "skip $rg"; continue; }
  for t in 1 2 3 4; do
    npx remotion render $B C1S out/de1q_part_$rg.mp4 --props=de1s_jepqhealth.json --frames=$rg --pixel-format=yuv420p --concurrency=1 --timeout=120000 --offthreadvideo-cache-size-in-bytes=67108864 --offthreadvideo-video-threads=1 > $D/render_part_$rg.log 2>&1 && break
    rm -f out/de1q_part_$rg.mp4; echo "retry $rg $t"
  done
  [ -f out/de1q_part_$rg.mp4 ] || { echo "PART_FAIL $rg"; exit 1; }
  echo "part $rg $(date +%H:%M)"
done
printf "file 'de1q_part_0-299.mp4'
file 'de1q_part_300-599.mp4'
file 'de1q_part_600-749.mp4'
file 'de1q_part_750-901.mp4'
" > out/de1q_parts.txt
cd out && $R/work/video/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe -y -hide_banner -loglevel error -f concat -safe 0 -i de1q_parts.txt -c copy de1s_jepqhealth_c1.mp4 && echo "CONCAT OK"
cd .. && PYTHONIOENCODING=utf-8 py -3.12 $R/work/video/deess.py out/de1s_jepqhealth_c1.mp4 out/de1s_jepqhealth_c1_ds.mp4 --chirp-short > $D/deess_1103.log 2>&1; tail -3 $D/deess_1103.log
echo "DE1Q_DONE $(date +%H:%M)"
