"""N-3 shot_plan 11/11 visual — shot_check 남은 2건 풀기.
① motion 부품 4줄(r18 blocks·r19 cap·r28 stairs·r37 mean)의 파일 칸이 없는 bg/n3/board/*.png를 가리킴 → 실제 있는 motion 미리보기 스틸로
② r37·r38 비교 그림 새로: 옛 shotcmp 왼쪽(경쟁 캡처, x<960)은 그대로 두고 오른쪽만 지금 판으로(r38 n3_partyear는 11/10 n3fit1110로 다시 그림)
"""
import os, re
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'N-3'); PUB = os.path.join(WORK, 'video', 'public')
MAP = {'bg/n3/board/n3_blocks.png': 'motion_preview/n3_st2/blocks_01.png', 'bg/n3/board/n3_pension_cap.png': 'motion_preview/n3_st/cap_04.png',
       'bg/n3/board/n3_rev_steps.png': 'motion_preview/n3_st2/stairs_09.png', 'bg/n3/board/n3_mean_drag.png': 'motion_preview/n3_st/mean_06.png'}
p = os.path.join(EP, 'shot_plan.md'); t = open(p, encoding='utf-8').read()
for a, b in MAP.items():
    assert os.path.exists(os.path.join(EP, b)), b
    t = t.replace('| ' + a + ' |', '| ' + b + ' |')
open(p, 'w', encoding='utf-8').write(t)
def fit(im, w, h):
    im = im.copy(); im.thumbnail((w, h)); bg = Image.new('RGB', (w, h), (20, 20, 22)); bg.paste(im, ((w - im.width) // 2, (h - im.height) // 2)); return bg
for old, new, ours in (('r37.jpg', 'r37n.jpg', os.path.join(EP, MAP['bg/n3/board/n3_mean_drag.png'])), ('r38.jpg', 'r38n.jpg', os.path.join(PUB, 'bg/n3/board/n3_partyear.png'))):
    im = Image.open(os.path.join(EP, 'shotcmp', old)).convert('RGB')
    im.paste(fit(Image.open(ours).convert('RGB'), 940, 530), (970, 56)); im.save(os.path.join(EP, 'shotcmp', new), quality=88); print(new)
