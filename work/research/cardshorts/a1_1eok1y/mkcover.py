# v2(23:3x 제미나이 6 반영: 기준 줄 작게·흐리게, 질문 키움) · a1_1eok1y 첫 1초 표지(firemap-shorts 10/4 23:2x): a1_spyi v8 통과 틀(분배금 대비만 보이고 승자는 영상 안) + 내 돈 대입(1억) — spyi 세 줄 3번 반영
import sys, os
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
from PIL import Image, ImageDraw
import cardshort as C
W, H = 1080, 1920; M = 64
im = Image.new('RGB', (W, H), C.BG); d = ImageDraw.Draw(im)
d.text((M, 240), '1억씩 넣고 1년', font=C.BHS(140), fill=C.WHITE)
d.text((M, 450), '세금 뗀 분배금', font=C.PD7(88), fill=C.WHITE)
d.text((M, 610), 'JEPQ', font=C.PD7(76), fill=C.YELLOW); d.text((M + 250, 560), '1,005만', font=C.BHS(190), fill=C.YELLOW)
d.text((M, 840), 'SCHD', font=C.PD7(76), fill=C.WHITE); d.text((M + 250, 790), '330만', font=C.BHS(190), fill=C.WHITE)
d.text((M, 1110), '1년 뒤 남은 돈은', font=C.BHS(150), fill=C.WHITE)
d.text((M, 1300), '누가 더 많을까?', font=C.BHS(160), fill=C.WHITE)
d.text((M, 1700), '2025.9.26 → 2026.9.28', font=C.PD7(44), fill=(150,150,160))
im.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cover.png'))
