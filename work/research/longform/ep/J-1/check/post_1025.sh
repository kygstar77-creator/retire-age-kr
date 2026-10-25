# J-1 10/25 PD: 10/23 05:58 CONCAT(j1.mp4, 받아쓰기 다시 받기 17줄 반영) → deess → 화면 → bgcheck
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr
EP=$R/work/research/longform/ep/J-1; OUT=$R/work/video/out
PYTHONIOENCODING=utf-8 py -3.12 $R/work/video/deess.py $OUT/j1.mp4 $OUT/j1_ds9.mp4 --chirp-short > $EP/check/deess9_1025.log 2>&1; tail -4 $EP/check/deess9_1025.log
echo "DEESS_DONE $(date +%H:%M)"
PYTHONIOENCODING=utf-8 py -3.12 $R/work/lfrender.py screen $EP $OUT/j1_ds9.mp4 > $EP/check/screen_1025.log 2>&1; tail -3 $EP/check/screen_1025.log
PYTHONIOENCODING=utf-8 py -3.12 $R/work/bgcheck.py $OUT/j1_ds9.mp4 > $EP/check/bgcheck_1025.log 2>&1; tail -12 $EP/check/bgcheck_1025.log
echo "POST_DONE $(date +%H:%M)"
