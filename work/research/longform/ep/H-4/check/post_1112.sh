# H-4 11/12 PD: 렌더 뒤 deess --chirp 두 번(P-3 실측 한 번 미달) → 화면 → bgcheck
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr
EP=$R/work/research/longform/ep/H-4; OUT=$R/work/video/out
PYTHONIOENCODING=utf-8 py -3.12 $R/work/video/deess.py $OUT/h4.mp4 $OUT/h4_ds1.mp4 --chirp > $EP/check/deess_1112a.log 2>&1; tail -3 $EP/check/deess_1112a.log
PYTHONIOENCODING=utf-8 py -3.12 $R/work/video/deess.py $OUT/h4_ds1.mp4 $OUT/h4_ds.mp4 --chirp > $EP/check/deess_1112b.log 2>&1; tail -4 $EP/check/deess_1112b.log
echo "DEESS_DONE $(date +%H:%M)"
PYTHONIOENCODING=utf-8 py -3.12 $R/work/lfrender.py screen $EP $OUT/h4_ds.mp4 > $EP/check/screen_1112.log 2>&1; tail -3 $EP/check/screen_1112.log
PYTHONIOENCODING=utf-8 py -3.12 $R/work/bgcheck.py $OUT/h4_ds.mp4 > $EP/check/bgcheck_1112.log 2>&1; tail -14 $EP/check/bgcheck_1112.log
echo "POST_DONE $(date +%H:%M)"
