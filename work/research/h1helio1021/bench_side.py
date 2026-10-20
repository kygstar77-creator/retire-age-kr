import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
def side(ours, theirs, out):
    ims = [Image.open(p).convert('RGB') for p in [ours] + theirs if os.path.exists(p)]
    h = 500; ims = [im.resize((int(im.width * h / im.height), h)) for im in ims]
    c = Image.new('RGB', (sum(i.width for i in ims) + 10 * (len(ims) - 1), h), 'white'); x = 0
    for im in ims: c.paste(im, (x, 0)); x += im.width + 10
    c.save(out); print(out, c.size)
side('pkg/img/00.png', ['bench_shots/c1_0.png', 'bench_shots/c2_0.png', 'bench_shots/c3_0.png', 'bench_shots/c4_0.png'], 'bench_shots/cmp_00.png')
side('pkg/img/01.png', ['bench_shots/c1_1.png', 'bench_shots/c2_1.png', 'bench_shots/c3_1.png'], 'bench_shots/cmp_01.png')
side('pkg/img/02.png', ['bench_shots/c2_1.png', 'bench_shots/c4_1.png'], 'bench_shots/cmp_02.png')
