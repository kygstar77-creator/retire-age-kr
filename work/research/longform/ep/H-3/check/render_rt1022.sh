# H-3 10/22 10시 PD: 올리기 전 확인(실거래 10/22 다시 받음) 반영 — 말 4:26 '431채' 다시 받음(+13프레임) · 화면 7장면 건수
#   바뀐 장면만 새 타임라인 프레임으로 렌더 → splice_rt1022.py가 h3_ds_v2(지도 고침본) 영상 + h3_full_v5b 원 소리에 끼워 h3_rt.mp4 → deess → h3_rt_ds.mp4
#   선행: firemap-editor screen_text 재서명(lfrender check 통과). 장면 범위(새 h3.json): s13 2985-3146 · s45 7720-7988 · s47~48 8121-8384 · s65 11324-11707 · s71 12462-12692 · s105 20570-20764
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr
EP=$R/work/research/longform/ep/H-3
OUT=$R/work/video/out
mkdir -p $OUT/h3rt1022
for rg in 8121-8384 2985-3146 7720-7988 11324-11707 12462-12692 20570-20764; do
  [ -f $OUT/h3rt1022/seg_$rg.mp4 ] && { echo "skip $rg"; continue; }
  PYTHONIOENCODING=utf-8 py -3.12 -u $R/work/lfrender.py render $EP --concurrency=2 --timeout=120000 --frames=$rg > $EP/check/render_rt1022_$rg.log 2>&1
  [ -f $OUT/h3.mp4 ] || { echo "FAIL $rg"; tail -5 $EP/check/render_rt1022_$rg.log; exit 1; }
  mv -f $OUT/h3.mp4 $OUT/h3rt1022/seg_$rg.mp4; mv -f $OUT/h3.screen.json $OUT/h3rt1022/seg_$rg.screen.json 2>/dev/null
  echo "seg $rg $(date +%H:%M)"
done
PYTHONIOENCODING=utf-8 py -3.12 $EP/check/splice_rt1022.py || { echo "SPLICE FAIL"; exit 1; }
PYTHONIOENCODING=utf-8 py -3.12 $R/work/video/deess.py $OUT/h3_rt.mp4 $OUT/h3_rt_ds.mp4 --chirp > $EP/check/deess_rt1022.log 2>&1; tail -4 $EP/check/deess_rt1022.log
PYTHONIOENCODING=utf-8 py -3.12 $R/work/lfrender.py screen $EP $OUT/h3_rt_ds.mp4 > $EP/check/screen_rt1022.log 2>&1; tail -3 $EP/check/screen_rt1022.log
PYTHONIOENCODING=utf-8 py -3.12 $R/work/bgcheck.py $OUT/h3_rt_ds.mp4 > $EP/check/bgcheck_rt1022.log 2>&1; tail -3 $EP/check/bgcheck_rt1022.log
echo "ALLDONE $(date +%H:%M)"
