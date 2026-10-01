// 강조는 잉크, 주황은 손그림 동그라미·파이어맵 숫자에만(guide ③, 2026-10-01 motion 감사)
// 범용 그림 부품(RULES 6-3 — E-1에서 처음 씀, research/longform/loop/parts.md에 기록). 숫자는 전부 props로 받는다.
// 세로 막대 계열(강조·테두리·점선 추정 막대) · 범위 띠+실제 점 · 전후 가로 막대(배수 꼬리표) · 도넛 · 저울 · 원문 카드 · 계단 막대
import React from 'react';
import {useCurrentFrame, interpolate} from 'remotion';
import {scaleLinear} from 'd3-scale';
import {T, F, CL, appear, CountUp} from './fm';

// 세로 막대 계열: vals 막대, hi=강조 칸(색), ring=테두리 칸, est=[값, ±]이면 오른쪽에 점선 추정 막대+오차 막대
export const BarSeries: React.FC<{x: number; y: number; w: number; h: number; vals: number[]; labels: string[]; p: number; color?: string;
  hi?: number[]; ring?: number[]; show?: number[]; est?: [number, number] | null; estP?: number; estLabel?: string; fmt?: (v: number) => string; max?: number}> =
  ({x, y, w, h, vals, labels, p, color = T.ink, hi = [], ring = [], show = [], est = null, estP = 0, estLabel = '', fmt = (v) => v.toLocaleString(), max}) => {
  const n = vals.length + (est ? 1 : 0); const slot = w / n; const bw = slot * 0.68;
  const mx = max ?? Math.max(...vals, est ? est[0] + est[1] : 0) * 1.1; const sy = scaleLinear().domain([0, mx]).range([0, h]);
  return (
    <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
      <line x1={x - 10} x2={x + w} y1={y} y2={y} stroke={T.ink3} strokeWidth={2} />
      {vals.map((v, i) => { const bh = sy(v) * appear(p * 60, i * 4, 30); const on = hi.includes(i), rg = ring.includes(i);
        return <g key={i}>
          <rect x={x + i * slot} y={y - bh} width={bw} height={bh} rx={8} fill={on ? color : T.line} stroke={rg ? T.ink : 'none'} strokeWidth={rg ? 4 : 0} />
          <text x={x + i * slot + bw / 2} y={y + 34} textAnchor="middle" fontFamily="PD" fontWeight={500} fontSize={24} fill={T.ink3}>{labels[i]}</text>
          {on || rg || show.includes(i) ? <text x={x + i * slot + bw / 2} y={y - bh - 14} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={on ? 36 : 28} fill={on ? color : T.ink} opacity={p}>{fmt(v)}</text> : null}
        </g>; })}
      {est ? (() => { const i = vals.length; const bh = sy(est[0]) * estP; const cx = x + i * slot + bw / 2;
        return <g opacity={Math.min(1, estP * 2)}>
          <rect x={x + i * slot} y={y - bh} width={bw} height={bh} rx={8} fill="none" stroke={color} strokeWidth={4} strokeDasharray="12 8" />
          <line x1={cx} x2={cx} y1={y - sy(est[0] + est[1])} y2={y - sy(est[0] - est[1])} stroke={T.ink} strokeWidth={4} opacity={estP} />
          {[est[0] + est[1], est[0] - est[1]].map((e) => <line key={e} x1={cx - 16} x2={cx + 16} y1={y - sy(e)} y2={y - sy(e)} stroke={T.ink} strokeWidth={4} opacity={estP} />)}
          <text x={cx} y={y - sy(est[0] + est[1]) - 18} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={34} fill={color}>{`${fmt(est[0])} ± ${est[1]}`}</text>
          <text x={cx} y={y + 34} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={24} fill={color}>{estLabel}</text>
        </g>; })() : null}
    </svg>
  );
};

// 범위 띠 + 실제 점: 전망 lo~hi 띠 위에 실제 값 점, 넘친 만큼 화살표
export const RangeDot: React.FC<{x0: number; x1: number; y: number; dom: [number, number]; lo: number; hi: number; act: number; pBand: number; pDot: number; unit?: string; bandLabel: string; actLabel: string}> =
  ({x0, x1, y, dom, lo, hi, act, pBand, pDot, unit = '', bandLabel, actLabel}) => {
  const sx = scaleLinear().domain(dom).range([x0, x1]); const ax = sx(hi) + (sx(act) - sx(hi)) * pDot;
  const ticks = []; for (let t = Math.ceil(dom[0] / 10) * 10; t <= dom[1]; t += 10) ticks.push(t);
  return (
    <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
      <line x1={x0} x2={x1} y1={y} y2={y} stroke={T.line} strokeWidth={6} />
      {ticks.map((t) => <g key={t}><line x1={sx(t)} x2={sx(t)} y1={y - 12} y2={y + 12} stroke={T.ink3} strokeWidth={2} />
        <text x={sx(t)} y={y + 50} textAnchor="middle" fontFamily="PD" fontWeight={500} fontSize={24} fill={T.ink3}>{t}</text></g>)}
      <g opacity={pBand}><rect x={sx(lo)} y={y - 50} width={(sx(hi) - sx(lo)) * pBand} height={100} rx={12} fill={T.ink3} opacity={0.35} />
        <text x={(sx(lo) + sx(hi)) / 2} y={y - 80} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={34} fill={T.ink2}>{bandLabel}</text>
        <text x={(sx(lo) + sx(hi)) / 2} y={y + 100} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={30} fill={T.ink2}>{`${lo}~${hi}${unit}`}</text></g>
      <g opacity={pDot}>
        <line x1={sx(hi)} x2={ax} y1={y - 130} y2={y - 130} stroke={T.ink} strokeWidth={4} strokeDasharray="8 6" />
        <circle cx={ax} cy={y} r={26} fill={T.ink} />
        <text x={ax} y={y - 150} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={48} fill={T.ink}>{actLabel}</text>
        <text x={(sx(hi) + ax) / 2} y={y - 100} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={28} fill={T.ink2}>{`상단보다 +${(act - hi).toFixed(1)}${unit}`}</text>
      </g>
    </svg>
  );
};

// 전후 가로 막대: 행마다 1년 전(회색) vs 지금(색) + 배수 꼬리표
export const PairBars: React.FC<{x: number; y: number; w: number; rows: [string, number, number][]; p: number[]; hi?: number; color?: string; tags: [string, string]}> =
  ({x, y, w, rows, p, hi = 0, color = T.ink, tags}) => {
  const mx = Math.max(...rows.map((r) => r[2])) * 1.05; const sx = scaleLinear().domain([0, mx]).range([0, w]);
  return (
    <div style={{position: 'absolute', left: 0, top: 0}}>
      <div style={{...F, position: 'absolute', left: x + 380, top: y - 50, display: 'flex', gap: 28, fontWeight: 700, fontSize: 24, color: T.ink3, whiteSpace: 'nowrap'}}>
        <span><span style={{display: 'inline-block', width: 22, height: 22, background: T.ink3, borderRadius: 4, marginRight: 8, verticalAlign: -3}} />{tags[0]}</span>
        <span><span style={{display: 'inline-block', width: 22, height: 22, background: color, borderRadius: 4, marginRight: 8, verticalAlign: -3}} />{tags[1]}</span></div>
      {rows.map(([n, a, b], i) => { const o = p[i] ?? 0; const on = i === hi;
        return <div key={n} style={{position: 'absolute', left: x, top: y + i * 142, opacity: Math.min(1, o * 2)}}>
          <div style={{...F, fontWeight: 700, fontSize: 32, color: on ? T.ink : T.ink2, width: 360, position: 'absolute', top: 24, wordBreak: 'keep-all', lineHeight: 1.2}}>{n}</div>
          <div style={{position: 'absolute', left: 380, top: 6, width: sx(a) * o, height: 44, borderRadius: 8, background: T.ink3, opacity: 0.55}} />
          <div style={{...F, position: 'absolute', left: 390 + sx(a) * o, top: 10, fontWeight: 500, fontSize: 26, color: T.ink2}}>{a.toLocaleString()}</div>
          <div style={{position: 'absolute', left: 380, top: 58, width: sx(b) * o, height: 60, borderRadius: 8, background: on ? color : T.ink2, opacity: on ? 1 : 0.55}} />
          <div style={{...F, position: 'absolute', left: 396 + sx(b) * o, top: 62, fontWeight: 700, fontSize: 36, color: on ? color : T.ink, whiteSpace: 'nowrap'}}>
            {b.toLocaleString()} <span style={{fontSize: 30, background: on ? color : T.line, color: on ? '#fff' : T.ink, borderRadius: 20, padding: '2px 14px', marginLeft: 8}}>{(b / a).toFixed(1)}배</span></div>
        </div>; })}
    </div>
  );
};

// 도넛: 비중 v%(0~100), 가운데 숫자
export const Donut: React.FC<{cx: number; cy: number; r: number; v: number; p: number; color?: string; label: string}> = ({cx, cy, r, v, p, color = T.ink, label}) => {
  const C = 2 * Math.PI * r; const dash = (C * v / 100) * p;
  return (
    <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0, opacity: Math.min(1, p * 3)}}>
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={T.line} strokeWidth={r * 0.34} />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={color} strokeWidth={r * 0.34} strokeDasharray={`${dash} ${C}`} transform={`rotate(-90 ${cx} ${cy})`} />
      <text x={cx} y={cy + 22} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={r * 0.52} fill={color}>{`${(v * p).toFixed(1)}%`}</text>
      <text x={cx} y={cy + r + 80} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={30} fill={T.ink}>{label}</text>
    </svg>
  );
};

// 저울: 왼쪽·오른쪽 값 비율로 막대가 기운다(최대 14도), 접시 위 숫자 카드
export const Seesaw: React.FC<{cx: number; cy: number; L: [string, string]; R: [string, string]; ratio: number; p: number; mid?: string[]; midP?: number}> =
  ({cx, cy, L, R, ratio, p, mid = [], midP = 0}) => {
  const ang = -14 * Math.max(-1, Math.min(1, ratio)) * p; const arm = 520; const rad = (ang * Math.PI) / 180;
  const lx = cx - arm * Math.cos(rad), ly = cy - arm * Math.sin(rad), rx = cx + arm * Math.cos(rad), ry = cy + arm * Math.sin(rad);
  const pan = (x: number, y: number, t: [string, string], big: boolean) => (
    <g><line x1={x} x2={x} y1={y} y2={y + 60} stroke={T.ink2} strokeWidth={4} />
      <rect x={x - 240} y={y + 60} width={480} height={big ? 170 : 130} rx={16} fill={big ? T.ink : T.surface} stroke={big ? 'none' : T.line} strokeWidth={3} />
      <text x={x} y={y + 108} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={28} fill={big ? '#fff' : T.ink2}>{t[0]}</text>
      <text x={x} y={y + (big ? 180 : 162)} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={big ? 52 : 44} fill={big ? '#fff' : T.ink}>{t[1]}</text></g>);
  return (
    <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
      <polygon points={`${cx},${cy} ${cx - 60},${cy + 200} ${cx + 60},${cy + 200}`} fill={T.ink2} />
      <line x1={lx} y1={ly} x2={rx} y2={ry} stroke={T.ink} strokeWidth={12} strokeLinecap="round" />
      {pan(lx, ly, L, true)}{pan(rx, ry, R, false)}
      <g opacity={midP}>{mid.map((m, i) => <text key={i} x={cx} y={cy - 160 + i * 56} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={40} fill={T.rise}>{m}</text>)}</g>
    </svg>
  );
};

// 원문 카드(한글 공시 인용): 위 출처 줄, 가운데 문장, 아래 큰 숫자
export const QuoteCard: React.FC<{x: number; y: number; w: number; h: number; o: number; src: string; body: string; big: string}> = ({x, y, w, h, o, src, body, big}) => (
  <div style={{position: 'absolute', left: x, top: y + (1 - o) * 24, width: w, height: h, background: T.surface, borderRadius: 20, opacity: o, borderTop: `8px solid ${T.ink}`}}>
    <div style={{...F, fontWeight: 700, fontSize: 26, color: T.ink3, padding: '28px 40px 0'}}>{src}</div>
    <div style={{position: 'absolute', left: 30, top: 70, fontFamily: 'PD', fontWeight: 700, fontSize: 110, color: T.line, lineHeight: 1}}>“</div>
    <div style={{...F, fontWeight: 500, fontSize: 36, color: T.ink2, padding: '40px 40px 0 90px', lineHeight: 1.45, wordBreak: 'keep-all'}}>{body}</div>
    <div style={{...F, fontWeight: 700, fontSize: 76, color: T.rise, position: 'absolute', left: 90, bottom: 36}}>{big}</div>
  </div>
);

// 계단 막대(가로 진행): 해마다 커지는 값, 마지막 칸 꼬리표
export const Stairs: React.FC<{x: number; y: number; w: number; h: number; rows: [string, number][]; p: number[]; tag: string; tagP: number; fmt: (v: number) => string}> =
  ({x, y, w, h, rows, p, tag, tagP, fmt}) => {
  const mx = Math.max(...rows.map((r) => r[1])) * 1.1; const slot = w / rows.length; const bw = slot * 0.62;
  return (
    <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
      <line x1={x - 10} x2={x + w} y1={y} y2={y} stroke={T.ink3} strokeWidth={2} />
      {rows.map(([n, v], i) => { const o = p[i] ?? 0; const bh = (v / mx) * h * o; const last = i === rows.length - 1;
        return <g key={n} opacity={Math.min(1, o * 2)}>
          <rect x={x + i * slot} y={y - bh} width={bw} height={bh} rx={10} fill={last ? T.ink : T.line} stroke={last ? 'none' : T.ink3} strokeWidth={2} />
          <text x={x + i * slot + bw / 2} y={y - bh - 18} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={last ? 44 : 36} fill={T.ink}>{fmt(v)}</text>
          <text x={x + i * slot + bw / 2} y={y + 42} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={30} fill={T.ink2}>{n}</text>
        </g>; })}
      <g opacity={tagP}><rect x={x + (rows.length - 1) * slot + bw / 2 - 230} y={y - h / 1.1 - 150} width={460} height={64} rx={32} fill={T.ink} />
        <text x={x + (rows.length - 1) * slot + bw / 2} y={y - h / 1.1 - 106} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={32} fill="#fff">{tag}</text></g>
    </svg>
  );
};

export const _unused = {interpolate, CL, CountUp};
