# P-3 11/9 PD: render_parts_1109 CONCAT(p3.mp4) → deess → 화면 → bgcheck (K-1 post_1105.sh 사본, 장편이라 --chirp)
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr
EP=$R/work/research/longform/ep/P-3; OUT=$R/work/video/out
PYTHONIOENCODING=utf-8 py -3.12 $R/work/video/deess.py $OUT/p3.mp4 $OUT/p3_ds.mp4 --chirp > $EP/check/deess_1109.log 2>&1; tail -4 $EP/check/deess_1109.log
echo "DEESS_DONE $(date +%H:%M)"
PYTHONIOENCODING=utf-8 py -3.12 $R/work/lfrender.py screen $EP $OUT/p3_ds.mp4 > $EP/check/screen_1109.log 2>&1; tail -3 $EP/check/screen_1109.log
PYTHONIOENCODING=utf-8 py -3.12 $R/work/bgcheck.py $OUT/p3_ds.mp4 > $EP/check/bgcheck_1109.log 2>&1; tail -12 $EP/check/bgcheck_1109.log
echo "POST_DONE $(date +%H:%M)"
