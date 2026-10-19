# 구겨진 종이 바탕(자체 합성, 외부 그림 0) — 높이 지도 = 무작위 접힌 선(텐트 함수) 수십 개 + 잔주름, 왼쪽 위 빛으로 음영.
# py -3.12 paper.py <out.jpg> <W> <H> [seed]
import numpy as np, cv2, sys
out=sys.argv[1]; W,H=int(sys.argv[2]),int(sys.argv[3]); seed=int(sys.argv[4]) if len(sys.argv)>4 else 7
rng=np.random.default_rng(seed)
S=0.5; w,h=int(W*S),int(H*S)          # 반 크기에서 만들고 키운다(빠르게·부드럽게)
yy,xx=np.mgrid[0:h,0:w].astype(np.float32)
hm=np.zeros((h,w),np.float32)
D=np.hypot(w,h)
for k in range(160):
    cx,cy=rng.uniform(0,w),rng.uniform(0,h); th=rng.uniform(0,np.pi); nx,ny=np.cos(th),np.sin(th)
    d=(xx-cx)*nx+(yy-cy)*ny; along=-(xx-cx)*ny+(yy-cy)*nx
    L=rng.uniform(0.08,0.45)*D; reach=rng.uniform(0.015,0.07)*D
    win=np.exp(-(along/L)**2)                         # 접힌 선은 끝이 흐려진다
    tent=np.minimum(np.abs(d),reach)                   # 접힌 자리에서 꺾이는 면
    hm+=rng.uniform(0.4,1.0)*rng.choice([-1,1])*tent*win
fine=cv2.GaussianBlur(rng.normal(0,1,(h,w)).astype(np.float32),(0,0),3)*6
hm+=fine
hm=cv2.GaussianBlur(hm,(0,0),0.8)
gx=cv2.Sobel(hm,cv2.CV_32F,1,0,ksize=3); gy=cv2.Sobel(hm,cv2.CV_32F,0,1,ksize=3)
sh=-(gx*0.6+gy*0.8)                                 # 왼쪽 위에서 오는 빛
sh/= (np.percentile(np.abs(sh),99)+1e-6)
sh=cv2.resize(sh,(W,H),interpolation=cv2.INTER_CUBIC)
grain=cv2.GaussianBlur(rng.normal(0,1,(H,W)).astype(np.float32),(0,0),0.7)
yy2,xx2=np.mgrid[0:H,0:W].astype(np.float32)
r=np.sqrt(((xx2-W/2)/(W/2))**2+((yy2-H/2)/(H/2))**2)
v=242+9*sh+1.0*grain-6*np.clip(r-0.55,0,1)**1.4
img=np.stack([v+1.0,v+0.2,v-2.2],-1)               # 살짝 따뜻한 흰색
ok,buf=cv2.imencode(out[out.rfind('.'):],np.clip(img[...,::-1],0,255).astype(np.uint8),[int(cv2.IMWRITE_JPEG_QUALITY),92]); buf.tofile(out)
print(out,float(v.mean()),float(v.std()))
