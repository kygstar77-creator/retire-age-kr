# D-ETF-1 10/27 PD(J-1 render_parts.sh 복사): 네 토막 — 끝 토막 먼저, 컴포지션 DETF1·props detf1.json
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr
EP=$R/work/research/longform/ep/D-ETF-1
OUT=$R/work/video/out
END=$(PYTHONIOENCODING=utf-8 py -3.12 -c "import json;p=json.load(open('$R/work/video/detf1.json',encoding='utf-8'));print(sum(s['frames'] for s in p['scenes'])-1)")
Q=$(( (END+1) / 4 ))
P1="0-$((Q-1))"; P2="$Q-$((2*Q-1))"; P3="$((2*Q))-$((3*Q-1))"; P4="$((3*Q))-$END"
for rg in ${PARTS:-$P4 $P1 $P2 $P3}; do
  if [ -f $OUT/detf1_part_$rg.mp4 ]; then echo "skip $rg"; continue; fi
  PYTHONIOENCODING=utf-8 py -3.12 -u $R/work/lfrender.py render $EP --concurrency=${CONC:-2} --timeout=120000 --offthreadvideo-cache-size-in-bytes=536870912 --frames=$rg > $EP/check/render_part_$rg.log 2>&1
  if ! grep -q "Rendered\|렌더 끝\|screen" $EP/check/render_part_$rg.log && [ ! -f $OUT/detf1.mp4 ]; then echo "FAIL $rg"; exit 1; fi
  [ -f $OUT/detf1.mp4 ] || { echo "FAIL $rg (detf1.mp4 없음)"; exit 1; }
  mv -f $OUT/detf1.mp4 $OUT/detf1_part_$rg.mp4
  echo "part $rg $(date +%H:%M)"
done
printf "file 'detf1_part_$P1.mp4'\nfile 'detf1_part_$P2.mp4'\nfile 'detf1_part_$P3.mp4'\nfile 'detf1_part_$P4.mp4'\n" > $OUT/detf1_parts.txt
cd $OUT && $R/work/video/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe -y -hide_banner -loglevel error -f concat -safe 0 -i detf1_parts.txt -c copy detf1.mp4 && echo "CONCAT OK $(date +%H:%M)"
