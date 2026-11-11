# H-4 11/12 07시 PD(운영실장): editor stamp 10a09aeb 뒤 렌더(CONC=1) → deess 두 번 → screen → bgcheck. 세션이 죽어도 살게 Start-Process로 떼어 냄
R=C:/Users/강영준/Documents/GitHub/retire-age-kr; EP=$R/work/research/longform/ep/H-4
echo "START $(date +%H:%M)"
CONC=1 bash $EP/check/render_parts_1112.sh || { echo "RENDER_FAIL $(date +%H:%M)"; exit 1; }
[ -f $R/work/video/out/h4.mp4 ] || { echo "NO h4.mp4 $(date +%H:%M)"; exit 1; }
bash $EP/check/post_1112.sh
echo "ALL_DONE $(date +%H:%M)"
