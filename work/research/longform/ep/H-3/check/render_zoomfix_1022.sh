# H-3 10/22 06시 PD: 지도 6장면 zoom 1.08→1.03(끝에서 OSM 출처가 화면 밖으로 잘림) — 그 장면 프레임만 다시 렌더해 h3fix1022/에 둔다
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr
EP=$R/work/research/longform/ep/H-3
OUT=$R/work/video/out
for rg in 2116-2268 184-321 4001-4053 5679-5922 9057-9248 23271-23523; do
  [ -f $OUT/h3fix1022/seg_$rg.mp4 ] && { echo "skip $rg"; continue; }
  PYTHONIOENCODING=utf-8 py -3.12 -u $R/work/lfrender.py render $EP --concurrency=2 --timeout=120000 --frames=$rg > $EP/check/render_zoomfix_$rg.log 2>&1
  [ -f $OUT/h3.mp4 ] || { echo "FAIL $rg"; tail -5 $EP/check/render_zoomfix_$rg.log; exit 1; }
  mv -f $OUT/h3.mp4 $OUT/h3fix1022/seg_$rg.mp4; mv -f $OUT/h3.screen.json $OUT/h3fix1022/seg_$rg.screen.json 2>/dev/null
  echo "seg $rg $(date +%H:%M)"
done
echo ALLDONE
