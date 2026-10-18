// 대출 한도 계단(LoanSteps) — H-2 5장 '대출은 둘 중 작은 쪽까지'·'25억이라는 선'(2026-10-18 motion, 견본 방식). TallyFrame 자식.
// phase rule: 집값 축 위에 '집값의 40%' 경사(점선) → 금액 한도 덮개(점선) → 말 따라 실제 한도 선(둘 중 작은 쪽)이 한 칸씩 굵게 그려지고, 오른쪽 칸에 지금 칸 한도 하나만 주황.
// phase edge: 25억 언저리 확대. 점이 선을 넘는 순간 4억 → '?' → 2억(주황·손 동그라미) · '절반' 꺾쇠 → 끝 줄은 점이 선 위에서 흔들리며 '은행이 보는 이 집 값은?'
// 선은 규칙 그대로(min(40%×집값, 금액 한도)) — 새 숫자 글자 없음. 글자는 HTML.
import React from 'react';
import {interpolate, useCurrentFrame, Easing, random, spring, useVideoConfig, Img, staticFile} from 'remotion';
import {T, F, CL, HandCircle} from '../parts/fm';
import {BOARD} from './TallyFrame';

export type LoanStepsProps = {
  seed: string; phase: 'rule' | 'edge'; xMax: number; yMax: number; ltv: number; ltvText: string;
  caps: [number, number, string][]; xTicks: [number, string][]; xName: string; yName: string; minText: string;
  show: string[]; edgeLo?: string; edgeHi?: string; half?: string; ask?: string; beats: number[]; paper?: boolean;
};

const out = Easing.out(Easing.cubic);
const g = (f: number, a: number, d = 16) => interpolate(f, [a, a + d], [0, 1], {...CL, easing: out});
const io = Easing.inOut(Easing.quad);

export const LoanSteps: React.FC<LoanStepsProps> = (p) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const r = (k: string) => random(p.seed + k);
  const B = p.beats; const at = (i: number) => B[i] ?? 1e9; const len = (i: number) => (B[i + 1] ?? at(i) + 180) - at(i);
  const sp = (a: number) => spring({frame: f - a, fps, config: {damping: 15}});
  const edge = p.phase === 'edge';
  const [x0, x1] = edge ? [21, 29] : [0, p.xMax]; const [y0, y1] = edge ? [0, 6] : [0, p.yMax];
  const XL = 260 + Math.round(r('xl') * 30), XR = 1420, YB = 790, YT = 330;
  const X = (v: number) => XL + (v - x0) / (x1 - x0) * (XR - XL);
  const Y = (v: number) => YB - (v - y0) / (y1 - y0) * (YB - YT);
  const cap = (x: number) => { for (const [lim, c] of p.caps) if (x <= lim) return c; return p.caps[p.caps.length - 1][1]; };
  const lim = (x: number) => Math.min(p.ltv * x, cap(x));
  // 한도 선 꼭짓점(경계에서 수직으로 떨어짐)
  const pts: [number, number][] = [[x0, lim(x0)]];
  for (const [b] of p.caps) if (b > x0 && b < x1) { pts.push([b, lim(b)]); pts.push([b, lim(b + 1e-6)]); }
  if (!edge) pts.splice(1, 0, [p.caps[0][1] / p.ltv, p.caps[0][1]]);   // 40% 선이 금액 한도에 닿는 곳(15억 6억)
  pts.push([x1, lim(x1)]);
  pts.sort((a, b) => a[0] - b[0]);
  const seg = (a: number, b: number) => pts.filter(([x]) => x >= a - 1e-9 && x <= b + 1e-9);
  const path = (q: [number, number][]) => q.map(([x, y], i) => `${i ? 'L' : 'M'}${X(x).toFixed(1)} ${Y(y).toFixed(1)}`).join(' ');
  const area = (q: [number, number][]) => q.length ? `${path(q)} L${X(q[q.length - 1][0])} ${YB} L${X(q[0][0])} ${YB} Z` : '';
  const lab = (x: number, y: number, s: string, o: number, st: React.CSSProperties = {}) =>
    <div style={{position: 'absolute', left: x, top: y, transform: 'translate(-50%, -50%)', opacity: o, ...F, fontWeight: 700, fontSize: 32, color: T.ink2, whiteSpace: 'nowrap', ...st}}>{s}</div>;
  const ax = g(f, at(0), 18);
  const paper = p.paper !== false && <div style={{position: 'absolute', left: BOARD.x, top: BOARD.y, width: BOARD.w, height: BOARD.h, borderRadius: 24, overflow: 'hidden', mixBlendMode: 'multiply', opacity: 0.85, pointerEvents: 'none'}}>
    <Img src={staticFile('paper.png')} style={{width: 1920, height: 1080, marginLeft: -BOARD.x, marginTop: -BOARD.y}} /></div>;
  const PX = 1500;   // 오른쪽 칸 왼끝

  if (!edge) {
    // 줄 → 일(props show): ltv · min · cap0 · cap1 · cap2
    const k = (name: string) => p.show.indexOf(name);
    const lt = g(f, at(k('ltv')) + 6, 30); const mn = g(f, at(k('min')) + 4, 20);
    const bounds: [number, number][] = [[0, p.caps[0][0]], [p.caps[0][0], p.caps[1][0]], [p.caps[1][0], p.xMax]];
    const step = [0, 1, 2].map((i) => interpolate(f, [at(k('cap' + i)) + 6, at(k('cap' + i)) + 34], [0, 1], {...CL, easing: io}));
    let curI = -1; step.forEach((s, i) => { if (s > 0) curI = i; });
    const ltvEnd = Math.min(p.xMax, y1 / p.ltv);
    return <>
      {paper}
      <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
        <line x1={XL} x2={XL + (XR - XL) * ax} y1={YB} y2={YB} stroke={T.ink3} strokeWidth={3} />
        <line x1={XL} x2={XL} y1={YB} y2={YB - (YB - YT) * ax} stroke={T.ink3} strokeWidth={3} />
        {p.caps.map(([, c], i) => <line key={i} x1={XL} x2={XR} y1={Y(c)} y2={Y(c)} stroke={T.line} strokeWidth={2} opacity={ax} />)}
        {/* 0줄 면: 40%가 허락하는 곳 · 1줄 면: 금액 한도가 허락하는 곳(줄마다 판 4% 넘게 바뀌게, 10/17 교훈) */}
        <path d={`M${X(0)} ${YB} L${X(ltvEnd)} ${Y(y1)} L${X(p.xMax)} ${Y(y1)} L${X(p.xMax)} ${YB} Z`} fill={T.ink3} opacity={0.34 * lt * (1 - mn)} />
        <path d={area([[0, 0], [p.caps[0][0], p.caps[0][1]], [p.caps[0][0], p.caps[1][1]], [p.caps[1][0], p.caps[1][1]], [p.caps[1][0], p.caps[2][1]], [p.xMax, p.caps[2][1]]])} fill={T.fall} opacity={0.34 * mn * (1 - Math.max(0, ...step.map((v) => Math.min(1, v * 3))))} />
        {/* 40% 경사 */}
        <line x1={X(0)} y1={Y(0)} x2={X(lt * ltvEnd)} y2={Y(lt * ltvEnd * p.ltv)} stroke={T.ink3} strokeWidth={5} strokeDasharray="14 10" strokeLinecap="round" opacity={curI >= 0 ? 0.45 : 1} />
        {/* 금액 한도 덮개 */}
        {mn > 0.01 && bounds.map(([a, b], i) => <line key={i} x1={X(a)} x2={X(a) + (X(b) - X(a)) * mn} y1={Y(p.caps[i][1])} y2={Y(p.caps[i][1])} stroke={T.ink3} strokeWidth={5} strokeDasharray="6 10" strokeLinecap="round" opacity={curI >= 0 ? 0.45 : 1} />)}
        {/* 칸마다 실제 한도(둘 중 작은 쪽) — 면적 + 굵은 선 */}
        {bounds.map(([a, b], i) => { const s = step[i]; if (s <= 0) return null; const e = a + (b - a) * s;
          // 칸 i 선: 앞 칸 끝 높이에서 수직으로 떨어진 뒤 이 칸 한도를 따라감
          const full: [number, number][] = i === 0 ? [[0, 0], [b, lim(b)]] : [[a, lim(a)], [a, lim(a + 1e-6)], [b, lim(b - 1e-6)]];
          const qs: [number, number][] = full.filter(([x]) => x <= e + 1e-9).concat(s < 1 ? [[e, i === 0 ? p.ltv * e : lim(e)] as [number, number]] : []);
          return <g key={i}><path d={area(qs)} fill={i === curI ? T.ink : T.ink3} opacity={i === curI ? 0.32 : 0.12} /><path d={path(qs)} fill="none" stroke={T.ink} strokeWidth={9} strokeLinejoin="round" strokeLinecap="round" /></g>; })}
        {p.caps.slice(0, 2).map(([b], i) => <line key={i} x1={X(b)} x2={X(b)} y1={YB} y2={YT - 10} stroke={T.ink3} strokeWidth={2} strokeDasharray="4 8" opacity={g(f, at(k('cap' + i)), 12) * 0.8} />)}
      </svg>
      {p.xTicks.map(([v, s], i) => lab(X(v), YB + 34, s, ax))}
      {lab(XR + 6, YB + 34, p.xName, ax, {color: T.ink3, fontSize: 28, transform: 'translate(0, -50%)'})}
      {p.caps.map(([, c, s], i) => lab(XL - 54, Y(c), s, g(f, at(k('min')) + i * 4, 12), {fontSize: 30, color: T.ink3}))}
      {lab(XL + 6, YT - 30, p.yName, ax, {color: T.ink3, fontSize: 28, transform: 'translate(0, -50%)'})}
      {lab(X(ltvEnd * 0.62), Y(ltvEnd * 0.62 * p.ltv) - 46, p.ltvText, lt * (curI >= 0 ? 0.5 : 1), {transform: 'translate(-50%, -50%) rotate(-24deg)'})}
      {curI < 0 && f >= at(k('min')) && <div style={{position: 'absolute', left: PX, top: 380, width: 290, opacity: sp(at(k('min')) + 10), ...F, fontWeight: 800, fontSize: 54, color: T.ink, lineHeight: 1.2}}>{p.minText}</div>}
      {/* 오른쪽 칸: 지금 칸 한도 하나만 주황, 지난 칸은 회색 작은 줄 */}
      {[0, 1, 2].map((i) => { if (step[i] <= 0) return null; const now = i === curI; const o = sp(at(k('cap' + i)) + 4);
        const rng = i === 0 ? `${p.xTicks[0][1]}까지 · 최대` : i === 1 ? `${p.xTicks[0][1]}~${p.xTicks[1][1]}` : `${p.xTicks[1][1]} 넘음`;
        return <div key={i} style={{position: 'absolute', left: PX, top: 360, width: 300, opacity: now ? Math.min(1, o) : 0}}>
          <div style={{...F, fontWeight: 700, fontSize: 34, color: T.ink2}}>{rng}</div>
          <div style={{...F, fontWeight: 800, fontSize: 120, color: T.accent, letterSpacing: -4, lineHeight: 1.05, transform: `scale(${0.85 + 0.15 * Math.min(1, o)})`, transformOrigin: '0 50%'}}>{p.caps[i][2]}</div>
        </div>; })}
      {curI > 0 && <div style={{position: 'absolute', left: PX, top: 560, width: 300}}>
        {[0, 1, 2].filter((i) => i < curI).map((i) => <div key={i} style={{...F, fontWeight: 700, fontSize: 30, color: T.ink3, marginTop: 8, whiteSpace: 'nowrap'}}>{i === 0 ? `${p.xTicks[0][1]}까지 · 최대` : `${p.xTicks[0][1]}~${p.xTicks[1][1]} ·`} {p.caps[i][2]}</div>)}
      </div>}
    </>;
  }

  // ── edge ──
  const k = (name: string) => p.show.indexOf(name);
  const ln = interpolate(f, [at(k('line')) + 4, at(k('line')) + 40], [0, 1], {...CL, easing: io});
  const tj0 = at(k('jump')) + len(k('jump')) * 0.12, tj1 = at(k('jump')) + len(k('jump')) * 0.5;
  const mv = interpolate(f, [tj0, tj1], [0, 1], {...CL, easing: io});
  const wob = f >= at(k('ask')) ? Math.sin((f - at(k('ask'))) / 10) * 1.1 * g(f, at(k('ask')), 14) : 0;
  const B25 = p.caps[1][0];
  const dx = f >= at(k('ask')) ? B25 + wob : 23 + 4 * mv;
  const crossAt = interpolate(B25, [23, 27], [tj0, tj1]);   // 근사(대칭이라 가운데)
  const qGap = 14; const opened = f >= crossAt + qGap;
  const circ = interpolate(f, [crossAt + qGap + 10, crossAt + qGap + 34], [0, 1], {...CL, easing: io});
  const over = dx > B25; const dy = over ? p.caps[2][1] : p.caps[1][1];
  const q = pts.filter(([x]) => x <= x0 + (x1 - x0) * ln + 1e-9).concat(ln < 1 ? [[x0 + (x1 - x0) * ln, lim(x0 + (x1 - x0) * ln)] as [number, number]] : []).sort((u, v) => u[0] - v[0] || v[1] - u[1]);
  const showDot = f >= at(k('jump'));
  const hiS = p.edgeHi ?? ''; const loS = p.edgeLo ?? '';
  return <>
    {paper}
    <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible'}}>
      <line x1={XL} x2={XR} y1={YB} y2={YB} stroke={T.ink3} strokeWidth={3} opacity={ax} />
      {f >= at(k('ask')) && <rect x={X(B25 - 1.2)} y={YT - 20} width={X(B25 + 1.2) - X(B25 - 1.2)} height={YB - YT + 20} fill={T.ink} opacity={0.08 * g(f, at(k('ask')), 14)} />}
      <path d={area(q)} fill={T.ink} opacity={0.1} />
      <path d={path(q)} fill="none" stroke={T.ink} strokeWidth={9} strokeLinejoin="round" strokeLinecap="round" />
      <line x1={X(B25)} x2={X(B25)} y1={YB} y2={YT - 30} stroke={T.ink} strokeWidth={4} strokeDasharray="10 8" opacity={g(f, at(k('line')) + 20, 14)} />
      {/* 절반 꺾쇠: 4억 높이 → 2억 높이 */}
      {opened && f < at(k('ask')) + 20 && <g opacity={g(f, crossAt + qGap, 12) * (1 - g(f, at(k('ask')), 14))}>
        <line x1={X(B25) + 40} x2={X(B25) + 40} y1={Y(p.caps[1][1])} y2={Y(p.caps[1][1]) + (Y(p.caps[2][1]) - Y(p.caps[1][1])) * g(f, crossAt + qGap, 18)} stroke={T.rise} strokeWidth={6} strokeLinecap="round" />
        <path d={`M${X(B25) + 24} ${Y(p.caps[2][1]) - 18} L${X(B25) + 40} ${Y(p.caps[2][1])} L${X(B25) + 56} ${Y(p.caps[2][1]) - 18}`} fill="none" stroke={T.rise} strokeWidth={6} strokeLinecap="round" strokeLinejoin="round" opacity={g(f, crossAt + qGap + 14, 8)} />
      </g>}
      {showDot && <circle cx={X(dx)} cy={Y(dy)} r={20 * sp(at(k('jump')))} fill={T.surface} stroke={T.ink} strokeWidth={7} />}
    </svg>
    {lab(X(B25), YB + 36, p.xTicks[1][1], ax, {fontSize: 40, color: T.ink})}
    {lab(XR - 40, YB + 36, p.xName, ax, {color: T.ink3, fontSize: 28})}
    {lab(X(22.5), Y(p.caps[1][1]) - 56, `${p.xTicks[0][1]}~${p.xTicks[1][1]} · 한도 ${loS}`, g(f, at(k('line')) + 10, 14), {fontSize: 36})}
    {lab(X(27.5), Y(p.caps[2][1]) - 56, `넘으면 · 한도 ${hiS}`, g(f, at(k('line')) + 30, 14), {fontSize: 36})}
    {opened && f < at(k('ask')) + 20 && lab(X(B25) + 130, (Y(p.caps[1][1]) + Y(p.caps[2][1])) / 2, p.half ?? '', g(f, crossAt + qGap + 8, 12) * (1 - g(f, at(k('ask')), 14)), {fontSize: 40, color: T.rise, transform: 'translate(0, -50%)'})}
    {/* 오른쪽 칸: 점이 있는 쪽 한도 — 넘는 순간 '?' 쉼 뒤 2억(주황 하나 + 손 동그라미) */}
    {showDot && <div style={{position: 'absolute', left: PX, top: 380, width: 300, opacity: sp(at(k('jump')))}}>
      <div style={{...F, fontWeight: 700, fontSize: 34, color: T.ink2}}>이 집 한도</div>
      <div style={{position: 'relative', marginTop: 18, ...F, fontWeight: 800, fontSize: 130, letterSpacing: -4, lineHeight: 1.05, color: !over ? T.ink : opened ? T.accent : T.ink3}}>
        {f >= at(k('ask')) ? <span style={{fontSize: 64, color: T.ink2, letterSpacing: -1}}>{loS}? {hiS}?</span> : !over ? loS : opened ? hiS : '?'}
        {over && opened && f < at(k('ask')) && <svg width={300} height={200} style={{position: 'absolute', left: -20, top: -30, overflow: 'visible'}}><HandCircle cx={124} cy={100} rx={150} ry={78} p={circ} /></svg>}
      </div>
    </div>}
    {f >= at(k('ask')) && <div style={{position: 'absolute', left: 300, top: 268, opacity: sp(at(k('ask')) + 6), background: T.dbg, borderRadius: 18, padding: '18px 32px', ...F, fontWeight: 800, fontSize: 48, color: '#fff', whiteSpace: 'nowrap'}}>{p.ask}</div>}
  </>;
};
