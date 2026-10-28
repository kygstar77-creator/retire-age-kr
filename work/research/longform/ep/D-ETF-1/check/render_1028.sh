# D-ETF-1 10/28 PD: B-31 쉼(줄 안 0.30초 넘는 쉼 → 0.30초)·끝 줄 금요일 뒤 전체 네 토막 다시 → deess → 화면·bgcheck (editor 서명 뒤에만 — lfrender가 막음)
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr; EP=$R/work/research/longform/ep/D-ETF-1; OUT=$R/work/video/out
bash $EP/check/render_parts.sh > $EP/check/render_parts_run_1028.log 2>&1; tail -3 $EP/check/render_parts_run_1028.log
grep -q "CONCAT OK" $EP/check/render_parts_run_1028.log || { echo RENDER_FAIL; exit 1; }
PYTHONIOENCODING=utf-8 py -3.12 $R/work/video/deess.py $OUT/detf1.mp4 $OUT/detf1_ds.mp4 --chirp-short > $EP/check/deess_1028.log 2>&1; tail -4 $EP/check/deess_1028.log
PYTHONIOENCODING=utf-8 py -3.12 $R/work/lfrender.py screen $EP $OUT/detf1_ds.mp4 > $EP/check/screen_1028.log 2>&1; tail -3 $EP/check/screen_1028.log
PYTHONIOENCODING=utf-8 py -3.12 $R/work/bgcheck.py $OUT/detf1_ds.mp4 > $EP/check/bgcheck_1028.log 2>&1; tail -12 $EP/check/bgcheck_1028.log
echo "ALL_DONE $(date +%H:%M)"
