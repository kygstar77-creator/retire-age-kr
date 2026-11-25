# H-6 11/25 23:5x PD(1122판 그대로 + 끝에 deess):  H-5 render_parts_1121.sh 꼴. 16314프레임 → 1000프레임 토막 17개, concurrency 1. 끝난 토막은 건너뜀(끊기면 다시 돌리면 이어짐)
# 이음은 concat -c copy 금지(lessons 11/21) → 화면만 concat(h6_vonly) + trim_concat_1122.py로 소리 얹음
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr
mkdir -p C:/fm_render_tmp; export TEMP=C:/fm_render_tmp TMP=C:/fm_render_tmp
EP=$R/work/research/longform/ep/H-6
OUT=$R/work/video/out
FF=$R/work/video/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe
LIST=""
for s in 0 1000 2000 3000 4000 5000 6000 7000 8000 9000 10000 11000 12000 13000 14000 15000; do LIST="$LIST $s-$((s+999))"; done; LIST="$LIST 16000-"
for rg in $LIST; do
  [ -f $OUT/h6_part_$rg.mp4 ] && { echo "skip $rg"; continue; }
  for t in 1 2 3; do
    rm -f $OUT/h6.mp4
    PYTHONIOENCODING=utf-8 py -3.12 -u $R/work/lfrender.py render $EP --concurrency=1 --timeout=120000 --offthreadvideo-cache-size-in-bytes=${CACHE:-1073741824} --frames=$rg > $EP/check/render_c_$rg.log 2>&1
    if [ -f $OUT/h6.mp4 ] && ! grep -q "An error occurred" $EP/check/render_c_$rg.log; then
      rm -rf C:/fm_render_tmp/remotion-* 2>/dev/null; mv -f $OUT/h6.mp4 $OUT/h6_part_$rg.mp4; echo "part $rg try$t $(date +%H:%M)"; break
    fi
    echo "retry $rg try$t $(date +%H:%M)"; cp $EP/check/render_c_$rg.log $EP/check/render_c_${rg}_fail$t.log
  done
  [ -f $OUT/h6_part_$rg.mp4 ] || { echo "FAIL $rg"; exit 1; }
done
: > $OUT/h6_parts.txt; for rg in $LIST; do echo "file 'h6_part_$rg.mp4'" >> $OUT/h6_parts.txt; done
cd $OUT && $FF -y -hide_banner -loglevel error -f concat -safe 0 -i h6_parts.txt -an -c:v copy h6_vonly.mp4 && echo "VONLY OK $(date +%H:%M)"
PYTHONIOENCODING=utf-8 py -3.12 $EP/check/trim_concat_1122.py && echo "TRIM OK $(date +%H:%M)"
cd $R/work/video && PYTHONIOENCODING=utf-8 py -3.12 deess.py out/h6.mp4 out/h6_dsl1125.mp4 --chirp-short > $EP/check/dsl_1125pd.log 2>&1; tail -3 $EP/check/dsl_1125pd.log
echo "H6_DONE $(date +%H:%M)"
