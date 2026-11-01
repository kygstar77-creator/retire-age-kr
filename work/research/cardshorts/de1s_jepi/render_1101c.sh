# de1s_jepi 11/1 PD: 배경 4칸 교체(안전 영역)·긴 답 손 밑줄(safeframe) → 2차(배경 2칸·글자 하한 56) h3s 1101b 뒤
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr; D=$R/work/research/cardshorts/de1s_jepi
: # 다시(11/1 404 일시 오류)
cd $R/work/video && npx remotion render src/m1s_index.ts M1S out/de1s_jepi.mp4 --props=de1s_jepi.json --concurrency=3 --timeout=120000 --offthreadvideo-cache-size-in-bytes=536870912 > $D/render_1101c.log 2>&1 || { echo RENDER_FAIL; exit 1; }
PYTHONIOENCODING=utf-8 py -3.12 $R/work/video/deess.py out/de1s_jepi.mp4 out/de1s_jepi_ds.mp4 --chirp-short > $D/deess_1101c.log 2>&1; tail -3 $D/deess_1101c.log
echo "DE1S_DONE $(date +%H:%M)"
