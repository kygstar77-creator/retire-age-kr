# J-1 render_1025.sh 끝(ALL_DONE·RENDER_FAIL) 기다린 뒤 혼자 렌더(동시 렌더 때 No frame found 2번 — backlog 10/23)
J=C:/Users/강영준/Documents/GitHub/retire-age-kr/work/research/longform/ep/J-1/check/render_1025.out
until grep -q "ALL_DONE\|RENDER_FAIL" $J 2>/dev/null; do sleep 60; done
bash render_1025.sh
