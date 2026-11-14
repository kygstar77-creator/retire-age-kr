# N-3 11/15 02:2x 정기 PD: editor 23:12 재서명(a37c8ebf) 뒤 렌더 → post. 떼어 낸 프로세스로(세션이 죽어도 산다)
R=C:/Users/강영준/Documents/GitHub/retire-age-kr; EP=$R/work/research/longform/ep/N-3
export OV_CONC=1 OV_CACHE=268435456
echo "START $(date +%H:%M)"
CONC=1 bash $EP/check/render_parts_1115.sh || { echo "RENDER_FAIL $(date +%H:%M)"; exit 1; }
[ -f $R/work/video/out/n3.mp4 ] || { echo "NO n3.mp4 $(date +%H:%M)"; exit 1; }
bash $EP/check/post_1115.sh
echo "ALL_DONE $(date +%H:%M)"
