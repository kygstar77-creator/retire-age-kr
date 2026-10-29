# D-ETF-1 10/29 PD: 받아쓰기 합의오독 2줄(0:8 '느나'·1:6 '대였어요') — 한 줄씩 다시 받기→줄 안 쉼 손질→build→받아쓰기, 통과까지 최대 5번
cd C:/Users/강영준/Documents/GitHub/retire-age-kr/work
E=research/longform/ep/D-ETF-1; export PYTHONIOENCODING=utf-8
for at in 0:8 1:6; do
  for k in 1 2 3 4 5; do
    py -3.12 lfvoice.py retake $E $at --takes 1 --nat | grep "다시 받음"
    py -3.12 $E/check/capquiet_1029.py $at
    py -3.12 -c "import sys;sys.path.insert(0,'.');import lfvoice;lfvoice.build('$E')" | tail -1
    if py -3.12 lfvoice.py readback $E $at | tail -3; then echo "PASS $at try $k"; break; fi
    echo "FAIL $at try $k"
  done
done
py -3.12 lfvoice.py check $E | tail -4
py -3.12 lfrender.py voice $E | tail -1
py -3.12 -c "import sys;sys.path.insert(0,'.');import ytlong;print('RB',ytlong.readback_check('$E'))"
echo FIX2_DONE $(date +%H:%M)
