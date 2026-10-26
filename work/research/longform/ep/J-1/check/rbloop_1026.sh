cd /c/Users/강영준/Documents/GitHub/retire-age-kr
EP=work/research/longform/ep/J-1
L=4:11,4:16,4:17,6:28,8:2,8:12,10:13
for r in 1 2 3 4; do
  echo "== 회차 $r ($(date +%H:%M)): $L"
  py -3.12 work/lfvoice.py retake $EP $L --takes 2 2>&1 | grep -E "다시 받음|⚠" | tail -40
  py -3.12 work/lfvoice.py readback $EP $L --whisper turbo 2>&1 | grep -E "^  [0-9]+:[0-9]+ |받아쓰기 대조" > $EP/check/rb_round_1026.log
  cat $EP/check/rb_round_1026.log
  L=$(grep -oE '^  [0-9]+:[0-9]+' $EP/check/rb_round_1026.log | tr -d ' ' | paste -sd,)
  [ -z "$L" ] && { echo "모두 통과 회차 $r"; break; }
done
echo "끝 $(date +%H:%M)"
