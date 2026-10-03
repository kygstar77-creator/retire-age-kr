// 화면 넘침·글자 크기·대비·누르는 칸 크기 측정값 모으기 (audit_screen.py가 판정한다).
//   node work/audit_screen_collect.mjs <url> <out.json> [shot.png] [폭=375]
// 브라우저는 설치된 Playwright chromium을 쓴다(playwright install 하지 않는다).
import { chromium } from '@playwright/test';
import fs from 'node:fs';

const [url, out, shot, widthArg] = process.argv.slice(2);
if (!url || !out) { console.error('사용법: node work/audit_screen_collect.mjs <url> <out.json> [shot.png] [폭=375]'); process.exit(2); }
const width = Number(widthArg || 375);

// 설치된 Playwright 버전과 브라우저 폴더 번호가 다를 때(클라우드 /opt/pw-browsers/chromium) 실행 파일을 직접 고른다.
const exe = process.env.AUDIT_CHROMIUM || ['/opt/pw-browsers/chromium/chrome-linux/chrome', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'].find((p) => fs.existsSync(p));
const browser = await chromium.launch(exe ? { executablePath: exe } : {});
const page = await browser.newPage({ viewport: { width, height: 812 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
await page.goto(url, { waitUntil: 'load', timeout: 45000 });
await page.waitForTimeout(2500);

const data = await page.evaluate(() => {
  const vw = document.documentElement.clientWidth;
  const parse = (c) => { const m = c && c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(',').map((x) => parseFloat(x)); return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 }; };
  const bgOf = (el) => {
    for (let e = el; e && e.nodeType === 1; e = e.parentElement) {
      const cs = getComputedStyle(e);
      if (cs.backgroundImage && cs.backgroundImage !== 'none') return { image: true, color: null };
      const c = parse(cs.backgroundColor);
      if (c && c.a > 0.5) return { image: false, color: c };
    }
    return { image: false, color: { r: 255, g: 255, b: 255, a: 1 } };
  };
  const inScroller = (el) => {
    for (let e = el.parentElement; e && e !== document.body; e = e.parentElement) {
      const ox = getComputedStyle(e).overflowX;
      if ((ox === 'auto' || ox === 'scroll') && e.scrollWidth > e.clientWidth) return true;
    }
    return false;
  };
  const visible = (el, r) => {
    if (r.width < 1 || r.height < 1) return false;
    const cs = getComputedStyle(el);
    return cs.visibility !== 'hidden' && cs.display !== 'none' && parseFloat(cs.opacity) > 0.05;
  };
  const path = (el) => { const p = []; for (let e = el; e && e.nodeType === 1 && p.length < 4; e = e.parentElement) { let s = e.tagName.toLowerCase(); if (e.id) s += '#' + e.id; else if (e.classList.length) s += '.' + [...e.classList].slice(0, 2).join('.'); p.unshift(s); } return p.join('>'); };
  const texts = []; const targets = [];
  for (const el of document.body.querySelectorAll('*')) {
    if (['SCRIPT', 'STYLE', 'NOSCRIPT', 'SVG', 'PATH'].includes(el.tagName)) continue;
    const r = el.getBoundingClientRect();
    if (!visible(el, r)) continue;
    const own = [...el.childNodes].filter((n) => n.nodeType === 3).map((n) => n.textContent).join('').trim();
    const cs = getComputedStyle(el);
    if (own) {
      const bg = bgOf(el);
      texts.push({
        sel: path(el), text: own.slice(0, 60), x: r.left, y: r.top + scrollY, w: r.width, h: r.height,
        font: parseFloat(cs.fontSize), weight: parseInt(cs.fontWeight, 10) || 400,
        color: parse(cs.color), bg: bg.color, bgImage: bg.image, inScroller: inScroller(el),
        clipped: (cs.overflow === 'hidden' || cs.overflowX === 'hidden' || cs.textOverflow === 'ellipsis') && el.scrollWidth > el.clientWidth + 1,
      });
    }
    const tag = el.tagName;
    const isTarget = ['A', 'BUTTON', 'SELECT', 'TEXTAREA'].includes(tag) || (tag === 'INPUT' && el.type !== 'hidden') || el.getAttribute('role') === 'button';
    if (isTarget) {
      const inline = tag === 'A' && el.parentElement && ['P', 'LI', 'SPAN'].includes(el.parentElement.tagName) && el.parentElement.textContent.trim().length > el.textContent.trim().length + 5;
      targets.push({ sel: path(el), text: (el.innerText || el.value || el.getAttribute('aria-label') || '').trim().slice(0, 40), x: r.left, y: r.top + scrollY, w: r.width, h: r.height, inline, inScroller: inScroller(el) });
    }
  }
  return { vw, docScrollWidth: document.documentElement.scrollWidth, bodyScrollWidth: document.body.scrollWidth, docHeight: document.documentElement.scrollHeight, texts, targets };
});
data.url = url; data.width = width; data.at = new Date().toISOString();
fs.writeFileSync(out, JSON.stringify(data, null, 1));
if (shot) await page.screenshot({ path: shot, fullPage: true });
await browser.close();
console.log(`${url} → ${out} (글자 ${data.texts.length}, 누르는 칸 ${data.targets.length}, 문서 폭 ${data.docScrollWidth}/${data.vw})`);
