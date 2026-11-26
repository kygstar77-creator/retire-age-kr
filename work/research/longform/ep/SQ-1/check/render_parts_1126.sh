# SQ-1 11/26 15:2x PD — H-6 check/render_parts_1125b.sh 사본(3토막·끝 deess). 14805프레임. 끝난 토막은 건너뜀(끊기면 다시 돌리면 이어짐)
# 이음은 concat -c copy 금지(lessons 11/21) → 화면만 concat(sq1_vonly) + trim_concat_1126.py로 소리 얹음
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr
mkdir -p C:/fm_render_tmp; export TEMP=C:/fm_render_tmp TMP=C:/fm_render_tmp
EP=$R/work/research/longform/ep/SQ-1
OUT=$R/work/video/out
FF=$R/work/video/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe
LIST=""
LIST="0-999 1000-7999 8000-"   # H-6처럼 3토막(토막마다 public 복사 시간 줄임)
for rg in $LIST; do
  [ -f $OUT/sq1_part_$rg.mp4 ] && { echo "skip $rg"; continue; }
  for t in 1 2 3; do
    rm -f $OUT/sq1.mp4
    PYTHONIOENCODING=utf-8 py -3.12 -u $R/work/lfrender.py render $EP --concurrency=1 --timeout=120000 --offthreadvideo-cache-size-in-bytes=${CACHE:-1073741824} --frames=$rg > $EP/check/render_c_$rg.log 2>&1
    if [ -f $OUT/sq1.mp4 ] && ! grep -q "An error occurred" $EP/check/render_c_$rg.log; then
      rm -rf C:/fm_render_tmp/remotion-* 2>/dev/null; mv -f $OUT/sq1.mp4 $OUT/sq1_part_$rg.mp4; echo "part $rg try$t $(date +%H:%M)"; break
    fi
    echo "retry $rg try$t $(date +%H:%M)"; cp $EP/check/render_c_$rg.log $EP/check/render_c_${rg}_fail$t.log
  done
  [ -f $OUT/sq1_part_$rg.mp4 ] || { echo "FAIL $rg"; exit 1; }
done
: > $OUT/sq1_parts.txt; for rg in $LIST; do echo "file 'sq1_part_$rg.mp4'" >> $OUT/sq1_parts.txt; done
cd $OUT && $FF -y -hide_banner -loglevel error -f concat -safe 0 -i sq1_parts.txt -an -c:v copy sq1_vonly.mp4 && echo "VONLY OK $(date +%H:%M)"
PYTHONIOENCODING=utf-8 py -3.12 $EP/check/trim_concat_1126.py && echo "TRIM OK $(date +%H:%M)"
cd $R/work/video && PYTHONIOENCODING=utf-8 py -3.12 deess.py out/sq1.mp4 out/sq1_dsl1126.mp4 --chirp-short > $EP/check/dsl_1126pd.log 2>&1; tail -3 $EP/check/dsl_1125pd.log
echo "SQ1_DONE $(date +%H:%M)"
