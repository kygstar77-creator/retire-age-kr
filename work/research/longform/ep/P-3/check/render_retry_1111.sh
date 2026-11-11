# P-3 11/11 PD: 토막 실패하면 다시(최대 4번), 끝난 토막은 skip
cd "$(dirname "$0")"
for n in 1 2 3 4; do
  rm -f parts_done_1111
  CONC=1 bash render_parts_1111.sh > render_try$n.log 2>&1
  cat render_try$n.log
  grep -q "CONCAT OK" render_try$n.log && { echo "DONE try $n $(date +%H:%M)"; exit 0; }
done
echo "GIVEUP $(date +%H:%M)"; exit 1
