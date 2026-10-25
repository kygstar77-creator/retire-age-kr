# d1s_dep 10/25 23:3x PD: v4 눈 검사에서 39.9초 한마디 '5억 4'(safeframe shortKick이 4,000의 쉼표에서 자름) → 칸 이름 '5억 4천만~9억원'·shortKick 고쳐 다시. x1s_deposit 렌더 끝난 뒤
R=C:/Users/강영준/Documents/GitHub/retire-age-kr
until grep -q "X1S_DONE\|RENDER_FAIL" $R/work/research/cardshorts/x1s_deposit/render_1025b.out 2>/dev/null; do sleep 20; done
bash $R/work/research/cardshorts/d1s_dep/v4live_1025.sh
