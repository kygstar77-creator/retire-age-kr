# H-2 10/19 PD: 바뀐 줄만 readback — 첫 귀 3.1-flash-lite(3.5 하루 한도), 둘째 귀 Whisper large-v3-turbo(제미나이 둘째 귀 한도)
import sys
sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
import lfvoice
lfvoice.WHISPER_SIZE, lfvoice.WHISPER = 'large-v3-turbo', 'whisper-turbo'
lfvoice.SECOND[:] = []
lfvoice.readback(r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\research\longform\ep\H-2', sys.argv[1].split(','))
