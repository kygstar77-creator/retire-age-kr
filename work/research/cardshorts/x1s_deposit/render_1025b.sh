# x1s_deposit 10/25 23시 PD: 21초 배경(6963836 키보드 글자)이 안전 영역 아래 672px에 글자 상자로 잡힘 → 그 칸만 8661806(동전) start 12로 바꿔 다시 렌더 → deess --chirp-short. d1s_dep v4 렌더 끝난 뒤(동시 렌더 No frame found 피함)
set -u
R=C:/Users/강영준/Documents/GitHub/retire-age-kr; D=$R/work/research/cardshorts/x1s_deposit
until grep -q "V4_DONE\|RENDER_FAIL\|SPLICE_FAIL" $R/work/research/cardshorts/d1s_dep/v4live_1025.out 2>/dev/null; do sleep 20; done
cd $R/work/video && npx remotion render src/m1s_index.ts M1S out/x1s_deposit.mp4 --props=x1s_deposit.json --concurrency=3 --timeout=120000 --offthreadvideo-cache-size-in-bytes=536870912 > $D/render_1025b.log 2>&1 || { echo RENDER_FAIL; exit 1; }
PYTHONIOENCODING=utf-8 py -3.12 $R/work/video/deess.py out/x1s_deposit.mp4 out/x1s_deposit_ds.mp4 --chirp-short > $D/deess_1025b.log 2>&1; tail -3 $D/deess_1025b.log
echo "X1S_DONE $(date +%H:%M)"
