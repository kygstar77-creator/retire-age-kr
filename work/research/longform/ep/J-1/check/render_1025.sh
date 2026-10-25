# J-1 10/25 PD: 끝 줄 요일(+32프레임)·746초 자막 '안' 넘김(TallyFrame capPages) → 16000~끝 두 토막 다시 렌더 → 이어 붙임 → deess → 화면·bgcheck
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr; EP=$R/work/research/longform/ep/J-1; OUT=$R/work/video/out
PARTS="24000-26065 16000-23999" bash $EP/check/render_parts.sh > $EP/check/render_parts_run_1025.log 2>&1; tail -3 $EP/check/render_parts_run_1025.log
grep -q "CONCAT OK" $EP/check/render_parts_run_1025.log || { echo RENDER_FAIL; exit 1; }
PYTHONIOENCODING=utf-8 py -3.12 $R/work/video/deess.py $OUT/j1.mp4 $OUT/j1_ds10.mp4 --chirp-short > $EP/check/deess10_1025.log 2>&1; tail -4 $EP/check/deess10_1025.log
PYTHONIOENCODING=utf-8 py -3.12 $R/work/lfrender.py screen $EP $OUT/j1_ds10.mp4 > $EP/check/screen10_1025.log 2>&1; tail -3 $EP/check/screen10_1025.log
PYTHONIOENCODING=utf-8 py -3.12 $R/work/bgcheck.py $OUT/j1_ds10.mp4 > $EP/check/bgcheck10_1025.log 2>&1; tail -12 $EP/check/bgcheck10_1025.log
echo "ALL_DONE $(date +%H:%M)"
