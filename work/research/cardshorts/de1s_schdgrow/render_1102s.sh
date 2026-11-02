# de1s_schdgrow 11/2 PD: c1clip 틀(C1S live) · de1s_jepi render_1102.sh 복사 — 같은 묶음(4tnpX9: d-etf-1 소리·bg/detf·human 있음)으로 렌더
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr; D=$R/work/research/cardshorts/de1s_schdgrow
cd $R/work/video && npx remotion render C:/Users/강영준/AppData/Local/Temp/remotion-webpack-bundle-4tnpX9 C1S out/de1s_schdgrow_c1.mp4 --props=de1s_schdgrow.json --pixel-format=yuv420p --concurrency=3 --timeout=120000 --offthreadvideo-cache-size-in-bytes=536870912 > $D/render_1102s.log 2>&1 || { echo RENDER_FAIL; tail -20 $D/render_1102s.log; exit 1; }
PYTHONIOENCODING=utf-8 py -3.12 $R/work/video/deess.py out/de1s_schdgrow_c1.mp4 out/de1s_schdgrow_c1_ds.mp4 --chirp-short > $D/deess_1102s.log 2>&1; tail -3 $D/deess_1102s.log
echo "DE1S_SCHD_DONE $(date +%H:%M)"
