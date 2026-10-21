EP=work/research/longform/ep/H-3
for r in 1 2 3 4; do
  L=$(grep -oE '^  [0-9]+:[0-9]+' $EP/check/rb_round.log | tr -d ' ' | paste -sd,)
  [ -z "$L" ] && { echo "모두 통과 회차 $r"; break; }
  echo "== 회차 $r ($(date +%H:%M)): $L"
  py -3.12 work/lfvoice.py retake $EP $L --takes 3 2>&1 | grep "다시 받음" | tail -40
  py -3.12 work/lfvoice.py readback $EP $L 2>&1 | grep -E "^  [0-9]+:[0-9]+ |받아쓰기 대조" > $EP/check/rb_round.log
  cat $EP/check/rb_round.log
done
