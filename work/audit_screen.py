# 화면 넘침·잘림·글자 크기·대비·누르는 칸 관문 (휴대폰 375px)
#   1) node work/audit_screen_collect.mjs <url> <out.json> [shot.png] [375]   ← 측정값 모으기(Playwright chromium)
#   2) python3 work/audit_screen.py <out.json> [...]                          ← 판정. 걸리면 종료 코드 1
# 기준(근거):
#   - 넘침: 문서 폭(scrollWidth)이 화면 폭보다 크거나, 가로 스크롤 상자 밖 글자가 화면 밖으로 나가면 거부(가로 스크롤 = WCAG 2.2 1.4.10 Reflow, 320 CSS px에서 두 방향 스크롤 금지).
#   - 잘림: overflow hidden/ellipsis 인데 내용 폭 > 상자 폭인 글자는 거부(같은 1.4.10 — 내용이 잘리면 안 됨).
#   - 글자 크기: 12px 미만 글자는 경고(Google Lighthouse 'Document uses legible font sizes' 감사의 12px 기준).
#   - 대비: 글자색/바탕색 대비가 WCAG 2.2 1.4.3(AA) 4.5:1 미만이면 거부. 큰 글자(24px 이상, 또는 18.66px 이상 굵게 700+)는 3:1. 바탕이 그림이면 '확인 안 함'.
#   - 누르는 칸: 24×24 CSS px 미만이면 경고(WCAG 2.2 2.5.8 Target Size Minimum, 문장 안 링크는 예외).
import json, sys

FONT_MIN = 12.0
TARGET_MIN = 24.0


def _lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminance(rgb):
    return 0.2126 * _lin(rgb['r']) + 0.7152 * _lin(rgb['g']) + 0.0722 * _lin(rgb['b'])


def blend(fg, bg):
    a = fg.get('a', 1)
    if a >= 1:
        return fg
    return {k: fg[k] * a + bg[k] * (1 - a) for k in ('r', 'g', 'b')}


def contrast(fg, bg):
    fg = blend(fg, bg)
    l1, l2 = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def is_large(font, weight):
    return font >= 24 or (font >= 18.66 and weight >= 700)


def evaluate(data):
    """측정 JSON → (거부 목록, 경고 목록, 확인 안 함 목록). 항목은 (종류, 설명) 튜플."""
    vw = data.get('vw') or data.get('width') or 375
    fail, warn, unk = [], [], []
    if data.get('docScrollWidth', vw) > vw + 1:
        fail.append(('넘침', f"문서 폭 {data['docScrollWidth']}px > 화면 {vw}px (가로 스크롤 생김)"))
    for t in data.get('texts', []):
        name = f"'{t.get('text', '')[:24]}' ({t.get('sel', '')})"
        if not t.get('inScroller') and (t['x'] < -1 or t['x'] + t['w'] > vw + 1):
            fail.append(('넘침', f"{name} x={t['x']:.0f}~{t['x'] + t['w']:.0f}px, 화면 {vw}px 밖"))
        if t.get('clipped'):
            fail.append(('잘림', f"{name} 내용이 상자보다 넓어 잘림"))
        if t.get('font', 99) < FONT_MIN:
            warn.append(('글자 크기', f"{name} {t['font']:.1f}px < {FONT_MIN:.0f}px"))
        if t.get('bgImage') or not t.get('color') or not t.get('bg'):
            unk.append(('대비', f"{name} 바탕이 그림이라 대비 확인 안 함"))
            continue
        need = 3.0 if is_large(t.get('font', 16), t.get('weight', 400)) else 4.5
        cr = contrast(t['color'], t['bg'])
        if cr < need:
            fail.append(('대비', f"{name} 대비 {cr:.2f}:1 < {need}:1 ({t.get('font', 0):.0f}px)"))
    for g in data.get('targets', []):
        if g.get('inline'):
            continue
        if g['w'] < TARGET_MIN or g['h'] < TARGET_MIN:
            warn.append(('누르는 칸', f"'{g.get('text', '')[:20]}' ({g.get('sel', '')}) {g['w']:.0f}×{g['h']:.0f}px < 24×24"))
        if not g.get('inScroller') and (g['x'] < -1 or g['x'] + g['w'] > vw + 1):
            fail.append(('넘침', f"누르는 칸 '{g.get('text', '')[:20]}' 화면 밖({g['x']:.0f}~{g['x'] + g['w']:.0f}px)"))
    return fail, warn, unk


def _dedupe(items):
    seen, out = set(), []
    for k, s in items:
        if (k, s) not in seen:
            seen.add((k, s)); out.append((k, s))
    return out


def main(argv):
    if not argv:
        print(__doc__ or '사용법: audit_screen.py <측정.json> [...]'); return 2
    bad = 0
    for p in argv:
        d = json.load(open(p, encoding='utf-8'))
        fail, warn, unk = (_dedupe(x) for x in evaluate(d))
        print(f"== {d.get('url', p)} (폭 {d.get('width', '?')}px): 거부 {len(fail)} · 경고 {len(warn)} · 확인 안 함 {len(unk)}")
        for k, s in fail:
            print(f'  [거부·{k}] {s}')
        for k, s in warn:
            print(f'  [경고·{k}] {s}')
        for k, s in unk[:5]:
            print(f'  [확인 안 함·{k}] {s}')
        bad += bool(fail)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main(sys.argv[1:]))
