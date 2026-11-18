// 받은 돈 합 경주(SumRace) — JT-1 '3. 늦게 들면 몇 살에 같아지나'(2026-11-16 motion). TallyFrame 자식. 장면 둘로 씀:
//  ① race: 나이 바늘이 걸으며 두 '받은 돈 합' 선을 그린다(늦게 든 쪽은 시작 나이까지 0) → 시작 자리 '못 받은 돈' 괄호 → 만남 '?' → '23년' 가로 괄호 → 손 동그라미 + 주황 '93세'.
//  ② gap: 같은 그림에서 늦게 든 쪽 선을 빼서 바닥선으로 눕힌다(lam 0→1) — 두 선 사이 좁은 틈이 큰 언덕(일찍 든 쪽이 더 받은 돈)으로 커지고,
//     중간 나이(80·85·90)마다 언덕 위 점·기둥·값 → 바닥선 아래로 내려간 93세 뒤만 연주황.
// 왜 빼나(11/16 첫 렌더 눈 검사): 5억 축에서 두 선 차(최대 7,584만원)는 화면 70px — 4,284·2,634·984 괄호가 선에 묻혀 안 읽혔다. 차를 직접 그리는 게 dataviz 기본.
// 정직성: 합 = 월지급금 × 받은 달 수(집값 그대로 가정), 모든 점이 그 식 그대로. 만남 = 두 직선 교점 92.98세(글자만 '93세'). 축 글자는 race 2억·4억, gap 없음(값은 점 위 글자).
// 반복 방지: seed로 왼쪽 여백·면 결 기울기. 글자는 전부 HTML. 판 전체 1.00→1.03 다가가기(U5).
import React from 'react';
import {interpolate, useCurrentFrame, Easing, random} from 'remotion';
import {T, F, CL, HandCircle} from '../parts/fm';

type Side = {name: string; start: number; monthly: number};   // monthly = 만원
type Mark = {text: string; at: number};
export type SumRaceProps = {
  seed: string; from: number; to: number;
  a: Side; b: Side;                                   // a = 일찍 든 쪽, b = 늦게 든 쪽(더 가파름)
  yRace: [number, number]; yGap: [number, number];    // 만원
  ticks: {v: number; text: string}[];                 // race 때만 보이는 축 글자
  ageTicks: number[];
  lam: {from: number; to: number; at: number};        // 0 = 두 합 선, 1 = b를 바닥으로(차 언덕)
  sweep: [number, number] | null;                     // null이면 처음부터 다 그려짐
  missed: Mark | null; years: Mark | null; meet: Mark; // meet.at < 0 이면 처음부터
  slices: {age: number; text: string; at: number}[];
  after: Mark | null;
  beats: number[];
};

const io = Easing.inOut(Easing.cubic), out = Easing.out(Easing.cubic);
const g = (f: number, a: number, d = 14, e = out) => interpolate(f, [a, a + d], [0, 1], {...CL, easing: e});
export const sumAt = (s: Side, age: number) => Math.max(0, age - s.start) * 12 * s.monthly;   // 만원
export const meetAge = (a: Side, b: Side) => (b.monthly * b.start - a.monthly * a.start) / (b.monthly - a.monthly);

export const SumRace: React.FC<SumRaceProps> = (p) => {
  const f = useCurrentFrame();
  const r = (k: string) => random(p.seed + k);
  const B = p.beats; const at = (x: number) => { if (x < 0) return -100; const i = Math.floor(x); const a = B[i] ?? 1e9; const n = (B[i + 1] ?? a + 150) - a; return a + n * (x - i); };
  const X0 = 290 + Math.round(r('x') * 50), X1 = 1520, YT = 290, YB = 770;
  const L = interpolate(f, [at(p.lam.at), at(p.lam.at) + 45], [p.lam.from, p.lam.to], {...CL, easing: io});
  const y0 = p.yRace[0] + (p.yGap[0] - p.yRace[0]) * L, y1 = p.yRace[1] + (p.yGap[1] - p.yRace[1]) * L;
  const X = (age: number) => X0 + (age - p.from) / (p.to - p.from) * (X1 - X0);
  const Y = (v: number) => YB - (v - y0) / (y1 - y0) * (YB - YT);
  const vA = (age: number) => sumAt(p.a, age) - L * sumAt(p.b, age);
  const vB = (age: number) => (1 - L) * sumAt(p.b, age);
  const endF = (B[B.length - 1] ?? 0) + 150;
  const push = interpolate(f, [0, endF], [1, 1.03], CL);
  const cross = meetAge(p.a, p.b), cx = X(cross), cy = Y(vA(cross));
  const mA = at(p.meet.at);
  const nearCross = cross - 0.6;
  const needle = !p.sweep ? p.to : f < mA ? interpolate(f, [at(p.sweep[0]), at(p.sweep[1])], [p.from, nearCross], {...CL, easing: io})
    : interpolate(f, [mA, mA + 40], [nearCross, p.to], {...CL, easing: io});
  const ages = (upTo: number) => [p.from, p.a.start, p.b.start, cross].map((x) => Math.max(p.from, Math.min(x, upTo))).concat([upTo]);   // 꺾이는 나이 모두(gap 언덕은 b 시작에서 꺾임)
  const pts = (fn: (a: number) => number, xs: number[]) => xs.map((age) => `${X(age).toFixed(1)},${Y(fn(age)).toFixed(1)}`).join(' ');
  const base = Y(Math.max(y0, Math.min(0, y1)));
  const area = (fn: (a: number) => number, xs: number[]) => `${X(p.from)},${base} ${pts(fn, xs)} ${X(xs[xs.length - 1])},${base}`;
  const tilt = 40 + Math.round(r('t') * 30);
  const lab = (s: React.CSSProperties) => ({position: 'absolute' as const, ...F, whiteSpace: 'nowrap' as const, ...s});
  const missAt = p.missed ? at(p.missed.at) : 1e9, yrAt = p.years ? at(p.years.at) : 1e9, afAt = p.after ? at(p.after.at) : 1e9;
  const mO = g(f, missAt, 14), yO = g(f, yrAt, 14) * (1 - L), meO = g(f, mA + 6, 22, Easing.inOut(Easing.quad)), afO = g(f, afAt, 16);
  const qO = (p.sweep && needle > p.b.start + 6 ? 1 : 0) * g(f, missAt + 30, 12) * (1 - g(f, mA, 8));
  const sl = p.slices.map((s, i) => ({...s, o: g(f, at(s.at), 12), hi: g(f, at(s.at), 12) * (1 - g(f, at(p.slices[i + 1]?.at ?? (p.after ? p.after.at : 1e6)), 12))}));
  const xsA = ages(needle), xsB = xsA;
  const peak = p.b.start;   // 차가 가장 큰 나이(= b 시작)
  const nameO = g(f, at(p.sweep ? p.sweep[0] : 0) + 10, 12);
  // 11/18 PD(JT-1 겹침 검사 3:18 '70세' 눈금 ← '70세에 든 쪽'): race에서 늦게 든 쪽 선이 아직 바닥(0)이면 이름표가 바닥선 아래 나이 눈금에 앉았다 → 바닥선 위로 올리고, 먼저 든 쪽 이름표는 그보다 56px 위
  const bTop = needle < cross ? Math.min(Y(vB(needle)) + 8, base - 54) : Y(vB(needle)) - 70;
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, transform: `scale(${push})`, transformOrigin: '45% 60%'}}>
      <svg style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080}}>
        <defs>
          <pattern id={'srA' + p.seed} width={14} height={14} patternUnits="userSpaceOnUse" patternTransform={`rotate(${tilt})`}><line x1={0} y1={0} x2={0} y2={14} stroke={T.ink2} strokeWidth={3} strokeOpacity={0.35} /></pattern>
          <pattern id={'srB' + p.seed} width={18} height={18} patternUnits="userSpaceOnUse" patternTransform={`rotate(${-tilt})`}><line x1={0} y1={0} x2={0} y2={18} stroke={T.ink3} strokeWidth={3} strokeOpacity={0.3 * (1 - L)} /></pattern>
        </defs>
        {p.ticks.map((tk) => <line key={tk.v} x1={X0} x2={X1} y1={Y(tk.v)} y2={Y(tk.v)} stroke={T.ink3} strokeOpacity={0.3 * (1 - L)} strokeWidth={2} />)}
        <polygon points={area(vA, xsA)} fill={`url(#srA${p.seed})`} />
        <polygon points={area(vB, xsB)} fill={`url(#srB${p.seed})`} />
        {/* 교점 뒤: 늦게 든 쪽이 앞선 칸 — 연주황 */}
        <polygon points={`${cx},${cy} ${X(p.to)},${Y(vB(p.to))} ${X(p.to)},${Y(vA(p.to))}`} fill={T.accent} opacity={0.3 * afO} />
        <line x1={X0} x2={X1} y1={base} y2={base} stroke={T.ink} strokeWidth={3} opacity={1 - L} />
        <polyline points={pts(vB, xsB)} fill="none" stroke={T.ink2} strokeWidth={6 + 2 * L} strokeDasharray="18 10" strokeLinejoin="round" />
        <polyline points={pts(vA, xsA)} fill="none" stroke={T.ink} strokeWidth={7} strokeLinejoin="round" />
        {p.sweep ? <line x1={X(needle)} x2={X(needle)} y1={YT - 30} y2={YB} stroke={T.ink} strokeOpacity={0.5 * (1 - g(f, mA + 40, 12) * 0.8)} strokeWidth={3} strokeDasharray="4 8" /> : null}
        {p.sweep ? <><circle cx={X(needle)} cy={Y(vA(needle))} r={11} fill={T.ink} /><circle cx={X(needle)} cy={Y(vB(needle))} r={10} fill={T.ink2} /></> : null}
        {/* 못 받은 돈: b 시작 나이에서 두 선 사이 세로 괄호 */}
        <path d={`M${X(peak) - 22} ${Y(vB(peak))} h22 V${Y(vA(peak))} h-22`} fill="none" stroke={T.ink} strokeWidth={4} opacity={mO} />
        <path d={`M${X(p.b.start)} ${YB + 74} v-14 H${cx} v14`} fill="none" stroke={T.ink} strokeWidth={4} opacity={yO} />
        {/* 남은 앞섬: 지금 부른 나이 → 만남까지 언덕 면(나이가 갈수록 줄어듦) · 만남 뒤 세로 띠 */}
        {sl.map((s) => <polygon key={'r' + s.age} points={`${X(s.age)},${Y(vB(s.age))} ${pts(vA, [s.age, cross])} ${cx},${Y(vB(cross))}`} fill={T.accent} opacity={0.22 * s.hi} />)}
        <rect x={cx + 10} y={YT - 20} width={X1 - cx + 50} height={YB - YT + 20} fill={T.accent} opacity={0.14 * afO} />
        {/* race: 못 받은 돈 글자 → 70세 괄호 지시선 */}
        <line x1={X(peak) - 40} y1={Y(vA(peak)) - 196} x2={X(peak) - 2} y2={Y(vA(peak)) - 8} stroke={T.ink} strokeWidth={3} opacity={mO * (1 - L)} />
        {sl.map((s) => <g key={s.age} opacity={s.o}>
          <line x1={X(s.age)} x2={X(s.age)} y1={Y(vB(s.age))} y2={Y(vA(s.age))} stroke={s.hi > 0.5 ? T.accent : T.ink2} strokeWidth={6} />
          <circle cx={X(s.age)} cy={Y(vA(s.age))} r={13} fill={s.hi > 0.5 ? T.accent : T.ink} />
        </g>)}
        <HandCircle cx={cx} cy={cy} rx={66} ry={54} p={p.meet.at < 0 ? 1 : meO} />
      </svg>
      {p.ticks.map((tk) => <div key={tk.v} style={lab({left: X0 - 150, top: Y(tk.v) - 17, width: 120, textAlign: 'right', fontWeight: 500, fontSize: 30, color: T.ink3, opacity: g(f, 4, 12) * (1 - L)})}>{tk.text}</div>)}
      {p.ageTicks.map((a) => <div key={a} style={lab({left: X(a) - 70, top: YB + 14, width: 140, textAlign: 'center', fontWeight: a === p.a.start || a === p.b.start ? 800 : 500, fontSize: 32, color: a === p.a.start || a === p.b.start ? T.ink : T.ink3, opacity: g(f, 6, 12)})}>{a}세</div>)}
      {/* 선 이름: race는 바늘 끝, gap은 왼쪽 위(언덕)·바닥선 왼쪽 */}
      <div style={lab({left: (1 - L) * (X(needle) + 24) + L * (X(peak) + 30), top: (1 - L) * (needle < cross ? Math.min(Y(vA(needle)) - 66, bTop - 56) : Y(vA(needle)) + 14) + L * (Y(vA(peak)) - 70), fontWeight: 800, fontSize: 40, color: T.ink, opacity: nameO * (1 - 0.6 * mO * L)})}>{p.a.name}</div>
      <div style={lab({left: (1 - L) * (X(needle) + 24) + L * (X0 + 10), top: (1 - L) * bTop + L * (base + 14), fontWeight: 800, fontSize: 40, color: T.ink2, opacity: nameO})}>{p.b.name}</div>
      {p.missed ? <div style={lab({left: (1 - L) * (X0 - 170) + L * (X(peak) - 440), top: (1 - L) * (Y(vA(peak)) - 250) + L * (Y(vA(peak)) - 26), width: (1 - L) * 900 + L * 410, textAlign: L > 0.5 ? 'right' : 'left', fontWeight: 800, fontSize: 46, color: T.ink, opacity: mO * (1 - 0.5 * g(f, at(p.slices[0]?.at ?? 1e6), 12))})}>{p.missed.text}</div> : null}
      {p.years ? <div style={lab({left: (X(p.b.start) + cx) / 2 - 200, top: YB + 80, width: 400, textAlign: 'center', fontWeight: 800, fontSize: 48, color: T.ink, opacity: yO})}>{p.years.text}</div> : null}
      <div style={lab({left: X(needle) - 60, top: Y(vA(needle)) - 190, width: 120, textAlign: 'center', fontWeight: 900, fontSize: 84, color: T.ink2, opacity: qO})}>?</div>
      <div style={lab({left: (1 - L) * (cx - 360) + L * (cx + 20), top: cy - 128 - L * 112, width: 290, textAlign: L > 0.5 ? 'left' : 'right', fontWeight: 900, fontSize: 104, color: T.accent, opacity: p.meet.at < 0 ? 1 : g(f, mA + 4, 12)})}>{p.meet.text}</div>
      {sl.map((s) => <div key={s.age} style={lab({left: X(s.age) + 18, top: Y(vA(s.age)) - 84, width: 330, textAlign: 'left', fontWeight: 900, fontSize: s.hi > 0.5 ? 60 : 44, color: s.hi > 0.5 ? T.accent : T.ink2, opacity: s.o})}>{s.text}</div>)}
      {p.after ? <div style={lab({left: cx - 700, top: base + 22, width: 620, textAlign: 'right', fontWeight: 800, fontSize: 46, color: T.accent, opacity: afO})}>{p.after.text}</div> : null}
    </div>
  );
};
