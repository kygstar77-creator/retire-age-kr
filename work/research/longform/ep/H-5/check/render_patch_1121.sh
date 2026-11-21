# H-5 11/21 PD: 토막 시작 0.1~0.6초 뒤 소리 끊김(50ms 0) 7곳 — 경계 3초 전부터 5초 토막을 렌더해 소리만 바꿔 끼울 재료
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr
export TEMP=C:/fm_render_tmp TMP=C:/fm_render_tmp
EP=$R/work/research/longform/ep/H-5; OUT=$R/work/video/out
for b in 2000 4000 5000 6000 7000 9000 10000; do
  [ -f $OUT/h5p_$b.mp4 ] && { echo "skip $b"; continue; }
  for t in 1 2; do
    rm -f $OUT/h5.mp4
    PYTHONIOENCODING=utf-8 py -3.12 -u $R/work/lfrender.py render $EP --concurrency=1 --timeout=120000 --frames=$((b-90))-$((b+59)) > $EP/check/render_p_$b.log 2>&1
    rm -rf C:/fm_render_tmp/remotion-* 2>/dev/null
    if [ -f $OUT/h5.mp4 ] && ! grep -q "An error occurred" $EP/check/render_p_$b.log; then mv -f $OUT/h5.mp4 $OUT/h5p_$b.mp4; echo "patch $b try$t $(date +%H:%M)"; break; fi
    echo "retry $b try$t $(date +%H:%M)"
  done
done
echo DONE $(date +%H:%M)
