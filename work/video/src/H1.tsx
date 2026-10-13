// H-1 "84㎡ 1년 실거래 전부로 둘러본 세 동네"(헬리오시티·올림픽파크포레온·고덕그라시움) 화면 — 재료 work/video/h1.json(ep/H-1/h1props.py가 script.md·voice.json·calc_out·raw/tour_*.json으로 만든다)
// 틀은 TallyFrame(제목·형광 부제·흰 보드·정확한 값 칩·말 자막·출처 y864). 색·글꼴은 parts/fm 토큰 그대로.
// 그림 종류: 지도(세 동네 한 좌표계·보행로) · 거래 점(1년 전부, 값 순 줄 세우기) · 짝 막대 · 기간 막대 · 달력 칸(달마다 건수) · 층 그림 · 거래 한 건 카드 ·
//   달별 가운데 값 선 · 걸음 거리 자 · 비교 카드 · 왼쪽으로 뻗는 차이 막대 · 동별 작은 막대 셋 · 신고 기한 달력 · 계산서(더 드는 돈) · 표 · 사람 카드 · 결론 줄 · 자료 칸.
// U5(같은 화면 8초 이하): 말 줄이 바뀔 때마다 오른쪽 카드·검은 카드·지도 시점이 바뀐다. 겹침 0: 숫자 글자는 그림 위에 두지 않고 오른쪽 칸·빈 자리에 둔다.
// 숫자 글자는 전부 h1.json에서 온다. 코드 안 숫자는 배치·눈금뿐.
import React, {useMemo} from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame, Easing} from 'remotion';
import {T, F, CL} from './parts/fm';
import {TallyFrame, TallyLine, tallyStarts, tallyIdx} from './motion/TallyFrame';

type HLine = TallyLine & {audio?: string | null};
export type HScene = {key: string; kind: string; title: string; sub?: string | null; source?: string | null; chapter?: string | null; data: any; lines: HLine[]; frames: number};
type Cx = {name: string; poly: number[][]; c: [number, number]; ppy: number | null; built: number; walk: Record<string, {name: string; m: number; pts: number[]; end: [number, number]} | null>};
type DMap = {name: string; roads: [number, number[]][]; parks: number[][]; blocks: number[][]; stations: [string, number, number][]; cx: Cx[]};
export type H1Props = {fps: number; scenes: HScene[]; missing: number; maps: Record<string, DMap>; mapBox: [number, number]};
export const h1Frames = (p: H1Props) => p.scenes.reduce((a, s) => a + s.frames, 0);

const Maps = React.createContext<Record<string, DMap>>({});
const fade = (f: number, at: number, d = 10) => interpolate(f, [at, at + d], [0, 1], CL);
const ease = (f: number, a: number, d: number) => interpolate(f, [a, a + d], [0, 1], {...CL, easing: Easing.inOut(Easing.cubic)});
const COL: Record<string, string> = {ink: T.ink, accent: T.accent, fall: T.fall, ink2: T.ink2};
const Y0 = 340;  // 판 안 그림 맨 위(정확한 값 칩 아래)

// 줄 박자: k = 지금 말하는 줄, at(i) = i번째 줄 시작 프레임(장면 안). 줄 수보다 큰 박자 번호는 마지막 줄로 당긴다.
const useBeat = (s: HScene) => {
  const f = useCurrentFrame(); const st = tallyStarts(s.lines); const n = s.lines.length;
  const k = Math.max(0, tallyIdx(s.lines, f));
  const at = (i: number) => st[Math.max(0, Math.min(n - 1, i))] ?? 0;
  const clampI = (i: number) => Math.max(0, Math.min(n - 1, i));
  return {f, k, at, n, clampI, end: s.frames};
};

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
// 오른쪽 세로 카드 줄 — 지금 박자 카드만 검게(나머지는 흰 테두리). cards[i] = [이름, 큰 글자, 작은 글자]
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
// 같은 줄에 여러 카드가 걸리면 20프레임씩 늦게
const staggered = (lineOf: number[], at: (i: number) => number) => { const seen: Record<number, number> = {}; return lineOf.map((l) => { const j = seen[l] ?? 0; seen[l] = j + 1; return at(l) + 6 + j * 20; }); };
const activeOf = (shown: number[], f: number) => { let a = -1; shown.forEach((t, i) => { if (f >= t) a = i; }); return a; };

// ───────── 지도 ─────────
type VB = {cx: number; cy: number; w: number};
const MX = 130, MY = 318, MW = 1060, MH = 524;
const pathOf = (q: number[], close = false) => { let d = ''; for (let i = 0; i < q.length; i += 2) d += (i ? 'L' : 'M') + q[i] + ',' + q[i + 1]; return close ? d + 'Z' : d; };
const lerpVB = (a: VB, b: VB, t: number): VB => ({cx: a.cx + (b.cx - a.cx) * t, cy: a.cy + (b.cy - a.cy) * t, w: a.w * Math.pow(b.w / a.w, t)});
const RC: Record<string, string> = {station: T.accent, school: T.fall, mart: T.ink2};

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
const cxByName = (maps: Record<string, DMap>, n: string) => { for (const m of Object.values(maps)) { const c = m.cx.find((x) => x.name === n); if (c) return c; } return null; };

const MapView: React.FC<{vb: VB; focus: string[]; color: string; routes?: {name: string; kind: string; t: number}[]; home?: string | null; dongLabels?: boolean; labels?: string[]; w?: number; h?: number; x?: number; y?: number}> =
  ({vb, focus, color, routes = [], home, dongLabels, labels, w = MW, h = MH, x = MX, y = MY}) => {
  const maps = React.useContext(Maps);
  const vh = vb.w * h / w; const s = vb.w / w;
  const all = Object.values(maps).flatMap((m) => m.cx);
  const ppys = focus.map((n) => cxByName(maps, n)?.ppy).filter((v): v is number => !!v);
  const lo = Math.min(...ppys), hi = Math.max(...ppys);
  const fill = (c: Cx) => {
    const on = focus.includes(c.name);
    if (!on) return '#d5d9e0';
    if (routes.length) return T.soft;
    if (color === 'ppy' && c.ppy && hi > lo) { const t = (c.ppy - lo) / (hi - lo); const mix = (a: number, b: number) => Math.round(a + (b - a) * t); return `rgb(${mix(255, 255)},${mix(214, 90)},${mix(186, 0)})`; }
    return T.accent;
  };
  const lab = (px: number, py: number, text: string, size: number, col = T.ink) => (
    <text x={px} y={py} textAnchor="middle" style={{...F, fontWeight: 700}} fontSize={size * s} fill={col} stroke="#fbfbfc" strokeWidth={6 * s} paintOrder="stroke">{text}</text>
  );
  return (
    <div style={{position: 'absolute', left: x, top: y, width: w, height: h, borderRadius: 18, overflow: 'hidden', background: '#fbfbfc', border: `2px solid ${T.line}`}}>
      <svg width={w} height={h} viewBox={`${vb.cx - vb.w / 2} ${vb.cy - vh / 2} ${vb.w} ${vh}`} style={{display: 'block'}}>
        <MapBase />
        {all.map((c, i) => { const rt = routes.length > 0 && focus.includes(c.name); return <g key={i}>{c.poly.map((q, j) => <path key={j} d={pathOf(q, true)} fill={fill(c)} stroke={rt ? T.accent : '#fff'} strokeWidth={rt ? 3 : 1.5} vectorEffect="non-scaling-stroke" />)}</g>; })}
        {vb.w > 3000 ? null : Object.values(maps).flatMap((m) => m.stations).map(([n, sx, sy], i) => <circle key={'s' + i} cx={sx} cy={sy} r={8 * s} fill="#fff" stroke={T.accent} strokeWidth={3} vectorEffect="non-scaling-stroke" />)}
        {routes.map((r, i) => {
          const c = cxByName(maps, r.name); const wk = c?.walk?.[r.kind]; if (!wk || r.t <= 0) return null;
          const n = wk.pts.length / 2; const k = Math.max(2, Math.ceil(n * r.t));
          return <g key={'w' + i}>
            <path d={pathOf(wk.pts.slice(0, k * 2))} fill="none" stroke={RC[r.kind]} strokeWidth={6} strokeLinecap="round" strokeLinejoin="round" vectorEffect="non-scaling-stroke" />
            {r.t >= 1 ? <circle cx={wk.end[0]} cy={wk.end[1]} r={12 * s} fill={RC[r.kind]} stroke="#fff" strokeWidth={3} vectorEffect="non-scaling-stroke" /> : null}
          </g>;
        })}
        {dongLabels ? Object.values(maps).map((m, i) => {
          const xs = m.cx.map((c) => c.c[0]), ys = m.cx.map((c) => c.c[1]);
          return <g key={'d' + i}>{lab(xs.reduce((a, b) => a + b, 0) / xs.length + 900 * s, ys.reduce((a, b) => a + b, 0) / ys.length, m.name, 44, T.ink2)}</g>;
        }) : null}
        {(labels ?? focus).map((n, i) => { const c = cxByName(maps, n); return c ? <g key={'f' + i}>{lab(c.c[0], c.c[1] - (n === home ? 60 : 22) * s, n, 26)}</g> : null; })}
        {home ? (() => { const c = cxByName(maps, home); if (!c) return null; return <g>
          <path d={`M${c.c[0]},${c.c[1] + 4 * s} l${-16 * s},${-30 * s} a${18 * s},${18 * s} 0 1 1 ${32 * s},0 z`} fill={T.ink} />
          {lab(c.c[0], c.c[1] + 40 * s, '손품 씨네', 24, T.ink)}</g>; })() : null}
      </svg>
      <div style={{...F, position: 'absolute', right: 10, bottom: 6, fontWeight: 500, fontSize: 14, color: T.ink3}}>© OpenStreetMap contributors</div>
    </div>
  );
};

const MapScene: React.FC<{s: HScene}> = ({s}) => {
  const {f, k, at, n, clampI} = useBeat(s); const d = s.data;
  const views: VB[] = d.views;
  let vb = views[0];
  for (let i = 1; i < views.length; i++) { const a = at(i); if (f >= a && i < n) vb = lerpVB(vb, views[i], ease(f, a, 36)); }
  // 한 줄짜리 지도는 천천히 다가간다(같은 화면 8초 방지)
  if (views.length === 1) vb = {...vb, w: vb.w * interpolate(f, [0, s.frames], [1.08, 0.92], CL)};
  const routes = (d.routes ?? []).map(([name, kind]: [string, string], i: number) => ({name, kind, t: ease(f, at(clampI(i + (s.key === 'g_map' ? 1 : 0))) + 8, 40)}));
  const cards: string[][] = d.cards ?? [];
  const lineOf = cards.map((_, i) => {
    if (s.key === 'h_walk') return clampI([0, 1, 1, 2][i] ?? i);
    if (s.key === 'f_walk') return clampI([0, 1, 1][i] ?? i);
    return n === 1 ? 0 : clampI(i);
  });
  const shown = staggered(lineOf, at);
  return (
    <>
      <MapView vb={vb} focus={d.focus} color={d.color} routes={routes} home={d.home} dongLabels={d.dongLabels} labels={d.labels} />
      <SideCards cards={cards} shownAt={shown} active={activeOf(shown, f)} f={f} />
      {k < 0 ? null : null}
    </>
  );
};

// ───────── 거래 점 ─────────
const MONTHS = ['2025.11', '2025.12', '2026.01', '2026.02', '2026.03', '2026.04', '2026.05', '2026.06', '2026.07', '2026.08', '2026.09', '2026.10'];
const PX0 = 230, PX1 = 1150, PY0 = Y0 + 20, PY1 = 790;
const Dots: React.FC<{s: HScene}> = ({s}) => {
  const {f, k, at, n} = useBeat(s); const d = s.data;
  const dots: [string, number, number, number, number][] = d.dots;
  const lo = 18, hi = 33;
  const yv = (v: number) => PY1 - (v - lo) / (hi - lo) * (PY1 - PY0);
  const mw = (PX1 - PX0) / MONTHS.length;
  const tx = (ym: string, dd: number) => PX0 + (MONTHS.indexOf(ym) + 0.15 + 0.7 * dd / 31) * mw;
  const order = dots.map((x, i) => [x[2], i] as [number, number]).sort((a, b) => a[0] - b[0]);
  const rank: number[] = []; order.forEach(([, i], r) => { rank[i] = r; });
  const mode = d.mode as string;
  const appear = (i: number) => fade(f, 4 + (i / dots.length) * 30, 6);
  // 박자: sort 0=줄 세우기, 1=23.82억, 2=2월만, 3=나머지 3건 / feb 0=2월만+23.82, 1=나머지 / may 0=5월+20억, 1=직거래, 2=띠, 3=뜻, 4=한 달 전체
  const sorted = mode === 'sort' ? (k === 0 ? ease(f, at(0) + 10, 40) : 1 - ease(f, at(1), 30)) : 0;
  const focusM = mode === 'may' ? '2026.05' : (mode === 'feb' || (mode === 'sort' && k >= 2)) ? '2026.02' : null;
  const fo = mode === 'feb' ? fade(f, 40, 12) : mode === 'sort' ? fade(f, at(2), 12) : fade(f, 30, 12);
  const lowI = dots.findIndex((x) => x[0] === '2026.02' && x[3] === 9);
  const mayLowI = dots.findIndex((x) => x[0] === '2026.05' && x[4] === 1);
  const showLow = mode === 'feb' || (mode === 'sort' && k >= 1);
  const ticks = [20, 24, 28, 32];
  const feb = (d.feb ?? []) as {d: number; amt: number; floor: number; kind: string}[];
  const medY = yv(d.median ?? 28.5);
  return (
    <>
      <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
        {ticks.map((v) => <g key={v}><line x1={PX0} x2={PX1} y1={yv(v)} y2={yv(v)} stroke={T.line} strokeWidth={2} />
          <text x={PX0 - 16} y={yv(v) + 8} textAnchor="end" style={{...F, fontWeight: 500}} fontSize={24} fill={T.ink3}>{v}억</text></g>)}
        {sorted > 0.02 ? null : MONTHS.map((m, i) => (i % 2 === 0 || m === focusM) ? <text key={m} x={PX0 + (i + 0.5) * mw} y={PY1 + 36} textAnchor="middle" style={{...F, fontWeight: m === focusM ? 700 : 500}} fontSize={22} fill={m === focusM ? T.ink : T.ink3}>{m.slice(2)}</text> : null)}
        {focusM ? <rect x={PX0 + MONTHS.indexOf(focusM) * mw} y={PY0 - 10} width={mw} height={PY1 - PY0 + 10} fill={T.soft} opacity={fo * 0.7} /> : null}
        {mode === 'may' && k >= 2 ? <rect x={PX0 + MONTHS.indexOf('2026.05') * mw - 6} y={yv(30.5) - 8} width={mw + 12} height={yv(27) - yv(30.5) + 16} rx={10} fill="none" stroke={T.ink} strokeWidth={4} opacity={fade(f, at(2), 8)} /> : null}
        {mode === 'may' && k >= 4 ? <rect x={PX0 + MONTHS.indexOf('2026.05') * mw - 14} y={PY0 - 4} width={mw + 28} height={PY1 - PY0} rx={14} fill="none" stroke={T.accent} strokeWidth={6} opacity={fade(f, at(4), 8)} /> : null}
        {mode === 'sort' && k === 0 ? <line x1={PX0} x2={PX1} y1={medY} y2={medY} stroke={T.accent} strokeWidth={3} strokeDasharray="10 8" opacity={ease(f, at(0) + 40, 15)} /> : null}
        {dots.map((x, i) => {
          const cx = tx(x[0], x[1]) * (1 - sorted) + (PX0 + 20 + rank[i] / (dots.length - 1) * (PX1 - PX0 - 40)) * sorted;
          const inF = focusM ? x[0] === focusM : true;
          const isLow = (showLow && i === lowI) || (mode === 'may' && i === mayLowI);
          const isMed = mode === 'sort' && k === 0 && rank[i] === Math.floor(dots.length / 2);
          const op = appear(i) * (inF || isLow ? 1 : 1 - 0.75 * fo);
          if (x[4] && !isLow) return <circle key={i} cx={cx} cy={yv(x[2] / 10000)} r={8} fill="#fff" stroke={T.ink3} strokeWidth={3} opacity={op} />;
          return <circle key={i} cx={cx} cy={yv(x[2] / 10000)} r={isLow || isMed ? 14 : 8} fill={isLow || isMed ? T.accent : inF && focusM ? T.ink : '#a9afb9'} stroke="#fff" strokeWidth={2} opacity={op} />;
        })}
        {showLow && lowI >= 0 ? <text x={tx('2026.02', 12) + 24} y={yv(23.82) + 9} style={{...F, fontWeight: 700}} fontSize={30} fill={T.accent} opacity={fade(f, mode === 'sort' ? at(1) + 10 : 50)} stroke="#fff" strokeWidth={6} paintOrder="stroke">23.82억</text> : null}
        {mode === 'sort' && k === 0 ? <text x={PX0 + 10} y={medY - 16} style={{...F, fontWeight: 700}} fontSize={28} fill={T.accent} opacity={ease(f, at(0) + 50, 15)} stroke="#fff" strokeWidth={6} paintOrder="stroke">가운데 값 28.50억 — 85건 중 43번째</text> : null}
        {mode === 'may' && mayLowI >= 0 ? <text x={tx('2026.05', 28) + 26} y={yv(20) + 9} style={{...F, fontWeight: 700}} fontSize={30} fill={T.accent} opacity={fade(f, 40)} stroke="#fff" strokeWidth={6} paintOrder="stroke">20.00억</text> : null}
        {mode === 'sort' && k === 0 ? <text x={PX0} y={PY1 + 36} style={{...F, fontWeight: 700}} fontSize={22} fill={T.ink2} opacity={ease(f, at(0) + 10, 20)}>싼 거래 ←  값 순서로 줄 세움  → 비싼 거래</text> : null}
      </svg>
      {/* 오른쪽 칸 */}
      {(mode === 'feb' || (mode === 'sort' && k >= 2)) ? (
        <div style={{position: 'absolute', left: 1215, top: Y0, width: 570, opacity: fade(f, mode === 'feb' ? 40 : at(2))}}>
          <div style={{...F, fontWeight: 700, fontSize: 26, color: T.ink2, marginBottom: 8}}>2026년 2월 · 84㎡대 4건</div>
          {[...feb].sort((a, b) => a.amt - b.amt).map((x, i) => {
            const hot = i === 0; const other = !hot && ((mode === 'feb' && k >= 1) || (mode === 'sort' && k >= 3));
            return <div key={i} style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', height: 74, padding: '0 22px', marginBottom: 8, borderRadius: 14,
              background: other ? T.ink : hot ? T.soft : '#fff', border: `2px solid ${hot ? T.accent : T.line}`}}>
              <span style={{...F, fontWeight: 700, fontSize: 26, color: other ? T.dink3 : T.ink2}}>{x.d}일 · {x.floor}층</span>
              <span style={{...F, fontWeight: 700, fontSize: 38, color: hot ? T.accent : other ? '#fff' : T.ink}}>{x.amt.toFixed(2)}억</span>
            </div>;
          })}
          <div style={{...F, fontWeight: 700, fontSize: 28, color: T.ink, marginTop: 10}}>{d.gap}</div>
        </div>
      ) : null}
      {mode === 'sort' && k === 1 ? <DarkCard f={f} x={1215} y={Y0 + 40} w={570} at={at(1)} big="23억대 거래 한 건" small="1년 85건 중 23억대 이하는 2건" /> : null}
      {mode === 'sort' && k === 0 ? <DarkCard f={f} x={1215} y={Y0 + 40} w={570} at={at(0) + 50} big="가운데 값" small="값 순서로 줄 세워 한가운데 오는 값" bg={T.accent} /> : null}
      {mode === 'may' ? (
        <div style={{position: 'absolute', left: 1215, top: Y0, width: 570}}>
          {k <= 1 ? <DarkCard f={f} x={0} y={0} w={570} at={k === 0 ? 30 : at(1)} big={k === 0 ? '28일 · 26층 · 20.00억' : '거래 유형: 직거래'} small={k === 0 ? '5월 거래 18건 중 하나' : '같은 달 다른 17건은 모두 중개거래'} bg={k === 0 ? T.accent : T.ink} size={40} /> : null}
          {k === 2 ? <DarkCard f={f} x={0} y={0} w={570} at={at(2)} big="나머지 17건" small={d.band} size={44} /> : null}
          {k === 3 ? <DarkCard f={f} x={0} y={0} w={570} at={at(3)} big={d.def[0]} small={d.def[1]} size={52} /> : null}
          {k >= 4 ? <DarkCard f={f} x={0} y={0} w={570} at={at(4)} big="한 건 대신 한 달 전체" small="2026년 5월 18건을 같이 본다" bg={T.accent} size={44} /> : null}
        </div>
      ) : null}
      {n < 0 ? null : null}
    </>
  );
};

// ───────── 짝 막대(세로) ─────────
const PairBars: React.FC<{s: HScene}> = ({s}) => {
  const {f, at} = useBeat(s); const d = s.data;
  const bars: [string, number, string, string, string][] = d.bars;
  const BX = 900, BW = 240, GAP = 160, BY = 750, BH = 330;
  return (
    <>
      {bars.map((b, i) => {
        const g = ease(f, 6 + i * 10, 30); const h = BH * b[1] / d.max * g; const x = BX + i * (BW + GAP);
        return <React.Fragment key={i}>
          <div style={{position: 'absolute', left: x, top: BY - h, width: BW, height: h, background: COL[b[4]] ?? T.ink2, borderRadius: '14px 14px 0 0'}} />
          <div style={{...F, position: 'absolute', left: x - 60, width: BW + 120, top: BY - h - 56, textAlign: 'center', fontWeight: 700, fontSize: 38, color: b[4] === 'accent' ? T.accent : T.ink, opacity: g}}>{b[2]}</div>
          <div style={{...F, position: 'absolute', left: x - 80, width: BW + 160, top: BY + 8, textAlign: 'center', fontWeight: 700, fontSize: 28, color: T.ink, whiteSpace: 'nowrap'}}>{b[0]}</div>
          <div style={{...F, position: 'absolute', left: x - 80, width: BW + 160, top: BY + 44, textAlign: 'center', fontWeight: 500, fontSize: 22, color: T.ink3, whiteSpace: 'nowrap'}}>{b[3]}</div>
        </React.Fragment>;
      })}
      <DarkCard f={f} x={160} y={Y0 + 60} w={600} at={at(0) + 45} big={d.diff} small={d.note} bg={T.accent} size={72} />
    </>
  );
};

// ───────── 기간 막대(겹치지 않는 세 구간) ─────────
const Period: React.FC<{s: HScene}> = ({s}) => {
  const {f, k, at, n} = useBeat(s); const d = s.data;
  const bars: [string, number, string, string][] = d.bars;
  const BX = 860, BW = 230, GAP = 70, BY = 790, BH = 380, mx = Math.max(...bars.map((b) => b[1]));
  return (
    <>
      {bars.map((b, i) => {
        const g = ease(f, 6 + i * 8, 26); const h = Math.max(6, BH * b[1] / mx * g); const x = BX + i * (BW + GAP);
        const hot = i === d.hot; const ring = n > 1 && k === 1 && i === 0;
        return <React.Fragment key={i}>
          <div style={{position: 'absolute', left: x, top: BY - h, width: BW, height: h, background: hot ? T.accent : ring ? T.ink : '#c4c9d2', borderRadius: '12px 12px 0 0'}} />
          <div style={{...F, position: 'absolute', left: x, width: BW, top: BY - h - 54, textAlign: 'center', fontWeight: 700, fontSize: 40, color: hot ? T.accent : T.ink}}>{b[2]}</div>
          <div style={{...F, position: 'absolute', left: x - 30, width: BW + 60, top: BY + 8, textAlign: 'center', fontWeight: 700, fontSize: 24, color: T.ink, whiteSpace: 'nowrap'}}>{b[0]}</div>
          <div style={{...F, position: 'absolute', left: x - 30, width: BW + 60, top: BY + 38, textAlign: 'center', fontWeight: 500, fontSize: 22, color: T.ink3}}>{b[3]}</div>
        </React.Fragment>;
      })}
      {k === 0 || n === 1 ? <DarkCard f={f} x={160} y={Y0 + 40} w={620} at={30} big={d.pct} small={d.sub84} bg={T.accent} size={52} /> : null}
      {n > 1 && k === 1 ? <DarkCard f={f} x={160} y={Y0 + 40} w={620} at={at(1)} big="그 앞 다섯 달은 1건" small="2025.11~2026.03 · 모든 평형" size={52} /> : null}
      {n > 1 && k >= 2 ? <DarkCard f={f} x={160} y={Y0 + 40} w={620} at={at(2)} big={d.why} small="이유는 짐작하지 않는다" size={46} /> : null}
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
  const {f, k, at, n} = useBeat(s); const d = s.data;
  const RX = 650, RW = 1130;
  const chip = (t: string, i: number, a: number, dark = true) => <div key={t} style={{...F, display: 'inline-block', marginRight: 18, marginBottom: 18, fontWeight: 700, fontSize: 44, color: dark ? '#fff' : T.ink,
    background: dark ? T.ink : '#fff', border: dark ? 'none' : `2px solid ${T.line}`, borderRadius: 16, padding: '18px 30px', opacity: fade(f, a + i * 12, 8)}}>{t}</div>;
  let body: React.ReactNode = null;
  if (d.teaser) {
    body = <div style={{position: 'absolute', left: RX, top: Y0 + 30, width: RW}}>
      {d.promise.map((t: string, i: number) => <div key={t} style={{...F, fontWeight: 700, fontSize: 60, color: i ? T.accent : T.ink, opacity: fade(f, 20 + i * Math.max(30, s.frames * 0.4), 10), marginBottom: 30}}>{i ? '→ ' : ''}{t}</div>)}
    </div>;
  } else {
    const b = Math.min(k, 5);
    if (b === 0) body = <DarkCard f={f} x={RX} y={Y0 + 30} w={RW} at={20} big="실제 인물이 아니라" small="계산을 위해 만든 가상 인물" size={64} />;
    if (b === 1) body = <div style={{position: 'absolute', left: RX, top: Y0 + 30, width: RW}}>{d.tags.map((t: string, i: number) => chip(t, i, at(1)))}</div>;
    if (b === 2) body = <DarkCard f={f} x={RX} y={Y0 + 30} w={RW} at={at(2)} big={d.home[1]} small={d.home[0]} size={56} />;
    if (b === 3) body = <DarkCard f={f} x={RX} y={Y0 + 30} w={RW} at={at(3)} big={`${d.deposit[0]} ${d.deposit[1]}`} small={d.deposit[2]} bg={T.accent} size={72} />;
    if (b === 4) body = <div style={{position: 'absolute', left: RX, top: Y0 + 30, width: RW}}>{d.dongs.map((t: string, i: number) => chip(t, i, at(4)))}</div>;
    if (b === 5) {
      const len = (s.lines[5]?.frames ?? 90);
      body = <div style={{position: 'absolute', left: RX, top: Y0 + 10, width: RW}}>
        <div style={{...F, fontWeight: 700, fontSize: 30, color: T.ink2, marginBottom: 14}}>손품 씨의 기준 세 가지</div>
        {d.rules.map((t: string, i: number) => <div key={t} style={{...F, fontWeight: 700, fontSize: 46, color: '#fff', background: i === Math.min(2, Math.floor((f - at(5)) / (len / 3))) ? T.accent : T.ink, borderRadius: 16, padding: '16px 28px', marginBottom: 14,
          opacity: fade(f, at(5) + i * len / 3, 8)}}>{i + 1}. {t}</div>)}
      </div>;
    }
  }
  return <><PersonCard f={f} dday={d.dday} />{body}{n < 0 ? null : null}</>;
};

// ───────── 결론 ─────────
const Concl: React.FC<{s: HScene}> = ({s}) => {
  const f = useCurrentFrame(); const rows: string[] = s.data.rows; const step = Math.max(24, (s.frames - 30) / rows.length);
  return (
    <div style={{position: 'absolute', left: 160, top: Y0 + 20, width: 1600}}>
      {rows.map((t, i) => {
        const a = 8 + i * step; const on = f >= a && (i === rows.length - 1 || f < a + step);
        return <div key={i} style={{display: 'flex', alignItems: 'center', gap: 28, height: 140, marginBottom: 16, borderRadius: 20, padding: '0 36px', opacity: fade(f, a, 8),
          background: on ? T.ink : '#fff', border: on ? 'none' : `2px solid ${T.line}`}}>
          <div style={{...F, fontWeight: 700, fontSize: 64, color: T.accent, width: 60}}>{i + 1}</div>
          <div style={{...F, fontWeight: 700, fontSize: 56, color: on ? '#fff' : T.ink, whiteSpace: 'nowrap'}}>{t}</div>
        </div>;
      })}
    </div>
  );
};

// ───────── 자료 칸(동별 건수 · 걷는 길 · 84㎡) ─────────
const Tiles: React.FC<{s: HScene}> = ({s}) => {
  const {f, k, at} = useBeat(s); const d = s.data;
  if (k <= 0) return (
    <div style={{position: 'absolute', left: 160, top: Y0 + 20, width: 1600}}>
      <div style={{...F, fontWeight: 700, fontSize: 30, color: T.ink2, marginBottom: 20}}>{d.tilesHead}</div>
      <div style={{display: 'flex', gap: 30}}>
        {d.tiles.map(([a, b]: string[], i: number) => <div key={a} style={{flex: 1, height: 300, background: T.ink, borderRadius: 22, padding: '40px 40px', boxSizing: 'border-box', opacity: fade(f, 10 + i * 14, 8)}}>
          <div style={{...F, fontWeight: 700, fontSize: 44, color: T.dink3}}>{a}</div>
          <div style={{...F, fontWeight: 700, fontSize: 110, color: '#fff', letterSpacing: -2}}>{b}</div>
        </div>)}
      </div>
    </div>
  );
  if (k === 1) {
    const w = d.walk; const t = ease(f, at(1) + 10, 50);
    return <>
      <MapView vb={w.views[0]} focus={w.focus} color="focus" routes={[{name: w.routes[0][0], kind: w.routes[0][1], t}]} x={MX} y={MY} />
      <DarkCard f={f} x={1215} y={Y0 + 20} w={570} at={at(1) + 20} big={d.walkNote[0]} small={d.walkNote[1]} size={50} />
    </>;
  }
  return <DarkCard f={f} x={160} y={Y0 + 40} w={1600} at={at(2)} big={d.size[0]} small={d.size[1]} bg={T.accent} size={150} />;
};

// ───────── 거래 카드 ─────────
const Deal: React.FC<{s: HScene}> = ({s}) => {
  const {f, k, at, n} = useBeat(s); const d = s.data;
  const cards: [string, string][][] = d.cards;
  const W = cards.length > 1 ? 760 : 900; const X0 = cards.length > 1 ? 150 : 510;
  return (
    <>
      {cards.map((rows, ci) => {
        const a = n > 1 ? at(Math.min(ci, n - 1)) : ci * 20; const o = fade(f, a, 10);
        const rh = 86;
        return <div key={ci} style={{position: 'absolute', left: X0 + ci * (W + 50), top: Y0 + (1 - o) * 20, width: W, opacity: o, background: '#fff', borderRadius: 18, border: `3px solid ${T.ink}`, padding: '10px 30px', boxSizing: 'border-box'}}>
          {rows.map(([l, v], ri) => {
            const hot = (d.hot[ci] ?? []).includes(ri) && f >= a + 24 + ri * 6;
            return <div key={ri} style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', height: rh, borderBottom: ri < rows.length - 1 ? `2px dashed ${T.line}` : 'none'}}>
              <span style={{...F, fontWeight: 700, fontSize: 30, color: T.ink3}}>{l}</span>
              <span style={{...F, fontWeight: 700, fontSize: v.length > 8 ? 38 : 46, color: hot ? '#fff' : T.ink, background: hot ? (v.includes('직거래') || ri === 2 && ci === 0 && cards.length === 1 ? T.accent : T.ink) : 'transparent', borderRadius: 10, padding: '2px 14px'}}>{v}</span>
            </div>;
          })}
        </div>;
      })}
      {k < 0 ? null : null}
    </>
  );
};

// ───────── 층 그림 ─────────
const Floors: React.FC<{s: HScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const deals: [number, string, string][] = d.deals;
  const top = d.top as number; const BX = 360, BW = 200, BT = Y0 + 10, BB = 830; const fy = (fl: number) => BB - (fl - 0.5) / top * (BB - BT);
  const sorted = [...deals].sort((a, b) => a[0] - b[0]);
  return (
    <>
      <div style={{position: 'absolute', left: BX, top: BT, width: BW, height: BB - BT, background: '#eef0f3', border: `3px solid ${T.ink2}`, borderRadius: '10px 10px 0 0'}}>
        {Array.from({length: top}).map((_, i) => <div key={i} style={{position: 'absolute', left: 10, right: 10, top: (BB - BT) - (i + 1) * (BB - BT) / top + 3, height: (BB - BT) / top - 6, background: '#fff', borderRadius: 2}} />)}
      </div>
      {sorted.map(([fl, amt, day], i) => {
        const y = fy(fl); const a = 10 + i * 18; const low = i === 0;
        return <React.Fragment key={i}>
          <div style={{position: 'absolute', left: BX - 8, top: y - 8, width: BW + 16, height: 16, background: low ? T.accent : T.ink, borderRadius: 6, opacity: fade(f, a)}} />
          <div style={{position: 'absolute', left: BX + BW + 16, top: y - 2, width: 120, borderTop: `3px solid ${low ? T.accent : T.ink}`, opacity: fade(f, a)}} />
          <div style={{...F, position: 'absolute', left: BX + BW + 150, top: y - 26, fontWeight: 700, fontSize: 40, color: low ? T.accent : T.ink, opacity: fade(f, a), whiteSpace: 'nowrap'}}>{fl}층 · {amt} <span style={{fontSize: 26, color: T.ink3}}>({day})</span></div>
        </React.Fragment>;
      })}
      <DarkCard f={f} x={1150} y={Y0 + 120} w={620} at={Math.max(60, s.frames * 0.45)} big={d.why[0]} small={d.why[1]} size={46} />
    </>
  );
};

// ───────── 선(달별 가운데 값) ─────────
const LX0 = 230, LX1 = 1130, LY0 = Y0 + 30, LY1 = 780;
const Lines: React.FC<{s: HScene}> = ({s}) => {
  const {f, k, at} = useBeat(s); const d = s.data;
  const series: [string, string, [string, number, number][]][] = d.series;
  const mw = (LX1 - LX0) / (MONTHS.length - 1);
  const xm = (ym: string) => LX0 + MONTHS.indexOf(ym) * mw; const yv = (v: number) => LY1 - (v - d.min) / (d.max - d.min) * (LY1 - LY0);
  const ticks: number[] = []; for (let v = Math.ceil(d.min / 2) * 2; v <= d.max; v += 2) ticks.push(v);
  const draw = ease(f, 8, 50);
  const one = series.length === 1;
  const lowOf = (pts: [string, number, number][]) => pts.filter((p) => p[0] === '2026.04')[0];
  const bandOn = d.band ? fade(f, at(Math.min(1, s.lines.length - 1)) + (s.lines.length > 1 ? 0 : 50), 10) : 0;
  return (
    <>
      <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
        {d.band ? <rect x={xm(d.band[0]) - mw / 2} y={LY0 - 10} width={mw * 2} height={LY1 - LY0 + 10} fill={T.soft} opacity={bandOn} /> : null}
        {ticks.map((v) => <g key={v}><line x1={LX0} x2={LX1} y1={yv(v)} y2={yv(v)} stroke={T.line} strokeWidth={2} />
          <text x={LX0 - 16} y={yv(v) + 8} textAnchor="end" style={{...F, fontWeight: 500}} fontSize={22} fill={T.ink3}>{v}억</text></g>)}
        {MONTHS.map((m, i) => i % 2 === 0 ? <text key={m} x={xm(m)} y={LY1 + 36} textAnchor="middle" style={{...F, fontWeight: 500}} fontSize={22} fill={T.ink3}>{m.slice(2)}</text> : null)}
        {series.map(([name, col, pts], si) => {
          const xy = pts.map((p) => [xm(p[0]), yv(p[1])]); const nn = Math.max(1, Math.ceil(xy.length * draw));
          return <g key={si}>
            <polyline points={xy.slice(0, nn).map((q) => q.join(',')).join(' ')} fill="none" stroke={COL[col]} strokeWidth={6} strokeLinejoin="round" strokeLinecap="round" />
            {xy.slice(0, nn).map((q, i) => <circle key={i} cx={q[0]} cy={q[1]} r={pts[i][0] === '2026.04' && (k >= 1 || one) ? 13 : 8} fill={pts[i][0] === '2026.04' && (k >= 1 || one) ? T.accent : COL[col]} stroke="#fff" strokeWidth={3} />)}
          </g>;
        })}
      </svg>
      {one ? (() => { const pts = series[0][2]; const lo = lowOf(pts); const last = pts[pts.length - 1]; const first = pts[0]; return (
        <SideCards f={f} cards={[[`${first[0]} (${first[2]}건)`, `${first[1].toFixed(2)}억`, ''], [`${lo[0]} · 가장 낮은 달 (${lo[2]}건)`, `${lo[1].toFixed(2)}억`, '봄에 내려갔다가'], [`${last[0]} (${last[2]}건)`, `${last[1].toFixed(2)}억`, '여름 지나 다시 올라옴']]}
          shownAt={[20, 50, 80]} active={activeOf([20, 50, 80], f)} />); })() : (
        <SideCards f={f} cards={series.map(([name, col, pts]) => { const lo = lowOf(pts); return [name, `4월 ${lo[1].toFixed(2)}억`, `${lo[2]}건 · 1년 중 낮은 쪽`]; })}
          shownAt={series.map((_, i) => (k >= 1 ? at(1) : 30) + i * 20)} active={k >= 1 ? 2 : -1} />
      )}
      {!one ? <div style={{display: 'flex', gap: 26, position: 'absolute', left: LX0, top: Y0 - 2}}>{series.map(([name, col]) => <span key={name} style={{...F, fontWeight: 700, fontSize: 22, color: COL[col]}}>━ {name}</span>)}</div> : null}
    </>
  );
};

// ───────── 달력 칸(달마다 건수) ─────────
const Cal: React.FC<{s: HScene}> = ({s}) => {
  const f = useCurrentFrame(); const cells: [string, number][] = s.data.cells; const mx = Math.max(...cells.map((c) => c[1]));
  const CW = 124, CH = 180, X = 170, Y = Y0 + 60;
  return (
    <>
      {cells.map(([m, v], i) => {
        const a = 6 + i * 6; const t = v / mx; const col = v === 0 ? '#eef0f3' : `rgb(255,${Math.round(227 - 137 * t)},${Math.round(209 - 209 * t)})`;
        return <div key={m} style={{position: 'absolute', left: X + i * (CW + 8), top: Y, width: CW, height: CH, background: col, borderRadius: 14, opacity: fade(f, a, 8)}}>
          <div style={{...F, position: 'absolute', top: 14, left: 0, right: 0, textAlign: 'center', fontWeight: 700, fontSize: 22, color: t > 0.5 ? '#fff' : T.ink2}}>{m.slice(2)}</div>
          <div style={{...F, position: 'absolute', top: 70, left: 0, right: 0, textAlign: 'center', fontWeight: 700, fontSize: 56, color: t > 0.5 ? '#fff' : v ? T.ink : T.ink3}}>{v}</div>
        </div>;
      })}
      <div style={{...F, position: 'absolute', left: X, top: Y + CH + 20, fontWeight: 500, fontSize: 24, color: T.ink3}}>칸 안 숫자 = 그달 계약 건수 · 진할수록 많음</div>
      <DarkCard f={f} x={X} y={Y + CH + 80} w={720} at={Math.max(50, s.frames * 0.4)} big={s.data.note} bg={T.accent} size={52} />
    </>
  );
};

// ───────── 전세 ─────────
const Rent: React.FC<{s: HScene}> = ({s}) => {
  const {f, k, at} = useBeat(s); const d = s.data;
  const b = Math.min(k, 3);
  const hbars = (rows: [string, number, string, string?][], max: number, a: number, unit: string) => (
    <div style={{position: 'absolute', left: 650, top: Y0 + 20, width: 1130}}>
      {rows.map((r, i) => { const g = ease(f, a + i * 10, 26); const hot = i === 0; return (
        <div key={i} style={{marginBottom: 26}}>
          <div style={{...F, fontWeight: 700, fontSize: 30, color: T.ink, marginBottom: 6}}>{r[0]} <span style={{fontSize: 22, color: T.ink3}}>{r[3] ?? ''}</span></div>
          <div style={{display: 'flex', alignItems: 'center', gap: 18}}>
            <div style={{width: 820 * r[1] / max * g, height: 54, borderRadius: 10, background: hot ? T.accent : '#c4c9d2'}} />
            <span style={{...F, fontWeight: 700, fontSize: 40, color: hot ? T.accent : T.ink, opacity: g}}>{r[2]}{unit}</span>
          </div>
        </div>); })}
    </div>
  );
  return (
    <>
      <PersonCard f={f} dday="전세 칸부터 봤다" />
      {b === 0 ? <DarkCard f={f} x={650} y={Y0 + 40} w={1130} at={20} big="매매보다 전세" small="손품 씨는 지금 전세로 산다" size={64} /> : null}
      {b === 1 ? hbars(d.bars.map((x: any[]) => [x[0], x[1], x[2], x[3]]), d.max, at(1), '') : null}
      {b === 2 ? <>{hbars(d.ratio.map((x: any[]) => [x[0], x[1], `${x[1]}`]), 60, at(2), '%')}<div style={{...F, position: 'absolute', left: 650, top: 800, fontWeight: 500, fontSize: 22, color: T.ink3}}>{d.ratioHead}</div></> : null}
      {b === 3 ? <DarkCard f={f} x={650} y={Y0 + 40} w={1130} at={at(3)} big={d.say[0]} small={d.say[1]} bg={T.accent} size={64} /> : null}
    </>
  );
};

// ───────── 걸음 거리 자 ─────────
const Walk: React.FC<{s: HScene}> = ({s}) => {
  const {f, k, at, n} = useBeat(s); const d = s.data;
  const groups: [string, [string, number, string, string][]][] = d.groups;
  const X = 560, W = 1000;
  const gAt = (gi: number) => n === 1 ? 6 : at(Math.min(n - 1, gi * 2));
  return (
    <>
      {groups.map(([head, rows], gi) => {
        const a = gAt(gi); if (f < a) return null; const top = Y0 + 10 + gi * 230;
        const flip = gi === 1 && k >= 3;
        return <div key={gi} style={{position: 'absolute', left: 150, top, width: 1630, opacity: fade(f, a)}}>
          <div style={{...F, fontWeight: 700, fontSize: 28, color: T.ink2, marginBottom: 10}}>{head}</div>
          {rows.map(([name, m, txt, col], i) => { const g = ease(f, a + 6 + i * 12, 30); const hot = col === 'accent' && (gi === 0 || flip || n === 1); return (
            <div key={i} style={{display: 'flex', alignItems: 'center', height: 80}}>
              <div style={{...F, width: X - 150, fontWeight: 700, fontSize: 30, color: T.ink, whiteSpace: 'nowrap'}}>{name}</div>
              <div style={{position: 'relative', width: W * m / d.max * g, height: 36, borderRadius: 18, background: hot ? T.accent : '#c4c9d2'}}>
                {Array.from({length: Math.floor(m / 100)}).map((_, j) => <div key={j} style={{position: 'absolute', left: (j + 0.5) * W * 100 / d.max - 5, top: 13, width: 10, height: 10, borderRadius: 5, background: '#fff', opacity: 0.7}} />)}
              </div>
              <span style={{...F, fontWeight: 700, fontSize: 40, color: hot ? T.accent : T.ink, marginLeft: 18, opacity: g}}>{txt}</span>
            </div>); })}
        </div>;
      })}
      {n === 1 ? <DarkCard f={f} x={150} y={640} w={760} at={50} big={d.note} small="같은 동네 안에서 세 배 넘게" bg={T.ink} size={48} /> : null}
      {n > 1 && k === 1 ? <DarkCard f={f} x={1230} y={Y0 + 10} w={550} at={at(1)} big="600m − 390m = 210m" small="손품 씨네보다 200m쯤 덜 걷는다" size={48} /> : null}
      {n > 1 && k >= 3 ? <DarkCard f={f} x={1230} y={Y0 + 10} w={550} at={at(3)} big="마트는 손품 씨네가 더 가까움" small="960m vs 1,170m" bg={T.accent} size={40} /> : null}
    </>
  );
};

// ───────── 비교 카드 ─────────
const Cards: React.FC<{s: HScene}> = ({s}) => {
  const {f, k, at, n} = useBeat(s); const cards: [string, [string, string][]][] = s.data.cards;
  return (
    <>
      {cards.map(([name, rows], ci) => (
        <div key={ci} style={{position: 'absolute', left: 150 + ci * 830, top: Y0, width: 790, background: '#fff', border: `2px solid ${T.line}`, borderRadius: 20, padding: '16px 34px', boxSizing: 'border-box', opacity: fade(f, 6 + ci * 14)}}>
          <div style={{...F, fontWeight: 700, fontSize: 40, color: T.ink, marginBottom: 6}}>{name}</div>
          {rows.map(([l, v], ri) => { const hot = (n > 1 && k >= 1 && ri < 2) || (n === 1 && ri < 2 && f > s.frames * 0.5); return (
            <div key={ri} style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', height: 92, padding: '0 18px', borderRadius: 12, marginTop: 6, background: hot ? T.ink : ri === 2 && k === 0 ? T.soft : 'transparent'}}>
              <span style={{...F, fontWeight: 700, fontSize: 30, color: hot ? T.dink3 : T.ink3}}>{l}</span>
              <span style={{...F, fontWeight: 700, fontSize: 48, color: hot ? '#fff' : T.ink}}>{v}</span>
            </div>); })}
        </div>
      ))}
      {at(0) < 0 ? null : null}
    </>
  );
};

// ───────── 차이 막대(왼쪽으로) ─────────
const Diff: React.FC<{s: HScene}> = ({s}) => {
  const {f, k, at, n} = useBeat(s); const d = s.data; const rows: [string, string, number, string, string][] = d.rows;
  const Z = 1700, W = 820;
  return (
    <>
      <div style={{position: 'absolute', left: Z, top: Y0, height: 470, borderLeft: `3px solid ${T.ink}`}} />
      <div style={{...F, position: 'absolute', left: Z - 160, top: Y0 + 474, width: 200, textAlign: 'right', fontWeight: 500, fontSize: 22, color: T.ink3}}>새 단지 기준</div>
      {rows.map(([dong, pair, v, txt, note], i) => {
        const a = 8 + i * 16; const g = ease(f, a, 28); const w = W * Math.abs(v) / Math.abs(d.min) * g; const top = Y0 + 10 + i * 150;
        const weak = !!note;
        return <React.Fragment key={i}>
          <div style={{...F, position: 'absolute', left: 150, top: top + 4, fontWeight: 700, fontSize: 36, color: T.ink, opacity: fade(f, a)}}>{dong}</div>
          <div style={{...F, position: 'absolute', left: 150, top: top + 52, fontWeight: 500, fontSize: 22, color: T.ink3, opacity: fade(f, a), whiteSpace: 'nowrap'}}>{pair}{note ? ` · ${note}` : ''}</div>
          <div style={{position: 'absolute', left: Z - w, top: top + 10, width: w, height: 70, borderRadius: '12px 0 0 12px', background: weak ? '#fff' : T.fall, border: weak ? `3px dashed ${T.fall}` : 'none', boxSizing: 'border-box'}} />
          <div style={{...F, position: 'absolute', left: Z - w - 170, width: 160, textAlign: 'right', top: top + 20, fontWeight: 700, fontSize: 40, color: T.fall, opacity: g}}>{txt}</div>
        </React.Fragment>;
      })}
      {(n > 1 && k >= 1) || (n === 1 && f > s.frames * 0.5) ? <DarkCard f={f} x={540} y={Y0} w={400} at={n > 1 ? at(1) : s.frames * 0.5} big="25% 넘게 벌어짐" small="84㎡대 평당, 세 동네 모두" bg={T.accent} size={36} /> : null}
    </>
  );
};

// ───────── 동별 작은 막대 셋 ─────────
const Vol: React.FC<{s: HScene}> = ({s}) => {
  const {f, k, at} = useBeat(s); const d = s.data; const dongs: [string, [string, number][], string][] = d.dongs;
  const mx = Math.max(...dongs.flatMap((x) => x[1].map((m) => m[1])));
  const PW = 500, PH = 230, BY = Y0 + 300;
  return (
    <>
      {dongs.map(([name, months, tot], di) => {
        const x0 = 150 + di * (PW + 40); const bw = PW / months.length - 6;
        return <div key={di} style={{position: 'absolute', left: x0, top: Y0, width: PW, opacity: fade(f, 6 + di * 10)}}>
          <div style={{...F, fontWeight: 700, fontSize: 32, color: T.ink}}>{name}</div>
          <div style={{...F, fontWeight: 700, fontSize: 22, color: T.accent}}>{tot}</div>
          {months.map(([m, v], i) => { const h = PH * v / mx * ease(f, 10 + di * 10 + i * 2, 20); const hot = /\.0[45]$/.test(m); return (
            <div key={m} style={{position: 'absolute', left: i * (bw + 6), top: 300 - h, width: bw, height: h, background: hot ? T.accent : (k >= 2 && /\.(0[7-9]|10)$/.test(m)) ? T.ink : '#c4c9d2', borderRadius: '6px 6px 0 0'}} />); })}
          <div style={{...F, position: 'absolute', left: 0, top: 308, fontWeight: 500, fontSize: 20, color: T.ink3}}>{months[0][0].slice(2)}</div>
          <div style={{...F, position: 'absolute', right: 0, top: 308, fontWeight: 500, fontSize: 20, color: T.ink3}}>{months[months.length - 1][0].slice(2)}</div>
        </div>;
      })}
      {k === 1 ? <DarkCard f={f} x={150} y={BY + 50} w={1000} at={at(1)} big="여름엔 가운데 값이 다시 올라감" small="대표 단지마다 거래 많은 평형 기준" size={42} /> : null}
      {k === 2 ? <DarkCard f={f} x={150} y={BY + 50} w={1000} at={at(2)} big={d.notes[0]} small="한 건이 가운데 값을 크게 움직인다" size={42} /> : null}
      {k >= 3 ? <DarkCard f={f} x={150} y={BY + 50} w={1000} at={at(3)} big={d.notes[1]} bg={T.accent} size={42} /> : null}
    </>
  );
};

// ───────── 신고 기한 달력 ─────────
const Deadline: React.FC<{s: HScene}> = ({s}) => {
  const {f, k, at, n} = useBeat(s); const d = s.data;
  const C = 66, X = 160;
  const inWin = (mo: number, day: number) => (mo === d.from[0] && day >= d.from[1]) || (mo === d.got[0] && day <= d.got[1]);
  return (
    <>
      {d.months.map(([y, mo, days]: number[], mi) => {
        const first = new Date(y, mo - 1, 1).getDay(); const x0 = X + mi * (7 * C + 60);
        return <div key={mi} style={{position: 'absolute', left: x0, top: Y0, opacity: fade(f, 6 + mi * 12)}}>
          <div style={{...F, fontWeight: 700, fontSize: 32, color: T.ink, marginBottom: 6}}>{y}년 {mo}월</div>
          {Array.from({length: days}).map((_, i) => {
            const day = i + 1; const cell = first + i; const on = inWin(mo, day) && f >= 30 + (mi * 30 + day) * 0.6; const got = mo === d.got[0] && day === d.got[1];
            return <div key={i} style={{...F, position: 'absolute', left: (cell % 7) * C, top: 46 + Math.floor(cell / 7) * (C - 4), width: C - 6, height: C - 10, borderRadius: 8,
              background: got ? T.ink : on ? T.soft : '#fff', border: `1px solid ${T.line}`, textAlign: 'center', lineHeight: `${C - 10}px`, fontWeight: 700, fontSize: 22, color: got ? '#fff' : T.ink2}}>{day}</div>;
          })}
        </div>;
      })}
      <div style={{position: 'absolute', left: 1230, top: Y0, width: 550}}>
        <div style={{...F, fontWeight: 700, fontSize: 30, color: T.ink, opacity: fade(f, 40)}}>■ 검은 칸 = 자료 받은 날(10.11)</div>
        <div style={{...F, fontWeight: 700, fontSize: 30, color: T.accent, opacity: fade(f, 60), marginTop: 10}}>■ 주황 칸 = 그 전 30일</div>
        <div style={{...F, fontWeight: 500, fontSize: 24, color: T.ink2, opacity: fade(f, 80), marginTop: 10, wordBreak: 'keep-all'}}>이 기간 계약은 신고 기한이 남아 있어 건수가 더 늘 수 있음</div>
      </div>
      {(n > 1 && k >= 1) || (n === 1 && f > s.frames * 0.5) ? <DarkCard f={f} x={1230} y={Y0 + 260} w={550} at={n > 1 ? at(1) : s.frames * 0.5} big={d.stamp} bg={T.accent} size={40} /> : null}
    </>
  );
};

// ───────── 계산서 ─────────
const Gap: React.FC<{s: HScene}> = ({s}) => {
  const {f, k, at, n} = useBeat(s); const d = s.data;
  const rows: [string, string, string, number, string, number][] = d.rows;
  const Z = 1150, PX = 25, RH = 86;
  const lastRow = Math.max(...rows.map((r) => r[5]));
  const ex = k > lastRow ? Math.min(d.extra.length - 1, k - lastRow - 1) : -1;
  const intro = k === 0 && Math.min(...rows.map((r) => r[5])) > 0;   // 첫 줄: 주황 카드만(기준선·작은 라벨은 칸이 나올 때부터)
  return (
    <>
      <div style={{position: 'absolute', left: 150, top: Y0, width: 420, height: 300, background: T.ink, borderRadius: 20, padding: '30px 34px', boxSizing: 'border-box', opacity: fade(f, 6)}}>
        <div style={{...F, fontWeight: 700, fontSize: 30, color: T.dink3}}>{d.deposit[0]}</div>
        <div style={{...F, fontWeight: 700, fontSize: 96, color: '#fff', letterSpacing: -2}}>{d.deposit[1]}</div>
        <div style={{...F, fontWeight: 700, fontSize: 22, color: T.daccent, wordBreak: 'keep-all'}}>{d.deposit[2]}</div>
      </div>
      {ex >= 0 ? <DarkCard f={f} x={150} y={Y0 + 330} w={420} at={at(lastRow + 1 + ex)} big={d.extra[ex]} bg={T.accent} size={32} /> : null}
      {intro ? <DarkCard f={f} x={620} y={Y0 + 40} w={1160} at={8} big={d.jeonse ? '전세로 옮기면 보증금이' : '사려면 더 드는 돈'} small={s.sub ?? ''} bg={T.accent} size={52} />
        : <div style={{...F, position: 'absolute', left: 620, top: Y0 - 4, fontWeight: 700, fontSize: 24, color: T.ink3}}>{d.jeonse ? '전세로 옮기면 보증금이' : '사려면 더 드는 돈'}</div>}
      {intro ? null : <div style={{position: 'absolute', left: Z, top: Y0 + 26, height: RH * rows.length, borderLeft: `3px solid ${T.ink3}`}} />}
      {rows.map(([name, base, txt, v, , line], i) => {
        const a = at(line) + 8; const g = ease(f, a, 24); const top = Y0 + 30 + i * RH; const w = Math.abs(v) * PX * g; const neg = v < 0; const cur = k === line;
        return <div key={i} style={{opacity: fade(f, a - 4)}}>
          <div style={{position: 'absolute', left: 610, top: top - 6, width: 1170, height: 78, borderRadius: 14, background: cur ? T.ink : 'transparent'}} />
          <div style={{...F, position: 'absolute', left: 630, top: top + 4, fontWeight: 700, fontSize: 30, color: cur ? '#fff' : T.ink, whiteSpace: 'nowrap'}}>{name}</div>
          <div style={{...F, position: 'absolute', left: 630, top: top + 42, fontWeight: 500, fontSize: 22, color: cur ? T.dink3 : T.ink3, whiteSpace: 'nowrap'}}>{base}</div>
          <div style={{position: 'absolute', left: neg ? Z - w : Z, top: top + 12, width: w, height: 50, borderRadius: 8, background: neg ? (cur ? T.dfall : T.fall) : cur ? T.accent : T.ink2}} />
          <div style={{...F, position: 'absolute', left: Z + (neg ? 16 : w + 16), top: top + 10, fontWeight: 700, fontSize: 40, color: neg ? (cur ? T.dfall : T.fall) : cur ? T.daccent : T.ink, whiteSpace: 'nowrap'}}>{txt}</div>
        </div>;
      })}
      <div style={{...F, position: 'absolute', left: 620, top: 812, fontWeight: 500, fontSize: 22, color: T.ink3}}>{d.foot}</div>
      {n < 0 ? null : null}
    </>
  );
};

// ───────── 표 ─────────
const Table: React.FC<{s: HScene}> = ({s}) => {
  const {f, k, at, n} = useBeat(s); const d = s.data; const cols: string[] = d.cols; const rows: string[][] = d.rows;
  const Wc = [330, 140, 130, 210, 150, 290, 360]; const RH = 52;
  const speechEnd = s.lines.reduce((a, l) => a + l.frames, 0);
  const cyc = f > speechEnd ? Math.floor((f - speechEnd) / 75) % rows.length : -1;
  return (
    <>
      <div style={{position: 'absolute', left: 140, top: Y0 - 6, width: 1640}}>
        <div style={{display: 'flex', height: 44, alignItems: 'center', borderBottom: `3px solid ${T.ink}`}}>
          {cols.map((c, i) => <div key={c} style={{...F, width: Wc[i], fontWeight: 700, fontSize: 22, color: T.ink2, textAlign: i ? 'right' : 'left', whiteSpace: 'nowrap'}}>{c}</div>)}
        </div>
        {rows.map((r, ri) => { const on = ri === cyc || (k === 0 && f < speechEnd && Math.floor((f - 10) / 40) === ri); return (
          <div key={ri} style={{display: 'flex', height: RH, alignItems: 'center', borderBottom: `1px solid ${T.line}`, opacity: fade(f, 10 + ri * 8), background: on ? T.ink : 'transparent', borderRadius: 8}}>
            {r.map((v, i) => <div key={i} style={{...F, width: Wc[i], fontWeight: i ? 600 : 700, fontSize: i ? 24 : 26, color: on ? '#fff' : T.ink, textAlign: i ? 'right' : 'left', whiteSpace: 'nowrap', overflow: 'hidden'}}>{v}</div>)}
          </div>); })}
      </div>
      {n > 1 && k >= 1 ? <DarkCard f={f} x={140} y={Y0 + 412} w={900} at={at(1)} big={`${d.cafe} · 37곳 전체 표`} bg={T.accent} size={34} /> : null}
    </>
  );
};

const Body: React.FC<{s: HScene}> = ({s}) => {
  switch (s.kind) {
    case 'map': return <MapScene s={s} />;
    case 'dots': return <Dots s={s} />;
    case 'bars': return <PairBars s={s} />;
    case 'period': return <Period s={s} />;
    case 'person': return <Person s={s} />;
    case 'concl': return <Concl s={s} />;
    case 'tiles': return <Tiles s={s} />;
    case 'deal': return <Deal s={s} />;
    case 'floors': return <Floors s={s} />;
    case 'line': return <Lines s={s} />;
    case 'cal': return <Cal s={s} />;
    case 'rent': return <Rent s={s} />;
    case 'walk': return <Walk s={s} />;
    case 'cards': return <Cards s={s} />;
    case 'diff': return <Diff s={s} />;
    case 'vol': return <Vol s={s} />;
    case 'deadline': return <Deadline s={s} />;
    case 'gap': return <Gap s={s} />;
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

export const H1: React.FC<H1Props> = (p) => {
  let from = 0;
  return (
    <Maps.Provider value={p.maps}>
      <AbsoluteFill style={{background: T.bg}}>
        {p.scenes.map((s, i) => { const el = <Sequence key={i} from={from} durationInFrames={s.frames}><SceneView s={s} /></Sequence>; from += s.frames; return el; })}
      </AbsoluteFill>
    </Maps.Provider>
  );
};
