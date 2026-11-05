# K-1 11/5 PD: render_parts_1104 CONCAT(k1.mp4) → deess → 화면 → bgcheck (J-1 post_1025.sh 사본)
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr
EP=$R/work/research/longform/ep/K-1; OUT=$R/work/video/out
PYTHONIOENCODING=utf-8 py -3.12 $R/work/video/deess.py $OUT/k1.mp4 $OUT/k1_ds.mp4 --chirp-short > $EP/check/deess_1105.log 2>&1; tail -4 $EP/check/deess_1105.log
echo "DEESS_DONE $(date +%H:%M)"
PYTHONIOENCODING=utf-8 py -3.12 $R/work/lfrender.py screen $EP $OUT/k1_ds.mp4 > $EP/check/screen_1105.log 2>&1; tail -3 $EP/check/screen_1105.log
PYTHONIOENCODING=utf-8 py -3.12 $R/work/bgcheck.py $OUT/k1_ds.mp4 > $EP/check/bgcheck_1105.log 2>&1; tail -12 $EP/check/bgcheck_1105.log
echo "POST_DONE $(date +%H:%M)"
