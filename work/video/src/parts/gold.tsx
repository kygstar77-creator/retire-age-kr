// 금·환율 분해 그림 부품 — G-1(금값 1천만원 영수증)에서 처음 씀(2026-10-07 PD, parts.md 기록). 숫자 글자는 전부 props(g1props.py가 calc_out에서 뽑음).
// DivRows(0 기준 좌우 막대, 줄마다 시작 프레임·자리표) · LossRows(줄어든 만큼 막대 + 받는 돈 글자) · SplitBar(한 덩어리를 두 몫으로) · SpreadBand(기준값 위아래 ±% 띠)
import React from 'react';
import {interpolate, useCurrentFrame, Easing, spring, useVideoConfig} from 'remotion';
import {T, F, CL} from './fm';

const grow = (f: number, at: number, d = 20) => interpolate(f, [at, at + d], [0, 1], {...CL, easing: Easing.out(Easing.cubic)});
const fade = (f: number, at: number, d = 10) => interpolate(f, [at, at + d], [0, 1], CL);

// 0 기준 좌우 막대. rows = [이름, 값(%), 글자, 시작 프레임]. 이름은 왼쪽 고정 칸, 값 글자는 오른쪽 고정 칸(음수 글자가 이름을 덮지 않게).
// 아직 안 나온 줄은 점선 자리표. 마지막 줄을 합계로 쓰면 total=true(굵은 선 위)
export const DivRows: React.FC<{x0: number; y: number; rowH: number; half: number; max: number; rows: [string, number, string, number][]; total?: boolean; labelW?: number}> =
  ({x0, y, rowH, half, max, rows, total, labelW = 340}) => {
  const f = useCurrentFrame();
  const lx = x0 - half - labelW - 30; const vx = x0 + half + 36;
  return (
    <div style={{position: 'absolute', left: 0, top: 0}}>
      <div style={{position: 'absolute', left: x0 - 1, top: y - 16, width: 3, height: rows.length * rowH + 8, background: T.ink3}} />
      {rows.map(([n, v, t, at], i) => {
        const last = total && i === rows.length - 1; const shown = f >= at;
        const w = Math.min(half, Math.max(4, (Math.abs(v) / max) * half)) * grow(f, at); const c = last ? T.accent : v < 0 ? T.fall : T.rise;
        const top = y + i * rowH + (last ? 20 : 0);
        return <div key={i} style={{position: 'absolute', left: 0, top}}>
          {last ? <div style={{position: 'absolute', left: lx, width: vx + 220 - lx, top: -16, borderTop: `3px solid ${T.ink}`, opacity: fade(f, at)}} /> : null}
          <div style={{...F, position: 'absolute', left: lx, width: labelW, textAlign: 'right', top: 0, height: rowH - 20, lineHeight: `${rowH - 20}px`, fontWeight: 700, fontSize: last ? 40 : 36,
            color: shown ? T.ink : T.ink3, whiteSpace: 'nowrap'}}>{n}</div>
          {shown ? null : <div style={{position: 'absolute', left: x0 - half * 0.4, top: 6, width: half * 0.8, height: rowH - 32, borderRadius: 10, border: `3px dashed ${T.line}`}} />}
          {shown ? <div style={{position: 'absolute', left: v < 0 ? x0 - w : x0, top: 4, width: w, height: rowH - 28, borderRadius: 8, background: c}} /> : null}
          {shown ? <div style={{...F, position: 'absolute', left: vx, top: 0, height: rowH - 20, lineHeight: `${rowH - 20}px`,
            fontWeight: 700, fontSize: last ? 48 : 40, color: c, opacity: fade(f, at + 12), whiteSpace: 'nowrap'}}>{t}</div> : null}
        </div>;
      })}
    </div>
  );
};

// 줄어든 만큼 막대(왼→오) + 오른쪽에 받는 돈. rows = [이름, 줄어든 원, 글자, 시작, 강조]
export const LossRows: React.FC<{x: number; y: number; w: number; rowH: number; max: number; rows: [string, number, string, number, boolean][]}> = ({x, y, w, rowH, max, rows}) => {
  const f = useCurrentFrame();
  return (
    <div style={{position: 'absolute', left: x, top: y}}>
      {rows.map(([n, v, t, at, hot], i) => {
        const p = grow(f, at, 22); const bw = (v / max) * w * p;
        return <div key={i} style={{position: 'absolute', left: 0, top: i * rowH, opacity: fade(f, at - 6, 6)}}>
          <div style={{...F, position: 'absolute', left: 0, width: 230, top: 0, height: rowH - 30, lineHeight: `${rowH - 30}px`, fontWeight: 700, fontSize: 36, color: T.ink, whiteSpace: 'nowrap'}}>{n}</div>
          <div style={{position: 'absolute', left: 250, top: 6, width: bw, height: rowH - 42, borderRadius: 8, background: hot ? T.fall : T.ink3, opacity: hot ? 1 : 0.55}} />
          <div style={{...F, position: 'absolute', left: 250 + bw + 18, top: 0, height: rowH - 30, lineHeight: `${rowH - 30}px`, fontWeight: 700, fontSize: hot ? 40 : 34, color: hot ? T.fall : T.ink2,
            opacity: fade(f, at + 16), whiteSpace: 'nowrap'}}>{t}</div>
        </div>;
      })}
    </div>
  );
};

// 한 덩어리(낸 돈)를 두 몫으로: 왼쪽 큰 몫(금값) + 오른쪽 작은 몫(세금, 빨강). 몫끼리 겹치지 않는다
export const SplitBar: React.FC<{x: number; y: number; w: number; h: number; ratio: number; at: number; splitAt: number; whole: string; a: [string, string]; b: [string, string]}> =
  ({x, y, w, h, ratio, at, splitAt, whole, a, b}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const p = grow(f, at, 24); const s = spring({frame: f - splitAt, fps, config: {damping: 14}});
  const gap = 18 * s; const wb = w * ratio; const wa = w - wb;
  return (
    <div style={{position: 'absolute', left: x, top: y}}>
      <div style={{...F, position: 'absolute', left: 0, top: -64, fontWeight: 700, fontSize: 36, color: T.ink2, opacity: fade(f, at), whiteSpace: 'nowrap'}}>{whole}</div>
      <div style={{position: 'absolute', left: 0, top: 0, width: (wa) * p, height: h, borderRadius: '12px 0 0 12px', background: T.ink2}} />
      <div style={{position: 'absolute', left: wa * p + gap, top: 0, width: wb * p, height: h, borderRadius: '0 12px 12px 0', background: f >= splitAt ? T.rise : T.ink2}} />
      <div style={{...F, position: 'absolute', left: 0, top: h + 18, fontWeight: 700, fontSize: 30, color: T.ink2, opacity: fade(f, splitAt), whiteSpace: 'nowrap'}}>{a[0]}</div>
      <div style={{...F, position: 'absolute', left: 0, top: h + 58, fontWeight: 700, fontSize: 52, color: T.ink, opacity: fade(f, splitAt), whiteSpace: 'nowrap'}}>{a[1]}</div>
      <div style={{...F, position: 'absolute', left: wa + gap + wb, top: h + 18, transform: 'translateX(-100%)', textAlign: 'right', fontWeight: 700, fontSize: 30, color: T.rise, opacity: fade(f, splitAt + 6), whiteSpace: 'nowrap'}}>{b[0]}</div>
      <div style={{...F, position: 'absolute', left: wa + gap + wb, top: h + 58, transform: 'translateX(-100%)', fontWeight: 700, fontSize: 52, color: T.rise, opacity: fade(f, splitAt + 6), whiteSpace: 'nowrap'}}>{b[1]}</div>
    </div>
  );
};

// 기준값 가운데 선 + 위(살 때 +%) 아래(팔 때 −%) 띠, 그 사이 폭 괄호
export const SpreadBand: React.FC<{x: number; y: number; w: number; step: number; mid: number; buy: number; sell: number; gap: number; labels: {mid: string; buy: string; sell: string; gap: string}}> =
  ({x, y, w, step, mid, buy, sell, gap, labels}) => {
  const f = useCurrentFrame();
  const line = (yy: number, at: number, c: string, txt: string, dash?: boolean) => (
    <div style={{position: 'absolute', left: 0, top: yy, opacity: fade(f, at)}}>
      <div style={{position: 'absolute', left: 0, top: 0, width: w * grow(f, at, 18), borderTop: `${dash ? 4 : 6}px ${dash ? 'dashed' : 'solid'} ${c}`}} />
      <div style={{...F, position: 'absolute', left: w + 24, top: -24, fontWeight: 700, fontSize: 36, color: c, whiteSpace: 'nowrap'}}>{txt}</div>
    </div>
  );
  return (
    <div style={{position: 'absolute', left: x, top: y}}>
      {f >= buy ? <div style={{position: 'absolute', left: 0, top: -step, width: w, height: step, background: T.rise, opacity: 0.12 * fade(f, buy)}} /> : null}
      {f >= sell ? <div style={{position: 'absolute', left: 0, top: 0, width: w, height: step, background: T.fall, opacity: 0.12 * fade(f, sell)}} /> : null}
      {line(0, mid, T.ink, labels.mid)}
      {line(-step, buy, T.rise, labels.buy, true)}
      {line(step, sell, T.fall, labels.sell, true)}
      <div style={{position: 'absolute', left: w * 0.5 - 4, top: -step, width: 8, height: step * 2 * grow(f, gap, 16), background: T.accent, borderRadius: 4}} />
      <div style={{...F, position: 'absolute', left: w * 0.5 - 180, top: step + 30, fontWeight: 700, fontSize: 40, color: T.accent, background: '#fff', borderRadius: 10, padding: '4px 14px', opacity: fade(f, gap + 10), whiteSpace: 'nowrap'}}>{labels.gap}</div>
    </div>
  );
};
