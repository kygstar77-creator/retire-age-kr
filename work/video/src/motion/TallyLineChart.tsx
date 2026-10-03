// Tally 움직임 부품 ⑦ 선 그래프 그리기 — 선이 왼쪽에서 오른쪽으로 그려지고, 기준선(점선)과 끝 이름표를 단다.
// 서로 다른 대상(겹치는 집단 아님)의 같은 단위 값만 받는다. 값 꼬리표는 TallyTag로 따로 붙인다(좌표는 xy()로 구함).
import React from 'react';
import {interpolate, useCurrentFrame, Easing} from 'remotion';
import {T, F, CL} from '../parts/fm';

export type TallySeries = {name: string; color: string; dash?: string; width?: number; pts: number[]};
export const lineXY = (x: number, y: number, w: number, h: number, min: number, max: number, n: number) => (i: number, v: number) => [x + (i / Math.max(1, n - 1)) * w, y + h - ((v - min) / (max - min)) * h] as const;

export const TallyLineChart: React.FC<{series: TallySeries[]; x: number; y: number; w: number; h: number; min: number; max: number; start: number; dur?: number;
  base?: {v: number; text: string}; ticks?: {v: number; text: string}[]; xlabels?: {i: number; text: string}[]}> =
  ({series, x, y, w, h, min, max, start, dur = 60, base, ticks = [], xlabels = []}) => {
  const f = useCurrentFrame();
  const p = interpolate(f, [start, start + dur], [0, 1], {...CL, easing: Easing.inOut(Easing.quad)});
  const n = series[0]?.pts.length ?? 1;
  const xy = lineXY(x, y, w, h, min, max, n);
  return (
    <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
      {ticks.map((t, i) => { const [, ty] = xy(0, t.v); return (
        <g key={i}><line x1={x} x2={x + w} y1={ty} y2={ty} stroke={T.line} strokeWidth={2} />
          <text x={x - 14} y={ty + 8} textAnchor="end" fontFamily="PD" fontWeight={500} fontSize={22} fill={T.ink3}>{t.text}</text></g>); })}
      {base ? (() => { const [, by] = xy(0, base.v); return (
        <g><line x1={x} x2={x + w} y1={by} y2={by} stroke={T.ink} strokeWidth={3} strokeDasharray="10 8" />
          <text x={x + w} y={by + 32} textAnchor="end" fontFamily="PD" fontWeight={700} fontSize={24} fill={T.ink}>{base.text}</text></g>); })() : null}
      {xlabels.map((l, i) => { const [lx] = xy(l.i, min); return <text key={i} x={lx} y={y + h + 34} textAnchor="middle" fontFamily="PD" fontWeight={500} fontSize={22} fill={T.ink3}>{l.text}</text>; })}
      {series.map((s, si) => {
        const d = s.pts.map((v, i) => { const [px, py] = xy(i, v); return `${i ? 'L' : 'M'}${px.toFixed(1)} ${py.toFixed(1)}`; }).join(' ');
        const [ex, ey] = xy(s.pts.length - 1, s.pts[s.pts.length - 1]);
        return (
          <g key={si}>
            <path d={d} fill="none" stroke={s.color} strokeWidth={s.width ?? 5} strokeLinejoin="round" strokeLinecap="round" strokeDasharray={s.dash}
              style={{clipPath: `inset(0 ${(1 - p) * 100}% 0 0)`}} />
            <text x={ex + 14} y={ey + 8} fontFamily="PD" fontWeight={700} fontSize={26} fill={s.color} opacity={p >= 1 ? 1 : 0}>{s.name}</text>
          </g>
        );
      })}
    </svg>
  );
};
