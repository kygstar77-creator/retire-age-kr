cd "/c/Users/강영준/Documents/GitHub/retire-age-kr/work/research/longform/ep/NDG-1"
for k in 2:6 2:10 3:14 3:21 4:1 4:3 4:16 4:18 4:20 5:10 6:0 6:5 6:11 7:0 7:3 7:7 8:5 ; do
  if py -3.12 ../../../../lfvoice.py readback . $k > rb_${k/:/_}_0.log 2>&1; then echo "$k PASS 0"; continue; fi
  for n in 1 2; do
    py -3.12 ../../../../lfvoice.py retake . $k --takes 3 --nat > rt_${k/:/_}_$n.log 2>&1
    if py -3.12 ../../../../lfvoice.py readback . $k > rb_${k/:/_}_$n.log 2>&1; then echo "$k PASS $n"; break; else echo "$k FAIL $n: $(tail -1 rb_${k/:/_}_$n.log | cut -c1-160)"; fi
  done
done
echo DONE
