cd /c/Users/강영준/Documents/GitHub/retire-age-kr/work/research/longform/ep/H-6
for c in c36/comp_*.jpg; do
  id=$(basename $c .jpg)
  others=$(ls c36/comp_*.jpg | grep -v "$id" | head -5 | tr '\n' ' ')
  py -3.12 ../../../../thumbpair.py thumb "$c" thumb_h6_n3.png $others --out c36/c39_n3_$id > c36/c39_n3_$id.log 2>&1
  echo "$id exit=$?" >> c36/c39_n3_summary.txt
done
