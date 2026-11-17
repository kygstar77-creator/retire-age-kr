# JT-1 11/17 PD: 렌더 뒤 deess --chirp 두 번 → 화면 → bgcheck (H-4 post_1117 그대로)
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr
EP=$R/work/research/longform/ep/JT-1; OUT=$R/work/video/out
PYTHONIOENCODING=utf-8 py -3.12 $R/work/video/deess.py $OUT/jt1.mp4 $OUT/jt1_ds1.mp4 --chirp > $EP/check/deess_1117a.log 2>&1; tail -3 $EP/check/deess_1117a.log
PYTHONIOENCODING=utf-8 py -3.12 $R/work/video/deess.py $OUT/jt1_ds1.mp4 $OUT/jt1_ds.mp4 --chirp > $EP/check/deess_1117b.log 2>&1; tail -4 $EP/check/deess_1117b.log
echo "DEESS_DONE $(date +%H:%M)"
PYTHONIOENCODING=utf-8 py -3.12 $R/work/lfrender.py screen $EP $OUT/jt1_ds.mp4 > $EP/check/screen_1117.log 2>&1; tail -3 $EP/check/screen_1117.log
PYTHONIOENCODING=utf-8 py -3.12 $R/work/bgcheck.py $OUT/jt1_ds.mp4 > $EP/check/bgcheck_1117.log 2>&1; tail -14 $EP/check/bgcheck_1117.log
echo "POST_DONE $(date +%H:%M)"
