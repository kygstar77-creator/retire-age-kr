// 환율 편 부품 — X-1 v3(2026-10-17 PD)에서 처음. TallyFrame 자식(흰 보드 x 100~1820 · y 236~852, [자막] 띠 y 252~310 아래에 그린다).
// TwoLines(같은 기간 두 선: 달러로 본 수익 vs 원화로 본 수익, 끝 값 칩) · DcaCal12(12칸 달력 — 칸마다 그날 환율 막대, 평균 줄·지금 줄)
// · CardSlips(우리가 그린 카드 결제/취소 전표 두 장 — 실제 카드사 양식 아님) · EqSteps(곱셈 식 칩 + 줄마다 보기 한 줄).
// 글자는 전부 HTML(SVG <text>는 mp4에서 어긋남 — 10/13 교훈), 숫자 글자는 props(x1props numcheck가 calc·대본과 대조)만.
import React from 'react';
import {interpolate, useCurrentFrame, Easing, spring, useVideoConfig} from 'remotion';
import {T, F, CL} from './fm';

const out = Easing.out(Easing.cubic);
const g = (f: number, a: number, d = 14) => interpolate(f, [a, a + d], [0, 1], {...CL, easing: out});

// ───────── 두 선(달러 vs 원화) ─────────
export type TwoLinesProps = {up: number[]; dn: number[]; min: number; max: number; ticks: [number, string][]; xl: [number, string][];
  nameUp: string; nameDn: string; tagUp: string; tagDn: string; beats: number[]; gapAt?: number; gapText?: string};
export const TwoLines: React.FC<TwoLinesProps> = (p) => {
  const f = useCurrentFrame();
  const X0 = 300, X1 = 1500, YT = 360, YB = 780;
  const n = p.up.length;
  const X = (i: number) => X0 + i / (n - 1) * (X1 - X0);
  const Y = (v: number) => YB - (v - p.min) / (p.max - p.min) * (YB - YT);
  const at = (i: number) => p.beats[i] ?? 1e9;
  const dUp = interpolate(f, [6, at(1) - 10], [0, 1], {...CL, easing: Easing.inOut(Easing.cubic)});
  const dDn = interpolate(f, [at(2), at(2) + 70], [0, 1], {...CL, easing: Easing.inOut(Easing.cubic)});
  const path = (vs: number[], d: number) => { const m = Math.max(1, Math.round(d * (n - 1))); return vs.slice(0, m + 1).map((v, i) => `${i ? 'L' : 'M'}${X(i).toFixed(1)},${Y(v).toFixed(1)}`).join(' '); };
  const end = (vs: number[], d: number) => { const m = Math.max(0, Math.round(d * (n - 1))); return [X(m), Y(vs[m])]; };
  const [ux, uy] = end(p.up, dUp); const [dx, dy] = end(p.dn, dDn);
  const gap = p.gapAt != null ? g(f, at(p.gapAt), 18) : 0;
  return (
    <>
      <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
        {p.ticks.map(([v], i) => <line key={i} x1={X0} x2={X1} y1={Y(v)} y2={Y(v)} stroke={v === 0 ? T.ink2 : T.line} strokeWidth={v === 0 ? 3 : 2} strokeDasharray={v === 0 ? '10 8' : undefined} />)}
        {gap > 0 && <rect x={X1 + 8} y={uy} width={18} height={(dy - uy) * gap} rx={5} fill={T.rise} opacity={0.85} />}
        <path d={path(p.up, dUp)} fill="none" stroke={T.ink} strokeWidth={6} strokeLinejoin="round" strokeLinecap="round" />
        {dDn > 0 && <path d={path(p.dn, dDn)} fill="none" stroke={T.fall} strokeWidth={6} strokeLinejoin="round" strokeLinecap="round" />}
        <circle cx={ux} cy={uy} r={11} fill={T.ink} stroke="#fff" strokeWidth={4} />
        {dDn > 0 && <circle cx={dx} cy={dy} r={11} fill={T.fall} stroke="#fff" strokeWidth={4} />}
      </svg>
      {p.ticks.map(([v, s], i) => <div key={i} style={{...F, position: 'absolute', left: X0 - 140, width: 124, textAlign: 'right', top: Y(v) - 16, fontSize: 26, fontWeight: 500, color: T.ink3}}>{s}</div>)}
      {p.xl.map(([i, s], k) => <div key={k} style={{...F, position: 'absolute', left: X(i) - 60, width: 120, textAlign: 'center', top: YB + 16, fontSize: 26, fontWeight: 500, color: T.ink3}}>{s}</div>)}
      <div style={{position: 'absolute', left: Math.min(ux, X1) + 28, top: uy - 74, opacity: g(f, at(1) - 12), ...F, whiteSpace: 'nowrap'}}>
        <div style={{fontSize: 28, fontWeight: 700, color: T.ink2}}>{p.nameUp}</div>
        <div style={{fontSize: 64, fontWeight: 800, color: T.ink, lineHeight: 1.05}}>{p.tagUp}</div></div>
      <div style={{position: 'absolute', left: Math.min(dx, X1) + 28, top: dy - 20, opacity: g(f, at(2) + 70), ...F, whiteSpace: 'nowrap'}}>
        <div style={{fontSize: 28, fontWeight: 700, color: T.fall}}>{p.nameDn}</div>
        <div style={{fontSize: 64, fontWeight: 800, color: T.fall, lineHeight: 1.05}}>{p.tagDn}</div></div>
      {gap > 0 && p.gapText ? <div style={{position: 'absolute', left: X0 + 40, top: 640, opacity: gap, background: T.ink, borderRadius: 12, padding: '10px 22px', ...F, fontSize: 34, fontWeight: 700, color: T.dink, whiteSpace: 'nowrap'}}>{p.gapText}</div> : null}
    </>
  );
};

// ───────── 12칸 달력(나눠 바꾸기) ─────────
// cells: [달 이름, 환율 글자, 환율 값] 12개 · 칸 안 막대 높이 = 환율(min~max) · 평균 줄·지금 줄은 칸을 가로질러 하나로
export type DcaCal12Props = {cells: [string, string, number][]; min: number; max: number; avg: number; avgText: string; now: number; nowText: string;
  each: string; res: string; beats: number[]; cellsAt: number; avgAt: number; nowAt: number; resAt: number};
export const DcaCal12: React.FC<DcaCal12Props> = (p) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const at = (i: number) => p.beats[i] ?? 1e9;
  const n = p.cells.length; const X0 = 150, CW = 122, GAP = 10, Y0 = 340, CH = 400;
  const BT = Y0 + 112, BB = Y0 + CH - 14;
  const Y = (v: number) => BB - (v - p.min) / (p.max - p.min) * (BB - BT);
  const c0 = at(p.cellsAt); const step = Math.max(6, Math.min(16, ((p.beats[p.cellsAt + 1] ?? c0 + 200) - c0 - 30) / n));
  const ya = Y(p.avg), yn = Y(p.now); const xr = X0 + n * CW + (n - 1) * GAP;
  const ao = g(f, at(p.avgAt), 18), no = g(f, at(p.nowAt), 18), ro = spring({frame: f - at(p.resAt) - 4, fps, config: {damping: 14}});
  return (
    <>
      {p.cells.map(([m, rt, v], i) => {
        const a = c0 + 4 + i * step; const o = g(f, a, 10); const h = (BB - Y(v)) * g(f, a + 4, 16); const x = X0 + i * (CW + GAP);
        const hi = ao > 0.5 && v > p.avg;
        return <div key={i} style={{position: 'absolute', left: x, top: Y0, width: CW, height: CH, borderRadius: 16, background: hi ? T.soft : T.bg, border: `2px solid ${T.line}`, opacity: o, transform: `translateY(${(1 - o) * 16}px)`}}>
          <div style={{...F, position: 'absolute', left: 0, width: CW, top: 10, textAlign: 'center', fontSize: 32, fontWeight: 700, color: T.ink}}>{m}</div>
          <div style={{...F, position: 'absolute', left: 0, width: CW, top: 54, textAlign: 'center', fontSize: 23, fontWeight: 700, color: T.ink2, whiteSpace: 'nowrap'}}>{rt}</div>
          <div style={{position: 'absolute', left: CW / 2 - 26, width: 52, top: Y(v) - Y0 + (BB - Y(v) - h), height: h, background: T.ink2, borderRadius: 6}} />
        </div>;
      })}
      <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
        {ao > 0 && <line x1={X0 - 10} x2={X0 - 10 + (xr - X0 + 20) * ao} y1={ya} y2={ya} stroke={T.accent} strokeWidth={6} strokeDasharray="18 10" />}
        {no > 0 && <line x1={xr + 10 - (xr - X0 + 20) * no} x2={xr + 10} y1={yn} y2={yn} stroke={T.fall} strokeWidth={6} strokeDasharray="18 10" />}
      </svg>
      {ao > 0 && <div style={{position: 'absolute', left: X0 + 6, top: ya - 62, opacity: ao, background: T.accent, borderRadius: 10, padding: '4px 16px', ...F, fontSize: 32, fontWeight: 700, color: '#fff', whiteSpace: 'nowrap'}}>{p.avgText}</div>}
      {no > 0 && <div style={{position: 'absolute', right: 1920 - xr - 6, top: yn + 12, opacity: no, background: T.fall, borderRadius: 10, padding: '4px 16px', ...F, fontSize: 32, fontWeight: 700, color: '#fff', whiteSpace: 'nowrap'}}>{p.nowText}</div>}
      <div style={{position: 'absolute', left: X0, top: Y0 + CH + 14, opacity: g(f, c0 + 10), ...F, fontSize: 28, fontWeight: 700, color: T.ink2, whiteSpace: 'nowrap'}}>{p.each}</div>
      {ro > 0.01 && <div style={{position: 'absolute', right: 1920 - xr, top: Y0 + CH + 6, opacity: Math.min(1, ro), transform: `scale(${0.9 + 0.1 * Math.min(1, ro)})`, transformOrigin: 'right center',
        background: T.ink, borderRadius: 12, padding: '6px 22px', ...F, fontSize: 36, fontWeight: 800, color: T.dink, whiteSpace: 'nowrap'}}>{p.res}</div>}
    </>
  );
};

// ───────── 카드 결제·취소 전표 두 장(우리가 그린 것) ─────────
export type SlipSide = {head: string; label: string; amt: string; sub: string};
export type CardSlipsProps = {a: SlipSide; b: SlipSide; mid: string; foot: string; beats: number[]; amtAt: number; midAt: number; footAt: number};
const Slip: React.FC<{s: SlipSide; x: number; o: number; amtO: number; red?: boolean; tilt: number}> = ({s, x, o, amtO, red, tilt}) => {
  const W = 520, H = 420; const teeth = 20;
  return (
    <div style={{position: 'absolute', left: x, top: 330 - (1 - o) * 60, width: W, opacity: o, transform: `rotate(${tilt}deg)`}}>
      <div style={{position: 'relative', width: W, height: H, background: '#fbfaf6', boxShadow: '0 16px 40px rgba(0,0,0,0.13)', borderRadius: '10px 10px 0 0'}}>
        <div style={{...F, position: 'absolute', left: 34, top: 26, fontSize: 34, fontWeight: 800, color: red ? T.rise : T.ink}}>{s.head}</div>
        <div style={{position: 'absolute', left: 34, right: 34, top: 88, borderTop: `3px dashed ${T.line}`}} />
        <div style={{...F, position: 'absolute', left: 34, top: 112, fontSize: 30, fontWeight: 500, color: T.ink2}}>{s.label}</div>
        <div style={{...F, position: 'absolute', left: 0, width: W, top: 170, textAlign: 'center', fontSize: 120, fontWeight: 800, letterSpacing: -4, color: red ? T.rise : T.ink, opacity: amtO, transform: `scale(${0.9 + 0.1 * amtO})`}}>{s.amt}</div>
        <div style={{position: 'absolute', left: 34, right: 34, top: 330, borderTop: `3px dashed ${T.line}`}} />
        <div style={{...F, position: 'absolute', left: 34, top: 348, fontSize: 28, fontWeight: 500, color: T.ink3, whiteSpace: 'nowrap'}}>{s.sub}</div>
      </div>
      <svg width={W} height={18} style={{display: 'block'}}><path d={Array.from({length: teeth}, (_, i) => `${i ? 'L' : 'M'}${i * W / teeth},0 L${(i + 0.5) * W / teeth},16`).join(' ') + ` L${W},0 Z`} fill="#fbfaf6" /></svg>
    </div>
  );
};
export const CardSlips: React.FC<CardSlipsProps> = (p) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const at = (i: number) => p.beats[i] ?? 1e9;
  const o1 = g(f, 6, 16), o2 = g(f, 22, 16), a1 = g(f, at(p.amtAt) + 4, 14), a2 = g(f, at(p.amtAt) + 40, 14);
  const m = spring({frame: f - at(p.midAt) - 4, fps, config: {damping: 13}});
  return (
    <>
      <Slip s={p.a} x={250} o={o1} amtO={a1} tilt={-2} />
      <Slip s={p.b} x={1150} o={o2} amtO={a2} red tilt={2} />
      <div style={{position: 'absolute', left: 820, width: 280, top: 470, textAlign: 'center', opacity: g(f, 30), ...F, fontSize: 90, fontWeight: 800, color: T.ink3}}>→</div>
      {m > 0.01 && <div style={{position: 'absolute', left: 760, width: 400, top: 590, display: 'flex', justifyContent: 'center', opacity: Math.min(1, m), transform: `scale(${0.85 + 0.15 * Math.min(1, m)})`}}>
        <div style={{background: T.fall, borderRadius: 14, padding: '8px 26px', ...F, fontSize: 44, fontWeight: 800, color: '#fff', whiteSpace: 'nowrap'}}>{p.mid}</div></div>}
      <div style={{position: 'absolute', left: 100, width: 1720, top: 790, textAlign: 'center', opacity: g(f, at(p.footAt) + 6), ...F, fontSize: 34, fontWeight: 700, color: T.ink2, whiteSpace: 'nowrap'}}>{p.foot}</div>
    </>
  );
};

// ───────── 곱셈 식 칩 + 보기 줄 ─────────
// formula: [a, op, b, '=', c] 상자 · steps: [왼쪽 글, 결과 글, 색(rise|fall|accent|ink), 나오는 줄]
export type EqStepsProps = {formula: string[]; steps: [string, string, string, number][]; beats: number[]};
export const EqSteps: React.FC<EqStepsProps> = (p) => {
  const f = useCurrentFrame();
  const at = (i: number) => p.beats[i] ?? 1e9;
  const COL: Record<string, string> = {rise: T.rise, fall: T.fall, accent: T.accent, ink: T.ink};
  const cur = (() => { let k = -1; p.steps.forEach((s, i) => { if (f >= at(s[3])) k = i; }); return k; })();
  return (
    <>
      <div style={{position: 'absolute', left: 100, width: 1720, top: 330, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 22}}>
        {p.formula.map((t, i) => { const op = t === '×' || t === '='; const o = g(f, 6 + i * 8);
          return op ? <div key={i} style={{...F, fontSize: 96, fontWeight: 800, color: T.ink3, opacity: o}}>{t}</div>
            : <div key={i} style={{...F, fontSize: 84, fontWeight: 800, color: i === p.formula.length - 1 ? '#fff' : T.ink, background: i === p.formula.length - 1 ? T.accent : T.bg,
              border: `3px solid ${i === p.formula.length - 1 ? T.accent : T.line}`, borderRadius: 22, padding: '6px 34px', opacity: o, transform: `translateY(${(1 - o) * 14}px)`, whiteSpace: 'nowrap'}}>{t}</div>; })}
      </div>
      <div style={{position: 'absolute', left: 260, width: 1400, top: 500}}>
        {p.steps.map(([a, b, c, ln], i) => { const o = g(f, at(ln) + 4, 12); const hot = i === cur;
          return <div key={i} style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', height: 92, padding: '0 34px', marginBottom: 8, borderRadius: 16,
            background: hot ? T.soft : '#fff', border: `2px solid ${hot ? T.soft : T.line}`, opacity: o, transform: `translateX(${(1 - o) * -24}px)`}}>
            <span style={{...F, fontSize: 46, fontWeight: 700, color: T.ink, whiteSpace: 'nowrap'}}>{a}</span>
            <span style={{...F, fontSize: 56, fontWeight: 800, color: COL[c] ?? T.ink, whiteSpace: 'nowrap', marginLeft: 30}}>{b}</span></div>; })}
      </div>
    </>
  );
};
