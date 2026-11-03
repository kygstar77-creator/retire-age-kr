# de1s_jepqhealth 11/3 PD: de1s_schdgrow render_1102s.sh 복사 — 같은 묶음 4tnpX9(빠진 배경 4개·새 wav 1개 채움)
# 11/3 렌더 1·2판 No frame found(7118320 1.83초·6343634 10.6초, 파일 정상·디코드 정상) → J-1처럼 concurrency 1
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr; D=$R/work/research/cardshorts/de1s_jepqhealth
cd $R/work/video && npx remotion render C:/Users/강영준/AppData/Local/Temp/remotion-webpack-bundle-4tnpX9 C1S out/de1s_jepqhealth_c1.mp4 --props=de1s_jepqhealth.json --pixel-format=yuv420p --concurrency=1 --timeout=120000 --offthreadvideo-cache-size-in-bytes=536870912 > $D/render_1103.log 2>&1 || { echo RENDER_FAIL; tail -20 $D/render_1103.log; exit 1; }
PYTHONIOENCODING=utf-8 py -3.12 $R/work/video/deess.py out/de1s_jepqhealth_c1.mp4 out/de1s_jepqhealth_c1_ds.mp4 --chirp-short > $D/deess_1103.log 2>&1; tail -3 $D/deess_1103.log
echo "DE1Q_DONE $(date +%H:%M)"
