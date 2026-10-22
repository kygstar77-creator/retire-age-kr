# 장르별 상위 5편 썸네일만 받아(영상은 받지 않음) 한 장에 모은다 → thumbs/<id>.jpg, sheets/*.png, thumbs_index.json
import json, csv, os, sys, subprocess
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
from PIL import Image, ImageDraw, ImageFont
lab = json.load(open(os.path.join(H, 'labels.json'), encoding='utf-8'))
B = list(csv.DictReader(open(os.path.join(H, 'outliers_1022.csv'), encoding='utf-8-sig')))
GEN = [('심리·인간관계', 4), ('건강·노화·병원비', 5), ('역사·사건·미스터리', 17), ('인물 일대기', 18), ('법률·생활 상식', 8), ('이사·전원·귀농', 10), ('직업·직장', 11),
       ('육아·교육', 12), ('지역·여행', 13), ('과학·AI·IT', 14), ('자동차', 15), ('음식·외식', 16), ('시니어 생활', 6), ('뉴스 해설', 19)]
groups = []
for name, g in GEN:
    m = sorted([r for r in B if lab.get(r['id']) == g], key=lambda r: -int(r['views']))[:5]
    groups.append((name, [(r['id'], int(r['views']), int(r['subs']), int(r['sec']), r['channel'], r['title']) for r in m]))
sub = json.load(open(os.path.join(H, 'subtopic_stats.json'), encoding='utf-8'))
SKIP = {'YqbGzTbZMvg', '9-BzjgQ5FQU', 'HFXPrlKn0l8', 'lwjmb13cfjo', 'a2eoXHEWRZk', 'F8MukS2DNNE', 'B3NwWbqRI4A', 'wY9sZF4Q8Gg', 'i7FOg2gnwmg', 'zzv0SlkhVBg', 'de7HCbccM7Y', '2dazqXXz2hs', '34HhyFd3T6k', 'IW1xKZE-coU'}
for k in ['요양·간병·부모 돌봄', '직장·퇴직·공무원 현실', '상속·이혼·가족 돈 법', '전원주택·귀농·시골집', '장례·사망 뒤 절차', '자동차 유지비·차 값', '병원비·건강보험·실손']:
    m = [t for t in sub[k]['top'] if t[5] not in SKIP][:5]
    groups.append(('[돈 옆] ' + k, [(t[5], t[0], t[1], t[2], t[4], t[6]) for t in m]))
json.dump(groups, open(os.path.join(H, 'thumbs_index.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for _, vs in groups:
    for v in vs:
        p = os.path.join(H, 'thumbs', v[0] + '.jpg')
        if not os.path.exists(p): subprocess.run(['curl', '-s', '-o', p, f'https://i.ytimg.com/vi/{v[0]}/hqdefault.jpg'])
try: font = ImageFont.truetype('C:/Windows/Fonts/malgun.ttf', 18)
except Exception: font = ImageFont.load_default()
W, TH = 320, 240
for si in range(0, len(groups), 2):
    img = Image.new('RGB', (W * 5, (TH + 34) * 2), 'white'); d = ImageDraw.Draw(img)
    for gi, (name, vs) in enumerate(groups[si:si+2]):
        y = gi * (TH + 34); d.text((4, y + 4), f'{si+gi+1}. {name}', fill='black', font=font)
        for j, v in enumerate(vs):
            try:
                t = Image.open(os.path.join(H, 'thumbs', v[0] + '.jpg')).convert('RGB').resize((W, TH))
                img.paste(t, (j * W, y + 30))
            except Exception: pass
    img.save(os.path.join(H, 'sheets', f'sheet{si//2+1:02d}.png'))
for i, (n, vs) in enumerate(groups): print(i+1, n, [(v[0], v[1], v[3], v[4][:8]) for v in vs])
