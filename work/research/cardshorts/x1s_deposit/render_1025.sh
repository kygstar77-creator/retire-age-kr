# x1s_deposit 10/25 PD: 10/23 03:48 렌더 실패('No frame found' bg/x1/6963836.mp4) 다시 → deess
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr; D=$R/work/research/cardshorts/x1s_deposit
cd $R/work/video && npx remotion render src/m1s_index.ts M1S out/x1s_deposit.mp4 --props=x1s_deposit.json --concurrency=1 --timeout=120000 --offthreadvideo-cache-size-in-bytes=536870912 > $D/render_1025.log 2>&1 || { echo RENDER_FAIL; exit 1; }
PYTHONIOENCODING=utf-8 py -3.12 $R/work/video/deess.py out/x1s_deposit.mp4 out/x1s_deposit_ds.mp4 > $D/deess_1025.log 2>&1; tail -3 $D/deess_1025.log
echo "X1S_DONE $(date +%H:%M)"
