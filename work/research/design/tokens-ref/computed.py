# Dembrandt 보조 — 375px 모바일 화면에서 getComputedStyle로 '보이는 글자 양' 가중 토큰을 뽑는다.
# Dembrandt는 요소 개수로 세서 마케팅 큰 제목(92px 등)이 위로 올라온다. 여기서는 글자 수·면적으로 센다.
# 사용: python computed.py <이름> <url> [<url> ...]  → <이름>/computed.json
import json, sys, pathlib
from collections import Counter
from playwright.sync_api import sync_playwright

JS = r"""
() => {
  const vis = (el) => { const r = el.getBoundingClientRect(); const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none' && +s.opacity > 0; };
  const text = {}, size = {}, weight = {}, family = {}, bg = {}, radius = {}, pad = {}, gap = {}, lh = {}, ls = {}, shadow = {}, btn = [];
  const add = (o, k, n) => { if (k == null || k === '') return; o[k] = (o[k] || 0) + n; };
  const body = getComputedStyle(document.body);
  for (const el of document.querySelectorAll('body *')) {
    if (!vis(el)) continue;
    const s = getComputedStyle(el), r = el.getBoundingClientRect();
    // 이 요소가 직접 가진 글자 수
    let own = 0; for (const n of el.childNodes) if (n.nodeType === 3) own += n.textContent.trim().length;
    if (own) {
      add(text, s.color, own); add(size, s.fontSize, own); add(weight, s.fontWeight, own);
      add(family, s.fontFamily.split(',')[0].replace(/["']/g, '').trim(), own);
      const l = s.lineHeight === 'normal' ? 'normal' : (parseFloat(s.lineHeight) / parseFloat(s.fontSize)).toFixed(2);
      add(lh, s.fontSize + ' / ' + l, own); add(ls, s.letterSpacing, own);
    }
    const a = Math.round(r.width * r.height / 100);
    if (s.backgroundColor !== 'rgba(0, 0, 0, 0)') add(bg, s.backgroundColor, a);
    if (s.borderTopLeftRadius !== '0px') add(radius, s.borderTopLeftRadius, 1);
    if (s.boxShadow !== 'none') add(shadow, s.boxShadow, 1);
    for (const p of [s.paddingTop, s.paddingLeft]) if (p !== '0px') add(pad, p, 1);
    if (s.display.includes('flex') || s.display.includes('grid')) if (s.rowGap !== 'normal' && s.rowGap !== '0px') add(gap, s.rowGap, 1);
    if ((el.tagName === 'BUTTON' || el.getAttribute('role') === 'button' || (el.tagName === 'A' && s.backgroundColor !== 'rgba(0, 0, 0, 0)')) && btn.length < 25 && el.innerText.trim())
      btn.push({ t: el.innerText.trim().slice(0, 20), bg: s.backgroundColor, color: s.color, fs: s.fontSize, fw: s.fontWeight, r: s.borderTopLeftRadius, h: Math.round(r.height), pad: s.padding });
  }
  const vars = {};
  for (const sh of document.styleSheets) { let rules; try { rules = sh.cssRules; } catch { continue; }
    for (const ru of rules) if (ru.selectorText === ':root' || ru.selectorText === 'html' || ru.selectorText === ':root, :host')
      for (const p of ru.style) if (p.startsWith('--')) vars[p] = ru.style.getPropertyValue(p).trim(); }
  const top = (o, n = 15) => Object.entries(o).sort((a, b) => b[1] - a[1]).slice(0, n);
  return { url: location.href, title: document.title, bodyBg: body.backgroundColor, bodyColor: body.color, bodyFont: body.fontFamily,
    text: top(text), size: top(size, 20), weight: top(weight), family: top(family, 6), lineHeight: top(lh, 15), letterSpacing: top(ls, 6),
    bg: top(bg), radius: top(radius), padding: top(pad), gap: top(gap, 10), shadow: top(shadow, 6), buttons: btn,
    rootVarCount: Object.keys(vars).length, rootVars: Object.fromEntries(Object.entries(vars).slice(0, 400)) };
}
"""

name, urls = sys.argv[1], sys.argv[2:]
out = []
with sync_playwright() as pw:
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={'width': 375, 'height': 812}, device_scale_factor=2, is_mobile=True, has_touch=True, locale='ko-KR',
                        user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1')
    for u in urls:
        pg = ctx.new_page()
        try:
            pg.goto(u, wait_until='networkidle', timeout=60000)
        except Exception as e:
            print('goto warn', u, str(e).splitlines()[0])
        pg.wait_for_timeout(1500)
        for _ in range(6):
            pg.mouse.wheel(0, 1200); pg.wait_for_timeout(400)
        try:
            out.append(pg.evaluate(JS))
        except Exception as e:
            out.append({'url': u, 'error': str(e).splitlines()[0]})
        pg.close()
    b.close()
p = pathlib.Path(__file__).parent / name / 'computed.json'
p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
for o in out:
    print('==', o.get('url'), o.get('title', ''), o.get('error', ''))
    for k in ('bodyBg', 'bodyColor', 'text', 'size', 'weight', 'family', 'bg', 'radius', 'buttons', 'rootVarCount'):
        print(' ', k, json.dumps(o.get(k), ensure_ascii=False)[:700])
