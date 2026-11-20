# H-5 11/21 07:1x PD: 06:37 토막 렌더가 1000-1999에서 No frame found(6964247.mp4, 캐시 256MB)로 두 번 실패 → 그 스크립트가 끝나면 1GB 캐시로 이어 렌더
R=C:/Users/강영준/Documents/GitHub/retire-age-kr
L=$R/work/research/longform/ep/H-5/check/render_parts_1121.log
while ! grep -qE "FAIL|CONCAT OK|part 1000-1999" $L; do sleep 20; done
if grep -q "FAIL" $L; then
  echo "=== 07:1x resume 1GB $(date +%H:%M)" >> $L
  CACHE=1073741824 bash $R/work/research/longform/ep/H-5/check/render_parts_1121.sh >> $L.resume 2>&1
  cat $L.resume >> $L
fi
tail -4 $L
