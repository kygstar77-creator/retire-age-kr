# P-3 11/10 PD: 다시 렌더(visual 판 32장) 뒤 deess --chirp 두 번(11/9 실측: 한 번 -11.9 미달, 두 번 -12.3) → 화면 → bgcheck
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr
EP=$R/work/research/longform/ep/P-3; OUT=$R/work/video/out
PYTHONIOENCODING=utf-8 py -3.12 $R/work/video/deess.py $OUT/p3.mp4 $OUT/p3_ds1.mp4 --chirp > $EP/check/deess_1110a.log 2>&1; tail -3 $EP/check/deess_1110a.log
PYTHONIOENCODING=utf-8 py -3.12 $R/work/video/deess.py $OUT/p3_ds1.mp4 $OUT/p3_ds.mp4 --chirp > $EP/check/deess_1110b.log 2>&1; tail -4 $EP/check/deess_1110b.log
echo "DEESS_DONE $(date +%H:%M)"
PYTHONIOENCODING=utf-8 py -3.12 $R/work/lfrender.py screen $EP $OUT/p3_ds.mp4 > $EP/check/screen_1110.log 2>&1; tail -3 $EP/check/screen_1110.log
PYTHONIOENCODING=utf-8 py -3.12 $R/work/bgcheck.py $OUT/p3_ds.mp4 > $EP/check/bgcheck_1110.log 2>&1; tail -14 $EP/check/bgcheck_1110.log
echo "POST_DONE $(date +%H:%M)"
