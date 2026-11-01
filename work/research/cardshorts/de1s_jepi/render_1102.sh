# de1s_jepi 11/2 PD: c1clip 틀(C1S live, E-18 통과 틀) · 답 1.9초(줄 순서) · 밝은 배경 4칸 교체
# 11/2 2차: 디스크 7GB라 public 5.9GB 복사가 덜 돼 소리 404 → 06:29 묶음에 이 편 파일(d-etf-1 소리·bg/detf·human 48MB)만 채우고 그 묶음으로 렌더
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr; D=$R/work/research/cardshorts/de1s_jepi
cd $R/work/video && npx remotion render C:/Users/강영준/AppData/Local/Temp/remotion-webpack-bundle-4tnpX9 C1S out/de1s_jepi_c1.mp4 --props=de1s_jepi.json --pixel-format=yuv420p --concurrency=3 --timeout=120000 --offthreadvideo-cache-size-in-bytes=536870912 > $D/render_1102.log 2>&1 || { echo RENDER_FAIL; tail -20 $D/render_1102.log; exit 1; }
PYTHONIOENCODING=utf-8 py -3.12 $R/work/video/deess.py out/de1s_jepi_c1.mp4 out/de1s_jepi_c1_ds.mp4 --chirp-short > $D/deess_1102.log 2>&1; tail -3 $D/deess_1102.log
echo "DE1S_DONE $(date +%H:%M)"
