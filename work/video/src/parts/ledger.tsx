// 장부(재무제표) 그림 부품 — E-2(테슬라)에서 처음 씀. 다른 종목 편도 같은 모양으로 쓴다(parts.md 기록).
// 막대+선 겹친 10분기 · 폭포(총이익→영업이익) · 기울기 줄(전→후) · 면적 원 2개(크기 비교) · 채움 막대(계획 대비 실적)
import React from 'react';
import {scaleLinear} from 'd3-scale';
import {line as d3line, curveMonotoneX} from 'd3-shape';
import {T, F, appear} from './fm';

// 막대(매출) + 선(비율) — 막대는 회색, 마지막만 잉크, 선은 주황. 선 최고·최저 점에 값
export const ComboBarLine: React.FC<{x: number; y: number; w: number; h: number; vals: number[]; labels: string[]; line: number[]; p: number; lp: number;
  lineMax: number; tagBars?: number[]; tagP?: number; fmt?: (v: number) => string; lfmt?: (v: number) => string}> =
  ({x, y, w, h, vals, labels, line, p, lp, lineMax, tagBars = [], tagP = 0, fmt = (v) => v.toLocaleString(), lfmt = (v) => `${v}%`}) => {
  const n = vals.length; const slot = w / n; const bw = slot * 0.62; const sy = scaleLinear().domain([0, Math.max(...vals) * 1.15]).range([0, h]);
  const ly = scaleLinear().domain([0, lineMax]).range([y, y - h]); const cx = (i: number) => x + i * slot + bw / 2;
  const m = Math.max(2, Math.round(n * lp)); const d = d3line<number>().x((_, i) => cx(i)).y((v) => ly(v)).curve(curveMonotoneX)(line.slice(0, m)) || '';
  const hiI = line.indexOf(Math.max(...line)), loI = line.indexOf(Math.min(...line));
  return (
    <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
      <line x1={x - 10} x2={x + w} y1={y} y2={y} stroke={T.ink3} strokeWidth={2} />
      {vals.map((v, i) => { const bh = sy(v) * appear(p * 60, i * 3, 30); const last = i === n - 1;
        return <g key={i}>
          <rect x={x + i * slot} y={y - bh} width={bw} height={bh} rx={8} fill={last ? T.ink : T.line} />
          <text x={cx(i)} y={y + 34} textAnchor="middle" fontFamily="PD" fontWeight={500} fontSize={22} fill={T.ink3}>{labels[i]}</text>
          {tagBars.includes(i) ? <text x={cx(i)} y={y - bh - 14} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={32} fill={T.ink} opacity={tagP}>{fmt(v)}</text> : null}
        </g>; })}
      <g opacity={Math.min(1, lp * 3)}>
        <path d={d} stroke={T.accent} strokeWidth={6} fill="none" strokeLinejoin="round" />
        {line.slice(0, m).map((v, i) => <circle key={i} cx={cx(i)} cy={ly(v)} r={i === hiI || i === loI ? 11 : 6} fill={T.accent} />)}
        {[hiI, loI].filter((i) => i < m).map((i) => <g key={'t' + i}>
          <rect x={cx(i) - 62} y={ly(line[i]) - 66} width={124} height={46} rx={23} fill={T.accent} />
          <text x={cx(i)} y={ly(line[i]) - 33} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={28} fill="#fff">{lfmt(line[i])}</text></g>)}
      </g>
    </svg>
  );
};

// 폭포: 첫 막대(총이익) → 빼는 칸들이 아래로 떠 내려감 → 마지막 막대(남은 것). p[i]는 칸마다 등장
export const Waterfall: React.FC<{x: number; y: number; w: number; h: number; steps: [string, number][]; p: number[]; tags?: string[]; tagP?: number; fmt?: (v: number) => string}> =
  ({x, y, w, h, steps, p, tags = [], tagP = 0, fmt = (v) => Math.abs(v).toLocaleString()}) => {
  const top = steps[0][1]; const sy = scaleLinear().domain([0, top * 1.12]).range([0, h]); const slot = w / steps.length; const bw = slot * 0.6;
  let run = 0;
  return (
    <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
      <line x1={x - 10} x2={x + w} y1={y} y2={y} stroke={T.ink3} strokeWidth={2} />
      {steps.map(([n, v], i) => {
        const o = p[i] ?? 0; const last = i === steps.length - 1; const first = i === 0;
        let y0: number, y1: number;
        if (first || last) { y0 = y - sy(v); y1 = y; if (first) run = v; } else { y0 = y - sy(run); y1 = y - sy(run + v); run += v; }
        const hh = (y1 - y0) * o; const bx = x + i * slot;
        return <g key={n} opacity={Math.min(1, o * 2)}>
          {i > 0 ? <line x1={bx - slot + bw} x2={bx} y1={y0} y2={y0} stroke={T.ink3} strokeWidth={2} strokeDasharray="6 6" /> : null}
          <rect x={bx} y={y0} width={bw} height={hh} rx={8} fill={first ? T.ink2 : last ? T.accent : T.line} stroke={first || last ? 'none' : T.fall} strokeWidth={3} />
          <text x={bx + bw / 2} y={first || last ? y0 - 16 : y0 + hh / 2 + 14} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={last ? 44 : 36}
            fill={last ? T.accent : first ? T.ink : T.fall}>{(v < 0 ? '−' : '') + fmt(v)}</text>
          <text x={bx + bw / 2} y={y + 40} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={28} fill={T.ink2}>{n}</text>
          {tags[i] ? <text x={bx + bw / 2} y={y + 78} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={26} fill={tags[i].startsWith('−') ? T.fall : T.rise} opacity={tagP}>{`1년 전보다 ${tags[i]}`}</text> : null}
        </g>;
      })}
    </svg>
  );
};

// 기울기 줄: 왼쪽 '전' 점 → 오른쪽 '후' 점, 줄마다 이름표. hi 줄만 진하게
export const SlopeRows: React.FC<{x: number; y: number; w: number; h: number; rows: [string, number, number][]; p: number[]; hi?: number; max: number; heads: [string, string]}> =
  ({x, y, w, h, rows, p, hi = -1, max, heads}) => {
  const sy = scaleLinear().domain([0, max]).range([y + h, y]); const xa = x + 360, xb = x + w - 200;
  // 오른쪽 값 글자가 겹치지 않게 46px 이상 벌린다(점 위치는 그대로)
  const ly: number[] = rows.map((r) => sy(r[2])); const ord = ly.map((_, i) => i).sort((a, b) => ly[a] - ly[b]);
  ord.forEach((i, k) => { if (k > 0 && ly[i] - ly[ord[k - 1]] < 46) ly[i] = ly[ord[k - 1]] + 46; });
  return (
    <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
      <text x={xa} y={y - 30} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={30} fill={T.ink3}>{heads[0]}</text>
      <text x={xb} y={y - 30} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={30} fill={T.ink}>{heads[1]}</text>
      <line x1={xa} x2={xa} y1={y} y2={y + h} stroke={T.line} strokeWidth={3} /><line x1={xb} x2={xb} y1={y} y2={y + h} stroke={T.line} strokeWidth={3} />
      {rows.map(([n, a, b], i) => { const o = p[i] ?? 0; const on = i === hi; const c = on ? T.accent : T.ink2; const xe = xa + (xb - xa) * o;
        const ye = sy(a) + (sy(b) - sy(a)) * o;
        return <g key={n} opacity={Math.min(1, o * 3)}>
          <line x1={xa} x2={xe} y1={sy(a)} y2={ye} stroke={c} strokeWidth={on ? 8 : 5} />
          <circle cx={xa} cy={sy(a)} r={12} fill={c} /><circle cx={xe} cy={ye} r={14} fill={c} />
          <text x={xa - 30} y={sy(a) + 12} textAnchor="end" fontFamily="PD" fontWeight={700} fontSize={36} fill={c}>{`${n} ${a}%`}</text>
          <text x={xb + 30} y={ly[i] + 12} fontFamily="PD" fontWeight={700} fontSize={on ? 48 : 38} fill={c} opacity={o}>{`${b}%`}</text>
        </g>; })}
    </svg>
  );
};

// 면적 원 2개 — 지름이 아니라 넓이로 크기 비교(6배면 넓이 6배)
export const AreaCircles: React.FC<{cx: number; cy: number; a: number; b: number; R: number; p: number; la: string; lb: string; gap?: number}> = ({cx, cy, a, b, R, p, la, lb, gap = 80}) => {
  const rb = R, ra = R * Math.sqrt(a / b); const xa = cx - rb - gap / 2 - ra, xb = cx + gap / 2;
  return (
    <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
      <circle cx={xa} cy={cy + rb - ra} r={ra} fill={T.line} stroke={T.ink3} strokeWidth={3} />
      <text x={xa} y={cy + rb - ra + 14} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={34} fill={T.ink}>{a}</text>
      <text x={xa} y={cy + rb + 50} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={28} fill={T.ink2}>{la}</text>
      <circle cx={xb + rb} cy={cy} r={rb * p} fill={T.ink} />
      <text x={xb + rb} y={cy + 30} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={96} fill="#fff" opacity={p}>{b}</text>
      <text x={xb + rb} y={cy + rb + 50} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={28} fill={T.ink} opacity={p}>{lb}</text>
    </svg>
  );
};

// 채움 막대: 계획(테두리) 안에 실적(채움) + 남은 칸(점선). ghost = 비교값(1년 전) 얇은 막대
export const FillBar: React.FC<{x: number; y: number; w: number; h: number; plan: number; done: number; p: number; planP: number; restP: number; ghost?: number; ghostP?: number;
  labels: {done: string; plan: string; rest: string; ghost?: string}}> = ({x, y, w, h, plan, done, p, planP, restP, ghost = 0, ghostP = 0, labels}) => {
  const sx = scaleLinear().domain([0, plan]).range([0, w]);
  return (
    <div style={{position: 'absolute', left: 0, top: 0}}>
      <div style={{position: 'absolute', left: x, top: y, width: w, height: h, borderRadius: 14, border: `4px solid ${T.ink}`, opacity: planP, boxSizing: 'border-box'}} />
      <div style={{...F, position: 'absolute', left: x + w - 460, top: y - 60, width: 460, textAlign: 'right', fontWeight: 700, fontSize: 34, color: T.ink, opacity: planP}}>{labels.plan}</div>
      <div style={{position: 'absolute', left: x, top: y, width: sx(done) * p, height: h, borderRadius: 14, background: T.accent}} />
      <div style={{...F, position: 'absolute', left: x, top: y + h + 16, fontWeight: 700, fontSize: 36, color: T.accent, opacity: p, whiteSpace: 'nowrap'}}>{labels.done}</div>
      <div style={{position: 'absolute', left: x + sx(done) + 8, top: y + 10, width: (w - sx(done) - 16) * restP, height: h - 20, borderRadius: 10,
        background: `repeating-linear-gradient(90deg, ${T.line} 0 18px, transparent 18px 30px)`}} />
      <div style={{...F, position: 'absolute', left: x + sx(done) + 40, top: y + h / 2 - 24, fontWeight: 700, fontSize: 40, color: T.ink2, opacity: restP, whiteSpace: 'nowrap'}}>{labels.rest}</div>
      {ghost ? <>
        <div style={{position: 'absolute', left: x, top: y + h + 90, width: sx(ghost) * ghostP, height: 40, borderRadius: 10, background: T.line, border: `2px solid ${T.ink3}`, boxSizing: 'border-box'}} />
        <div style={{...F, position: 'absolute', left: x + sx(ghost) + 20, top: y + h + 92, fontWeight: 700, fontSize: 30, color: T.ink2, opacity: ghostP, whiteSpace: 'nowrap'}}>{labels.ghost}</div>
      </> : null}
    </div>
  );
};
