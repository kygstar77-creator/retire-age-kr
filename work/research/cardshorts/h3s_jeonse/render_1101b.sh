# h3s_jeonse 11/1 PD 2차: 배경 2칸 교체(안전 영역) → de1s_jepi 렌더 끝난 뒤 혼자
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr; D=$R/work/research/cardshorts/h3s_jeonse
until grep -qE "DE1S_DONE|RENDER_FAIL" $R/work/research/cardshorts/de1s_jepi/render_1101.out 2>/dev/null; do sleep 20; done
cd $R/work/video && npx remotion render src/m1s_index.ts M1S out/h3s_jeonse.mp4 --props=h3s_jeonse.json --concurrency=3 --timeout=120000 --offthreadvideo-cache-size-in-bytes=536870912 > $D/render_1101b.log 2>&1 || { echo RENDER_FAIL; exit 1; }
PYTHONIOENCODING=utf-8 py -3.12 $R/work/video/deess.py out/h3s_jeonse.mp4 out/h3s_jeonse_ds.mp4 --chirp-short > $D/deess_1101b.log 2>&1; tail -3 $D/deess_1101b.log
echo "H3S_DONE $(date +%H:%M)"
