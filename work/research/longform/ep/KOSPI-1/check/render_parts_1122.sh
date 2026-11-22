# KOSPI-1 11/22 22:4x PD: H-6 render_parts_1122.sh 꼴. 14457프레임 → 토막 15개, concurrency 1. 끝난 토막은 건너뜀(끊기면 다시 돌리면 이어짐)
# 이음은 concat -c copy 금지(lessons 11/21) → 화면만 concat(kospi1_vonly) + trim_concat_1122.py로 소리 얹음
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr
mkdir -p C:/fm_render_tmp; export TEMP=C:/fm_render_tmp TMP=C:/fm_render_tmp
EP=$R/work/research/longform/ep/KOSPI-1
OUT=$R/work/video/out
FF=$R/work/video/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe
LIST=""
for s in 0 1000 2000 3000 4000 5000 6000 7000 8000 9000 10000 11000 12000 13000; do LIST="$LIST $s-$((s+999))"; done; LIST="$LIST 14000-"
for rg in $LIST; do
  [ -f $OUT/kospi1_part_$rg.mp4 ] && { echo "skip $rg"; continue; }
  for t in 1 2 3; do
    rm -f $OUT/kospi1.mp4
    PYTHONIOENCODING=utf-8 py -3.12 -u $R/work/lfrender.py render $EP --concurrency=1 --timeout=120000 --offthreadvideo-cache-size-in-bytes=${CACHE:-1073741824} --frames=$rg > $EP/check/render_d_$rg.log 2>&1
    if [ -f $OUT/kospi1.mp4 ] && ! grep -q "An error occurred" $EP/check/render_d_$rg.log; then
      rm -rf C:/fm_render_tmp/remotion-* 2>/dev/null; mv -f $OUT/kospi1.mp4 $OUT/kospi1_part_$rg.mp4; echo "part $rg try$t $(date +%H:%M)"; break
    fi
    echo "retry $rg try$t $(date +%H:%M)"; cp $EP/check/render_d_$rg.log $EP/check/render_d_${rg}_fail$t.log
  done
  [ -f $OUT/kospi1_part_$rg.mp4 ] || { echo "FAIL $rg"; exit 1; }
done
: > $OUT/kospi1_parts.txt; for rg in $LIST; do echo "file 'kospi1_part_$rg.mp4'" >> $OUT/kospi1_parts.txt; done
cd $OUT && $FF -y -hide_banner -loglevel error -f concat -safe 0 -i kospi1_parts.txt -an -c:v copy kospi1_vonly.mp4 && echo "VONLY OK $(date +%H:%M)"
PYTHONIOENCODING=utf-8 py -3.12 $EP/check/trim_concat_1122.py && echo "TRIM OK $(date +%H:%M)"
