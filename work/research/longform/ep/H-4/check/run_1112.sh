# H-4 11/12 07시 PD(운영실장): editor stamp 10a09aeb 뒤 렌더(CONC=1) → deess 두 번 → screen → bgcheck. 세션이 죽어도 살게 Start-Process로 떼어 냄
R=C:/Users/강영준/Documents/GitHub/retire-age-kr; EP=$R/work/research/longform/ep/H-4
# 07:17 첫 시도: 겹침 검사(ovcheck) 프레임 2040(실사 40294066)에서 죽음 → 11/5 메모대로 OV_CONC=1·OV_CACHE 낮춤
export OV_CONC=1 OV_CACHE=268435456
echo "START $(date +%H:%M)"
CONC=1 bash $EP/check/render_parts_1112.sh || { echo "RENDER_FAIL $(date +%H:%M)"; exit 1; }
[ -f $R/work/video/out/h4.mp4 ] || { echo "NO h4.mp4 $(date +%H:%M)"; exit 1; }
bash $EP/check/post_1112.sh
echo "ALL_DONE $(date +%H:%M)"
