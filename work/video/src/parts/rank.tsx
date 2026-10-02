// 줄 세우기(백분위) 그림 부품 — N-1 '나 vs 남들'에서 처음 씀. 다음 나 vs 남들 편도 같은 모양으로 쓴다(parts.md 기록).
// 100칸 띠+자리 표시 · 100칸 막대(넘치는 칸은 끊김 표시) · 백분위 눈금자+핀 · 가운데 0 기준 좌우 막대(증감)
import React from 'react';
import {scaleLinear} from 'd3-scale';
import {T, F, appear} from './fm';

// 100칸 띠 — 왼쪽 = 상위 1%. pos(상위 %)에 역삼각 표시, 표시가 from → to로 미끄러진다
export const PctStrip: React.FC<{x: number; y: number; w: number; h?: number; o: number; mark?: number; label?: string; markO?: number; hiFrom?: number; hiTo?: number; hiO?: number; color?: string}> =
  ({x, y, w, h = 70, o, mark, label, markO = 1, hiFrom, hiTo, hiO = 0, color = T.accent}) => {
  const cw = w / 100; const mx = mark === undefined ? 0 : x + mark * cw;
  return (
    <div style={{position: 'absolute', left: 0, top: 0, opacity: o}}>
      {Array.from({length: 100}).map((_, i) => {
        const on = hiFrom !== undefined && hiTo !== undefined && i >= hiFrom && i < hiTo;
        return <div key={i} style={{position: 'absolute', left: x + i * cw, top: y, width: cw - 2, height: h, borderRadius: 3,
          background: on && hiO > 0.5 ? color : i % 10 === 9 ? T.ink3 : T.line}} />;
      })}
      {[0, 25, 50, 75, 100].map((p) => <div key={p} style={{...F, position: 'absolute', left: x + p * cw - 60, width: 120, textAlign: 'center', top: y + h + 12, fontWeight: 500, fontSize: 24, color: T.ink3}}>
        {p === 0 ? '상위 0%' : `${p}%`}</div>)}
      {mark !== undefined ? <div style={{position: 'absolute', left: mx, top: y - 18, opacity: markO}}>
        <div style={{position: 'absolute', left: -16, top: -10, width: 0, height: 0, borderLeft: '16px solid transparent', borderRight: '16px solid transparent', borderTop: `22px solid ${color}`}} />
        <div style={{position: 'absolute', left: -2, top: 10, width: 4, height: h + 18, background: color}} />
        {label ? <div style={{...F, position: 'absolute', left: -200, width: 400, textAlign: 'center', top: -76, fontWeight: 700, fontSize: 40, color}}>{label}</div> : null}
      </div> : null}
    </div>
  );
};

// 100칸 막대 — vals[0] = 상위 1% 칸. cap을 넘는 칸은 위를 끊고 '≈' 표시
export const HundredBars: React.FC<{x: number; y: number; w: number; h: number; vals: number[]; cap: number; p: number; hi?: number[]; hiColor?: string; dim?: number}> =
  ({x, y, w, h, vals, cap, p, hi = [], hiColor = T.accent, dim = 0}) => {
  const cw = w / vals.length; const sy = scaleLinear().domain([0, cap]).range([0, h]);
  return (
    <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
      <line x1={x - 6} x2={x + w} y1={y} y2={y} stroke={T.ink3} strokeWidth={2} />
      {vals.map((v, i) => { const g = appear(p * 80, i * 0.5, 24); const bh = sy(Math.min(v, cap)) * g; const on = hi.includes(i);
        return <g key={i}>
          <rect x={x + i * cw} y={y - bh} width={cw - 3} height={bh} rx={2} fill={on ? hiColor : T.ink2} opacity={on ? 1 : 1 - dim * 0.6} />
          {v > cap && g > 0.9 ? <text x={x + i * cw + cw / 2} y={y - h - 10} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={22} fill={T.ink2}>≈</text> : null}
        </g>; })}
    </svg>
  );
};

// 백분위 눈금자 — ticks = [[백분위, 값 글자]], 왼쪽 P10 → 오른쪽 P90. 핀은 [글자, 백분위(0~100)]
export const PctRuler: React.FC<{x: number; y: number; w: number; ticks: [number, string][]; o: number[]; pins?: [string, number, number, string?][]; color?: string; hiTick?: number; hiO?: number}> =
  ({x, y, w, ticks, o, pins = [], color = T.fall, hiTick, hiO = 0}) => {
  const px = (p: number) => x + (p / 100) * w;
  return (
    <div style={{position: 'absolute', left: 0, top: 0}}>
      <div style={{position: 'absolute', left: x, top: y, width: w, height: 8, borderRadius: 4, background: T.line}} />
      <div style={{position: 'absolute', left: x, top: y, width: w * (o[0] ?? 1), height: 8, borderRadius: 4, background: color}} />
      {ticks.map(([p, t], i) => { const on = hiTick === p && hiO > 0.5; const tO = o[1] === undefined ? 1 : appear(o[1] * 60, i * 4, 14);
        return <div key={p} style={{position: 'absolute', left: px(p), top: y - 20, opacity: tO}}>
          <div style={{position: 'absolute', left: -3, top: 0, width: 6, height: 48, background: on ? T.accent : T.ink}} />
          <div style={{...F, position: 'absolute', left: -60, width: 120, textAlign: 'center', top: 60, fontWeight: 700, fontSize: 24, color: T.ink3}}>{`P${p}`}</div>
          <div style={{...F, position: 'absolute', left: -80, width: 160, textAlign: 'center', top: 92, fontWeight: 700, fontSize: on ? 30 : 25, lineHeight: 1.2, color: on ? T.accent : T.ink2}}>
            {t.split(' ').map((w, j) => <div key={j}>{w}</div>)}</div>
        </div>; })}
      {pins.map(([t, p, po, c], i) => (
        <div key={i} style={{position: 'absolute', left: px(p), top: y - 150 + (1 - po) * -30, opacity: po}}>
          <div style={{...F, position: 'absolute', left: -110, width: 220, textAlign: 'center', top: 0, fontWeight: 700, fontSize: 34, color: '#fff', background: c ?? T.ink, borderRadius: 30, padding: '8px 0'}}>{t}</div>
          <div style={{position: 'absolute', left: -2, top: 62, width: 4, height: 92, background: c ?? T.ink}} />
        </div>))}
    </div>
  );
};

// 가운데 0 기준 좌우 막대(증감) — rows = [이름, 값], 음수는 파랑 왼쪽, 양수는 빨강 오른쪽
export const DivergeRows: React.FC<{x0: number; y: number; rowH: number; rows: [string, number][]; max: number; half: number; p: number; hi: number[]; dimOthers?: number; fmt: (v: number) => string}> =
  ({x0, y, rowH, rows, max, half, p, hi, dimOthers = 0, fmt}) => (
  <div style={{position: 'absolute', left: 0, top: 0}}>
    <div style={{position: 'absolute', left: x0 - 1, top: y - 10, width: 2, height: rows.length * rowH, background: T.ink3}} />
    {rows.map(([n, v], i) => { const w = (Math.abs(v) / max) * half * appear(p * 60, i * 3, 20); const on = hi.includes(i); const op = on || !dimOthers ? 1 : 1 - dimOthers * 0.65;
      const c = v < 0 ? T.fall : T.rise;
      return <div key={n} style={{position: 'absolute', left: 0, top: y + i * rowH, opacity: op}}>
        <div style={{...F, position: 'absolute', left: x0 - 520, width: 120, textAlign: 'right', top: 4, fontWeight: 700, fontSize: 28, color: T.ink}}>{n}</div>
        <div style={{position: 'absolute', left: v < 0 ? x0 - Math.max(3, w) : x0, top: 4, width: Math.max(3, w), height: rowH - 18, borderRadius: 6, background: c, outline: on ? `3px solid ${T.accent}` : 'none'}} />
        <div style={{...F, position: 'absolute', left: v < 0 ? x0 - Math.max(3, w) - 14 : x0 + Math.max(3, w) + 14, transform: v < 0 ? 'translateX(-100%)' : 'none', top: 2, fontWeight: 700, fontSize: on ? 34 : 28, color: on ? c : T.ink2, whiteSpace: 'nowrap'}}>{fmt(v)}</div>
      </div>; })}
  </div>
);
