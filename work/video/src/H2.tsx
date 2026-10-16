// H-2 "잠실·대치·반포, 오래된 단지 vs 새 단지"(손품 씨 2화) 화면 — 재료 work/video/h2.json(ep/H-2/h2props.py가 script.md·voice.json·calc_out·raw/tour_*.json으로 만든다)
// 틀은 TallyFrame(제목·형광 부제·흰 보드·정확한 값 칩·말 자막·출처). 색·글꼴은 parts/fm 토큰 그대로. H1.tsx의 지도·카드 방식을 이어 쓴다.
// 색 규칙: 1990년 전에 지은 단지 = 회색(ink2), 그 뒤 단지 = 주황(accent) — 대본 (화면:) 줄 그대로.
// 그림 종류: 지도(잠실·대치 한 좌표계·보행로) · 순위 막대 · 한 달 거래 점(값 축) · 층×값 점 · 달별 선 · 짝 막대 · 건수 점 · 매매/전세 겹 막대 · 보증금 안 전세 막대 · 걸음 거리 막대 · 사람 카드 · 결론 줄 · 자료 칸 · 표.
// U5(같은 화면 8초 이하): 말 줄마다 강조 줄·오른쪽 카드가 바뀌고, 긴 줄 안에서는 강조가 차례로 넘어간다. 숫자 글자는 그림 위에 두지 않는다.
import React, {useMemo} from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame, Easing} from 'remotion';
import {T, F, CL} from './parts/fm';
import {TallyFrame, TallyLine, tallyStarts, tallyIdx} from './motion/TallyFrame';

type HLine = TallyLine & {audio?: string | null};
export type HScene = {key: string; kind: string; title: string; sub?: string | null; source?: string | null; chapter?: string | null; data: any; lines: HLine[]; frames: number};
type Cx = {name: string; poly: number[][]; c: [number, number]; ppy: number | null; built: number; walk: Record<string, {name: string; m: number; pts: number[]; end: [number, number]} | null>};
type DMap = {name: string; roads: [number, number[]][]; parks: number[][]; blocks: number[][]; stations: [string, number, number][]; cx: Cx[]};
export type H2Props = {fps: number; scenes: HScene[]; missing: number; maps: Record<string, DMap>; mapBox: [number, number]};
export const h2Frames = (p: H2Props) => p.scenes.reduce((a, s) => a + s.frames, 0);

const Maps = React.createContext<Record<string, DMap>>({});
const fade = (f: number, at: number, d = 10) => interpolate(f, [at, at + d], [0, 1], CL);
const ease = (f: number, a: number, d: number) => interpolate(f, [a, a + d], [0, 1], {...CL, easing: Easing.inOut(Easing.cubic)});
const OLDC = T.ink2, NEWC = T.accent;
const ageCol = (o: string) => (o === 'old' ? OLDC : NEWC);
const Y0 = 340;

const useBeat = (s: HScene) => {
  const f = useCurrentFrame(); const st = tallyStarts(s.lines); const n = s.lines.length;
  const k = Math.max(0, tallyIdx(s.lines, f));
  const at = (i: number) => st[Math.max(0, Math.min(n - 1, i))] ?? 0;
  const len = (i: number) => s.lines[Math.max(0, Math.min(n - 1, i))]?.frames ?? 90;
  const clampI = (i: number) => Math.max(0, Math.min(n - 1, i));
  return {f, k, at, n, len, clampI};
};
// 지금 줄의 강조 목록을 줄 길이 안에서 차례로 켠다(긴 줄도 8초 안에 화면이 바뀐다)
const seqOn = (idx: number[], f: number, a: number, len: number) => idx.filter((_, j) => f >= a + 6 + j * Math.min(60, (len - 12) / Math.max(1, idx.length)));

// ───────── 공통 카드 ─────────
const DarkCard: React.FC<{x: number; y: number; w: number; at: number; big: string; small?: string; bg?: string; size?: number; f: number}> = ({x, y, w, at, big, small, bg = T.ink, size = 46, f}) => {
  const o = fade(f, at, 8);
  return (
    <div style={{position: 'absolute', left: x, top: y + (1 - o) * 10, width: w, opacity: o, background: bg, borderRadius: 18, padding: '20px 28px', boxSizing: 'border-box'}}>
      <div style={{...F, fontWeight: 700, fontSize: size, color: '#fff', lineHeight: 1.2, wordBreak: 'keep-all'}}>{big}</div>
      {small ? <div style={{...F, fontWeight: 700, fontSize: 26, color: bg === T.ink ? T.daccent : '#ffe3d1', marginTop: 8, wordBreak: 'keep-all'}}>{small}</div> : null}
    </div>
  );
};
const StepCard: React.FC<{st: any; f: number; at: number; x?: number; y?: number; w?: number; size?: number}> = ({st, f, at, x = 1215, y = Y0 + 20, w = 570, size = 44}) =>
  st ? <DarkCard f={f} x={x} y={y} w={w} at={at} big={st[0]} small={st[1]} bg={st[2] === 'accent' ? T.accent : T.ink} size={size} /> : null;
const SideCards: React.FC<{cards: string[][]; shownAt: number[]; active: number; f: number; x?: number; w?: number; y?: number; gap?: number}> = ({cards, shownAt, active, f, x = 1215, w = 570, y = Y0, gap = 14}) => {
  const n = cards.length; const h = Math.min(150, (840 - y - gap * (n - 1)) / n);
  return (
    <>
      {cards.map((c, i) => {
        const o = fade(f, shownAt[i], 8); if (o <= 0) return null;
        const on = i === active;
        return (
          <div key={i} style={{position: 'absolute', left: x, top: y + i * (h + gap), width: w, height: h, opacity: o, boxSizing: 'border-box', borderRadius: 16, padding: '14px 24px',
            background: on ? T.ink : '#fff', border: on ? 'none' : `2px solid ${T.line}`, display: 'flex', flexDirection: 'column', justifyContent: 'center'}}>
            <div style={{...F, fontWeight: 700, fontSize: 24, color: on ? T.dink3 : T.ink3, whiteSpace: 'nowrap'}}>{c[0]}</div>
            <div style={{...F, fontWeight: 700, fontSize: c[1].length > 14 ? 30 : 40, color: on ? '#fff' : T.ink, whiteSpace: 'nowrap', lineHeight: 1.15}}>{c[1]}</div>
            {c[2] ? <div style={{...F, fontWeight: 700, fontSize: 22, color: on ? T.daccent : T.ink2, whiteSpace: 'nowrap'}}>{c[2]}</div> : null}
          </div>
        );
      })}
    </>
  );
};
const activeOf = (shown: number[], f: number) => { let a = -1; shown.forEach((t, i) => { if (f >= t) a = i; }); return a; };
const Legend: React.FC<{x: number; y: number; o?: number}> = ({x, y, o = 1}) => (
  <div style={{position: 'absolute', left: x, top: y, display: 'flex', gap: 24, opacity: o}}>
    <span style={{...F, fontWeight: 700, fontSize: 22, color: OLDC}}>■ 1990년 전에 지은 단지</span>
    <span style={{...F, fontWeight: 700, fontSize: 22, color: NEWC}}>■ 그 뒤 단지</span>
  </div>
);

// ───────── 지도 ─────────
type VB = {cx: number; cy: number; w: number};
const MX = 130, MY = 318, MW = 1060, MH = 524;
const pathOf = (q: number[], close = false) => { let d = ''; for (let i = 0; i < q.length; i += 2) d += (i ? 'L' : 'M') + q[i] + ',' + q[i + 1]; return close ? d + 'Z' : d; };
const lerpVB = (a: VB, b: VB, t: number): VB => ({cx: a.cx + (b.cx - a.cx) * t, cy: a.cy + (b.cy - a.cy) * t, w: a.w * Math.pow(b.w / a.w, t)});
const cxByName = (maps: Record<string, DMap>, n: string) => { for (const m of Object.values(maps)) { const c = m.cx.find((x) => x.name === n); if (c) return c; } return null; };
const MapBase: React.FC = () => {
  const maps = React.useContext(Maps);
  const body = useMemo(() => Object.entries(maps).map(([k, m]) => (
    <g key={k}>
      {m.parks.map((q, i) => <path key={'p' + i} d={pathOf(q, true)} fill="#e3efe0" />)}
      {m.blocks.map((q, i) => <path key={'b' + i} d={pathOf(q, true)} fill="#eceef2" />)}
      {m.roads.map(([w, q], i) => <path key={'r' + i} d={pathOf(q)} fill="none" stroke="#d9dde3" strokeWidth={w} strokeLinecap="round" vectorEffect="non-scaling-stroke" />)}
    </g>
  )), [maps]);
  return <>{body}</>;
};
const MapView: React.FC<{vb: VB; focus: string[]; old: string[]; routes?: {name: string; t: number}[]; dongLabels?: boolean; labels?: string[]}> = ({vb, focus, old, routes = [], dongLabels, labels}) => {
  const maps = React.useContext(Maps);
  const vh = vb.w * MH / MW; const s = vb.w / MW;
  const all = Object.values(maps).flatMap((m) => m.cx);
  const fill = (c: Cx) => {
    const on = focus.includes(c.name); const o = old.includes(c.name);
    if (!on) return o ? '#c9cdd4' : '#ffe0cc';
    return o ? OLDC : NEWC;
  };
  const lab = (px: number, py: number, text: string, size: number, col = T.ink) => (
    <text x={px} y={py} textAnchor="middle" style={{...F, fontWeight: 700}} fontSize={size * s} fill={col} stroke="#fbfbfc" strokeWidth={6 * s} paintOrder="stroke">{text}</text>
  );
  return (
    <div style={{position: 'absolute', left: MX, top: MY, width: MW, height: MH, borderRadius: 18, overflow: 'hidden', background: '#fbfbfc', border: `2px solid ${T.line}`}}>
      <svg width={MW} height={MH} viewBox={`${vb.cx - vb.w / 2} ${vb.cy - vh / 2} ${vb.w} ${vh}`} style={{display: 'block'}}>
        <MapBase />
        {all.map((c, i) => <g key={i}>{c.poly.map((q, j) => <path key={j} d={pathOf(q, true)} fill={fill(c)} stroke="#fff" strokeWidth={1.5} vectorEffect="non-scaling-stroke" />)}</g>)}
        {vb.w > 3500 ? null : Object.values(maps).flatMap((m) => m.stations).map(([, sx, sy], i) => <circle key={'s' + i} cx={sx} cy={sy} r={8 * s} fill="#fff" stroke={T.accent} strokeWidth={3} vectorEffect="non-scaling-stroke" />)}
        {routes.map((r, i) => {
          const c = cxByName(maps, r.name); const wk = c?.walk?.station; if (!wk || r.t <= 0) return null;
          const n = wk.pts.length / 2; const k = Math.max(2, Math.ceil(n * r.t));
          return <g key={'w' + i}>
            <path d={pathOf(wk.pts.slice(0, k * 2))} fill="none" stroke={T.ink} strokeWidth={6} strokeLinecap="round" strokeLinejoin="round" vectorEffect="non-scaling-stroke" />
            {r.t >= 1 ? <circle cx={wk.end[0]} cy={wk.end[1]} r={12 * s} fill={T.ink} stroke="#fff" strokeWidth={3} vectorEffect="non-scaling-stroke" /> : null}
          </g>;
        })}
        {dongLabels ? Object.values(maps).map((m, i) => {
          const xs = m.cx.map((c) => c.c[0]), ys = m.cx.map((c) => c.c[1]);
          return <g key={'d' + i}>{lab(Math.min(...xs) - 300 * s, Math.min(...ys) - 80 * s, m.name, 48, T.ink)}</g>;
        }) : null}
        {(labels ?? []).map((n, i) => { const c = cxByName(maps, n); return c ? <g key={'f' + i}>{lab(c.c[0], c.c[1] - 22 * s, n, 26)}</g> : null; })}
      </svg>
      <div style={{...F, position: 'absolute', right: 10, bottom: 6, fontWeight: 500, fontSize: 14, color: T.ink3}}>© OpenStreetMap contributors</div>
      <Legend x={14} y={MH - 40} />
    </div>
  );
};
const MapScene: React.FC<{s: HScene}> = ({s}) => {
  const {f, at, n, clampI} = useBeat(s); const d = s.data;
  const views: VB[] = d.views;
  let vb = views[0];
  for (let i = 1; i < views.length; i++) { const a = n === 1 ? (s.frames * i) / views.length : at(i); if (f >= a) vb = lerpVB(vb, views[i], ease(f, a, 36)); }
  if (views.length === 1) vb = {...vb, w: vb.w * interpolate(f, [0, s.frames], [1.1, 0.9], CL)};
  const routes = (d.routes ?? []).map(([name]: [string, string], i: number) => ({name, t: ease(f, at(clampI(i)) + 10, 40)}));
  const cards: string[][] = d.cards ?? [];
  const shown = cards.map((_, i) => (n === 1 ? 6 + i * Math.min(80, (s.frames - 20) / cards.length) : at(clampI(i)) + 6));
  return (
    <>
      <MapView vb={vb} focus={d.focus} old={d.old} routes={routes} dongLabels={d.dongLabels} labels={d.labels} />
      <SideCards cards={cards} shownAt={shown} active={activeOf(shown, f)} f={f} />
    </>
  );
};

// ───────── 순위 막대(가로) ─────────
const Rank: React.FC<{s: HScene}> = ({s}) => {
  const {f, k, at, len} = useBeat(s); const d = s.data;
  const rows: [string, number, string, string, string][] = d.rows; const steps: any[] = d.steps ?? [];
  const st = steps[Math.min(k, steps.length - 1)];
  const hi: number[] = st && st[3] ? seqOn(st[3], f, at(k), len(k)) : [];
  const RH = Math.min(82, 420 / rows.length), X = 440, W = 430;
  return (
    <>
      <Legend x={150} y={Y0 - 6} />
      {d.line2 ? (() => { const x = X + W * d.line2 / d.max; return <>
        <div style={{position: 'absolute', left: x, top: Y0 + 30, height: RH * 3, borderLeft: `3px dashed ${T.ink}`, opacity: fade(f, at(2))}} />
        <div style={{...F, position: 'absolute', left: x - 60, width: 120, textAlign: 'center', top: Y0 + 4, fontWeight: 700, fontSize: 22, color: T.ink, opacity: fade(f, at(2))}}>평당 2억</div></>; })() : null}
      {rows.map(([name, v, txt, sub, age], i) => {
        const g = ease(f, 6 + i * 8, 26); const top = Y0 + 34 + i * RH; const on = hi.includes(i); const dim = hi.length > 0 && !on;
        return <div key={i} style={{opacity: dim ? 0.35 : 1}}>
          {on ? <div style={{position: 'absolute', left: 140, top: top - 4, width: 1050, height: RH - 8, borderRadius: 12, background: T.soft}} /> : null}
          <div style={{...F, position: 'absolute', left: 160, top: top + 4, fontWeight: 700, fontSize: 30, color: T.ink, whiteSpace: 'nowrap'}}>{name}</div>
          <div style={{...F, position: 'absolute', left: 160, top: top + 42, fontWeight: 500, fontSize: 20, color: T.ink3, whiteSpace: 'nowrap'}}>{sub}</div>
          <div style={{position: 'absolute', left: X, top: top + 12, width: W * v / d.max * g, height: RH - 36, borderRadius: 8, background: ageCol(age)}} />
          <div style={{...F, position: 'absolute', left: X + W * v / d.max * g + 14, top: top + 10, fontWeight: 700, fontSize: 32, color: age === 'old' ? T.ink : T.accent, opacity: g, whiteSpace: 'nowrap'}}>{txt}</div>
        </div>;
      })}
      <StepCard st={st} f={f} at={at(k) + 4} />
    </>
  );
};

// ───────── 한 달 거래 점(값 축) ─────────
const Strip: React.FC<{s: HScene}> = ({s}) => {
  const {f, k, at, n} = useBeat(s); const d = s.data;
  const deals: [number, number, number][] = d.deals; const X0 = 220, X1 = 1120, AY = 640;
  const xv = (v: number) => X0 + (v - d.lo) / (d.hi - d.lo) * (X1 - X0);
  const sorted = deals.map((x, i) => [x[1], i] as [number, number]).sort((a, b) => a[0] - b[0]);
  const stack: Record<string, number> = {}; const ys: number[] = [];
  sorted.forEach(([v, i]) => { const key = v.toFixed(2); const j = stack[key] ?? 0; stack[key] = j + 1; ys[i] = AY - 40 - j * 46; });
  const rank: number[] = []; sorted.forEach(([, i], r) => { rank[i] = r; });
  const span = n === 1 ? s.frames * 0.5 : Math.min(90, s.lines[0].frames * 0.6);
  const lo = sorted[0][0], hi = sorted[sorted.length - 1][0];
  const br = fade(f, 10 + span, 10);
  const ticks: number[] = []; for (let v = d.lo; v <= d.hi; v += 5) ticks.push(v);
  const st = (d.steps ?? [])[Math.min(k, (d.steps ?? []).length - 1)];
  return (
    <>
      <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
        <line x1={X0} x2={X1} y1={AY} y2={AY} stroke={T.ink} strokeWidth={3} />
        {ticks.map((v) => <g key={v}><line x1={xv(v)} x2={xv(v)} y1={AY} y2={AY + 12} stroke={T.ink} strokeWidth={3} />
          <text x={xv(v)} y={AY + 44} textAnchor="middle" style={{...F, fontWeight: 500}} fontSize={24} fill={T.ink3}>{v}억</text></g>)}
        {deals.map((x, i) => { const o = fade(f, 8 + rank[i] / deals.length * span, 6); return <circle key={i} cx={xv(x[1])} cy={ys[i]} r={18} fill={T.accent} stroke="#fff" strokeWidth={3} opacity={o} />; })}
        <g opacity={br}>
          <line x1={xv(lo)} x2={xv(hi)} y1={Y0 + 70} y2={Y0 + 70} stroke={T.ink} strokeWidth={4} />
          <line x1={xv(lo)} x2={xv(lo)} y1={Y0 + 56} y2={Y0 + 84} stroke={T.ink} strokeWidth={4} />
          <line x1={xv(hi)} x2={xv(hi)} y1={Y0 + 56} y2={Y0 + 84} stroke={T.ink} strokeWidth={4} />
          <text x={(xv(lo) + xv(hi)) / 2} y={Y0 + 50} textAnchor="middle" style={{...F, fontWeight: 700}} fontSize={36} fill={T.ink}>{d.gap}</text>
        </g>
        {k >= 1 ? deals.map((x, i) => <text key={'t' + i} x={xv(x[1])} y={ys[i] + 8} textAnchor="middle" style={{...F, fontWeight: 700}} fontSize={15} fill="#fff" opacity={fade(f, at(1) + 6 + rank[i] * 3)}>중개</text>) : null}
      </svg>
      <StepCard st={st} f={f} at={n === 1 ? 14 + span : at(k) + 4} size={40} />
    </>
  );
};

// ───────── 층 × 값 점 ─────────
const Floors: React.FC<{s: HScene}> = ({s}) => {
  const {f, k, at} = useBeat(s); const d = s.data;
  const deals: [number, string, string][] = d.deals; const X0 = 260, X1 = 1110, YT = Y0 + 30, YB = 790;
  const vals = deals.map((x) => parseFloat(x[1])); const lo = 50, hi = 75;
  const xv = (v: number) => X0 + (v - lo) / (hi - lo) * (X1 - X0); const yv = (fl: number) => YB - fl / d.top * (YB - YT);
  const order = deals.map((x, i) => [parseInt(x[2]), i] as [number, number]).sort((a, b) => a[0] - b[0]);
  const st = (d.steps ?? [])[Math.min(k, (d.steps ?? []).length - 1)];
  return (
    <>
      <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
        {[0, 5, 10, 15, 20, 25].map((fl) => <g key={fl}><line x1={X0} x2={X1} y1={yv(fl)} y2={yv(fl)} stroke={T.line} strokeWidth={2} />
          <text x={X0 - 14} y={yv(fl) + 8} textAnchor="end" style={{...F, fontWeight: 500}} fontSize={22} fill={T.ink3}>{fl}층</text></g>)}
        {[50, 55, 60, 65, 70, 75].map((v) => <text key={v} x={xv(v)} y={YB + 36} textAnchor="middle" style={{...F, fontWeight: 500}} fontSize={22} fill={T.ink3}>{v}억</text>)}
        {order.map(([, i], r) => { const x = deals[i]; const o = fade(f, 6 + r * 8, 6); return <circle key={i} cx={xv(vals[i])} cy={yv(x[0])} r={16} fill={k >= 1 ? T.ink : T.accent} stroke="#fff" strokeWidth={3} opacity={o} />; })}
      </svg>
      <div style={{...F, position: 'absolute', left: X0, top: Y0 - 6, fontWeight: 700, fontSize: 22, color: T.ink2}}>세로 = 층 · 가로 = 거래 값 · 점 = 계약 한 건(계약일 순으로 나타남)</div>
      <StepCard st={st} f={f} at={at(k) + 10} />
    </>
  );
};

// ───────── 달별 선 ─────────
const MONTHS = ['2025.11', '2025.12', '2026.01', '2026.02', '2026.03', '2026.04', '2026.05', '2026.06', '2026.07', '2026.08', '2026.09', '2026.10'];
const COL: Record<string, string> = {ink: T.ink, accent: T.accent, ink2: T.ink2};
const Lines: React.FC<{s: HScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data;
  const series: [string, string, [string, number, number][]][] = d.series;
  const LX0 = 230, LX1 = 1130, LY0 = Y0 + 40, LY1 = 780;
  const mw = (LX1 - LX0) / (MONTHS.length - 1);
  const xm = (ym: string) => LX0 + MONTHS.indexOf(ym) * mw; const yv = (v: number) => LY1 - (v - d.min) / (d.max - d.min) * (LY1 - LY0);
  const ticks: number[] = []; for (let v = Math.ceil(d.min / 3) * 3; v <= d.max; v += 3) ticks.push(v);
  const shown = series.map((_, i) => 6 + i * Math.max(30, s.frames * 0.35));
  return (
    <>
      <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
        {ticks.map((v) => <g key={v}><line x1={LX0} x2={LX1} y1={yv(v)} y2={yv(v)} stroke={T.line} strokeWidth={2} />
          <text x={LX0 - 16} y={yv(v) + 8} textAnchor="end" style={{...F, fontWeight: 500}} fontSize={22} fill={T.ink3}>{v}억</text></g>)}
        {MONTHS.map((m, i) => i % 2 === 0 ? <text key={m} x={xm(m)} y={LY1 + 36} textAnchor="middle" style={{...F, fontWeight: 500}} fontSize={22} fill={T.ink3}>{m.slice(2)}</text> : null)}
        {series.map(([, col, pts], si) => {
          const draw = ease(f, shown[si], 40); const xy = pts.map((p) => [xm(p[0]), yv(p[1])]); const nn = Math.max(1, Math.ceil(xy.length * draw));
          if (f < shown[si]) return null;
          return <g key={si}>
            <polyline points={xy.slice(0, nn).map((q) => q.join(',')).join(' ')} fill="none" stroke={COL[col]} strokeWidth={6} strokeLinejoin="round" strokeLinecap="round" />
            {xy.slice(0, nn).map((q, i) => <circle key={i} cx={q[0]} cy={q[1]} r={9} fill={COL[col]} stroke="#fff" strokeWidth={3} />)}
          </g>;
        })}
      </svg>
      <div style={{display: 'flex', gap: 26, position: 'absolute', left: LX0, top: Y0 - 6}}>{series.map(([name, col]) => <span key={name} style={{...F, fontWeight: 700, fontSize: 24, color: COL[col]}}>━ {name}</span>)}</div>
      <SideCards f={f} cards={d.cards} shownAt={shown.map((x) => x + 20)} active={activeOf(shown.map((x) => x + 20), f)} />
    </>
  );
};

// ───────── 짝 막대(세로) ─────────
const PairBars: React.FC<{s: HScene}> = ({s}) => {
  const {f, k, at} = useBeat(s); const d = s.data;
  const bars: [string, number, string, string, string][] = d.bars;
  const BX = 900, BW = 240, GAP = 160, BY = 760, BH = 380;
  const st = (d.steps ?? [])[Math.min(k, (d.steps ?? []).length - 1)];
  return (
    <>
      {bars.map((b, i) => {
        const a = i === 0 ? 6 : at(0) + 20; const g = ease(f, a, 30); const h = BH * b[1] / d.max * g; const x = BX + i * (BW + GAP);
        return <React.Fragment key={i}>
          <div style={{position: 'absolute', left: x, top: BY - h, width: BW, height: h, background: COL[b[4]] ?? T.ink2, borderRadius: '14px 14px 0 0'}} />
          <div style={{...F, position: 'absolute', left: x - 60, width: BW + 120, top: BY - h - 56, textAlign: 'center', fontWeight: 700, fontSize: 38, color: b[4] === 'accent' ? T.accent : T.ink, opacity: g}}>{b[2]}</div>
          <div style={{...F, position: 'absolute', left: x - 80, width: BW + 160, top: BY + 8, textAlign: 'center', fontWeight: 700, fontSize: 28, color: T.ink, whiteSpace: 'nowrap'}}>{b[0]}</div>
          <div style={{...F, position: 'absolute', left: x - 80, width: BW + 160, top: BY + 44, textAlign: 'center', fontWeight: 500, fontSize: 22, color: T.ink3, whiteSpace: 'nowrap'}}>{b[3]}</div>
        </React.Fragment>;
      })}
      <StepCard st={st} f={f} at={at(k) + 8} x={160} y={Y0 + 60} w={620} size={k === 1 ? 64 : 48} />
    </>
  );
};

// ───────── 건수 점 ─────────
const Count: React.FC<{s: HScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const groups: [string, number, string][] = d.groups;
  const PER = 45, R = 9, G = 22;
  let top = Y0 + 10;
  const st = (d.steps ?? [])[0];
  return (
    <>
      {groups.map(([name, nn, age], gi) => {
        const rowsN = Math.ceil(nn / PER); const y = top; top += 46 + rowsN * G + 20; const a = 6 + gi * Math.max(18, s.frames * 0.12);
        return <div key={gi} style={{position: 'absolute', left: 150, top: y, opacity: fade(f, a)}}>
          <div style={{...F, fontWeight: 700, fontSize: 28, color: T.ink, whiteSpace: 'nowrap'}}>{name} <span style={{color: ageCol(age)}}>{nn}건</span></div>
          <svg width={PER * G} height={rowsN * G + 4} style={{position: 'absolute', left: 0, top: 42}}>
            {Array.from({length: nn}).map((_, i) => <circle key={i} cx={R + (i % PER) * G} cy={R + Math.floor(i / PER) * G} r={R} fill={ageCol(age)} opacity={fade(f, a + 4 + i * 0.4, 4)} />)}
          </svg>
        </div>;
      })}
      <div style={{...F, position: 'absolute', left: 1215, top: Y0 - 6, fontWeight: 700, fontSize: 24, color: T.ink2}}>{d.total}</div>
      <StepCard st={st} f={f} at={Math.max(40, s.frames * 0.5)} y={Y0 + 40} />
    </>
  );
};

// ───────── 매매 / 전세 겹 막대 ─────────
const Pair2: React.FC<{s: HScene}> = ({s}) => {
  const {f, k, at} = useBeat(s); const d = s.data;
  const rows: [string, string, number, string, number, string, string, string, number][] = d.rows;
  const X = 560, W = 760, RH = 62; const xv = (v: number) => X + W * v / d.max;
  let gtop = Y0 + 30; const tops: number[] = []; let prev = '';
  rows.forEach((r) => { if (r[0] !== prev) { gtop += prev ? 18 : 0; prev = r[0]; } tops.push(gtop); gtop += RH; });
  const stepAt = Object.keys(d.steps ?? {}).map(Number);
  const stepOn = stepAt.includes(k);
  return (
    <>
      <div style={{display: 'flex', gap: 24, position: 'absolute', left: 150, top: Y0 - 8}}>
        <span style={{...F, fontWeight: 700, fontSize: 22, color: T.ink3}}>■ 긴 회색 막대 = 매매 가운데 값</span>
        <span style={{...F, fontWeight: 700, fontSize: 22, color: T.ink}}>■ 색 막대 = 전세 가운데 값</span>
        <span style={{...F, fontWeight: 700, fontSize: 22, color: T.accent}}>┆ {d.depositTxt}</span>
      </div>
      <div style={{position: 'absolute', left: xv(d.deposit), top: Y0 + 24, height: gtop - Y0 - 20, borderLeft: `3px dashed ${T.accent}`, opacity: fade(f, 10)}} />
      {rows.map(([g, name, sale, saleT, rent, rentT, ratio, age, line], i) => {
        const a = at(line) + 4; const gs = ease(f, a, 22); const gr = ease(f, a + 12, 20); const cur = k === line; const hot = stepOn && i === 0;
        return <div key={i} style={{opacity: fade(f, a - 2)}}>
          <div style={{position: 'absolute', left: 140, top: tops[i] - 4, width: 1650, height: RH - 6, borderRadius: 10, background: hot ? T.soft : cur ? '#f0f1f4' : 'transparent'}} />
          <div style={{...F, position: 'absolute', left: 156, top: tops[i] + 10, fontWeight: 700, fontSize: 22, color: T.ink3}}>{g}</div>
          <div style={{...F, position: 'absolute', left: 222, top: tops[i] + 6, fontWeight: 700, fontSize: 28, color: age === 'old' ? OLDC : T.accent, whiteSpace: 'nowrap'}}>{name}</div>
          <div style={{position: 'absolute', left: X, top: tops[i] + 8, width: (xv(sale) - X) * gs, height: 40, borderRadius: 6, background: '#d7dbe1'}} />
          <div style={{position: 'absolute', left: X, top: tops[i] + 8, width: (xv(rent) - X) * gr, height: 40, borderRadius: 6, background: ageCol(age)}} />
          <div style={{...F, position: 'absolute', left: xv(sale) + 14, top: tops[i] + 8, fontWeight: 700, fontSize: 26, color: T.ink, opacity: gr, whiteSpace: 'nowrap'}}>
            매매 {saleT} · <span style={{color: ageCol(age)}}>전세 {rentT}</span> <span style={{fontSize: 20, color: T.ink3}}>({ratio})</span></div>
        </div>;
      })}
      {stepOn ? <div style={{...F, position: 'absolute', left: 150, top: 806, fontWeight: 700, fontSize: 26, color: T.accent, opacity: fade(f, at(k) + 4)}}>{d.steps[String(k)][0]} · <span style={{color: T.ink3, fontSize: 22}}>{d.steps[String(k)][1]}</span></div> : null}
    </>
  );
};

// ───────── 보증금 안 전세 ─────────
const Under: React.FC<{s: HScene}> = ({s}) => {
  const {f, k, at} = useBeat(s); const d = s.data;
  const rows: [string, number, string, number, string, number][] = d.rows; const steps: any[] = d.steps;
  const st = steps[Math.min(k, steps.length - 1)]; const want = st ? st[3] : null;
  const X = 470, W = 520, RH = 56; const xv = (v: number) => X + W * v / d.max;
  return (
    <>
      <Legend x={150} y={Y0 - 8} />
      <div style={{position: 'absolute', left: xv(d.deposit), top: Y0 + 24, height: RH * rows.length + 8, borderLeft: `3px dashed ${T.accent}`}} />
      <div style={{...F, position: 'absolute', left: xv(d.deposit) - 120, width: 240, textAlign: 'center', top: Y0 + 34 + RH * rows.length, fontWeight: 700, fontSize: 22, color: T.accent}}>보증금 9.50억</div>
      {rows.map(([name, v, txt, built, age, nn], i) => {
        const a = 6 + i * Math.min(14, (s.lines[0].frames - 20) / rows.length); const g = ease(f, a, 18); const top = Y0 + 30 + i * RH;
        const dim = want && age !== want; const on = want && age === want;
        return <div key={i} style={{opacity: (dim ? 0.3 : 1) * fade(f, a - 2)}}>
          {on ? <div style={{position: 'absolute', left: 140, top: top - 2, width: 1040, height: RH - 6, borderRadius: 10, background: T.soft}} /> : null}
          <div style={{...F, position: 'absolute', left: 156, top: top + 6, fontWeight: 700, fontSize: 28, color: T.ink, whiteSpace: 'nowrap'}}>{name} <span style={{fontSize: 20, color: T.ink3}}>{built}</span></div>
          <div style={{position: 'absolute', left: X, top: top + 8, width: (xv(v) - X) * g, height: 34, borderRadius: 6, background: ageCol(age)}} />
          <div style={{...F, position: 'absolute', left: xv(d.max) + 20, top: top + 4, fontWeight: 700, fontSize: 28, color: ageCol(age), opacity: g, whiteSpace: 'nowrap'}}>{txt} <span style={{fontSize: 18, color: T.ink3}}>{nn}건</span></div>
        </div>;
      })}
      {k === 0 ? <DarkCard f={f} x={1215} y={Y0 + 20} w={570} at={Math.max(30, s.lines[0].frames * 0.6)} big="8곳" small="세 동네 84㎡대 거래 3건 이상 28단지 중" size={72} /> : <StepCard st={st} f={f} at={at(k) + 4} size={40} />}
    </>
  );
};

// ───────── 걸음 거리 막대 ─────────
const Walk: React.FC<{s: HScene}> = ({s}) => {
  const {f, k, at, len} = useBeat(s); const d = s.data;
  const rows: [string, number, string, string][] = d.rows; const st0 = d.steps[Math.min(k, d.steps.length - 1)];
  const half = st0 && st0[4] && f >= at(k) + len(k) * 0.5;   // 긴 줄: 줄 가운데에서 둘째 카드·강조로 넘김(같은 화면 8초 방지)
  const st = half ? st0[4] : st0;
  const hi = st ? (half ? st[3] : seqOn(st[3], f, at(k), len(k))) : [];
  const X = 520, W = 560, RH = 74;
  return (
    <>
      <Legend x={150} y={Y0 - 8} />
      {rows.map(([name, m, txt, age], i) => {
        const g = ease(f, 6 + i * 8, 26); const top = Y0 + 34 + i * RH; const on = hi.includes(i); const dim = hi.length > 0 && !on;
        return <div key={i} style={{opacity: dim ? 0.35 : 1}}>
          {on ? <div style={{position: 'absolute', left: 140, top: top - 4, width: 1040, height: RH - 8, borderRadius: 12, background: T.soft}} /> : null}
          <div style={{...F, position: 'absolute', left: 160, top: top + 10, fontWeight: 700, fontSize: 30, color: T.ink, whiteSpace: 'nowrap'}}>{name}</div>
          <div style={{position: 'absolute', left: X, top: top + 14, width: W * m / d.max * g, height: 34, borderRadius: 17, background: ageCol(age)}}>
            {Array.from({length: Math.floor(m / 100)}).map((_, j) => <div key={j} style={{position: 'absolute', left: (j + 0.5) * W * 100 / d.max - 5, top: 12, width: 10, height: 10, borderRadius: 5, background: '#fff', opacity: 0.7 * g}} />)}
          </div>
          <div style={{...F, position: 'absolute', left: X + W * m / d.max * g + 16, top: top + 8, fontWeight: 700, fontSize: 36, color: ageCol(age), opacity: g, whiteSpace: 'nowrap'}}>{txt}</div>
        </div>;
      })}
      <StepCard key={half ? 'b' : 'a'} st={st} f={f} at={half ? at(k) + len(k) * 0.5 : at(k) + 4} size={40} />
    </>
  );
};

// ───────── 사람 ─────────
const Avatar: React.FC<{x: number; y: number; size: number; f: number}> = ({x, y, size, f}) => {
  const o = ease(f, 0, 16);
  return (
    <svg width={size} height={size} viewBox="0 0 100 100" style={{position: 'absolute', left: x, top: y + (1 - o) * 30, opacity: o}}>
      <circle cx={50} cy={50} r={50} fill={T.soft} />
      <circle cx={50} cy={38} r={17} fill={T.ink} />
      <path d="M18 92 C20 66 36 58 50 58 C64 58 80 66 82 92 Z" fill={T.ink} />
      <rect x={38} y={60} width={24} height={8} rx={3} fill={T.accent} />
    </svg>
  );
};
const PersonCard: React.FC<{f: number; dday: string}> = ({f, dday}) => (
  <div style={{position: 'absolute', left: 150, top: Y0, width: 440, height: 480, background: '#fff', border: `2px solid ${T.line}`, borderRadius: 22}}>
    <Avatar x={110} y={30} size={220} f={f} />
    <div style={{...F, position: 'absolute', left: 0, right: 0, top: 268, textAlign: 'center', fontWeight: 700, fontSize: 52, color: T.ink}}>손품 씨</div>
    <div style={{...F, position: 'absolute', left: 120, top: 344, fontWeight: 700, fontSize: 26, color: T.accent, border: `3px solid ${T.accent}`, borderRadius: 10, padding: '2px 14px', transform: 'rotate(-4deg)', opacity: fade(f, 14)}}>가상 인물 · 계산용</div>
    <div style={{...F, position: 'absolute', left: 0, right: 0, top: 410, textAlign: 'center', fontWeight: 700, fontSize: 28, color: T.ink2, opacity: fade(f, 24)}}>{dday}</div>
  </div>
);
const Person: React.FC<{s: HScene}> = ({s}) => {
  const {f, k, at} = useBeat(s); const d = s.data;
  const RX = 650, RW = 1130;
  let body: React.ReactNode = null;
  if (d.teaser) {
    body = <div style={{position: 'absolute', left: RX, top: Y0 + 40, width: RW}}>
      {d.promise.map((t: string, i: number) => <div key={t} style={{...F, fontWeight: 700, fontSize: 64, color: i ? T.accent : T.ink, opacity: fade(f, 12 + i * Math.max(30, s.frames * 0.4), 10), marginBottom: 34}}>{i ? '→ ' : ''}{t}</div>)}
    </div>;
  } else {
    const b = d.beats[Math.min(k, d.beats.length - 1)];
    body = <StepCard st={b} f={f} at={at(k) + 10} x={RX} y={Y0 + 30} w={RW} size={64} />;
    if (d.beats.length === 1) body = <>{body}<DarkCard f={f} x={RX} y={Y0 + 260} w={RW} at={Math.max(40, s.frames * 0.5)} big="전세 칸부터 본다" small="잠실 · 대치 · 반포 84㎡대 신규 순수전세" size={48} /></>;
  }
  return <><PersonCard f={f} dday={d.dday} />{body}</>;
};

// ───────── 결론 ─────────
const Concl: React.FC<{s: HScene}> = ({s}) => {
  const f = useCurrentFrame(); const rows: string[] = s.data.rows; const step = Math.max(24, (s.frames - 30) / rows.length);
  return (
    <div style={{position: 'absolute', left: 160, top: Y0 - 10, width: 1600}}>
      {rows.map((t, i) => {
        const a = 8 + i * step; const on = f >= a && (i === rows.length - 1 || f < a + step);
        return <div key={i} style={{display: 'flex', alignItems: 'center', gap: 28, height: 112, marginBottom: 14, borderRadius: 20, padding: '0 36px', opacity: fade(f, a, 8),
          background: on ? T.ink : '#fff', border: on ? 'none' : `2px solid ${T.line}`}}>
          <div style={{...F, fontWeight: 700, fontSize: 56, color: T.accent, width: 60}}>{i + 1}</div>
          <div style={{...F, fontWeight: 700, fontSize: 50, color: on ? '#fff' : T.ink, whiteSpace: 'nowrap'}}>{t}</div>
        </div>;
      })}
    </div>
  );
};

// ───────── 자료 칸 ─────────
const Tiles: React.FC<{s: HScene}> = ({s}) => {
  const {f, k, at} = useBeat(s); const d = s.data;
  if (k <= 0) return (
    <div style={{position: 'absolute', left: 160, top: Y0 + 20, width: 1600}}>
      <div style={{...F, fontWeight: 700, fontSize: 30, color: T.ink2, marginBottom: 20}}>{d.tilesHead}</div>
      <div style={{display: 'flex', gap: 30}}>
        {d.tiles.map(([a, b]: string[], i: number) => <div key={a} style={{flex: 1, height: 300, background: T.ink, borderRadius: 22, padding: '40px 40px', boxSizing: 'border-box', opacity: fade(f, 10 + i * 30, 8)}}>
          <div style={{...F, fontWeight: 700, fontSize: 44, color: T.dink3}}>{a}</div>
          <div style={{...F, fontWeight: 700, fontSize: 110, color: '#fff', letterSpacing: -2}}>{b}</div>
        </div>)}
      </div>
    </div>
  );
  const st = d.steps[Math.min(k, d.steps.length - 1)];
  return <StepCard st={st} f={f} at={at(k) + 4} x={160} y={Y0 + 40} w={1600} size={110} />;
};

// ───────── 표 ─────────
const Table: React.FC<{s: HScene}> = ({s}) => {
  const {f, k, at, n} = useBeat(s); const d = s.data; const cols: string[] = d.cols; const rows: string[][] = d.rows;
  const Wc = [150, 400, 180, 330, 230, 330]; const RH = 62;
  const speechEnd = s.lines.reduce((a, l) => a + l.frames, 0);
  const cyc = f > speechEnd ? Math.floor((f - speechEnd) / 75) % rows.length : -1;
  return (
    <>
      <div style={{position: 'absolute', left: 140, top: Y0 - 6, width: 1640}}>
        <div style={{display: 'flex', height: 44, alignItems: 'center', borderBottom: `3px solid ${T.ink}`}}>
          {cols.map((c, i) => <div key={c} style={{...F, width: Wc[i], fontWeight: 700, fontSize: 22, color: T.ink2, textAlign: i > 1 ? 'right' : 'left', whiteSpace: 'nowrap'}}>{c}</div>)}
        </div>
        {rows.map((r, ri) => { const on = ri === cyc || (k === 0 && f < speechEnd && Math.floor((f - 10) / 45) === ri); const old = d.old[ri]; return (
          <div key={ri} style={{display: 'flex', height: RH, alignItems: 'center', borderBottom: `1px solid ${T.line}`, opacity: fade(f, 10 + ri * 8), background: on ? T.ink : 'transparent', borderRadius: 8}}>
            {r.map((v, i) => <div key={i} style={{...F, width: Wc[i], fontWeight: i === 1 ? 700 : 600, fontSize: i === 1 ? 30 : 28, color: on ? '#fff' : i === 1 ? (old ? OLDC : T.accent) : T.ink, textAlign: i > 1 ? 'right' : 'left', whiteSpace: 'nowrap', overflow: 'hidden'}}>{v}</div>)}
          </div>); })}
      </div>
      {n > 1 && k >= 1 ? <DarkCard f={f} x={140} y={Y0 + 396} w={1000} at={at(1)} big={`${d.cafe} · 세 동네 전체 표`} bg={T.accent} size={34} /> : null}
    </>
  );
};

const Body: React.FC<{s: HScene}> = ({s}) => {
  switch (s.kind) {
    case 'map': return <MapScene s={s} />;
    case 'rank': return <Rank s={s} />;
    case 'strip': return <Strip s={s} />;
    case 'floors': return <Floors s={s} />;
    case 'line': return <Lines s={s} />;
    case 'pair': return <PairBars s={s} />;
    case 'count': return <Count s={s} />;
    case 'pair2': return <Pair2 s={s} />;
    case 'under': return <Under s={s} />;
    case 'walk': return <Walk s={s} />;
    case 'person': return <Person s={s} />;
    case 'concl': return <Concl s={s} />;
    case 'tiles': return <Tiles s={s} />;
    case 'table': return <Table s={s} />;
    default: return null;
  }
};

const SceneView: React.FC<{s: HScene}> = ({s}) => {
  const st = tallyStarts(s.lines);
  return (
    <TallyFrame title={s.title} sub={s.sub} source={s.source} chapter={s.chapter} lines={s.lines}>
      <Body s={s} />
      {s.lines.map((l, i) => l.audio ? <Sequence key={i} from={st[i]} durationInFrames={l.frames}><Audio src={staticFile(l.audio)} /></Sequence> : null)}
    </TallyFrame>
  );
};

export const H2: React.FC<H2Props> = (p) => {
  let from = 0;
  return (
    <Maps.Provider value={p.maps}>
      <AbsoluteFill style={{background: T.bg}}>
        {p.scenes.map((s, i) => { const el = <Sequence key={i} from={from} durationInFrames={s.frames}><SceneView s={s} /></Sequence>; from += s.frames; return el; })}
      </AbsoluteFill>
    </Maps.Provider>
  );
};
