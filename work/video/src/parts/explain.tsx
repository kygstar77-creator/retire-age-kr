// 설명형 그림 부품(RULES 6-3 — D-1에서 처음 씀, research/longform/loop/parts.md에 기록). 숫자·글은 전부 props로 받는다, 색은 fm.tsx 토큰만.
// 조건 꼬리표 · 흐름도(상자+꺾은 화살표) · 칸 채우는 계산식 · 절벽 막대(하한선+점프 괄호) · 달력 줄(월 칸+구간) · 기간 띠 · 단계 카드 · 체크리스트
import React from 'react';
import {T, F, appear} from './fm';

// 조건 꼬리표 — 장면 왼쪽 위(제목 위) 작은 칩. 예: '예시 조건: 지역가입자 1인 · 재산 0 · 2026년 기준'
export const CondTag: React.FC<{text: string; dark?: boolean; o?: number}> = ({text, dark, o = 1}) => (
  <div style={{...F, position: 'absolute', left: 120, top: 18, fontWeight: 700, fontSize: 22, color: dark ? T.dink : T.ink2, opacity: o,
    background: dark ? T.dsurface : T.line, borderRadius: 10, padding: '5px 14px', whiteSpace: 'nowrap'}}>{text}</div>
);

// 흐름도: 상자(nodes)와 꺾은 화살표(edges, 점 목록). o는 0~1 등장값
export type FlowNode = {x: number; y: number; w: number; h: number; title: string; sub?: string; o: number; tone?: 'ink' | 'surface' | 'soft' | 'line'; big?: boolean};
export type FlowEdge = {pts: [number, number][]; o: number; dashed?: boolean; label?: string; lx?: number; ly?: number};
export const Flow: React.FC<{nodes: FlowNode[]; edges: FlowEdge[]}> = ({nodes, edges}) => (
  <>
    <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
      {edges.map((e, i) => {
        const [a, b] = e.pts.slice(-2); const ang = Math.atan2(b[1] - a[1], b[0] - a[0]);
        const head = [[b[0], b[1]], [b[0] - 22 * Math.cos(ang - 0.45), b[1] - 22 * Math.sin(ang - 0.45)], [b[0] - 22 * Math.cos(ang + 0.45), b[1] - 22 * Math.sin(ang + 0.45)]];
        return <g key={i} opacity={Math.min(1, e.o * 4)}>
          {e.dashed
            ? <polyline points={e.pts.map((p) => p.join(',')).join(' ')} fill="none" stroke={T.ink2} strokeWidth={5} strokeDasharray="14 10" opacity={e.o} />
            : <polyline points={e.pts.map((p) => p.join(',')).join(' ')} fill="none" stroke={T.ink2} strokeWidth={5} strokeLinejoin="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - e.o} />}
          <polygon points={head.map((p) => p.join(',')).join(' ')} fill={T.ink2} opacity={e.o > 0.9 ? 1 : 0} />
          {e.label ? <text x={e.lx} y={e.ly} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={26} fill={T.ink2} opacity={e.o}>{e.label}</text> : null}
        </g>;
      })}
    </svg>
    {nodes.map((n, i) => {
      const bg = n.tone === 'ink' ? T.ink : n.tone === 'soft' ? T.soft : n.tone === 'line' ? T.line : T.surface;
      const fg = n.tone === 'ink' ? '#fff' : T.ink;
      return <div key={i} style={{position: 'absolute', left: n.x, top: n.y + (1 - n.o) * 18, width: n.w, height: n.h, opacity: n.o, background: bg, borderRadius: 20,
        display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', textAlign: 'center', border: n.tone === 'surface' || !n.tone ? `3px solid ${T.line}` : 'none'}}>
        <div style={{...F, fontWeight: 700, fontSize: n.big ? 46 : 36, color: fg, lineHeight: 1.2, wordBreak: 'keep-all'}}>{n.title}</div>
        {n.sub ? <div style={{...F, fontWeight: 500, fontSize: 26, color: n.tone === 'ink' ? T.line : T.ink2, marginTop: 8, wordBreak: 'keep-all', lineHeight: 1.3}}>{n.sub}</div> : null}
      </div>;
    })}
  </>
);

// 칸 채우는 계산식: 항(term)은 비어 있을 땐 점선 빈칸, 채워지면 글이 떠오른다. 연산자(op)는 그냥 나타난다
export type Tok = {t: string; o: number; op?: boolean; tone?: 'ink' | 'num' | 'soft'; w?: number; sub?: string; subO?: number};
export const Tokens: React.FC<{x: number; y: number; toks: Tok[]; size?: number; gap?: number}> = ({x, y, toks, size = 54, gap = 14}) => (
  <div style={{position: 'absolute', left: x, top: y, display: 'flex', alignItems: 'center', gap}}>
    {toks.map((k, i) => k.op
      ? <span key={i} style={{...F, fontWeight: 700, fontSize: size, color: T.ink3, opacity: Math.max(0.0, k.o)}}>{k.t}</span>
      : <div key={i} style={{position: 'relative', minWidth: k.w ?? 0, height: size * 1.7, borderRadius: 16, padding: '0 24px', display: 'flex', alignItems: 'center', justifyContent: 'center',
          border: `3px dashed ${k.o > 0.05 ? 'transparent' : T.ink3}`, background: k.o > 0.05 ? (k.tone === 'ink' ? T.ink : k.tone === 'soft' ? T.soft : T.surface) : 'transparent'}}>
          <span style={{...F, fontWeight: 700, fontSize: size, whiteSpace: 'nowrap', color: k.tone === 'ink' ? '#fff' : T.ink, opacity: k.o, transform: `translateY(${(1 - k.o) * 14}px)`, display: 'inline-block'}}>{k.t}</span>
          {k.sub ? <span style={{...F, position: 'absolute', left: 0, right: 0, top: size * 1.7 + 12, textAlign: 'center', fontWeight: 700, fontSize: 26, color: T.ink2, whiteSpace: 'nowrap', opacity: k.subO ?? k.o}}>{k.sub}</span> : null}
        </div>)}
  </div>
);

// 절벽 막대: 범주 막대 + 하한 점선 + 두 막대 사이 점프 괄호(꼬리표)
export const CliffBars: React.FC<{x: number; y: number; w: number; h: number; rows: [string, number][]; p: number[]; jumpAt: number; jumpP: number; jumpLabel: string;
  floor?: number; floorP?: number; floorLabel?: string; fmt: (v: number) => string; xTitle?: string}> =
  ({x, y, w, h, rows, p, jumpAt, jumpP, jumpLabel, floor, floorP = 0, floorLabel = '', fmt, xTitle}) => {
  const mx = Math.max(...rows.map((r) => r[1])) * 1.08; const slot = w / rows.length; const bw = slot * 0.6; const sy = (v: number) => (v / mx) * h;
  const a = rows[jumpAt], b = rows[jumpAt + 1]; const jx = x + (jumpAt + 1) * slot - (slot - bw) / 2 - 4;
  return (
    <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
      <line x1={x - 10} x2={x + w} y1={y} y2={y} stroke={T.ink3} strokeWidth={2} />
      {floor ? <g opacity={floorP}><line x1={x - 10} x2={x - 10 + (w + 10) * floorP} y1={y - sy(floor)} y2={y - sy(floor)} stroke={T.fall} strokeWidth={3} strokeDasharray="10 8" />
        {floorLabel.split(' + ').map((t, i) => <text key={i} x={x + 20} y={y - sy(floor) - 140 + i * 34} fontFamily="PD" fontWeight={700} fontSize={26} fill={T.fall}>{i ? '+ ' + t : t}</text>)}</g> : null}
      {rows.map(([n, v], i) => { const o = p[i] ?? 0; const bh = sy(v) * appear(o * 30, 0, 30); const after = i > jumpAt;
        return <g key={n} opacity={Math.min(1, o * 3)}>
          <rect x={x + i * slot} y={y - bh} width={bw} height={bh} rx={8} fill={after ? (i === jumpAt + 1 ? T.rise : T.ink) : T.ink3} />
          <text x={x + i * slot + bw / 2} y={y - bh - 16} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={i === jumpAt + 1 ? 38 : 32} fill={i === jumpAt + 1 ? T.rise : T.ink}>{fmt(v)}</text>
        </g>; })}
      {rows.map(([n], i) => <text key={'l' + n} x={x + i * slot + bw / 2} y={y + 40} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={30} fill={(p[i] ?? 0) > 0.5 ? T.ink : T.ink3}>{n}</text>)}
      {xTitle ? <text x={x + w} y={y + 84} textAnchor="end" fontFamily="PD" fontWeight={500} fontSize={24} fill={T.ink3}>{xTitle}</text> : null}
      <g opacity={jumpP}>
        <line x1={x + jumpAt * slot + bw} x2={jx + 30} y1={y - sy(a[1])} y2={y - sy(a[1])} stroke={T.rise} strokeWidth={3} strokeDasharray="6 6" />
        <line x1={jx + 30} x2={jx + 30} y1={y - sy(a[1])} y2={y - sy(a[1]) - (sy(b[1]) - sy(a[1])) * jumpP} stroke={T.rise} strokeWidth={5} />
        <polygon points={`${jx + 30},${y - sy(b[1]) - 4} ${jx + 18},${y - sy(b[1]) + 18} ${jx + 42},${y - sy(b[1]) + 18}`} fill={T.rise} opacity={jumpP > 0.9 ? 1 : 0} />
        <rect x={jx - 170} y={y - sy(b[1]) - 150} width={400} height={64} rx={32} fill={T.rise} />
        <text x={jx + 30} y={y - sy(b[1]) - 106} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={34} fill="#fff">{jumpLabel}</text>
      </g>
    </svg>
  );
};

// 달력 줄: 해마다 12칸, spans로 칸 칠하기(라벨은 칸 위), marks로 칸 아래 작은 글
export type MonthSpan = {row: number; from: number; to: number; tone: 'ink' | 'fall' | 'soft' | 'line'; o: number; label?: string; right?: boolean; below?: boolean};
export const MonthRows: React.FC<{x: number; y: number; cell: number; rowGap: number; years: string[]; spans: MonthSpan[]; o?: number}> = ({x, y, cell, rowGap, years, spans, o = 1}) => {
  const ch = 64;
  const col = (t: MonthSpan['tone']) => (t === 'ink' ? T.ink : t === 'fall' ? T.fall : t === 'soft' ? T.soft : T.line);
  return (
    <div style={{position: 'absolute', left: 0, top: 0, opacity: o}}>
      {years.map((yr, r) => <div key={yr}>
        <div style={{...F, position: 'absolute', left: x - 230, width: 210, textAlign: 'right', top: y + r * rowGap + 14, fontWeight: 700, fontSize: 30, color: T.ink, whiteSpace: 'nowrap'}}>{yr}</div>
        {Array.from({length: 12}).map((_, m) => <div key={m} style={{position: 'absolute', left: x + m * cell, top: y + r * rowGap, width: cell - 6, height: ch, borderRadius: 8,
          background: T.surface, border: `2px solid ${T.line}`}} />)}
      </div>)}
      {spans.map((s, i) => { const L = x + s.from * cell, W = (s.to - s.from + 1) * cell - 6;
        return <div key={i} style={{position: 'absolute', left: L, top: y + s.row * rowGap, width: W * s.o, height: ch, borderRadius: 8, background: col(s.tone), opacity: Math.min(1, s.o * 3), overflow: 'visible'}}>
          {s.label ? <div style={{...F, position: 'absolute', ...(s.right ? {right: 0} : {left: 0}), top: s.below ? ch + 10 : -44, fontWeight: 700, fontSize: 28, whiteSpace: 'nowrap', color: s.tone === 'fall' ? T.fall : T.ink, opacity: s.o}}>{s.label}</div> : null}
        </div>; })}
      {years.map((yr, r) => Array.from({length: 12}).map((_, m) => {
        const cov = spans.find((s) => s.row === r && m >= s.from && m <= s.to && s.o > 0.5 && (s.tone === 'ink' || s.tone === 'fall'));
        return <div key={yr + r + m} style={{...F, position: 'absolute', left: x + m * cell, top: y + r * rowGap, width: cell - 6, height: ch, display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontWeight: cov ? 700 : 500, fontSize: 22, color: cov ? '#fff' : T.ink3}}>{m + 1}월</div>; }))}
    </div>
  );
};

// 기간 띠: 시작점부터 n칸(개월)이 자라고, 눈금 12개월마다
export const PeriodBand: React.FC<{x0: number; x1: number; y: number; n: number; p: number; start: string; end: string; tick?: number}> = ({x0, x1, y, n, p, start, end, tick = 12}) => {
  const sx = (m: number) => x0 + (x1 - x0) * (m / n); const ticks = Array.from({length: Math.floor(n / tick) + 1}).map((_, i) => i * tick);
  return (
    <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
      <rect x={x0} y={y - 40} width={x1 - x0} height={80} rx={14} fill={T.line} />
      <rect x={x0} y={y - 40} width={(x1 - x0) * p} height={80} rx={14} fill={T.ink} />
      {ticks.map((t) => <g key={t} opacity={p >= t / n - 0.001 ? 1 : 0.35}>
        <line x1={sx(t)} x2={sx(t)} y1={y + 46} y2={y + 70} stroke={T.ink3} strokeWidth={3} />
        <text x={sx(t)} y={y + 108} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={30} fill={T.ink2}>{t ? `${t}개월` : '0'}</text></g>)}
      <text x={x0} y={y - 70} fontFamily="PD" fontWeight={700} fontSize={34} fill={T.ink}>{start}</text>
      <text x={x1} y={y - 70} textAnchor="end" fontFamily="PD" fontWeight={700} fontSize={34} fill={T.ink} opacity={p > 0.95 ? 1 : 0.3}>{end}</text>
    </svg>
  );
};

// 단계 카드: 가로로 번호 카드 + 사이 화살표
export const StepCards: React.FC<{x: number; y: number; w: number; h: number; gap: number; steps: [string, string][]; o: number[]}> = ({x, y, w, h, gap, steps, o}) => (
  <>
    {steps.map(([t, sub], i) => { const v = o[i] ?? 0;
      return <div key={i} style={{position: 'absolute', left: x + i * (w + gap), top: y + (1 - v) * 24, width: w, height: h, opacity: v, background: T.surface, borderRadius: 22, border: `3px solid ${i === steps.length - 1 && v > 0.9 ? T.ink : T.line}`}}>
        <div style={{position: 'absolute', left: 36, top: 36, width: 76, height: 76, borderRadius: 38, background: T.ink, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
          <span style={{...F, fontWeight: 700, fontSize: 42, color: '#fff'}}>{i + 1}</span></div>
        <div style={{...F, position: 'absolute', left: 36, right: 30, top: 150, fontWeight: 700, fontSize: 44, color: T.ink, lineHeight: 1.25, wordBreak: 'keep-all'}}>{t}</div>
        <div style={{...F, position: 'absolute', left: 36, right: 30, top: 270, fontWeight: 500, fontSize: 30, color: T.ink2, lineHeight: 1.35, wordBreak: 'keep-all'}}>{sub}</div>
        {i < steps.length - 1 ? <div style={{...F, position: 'absolute', right: -gap / 2 - 18, top: h / 2 - 30, fontWeight: 700, fontSize: 48, color: T.ink3, opacity: o[i + 1] ?? 0}}>→</div> : null}
      </div>; })}
  </>
);

// 체크리스트: 줄마다 빈 네모 → 체크, 이름표·본문·보조 설명
export const CheckList: React.FC<{x: number; y: number; w: number; rowH: number; items: [string, string, string][]; o: number[]; sub: number[]; check: number[]}> = ({x, y, w, rowH, items, o, sub, check}) => (
  <>
    {items.map(([k, main, note], i) => <div key={i} style={{position: 'absolute', left: x, top: y + i * (rowH + 30) + (1 - (o[i] ?? 0)) * 20, width: w, height: rowH, background: T.surface, borderRadius: 22, opacity: o[i] ?? 0}}>
      <div style={{position: 'absolute', left: 40, top: rowH / 2 - 42, width: 84, height: 84, borderRadius: 16, border: `5px solid ${T.ink}`, background: (check[i] ?? 0) > 0.5 ? T.ink : 'transparent',
        display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
        <svg width={60} height={60} viewBox="0 0 60 60"><polyline points="10,32 25,46 50,14" fill="none" stroke="#fff" strokeWidth={8} strokeLinecap="round" strokeLinejoin="round"
          pathLength={1} strokeDasharray={1} strokeDashoffset={1 - (check[i] ?? 0)} /></svg></div>
      <div style={{...F, position: 'absolute', left: 160, top: 34, fontWeight: 700, fontSize: 30, color: T.ink3}}>{k}</div>
      <div style={{...F, position: 'absolute', left: 160, top: 76, fontWeight: 700, fontSize: 52, color: T.ink, whiteSpace: 'nowrap'}}>{main}</div>
      <div style={{...F, position: 'absolute', left: 160, right: 40, top: 152, fontWeight: 500, fontSize: 30, color: T.ink2, opacity: sub[i] ?? 0, wordBreak: 'keep-all'}}>{note}</div>
    </div>)}
  </>
);
