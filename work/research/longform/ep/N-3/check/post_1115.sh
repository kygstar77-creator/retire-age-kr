# N-3 11/15 PD: 렌더 뒤 deess --chirp 두 번 → 화면 → bgcheck (H-4 post_1112 그대로)
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr
EP=$R/work/research/longform/ep/N-3; OUT=$R/work/video/out
PYTHONIOENCODING=utf-8 py -3.12 $R/work/video/deess.py $OUT/n3.mp4 $OUT/n3_ds1.mp4 --chirp > $EP/check/deess_1115a.log 2>&1; tail -3 $EP/check/deess_1112a.log
PYTHONIOENCODING=utf-8 py -3.12 $R/work/video/deess.py $OUT/n3_ds1.mp4 $OUT/n3_ds.mp4 --chirp > $EP/check/deess_1115b.log 2>&1; tail -4 $EP/check/deess_1112b.log
echo "DEESS_DONE $(date +%H:%M)"
PYTHONIOENCODING=utf-8 py -3.12 $R/work/lfrender.py screen $EP $OUT/n3_ds.mp4 > $EP/check/screen_1115.log 2>&1; tail -3 $EP/check/screen_1112.log
PYTHONIOENCODING=utf-8 py -3.12 $R/work/bgcheck.py $OUT/n3_ds.mp4 > $EP/check/bgcheck_1115.log 2>&1; tail -14 $EP/check/bgcheck_1112.log
echo "POST_DONE $(date +%H:%M)"
