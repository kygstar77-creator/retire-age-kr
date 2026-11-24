cd /c/Users/강영준/Documents/GitHub/retire-age-kr/work/research/longform/ep/H-6
for t in p1 p2; do for c in c36/comp_*.jpg; do
  id=$(basename $c .jpg); others=$(ls c36/comp_*.jpg | grep -v "$id" | head -5 | tr '\n' ' ')
  py -3.12 ../../../../thumbpair.py thumb "$c" thumb_h6_$t.png $others --out c36/c39_${t}_$id > c36/c39_${t}_$id.log 2>&1
  echo "$t $id exit=$?" >> c36/c39_p_summary.txt
done; done
for pr in "n3 p1" "n3 p2" "p1 p2"; do set -- $pr
  py -3.12 ../../../../thumbpair.py thumb thumb_h6_$1.png thumb_h6_$2.png $(ls c36/comp_*.jpg | head -5) --out c36/pair_$1_$2 > c36/pair_$1_$2.log 2>&1
  echo "pair $1(지금) $2(새) exit=$?" >> c36/c39_p_summary.txt
done
