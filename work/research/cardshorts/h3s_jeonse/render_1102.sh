# h3s_jeonse 11/2 motion: 어두운 배경 3칸 교체(B-46 benchmark 지시) — 혼자 렌더
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr; D=$R/work/research/cardshorts/h3s_jeonse
cd $R/work/video && npx remotion render src/m1s_index.ts M1S out/h3s_jeonse.mp4 --props=h3s_jeonse.json --concurrency=2 --timeout=120000 --offthreadvideo-cache-size-in-bytes=536870912 > $D/render_1102.log 2>&1 || { echo RENDER_FAIL; exit 1; }
PYTHONIOENCODING=utf-8 py -3.12 $R/work/video/deess.py out/h3s_jeonse.mp4 out/h3s_jeonse_ds.mp4 --chirp-short > $D/deess_1102.log 2>&1; tail -3 $D/deess_1102.log
echo "H3S_DONE $(date +%H:%M)"
