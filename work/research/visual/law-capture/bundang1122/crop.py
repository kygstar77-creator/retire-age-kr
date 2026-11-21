# bundang1122 c04 '매매 신고 30일' 근거 — law.go.kr 부동산거래신고법 제3조 원문 캡처(raw.png, lawcap.py) 잘라 붙이기, 글자 손대지 않음
from PIL import Image
k=1.05; im=Image.open('raw.png').convert('RGB')
c=lambda a,b,x,y: im.crop(tuple(int(v*k) for v in (a,b,x,y)))
head=c(18,190,420,285); body=c(505,288,1235,695)
W=max(head.width,body.width)+60; H=head.height+body.height+70
out=Image.new('RGB',(W,H),'white'); out.paste(head,(30,25)); out.paste(body,(30,25+head.height+20))
out.save('03.png'); print(out.size)
