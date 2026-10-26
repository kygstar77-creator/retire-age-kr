# h3s_jeonse 10/26 PD: J-1 render_parts CONCAT 뒤 혼자 렌더(동시 렌더 No frame found) → deess --chirp-short
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr; D=$R/work/research/cardshorts/h3s_jeonse
until grep -qE "CONCAT OK|FAIL" $R/work/research/longform/ep/J-1/check/render_parts_run_1026.log 2>/dev/null; do sleep 30; done
cd $R/work/video && npx remotion render src/m1s_index.ts M1S out/h3s_jeonse.mp4 --props=h3s_jeonse.json --concurrency=3 --timeout=120000 --offthreadvideo-cache-size-in-bytes=536870912 > $D/render_1026.log 2>&1 || { echo RENDER_FAIL; exit 1; }
PYTHONIOENCODING=utf-8 py -3.12 $R/work/video/deess.py out/h3s_jeonse.mp4 out/h3s_jeonse_ds.mp4 --chirp-short > $D/deess_1026.log 2>&1; tail -3 $D/deess_1026.log
echo "H3S_DONE $(date +%H:%M)"
