# D-ETF-1 10/27 PD: 네 토막 렌더 → deess → 화면·bgcheck
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr; EP=$R/work/research/longform/ep/D-ETF-1; OUT=$R/work/video/out
bash $EP/check/render_parts.sh > $EP/check/render_parts_run_1027.log 2>&1; tail -3 $EP/check/render_parts_run_1027.log
grep -q "CONCAT OK" $EP/check/render_parts_run_1027.log || { echo RENDER_FAIL; exit 1; }
PYTHONIOENCODING=utf-8 py -3.12 $R/work/video/deess.py $OUT/detf1.mp4 $OUT/detf1_ds.mp4 --chirp-short > $EP/check/deess_1027.log 2>&1; tail -4 $EP/check/deess_1027.log
PYTHONIOENCODING=utf-8 py -3.12 $R/work/lfrender.py screen $EP $OUT/detf1_ds.mp4 > $EP/check/screen_1027.log 2>&1; tail -3 $EP/check/screen_1027.log
PYTHONIOENCODING=utf-8 py -3.12 $R/work/bgcheck.py $OUT/detf1_ds.mp4 > $EP/check/bgcheck_1027.log 2>&1; tail -12 $EP/check/bgcheck_1027.log
echo "ALL_DONE $(date +%H:%M)"
