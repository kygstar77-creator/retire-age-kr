# OG 카드용 Pretendard 서브셋 생성 — functions/og-fonts-pd.js
# 가변 폰트(public/fonts/PretendardVariable.woff2)를 굵기 700·450으로 고정한 뒤,
# functions/og-card.js가 쓰는 글자 + 숫자·기호만 남겨 base64로 박는다.
# 실행: python work/gen-og-fonts.py   (fontTools 필요: pip install fonttools brotli)
import base64, io, re, sys, os
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools import subset

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'public', 'fonts', 'PretendardVariable.woff2')
CARD = os.path.join(ROOT, 'functions', 'og-card.js')
OUT = os.path.join(ROOT, 'functions', 'og-fonts-pd.js')

card = io.open(CARD, encoding='utf-8').read()
hangul = set(re.findall(r'[가-힣]', card))
# 동적으로 들어오는 값에 쓰이는 글자(금액·나이·회차·비공개 등)도 포함
hangul |= set('억만원세년월일회차비공개아직미만이상목표보다빨라요늦어요같아요준비중현재자산저축액생활비수익률물가연금계산가능나이파이어맵인증카드전체또래상위등')
ascii_chars = set(' 0123456789.,%~:+-/()·—?!×→')
ascii_chars |= set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
chars = ''.join(sorted(hangul | ascii_chars))

def build(weight):
    f = TTFont(SRC)
    f = instancer.instantiateVariableFont(f, {'wght': weight})
    opts = subset.Options()
    opts.flavor = 'woff2'
    opts.notdef_outline = False
    opts.layout_features = ['kern', 'liga', 'tnum']
    ss = subset.Subsetter(options=opts)
    ss.populate(text=chars)
    ss.subset(f)
    buf = io.BytesIO(); f.save(buf)
    return base64.b64encode(buf.getvalue()).decode('ascii')

bold = build(700); regular = build(450)
js = ("// 파이어맵 OG 카드용 Pretendard 서브셋 — 가변 폰트를 700/450으로 고정한 뒤 카드가 쓰는 글자만 남겼다.\n"
      "// 앱 화면과 같은 서체로 공유 이미지를 그리려고 만든 것. 재생성은 work/gen-og-fonts.py.\n"
      f"// 글자 {len(chars)}자 · 생성 스크립트가 og-card.js의 한글을 자동으로 모은다.\n"
      f"export const PD_BOLD_B64 = '{bold}';\n"
      f"export const PD_REGULAR_B64 = '{regular}';\n")
io.open(OUT, 'w', encoding='utf-8').write(js)
sys.stdout.reconfigure(encoding='utf-8')
print('chars', len(chars), '| bold', len(bold) // 1024, 'KB | regular', len(regular) // 1024, 'KB | 때 포함:', '때' in chars)
