"""썸네일 길이 칸(오른쪽 아래 재생 시간 표시) 위 글자 검사 — 11/11 visual
근거: C-15(답 숫자·핵심 낱말만 길이 칸에 안 걸리게), 11/10 PD 알림(K-1 '더' 반쯤 가림)·H-4 g3·N-3 c 걸림.
칸: 1280×720 기준 x 1143~1265 · y 647~705 (유튜브 412px 홈 피드 길이 칸을 1280으로 늘린 자리, 11/10 실측).
글자 픽셀 = 우리 썸네일 큰 글 색: 흰(R,G,B ≥ 235) 또는 주황 #FF5A00 근처(R≥225, 60≤G≤120, B≤60).
사진의 흰 하이라이트도 잡힐 수 있어 '사진만 있는 칸'은 기준판(same photo, 글자 없음)과 비교: --base 사진.
쓰는 법: py -3.12 work/thumblen.py <thumb.png> [...] [--base <글자 없는 사진.png>] → 걸림 있으면 종료 코드 1
"""
import sys
from PIL import Image

BOX = (1143, 647, 1265, 705)
LIMIT = 30   # 글자 픽셀 30개 넘으면 걸림(획 하나 끝만 닿는 정도 허용)


def is_text(p):
    r, g, b = p[:3]
    return (r >= 235 and g >= 235 and b >= 235) or (r >= 225 and 60 <= g <= 120 and b <= 60)


def count(path, base=None):
    im = Image.open(path).convert('RGB').resize((1280, 720), Image.LANCZOS)
    reg = im.crop(BOX); px = reg.load()
    bpx = None
    if base:
        bpx = Image.open(base).convert('RGB').resize((1280, 720), Image.LANCZOS).crop(BOX).load()
    n = 0
    for y in range(reg.height):
        for x in range(reg.width):
            if is_text(px[x, y]) and not (bpx and is_text(bpx[x, y])):
                n += 1
    return n


def main(argv):
    base = None
    if '--base' in argv:
        i = argv.index('--base'); base = argv[i + 1]; argv = argv[:i] + argv[i + 2:]
    bad = 0
    for p in argv:
        n = count(p, base)
        ok = n <= LIMIT
        bad += not ok
        print(f"{'OK  ' if ok else '걸림'} 길이 칸 글자 픽셀 {n:5d}  {p}")
    return 1 if bad else 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main(sys.argv[1:]))
