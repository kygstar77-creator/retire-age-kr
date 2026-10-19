# 장 바뀜 '띠링' — 자체 합성(외부 음원 0). 수페TV 장 전환 소리 듣기(제미나이 flash, 10/19): 차임·벨 계열, 두 음 올라감, 0.5~0.7초, 목소리와 같거나 조금 작게, 말 쉬는 틈.
import numpy as np, wave, sys
SR=48000; out=sys.argv[1]
def bell(f, dur, tau):
    t=np.arange(int(SR*dur))/SR
    env=np.minimum(1,t/0.004)*np.exp(-t/tau)
    s=np.sin(2*np.pi*f*t)+0.32*np.sin(2*np.pi*2.0*f*t)*np.exp(-t/(tau*0.6))+0.12*np.sin(2*np.pi*2.76*f*t)*np.exp(-t/(tau*0.4))+0.05*np.sin(2*np.pi*4.07*f*t)*np.exp(-t/(tau*0.25))
    return s*env
L=0.72; y=np.zeros(int(SR*L))
a=bell(1046.5,0.6,0.15); y[:len(a)]+=a*0.85                 # C6
o=int(SR*0.115); b=bell(1568.0,L-0.115,0.2); y[o:o+len(b)]+=b  # G6 (올라감)
# 아주 짧은 방 울림
d=int(SR*0.045); y[d:]+=0.18*y[:-d]
fade=np.ones_like(y); n=int(SR*0.08); fade[-n:]=np.linspace(1,0,n); y*=fade
y=y/np.abs(y).max()*0.5   # −6 dBFS
w=wave.open(out,'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((y*32767).astype(np.int16).tobytes()); w.close()
print(out, L)
