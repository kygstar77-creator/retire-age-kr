// 겹침 탐침(2026-10-11 motion, U5) — 숫자 글자가 다른 카드·글자·도형에 가려지는지 렌더 중 브라우저 안에서 잰다.
// 사고: M-1 0:20~0:22 '2026년 10월 2일 기준' 카드가 막대 위 4.85억·5.10억을 가렸다(quality-gap-1011 ③).
// 직접 쓰지 않는다 — work/video/ovcheck.mjs가 편 컴포지션 옆에 붙여 every 프레임마다 재고 console에 'OVPROBE {json}'을 남긴다.
// 잰다: 숫자가 든 글자(HTML 글자 노드·SVG text)의 글자 상자 안 5점에서 document.elementsFromPoint로 그 글자보다 위에 그려진 것을 본다.
//   위에 있는 것이 '칠해진 것'(배경색·배경그림·img·fill 있는 SVG 도형·자기 글자)이고 보이는 정도(조상까지 곱한 opacity) 0.3 이상이면 가림. 5점 중 2점 이상 가려지면 겹침 1건.
//   선만 있는 도형(손그림 동그라미 등)은 가림으로 치지 않는다. 자막 상자가 숫자를 가려도 겹침이다.
import React, {useLayoutEffect} from 'react';
import {continueRender, delayRender, useCurrentFrame} from 'remotion';

const DIGIT = /[0-9]/;
const alpha = (c: string) => {
  if (!c || c === 'transparent') return 0;
  const m = c.match(/rgba?\(([^)]+)\)/);
  if (!m) return 1;
  const p = m[1].split(/[ ,/]+/).filter(Boolean);
  return p.length >= 4 ? parseFloat(p[3]) : 1;
};
const effOpacity = (el: Element | null) => {
  let o = 1;
  for (let e = el; e && e instanceof Element; e = e.parentElement) {
    const s = getComputedStyle(e);
    if (s.display === 'none' || s.visibility === 'hidden') return 0;
    o *= parseFloat(s.opacity || '1');
    if (o < 0.01) return 0;
  }
  return o;
};
const ownText = (el: Element) => Array.from(el.childNodes).filter((n) => n.nodeType === 3).map((n) => n.textContent || '').join('').trim();
const SHAPES = new Set(['rect', 'path', 'circle', 'ellipse', 'polygon', 'polyline']);
const paints = (el: Element) => {
  const s = getComputedStyle(el);
  const tag = el.tagName.toLowerCase();
  if (tag === 'img' || tag === 'canvas' || tag === 'video') return 'img';
  if (SHAPES.has(tag)) {
    const fill = s.fill;
    if (!fill || fill === 'none' || alpha(fill) * parseFloat(s.fillOpacity || '1') < 0.3) return '';
    return 'shape';
  }
  if (alpha(s.backgroundColor) >= 0.3) return 'bg';
  if (s.backgroundImage && s.backgroundImage !== 'none') return 'bgimg';
  if (ownText(el)) return 'text';
  return '';
};
const rgb = (c: string) => { const m = c.match(/rgba?\(([^)]+)\)/); return m ? m[1].split(/[ ,/]+/).filter(Boolean).slice(0, 3).map(Number) : [255, 255, 255]; };
// 글자 뒤 바탕색: 글자의 조상 중 처음 나오는 불투명 배경(없으면 흰색)
const backdrop = (el: Element) => {
  for (let e: Element | null = el; e; e = e.parentElement) { const c = getComputedStyle(e).backgroundColor; if (alpha(c) >= 0.9) return rgb(c); }
  return [255, 255, 255];
};
const sameColor = (a: number[], b: number[]) => a.every((v, i) => Math.abs(v - b[i]) <= 10);
const inOwnText = (el: Element, x: number, y: number) => Array.from(el.childNodes).some((n) => {
  if (n.nodeType !== 3 || !(n.textContent || '').trim()) return false;
  const r = document.createRange(); r.selectNodeContents(n);
  return Array.from(r.getClientRects()).some((q) => x >= q.left && x <= q.right && y >= q.top && y <= q.bottom);
});
const desc = (el: Element) => {
  const t = (ownText(el) || (el.textContent || '').trim()).replace(/\s+/g, ' ').slice(0, 30);
  const cls = typeof (el as HTMLElement).className === 'string' ? (el as HTMLElement).className.slice(0, 30) : '';
  return `${el.tagName.toLowerCase()}${cls ? '.' + cls : ''}${t ? ` '${t}'` : ''}`;
};

type Hit = {num: string; by: string; how: string; x: number; y: number; w: number; h: number};

export const probeOverlaps = (): {checked: number; hits: Hit[]} => {
  const hits: Hit[] = [];
  let checked = 0;
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const W = window.innerWidth, H = window.innerHeight;
  for (let n = walker.nextNode(); n; n = walker.nextNode()) {
    const txt = (n.textContent || '').trim();
    if (!txt || !DIGIT.test(txt)) continue;
    const host = n.parentElement;
    if (!host || effOpacity(host) < 0.5) continue;
    const r = document.createRange(); r.selectNodeContents(n);
    const b = r.getBoundingClientRect();
    if (b.width < 4 || b.height < 4 || b.right < 0 || b.bottom < 0 || b.left > W || b.top > H) continue;
    checked++;
    const pts = [[0.5, 0.5], [0.25, 0.35], [0.75, 0.35], [0.25, 0.65], [0.75, 0.65]].map(([fx, fy]) => [b.left + b.width * fx, b.top + b.height * fy]);
    let covered = 0; let by: Element | null = null; let how = '';
    for (const [x, y] of pts) {
      if (x < 0 || y < 0 || x >= W || y >= H) continue;
      for (const el of document.elementsFromPoint(x, y)) {
        if (el === host || host.contains(el)) break;          // 글자 자신에 닿았다 = 위에 아무것도 없다
        if (el.contains(host)) continue;                       // 조상(배경판)은 글자 아래
        const p = paints(el);
        if (!p || effOpacity(el) < 0.3) continue;
        const q = el.getBoundingClientRect();
        if (q.width * q.height >= 0.5 * W * H) continue;                        // 화면 절반 넘는 판 = 장면 층(전환·훅 카드) — 아래 장면이 통째로 안 보일 뿐
        if (p === 'bg' && !ownText(el) && sameColor(rgb(getComputedStyle(el).backgroundColor), backdrop(host))) continue;   // 바탕색 가림막(차례로 드러내기)
        if (p === 'text' && !inOwnText(el, x, y)) continue;                     // 글자끼리는 줄 상자가 아니라 실제 글자 자리로
        covered++; by = el; how = p; break;
      }
    }
    if (covered >= 2 && by) hits.push({num: txt.slice(0, 24), by: desc(by), how, x: Math.round(b.left), y: Math.round(b.top), w: Math.round(b.width), h: Math.round(b.height)});
  }
  return {checked, hits};
};

export const OverlapProbe: React.FC<{every: number}> = ({every}) => {
  const frame = useCurrentFrame();
  useLayoutEffect(() => {
    if (frame % every !== 0) return;
    const h = delayRender('overlap probe');
    const st = document.createElement('style'); st.textContent = '*{pointer-events:auto !important}';
    document.head.appendChild(st);
    requestAnimationFrame(() => requestAnimationFrame(() => {
      try {
        const res = probeOverlaps();
        console.log('OVPROBE ' + JSON.stringify({f: frame, ...res}));
      } catch (e) { console.log('OVPROBE ' + JSON.stringify({f: frame, err: String(e)})); }
      st.remove(); continueRender(h);
    }));
  }, [frame]);
  return null;
};
