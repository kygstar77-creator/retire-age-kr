# P-3 11/11 07시 PD(운영실장): 3:7 새 말 뒤 다시 렌더(CONC=1) → deess 두 번 → screen → bgcheck. 06:17 회차가 07:05에 건 렌더는 세션과 함께 죽음(로그 0바이트) → 이번엔 Start-Process로 떼어 냄
R=C:/Users/강영준/Documents/GitHub/retire-age-kr; EP=$R/work/research/longform/ep/P-3
echo "START $(date +%H:%M)"
CONC=1 bash $EP/check/render_parts_1110b.sh || { echo "RENDER_FAIL $(date +%H:%M)"; exit 1; }
[ -f $R/work/video/out/p3.mp4 ] || { echo "NO p3.mp4 $(date +%H:%M)"; exit 1; }
bash $EP/check/post_1111.sh
echo "ALL_DONE $(date +%H:%M)"
