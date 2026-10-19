from PIL import Image
def side(a,bs,out):
    ims=[Image.open(x).convert('RGB') for x in [a]+bs]; h=420
    ims=[i.resize((int(i.width*h/i.height),h)) for i in ims]
    W=sum(i.width for i in ims)+20*(len(ims)-1); c=Image.new('RGB',(W,h),'white'); x=0
    for i in ims: c.paste(i,(x,0)); x+=i.width+20
    c.save(out)
side('pkg/img/00.png',['bench_shots/c3_0.png','bench_shots/c5_0.png'],'bench_shots/cmp_00.png')
side('pkg/img/01.png',['bench_shots/c3_1.png','bench_shots/c5_1.png'],'bench_shots/cmp_01.png')
side('pkg/img/02.png',['bench_shots/c5_2.png','bench_shots/c4_1.png'],'bench_shots/cmp_02.png')
