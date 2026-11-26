# CC-1 장 카드·끝 그림 스틸(비교 그림 오른쪽 칸용) — PD 11/27, renderlock 안에서 부른다
R="C:/Users/강영준/Documents/GitHub/retire-age-kr"; D="$R/work/research/visual/CC-1-shots"
. $R/work/video/bundle_lib.sh
B=$(fm_bundle $D src/index.ts) || { echo BUNDLE_FAIL; exit 1; }
mkdir -p $D/stills
cd $R/work/video
for nf in 1:850 2:2052 3:3297 4:5109 5:6701 6:8625 7:10749 8:13189 end:14364; do
  n=${nf%%:*}; f=${nf##*:}
  npx remotion still "$B" CC1 "$D/stills/ask_$n.png" --frame=$f --scale=0.5 > /dev/null 2>&1 || echo "STILL_FAIL $n"
done
ls $D/stills; fm_bundle_done $B
