// 실거래 점 줄(DealDots) — H-6 은마 84㎡ '1년 새 얼마 내렸나'(2026-11-20 motion). TallyFrame 자식.
// 경쟁: 땅집고 RvCiGDtCqn8(국토부 실거래 화면 한 줄 노란 칠) · 부태희TV WzQebWiEi14(막대 5개, 인가 전후 색 바꿈) — 우리는 한 건도 빼지 않고 전부 찍는다.
// 줄마다 화면에 새 일 하나(U5): ① 점이 날짜 순서로 하나씩 떨어짐 ② 최고 한 건 손 동그라미 ③ 마지막 같은 높은 층 한 건 + 세로 괄호 차
// ④ 묶음 가운데 값 계단 선이 왼쪽부터 써짐 ⑤ 인가 고시일 세로 선이 내려오고, 그 앞 몫만 괄호가 주황.
// 세로 축은 0원부터가 아니다 → 아래에 물결 끊김 표시 + 눈금 글자를 늘 보인다(11/1 교훈: 바닥 자른 그림 오독).
// 숫자는 전부 props(편 스크립트가 calc_out과 assert). 주황은 그 줄의 답 하나만, 다음 답이 열리면 앞 답은 먹색.
// 반복 방지: seed로 왼쪽 여백·점 떨어지는 빠르기, 편 스크립트에서 점 색·계단 묶음 길이를 바꾼다.
import React from 'react';
import {interpolate, useCurrentFrame, Easing, random} from 'remotion';
import {T, F, CL, HandCircle} from '../parts/fm';

export type Deal = {d: string; v: number; fl: number};
export type DealDotsProps = {
  seed: string;
  deals: Deal[]; from: string; to: string;          // 날짜 'YYYY-MM-DD'
  min: number; max: number; ticks: number[]; unit: string;
  months: {d: string; text: string}[];
  dropAt: number;                                   // 점 떨어지기 시작 줄
  peak: {i: number; text: string; at: number};
  last: {i: number; text: string; at: number; gap: string; gapAt: number};
  steps: {a: string; b: string; v: number; text: string}[]; stepsAt: number; stepGap: {text: string; at: number};
  mark: {d: string; text: string; at: number}; before: {text: string; at: number};
  beats: number[];
};

const io = Easing.inOut(Easing.cubic), out = Easing.out(Easing.cubic);
const g = (f: number, a: number, d = 14, e = out) => interpolate(f, [a, a + d], [0, 1], {...CL, easing: e});
const day = (s: string) => Date.UTC(+s.slice(0, 4), +s.slice(5, 7) - 1, +s.slice(8, 10)) / 864e5;

export const DealDots: React.FC<DealDotsProps> = (p) => {
  const f = useCurrentFrame();
  const r = (k: string) => random(p.seed + k);
  const B = p.beats; const at = (x: number) => { if (x < 0) return -1e9; const i = Math.floor(x); const a = B[i] ?? 1e9; const n = (B[i + 1] ?? a + 150) - a; return a + n * (x - i); };
  const X0 = 250 + Math.round(r('x') * 50), X1 = 1470, YT = 340, YB = 750;
  const D0 = day(p.from), D1 = day(p.to);
  const X = (s: string) => X0 + (day(s) - D0) / (D1 - D0) * (X1 - X0);
  const Y = (v: number) => YB - (v - p.min) / (p.max - p.min) * (YB - YT);
  const endF = (B[B.length - 1] ?? 0) + 160;
  const push = interpolate(f, [0, endF], [1, 1.035], CL);
  const dA = at(p.dropAt), pA = at(p.peak.at), lA = at(p.last.at), gA = at(p.last.gapAt), sA = at(p.stepsAt), sgA = at(p.stepGap.at), mA = at(p.mark.at), bA = at(p.before.at);
  const gap = Math.max(3, (at(p.dropAt + 0.8) - dA) / p.deals.length) * (0.9 + r('sp') * 0.2);   // 첫 줄 내내 떨어진다(U5)
  const pkO = g(f, pA, 30, io) * (1 - g(f, sA, 12));   // 최고값 높이 선 — 왼→오 그어진다
  const pk = p.deals[p.peak.i], ls = p.deals[p.last.i];
  // 카메라(U5 — 160×90에서 점·가는 선은 4%를 못 바꾼다): 최고 줄에 그 점 쪽으로 다가가고, 마지막 줄에 오른쪽 끝으로 옮겨 가고, 계단 줄에 다시 전체
  const zin = g(f, pA, 36, io) * (1 - g(f, sA, 36, io)), mv = g(f, lA, 40, io);
  // 첫 줄: 왼쪽(처음 날짜)에 붙어 있다가 점이 찍히는 대로 오른쪽으로 물러난다
  const dEnd = at(p.dropAt + 0.8), intro = 1 - g(f, dA, Math.max(30, dEnd - dA), io), w = intro / (intro + zin + 1e-6);
  const z = push * (1 + (0.13 - 0.08 * mv) * zin + 0.16 * intro);
  const ox = (X(pk.d) + (X(ls.d) - X(pk.d)) * mv) * (1 - w) + (X0 + (X1 - X0) * (1 - intro)) * w;
  const oy = (Y(pk.v) + (Y(ls.v) - Y(pk.v)) * mv) * (1 - w) + ((YT + YB) / 2) * w;
  const stepFill = g(f, sA + 20, 40) * 0.32;
  const lab = (s: React.CSSProperties) => ({position: 'absolute' as const, ...F, whiteSpace: 'nowrap' as const, ...s});
  const dim = g(f, sA, 16);                          // 계단이 오면 점은 옅게
  // 계단 선 경로(묶음마다 가로, 사이는 세로)
  let sd = ''; p.steps.forEach((s, k) => { sd += `${k ? 'L' : 'M'}${X(s.a).toFixed(1)} ${Y(s.v).toFixed(1)}L${X(s.b).toFixed(1)} ${Y(s.v).toFixed(1)}`; });
  const s0 = p.steps[0], sN = p.steps[p.steps.length - 1];
  const mx = X(p.mark.d);
  // 인가 전 몫: 첫 묶음 값 → 인가 직전 묶음 값
  const pre = p.steps.filter((s) => day(s.b) <= day(p.mark.d) + 1); const preV = pre.length ? pre[pre.length - 1].v : s0.v;
  const brR = true;                                  // 왼쪽은 눈금 글자 자리라 괄호는 늘 오른쪽(차 괄호가 사라진 자리)
  const bx = X1 + 40;
  const gapO = g(f, gA, 14) * (1 - g(f, sA, 12));
  const accGap = f < sgA;                             // 다음 답이 열리면 앞 답은 먹색
  const accStep = f >= sgA && f < bA;
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, transform: `translate(${ox * (1 - z)}px, ${oy * (1 - z)}px) scale(${z})`, transformOrigin: '0 0'}}>
      <svg style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080}}>
        {p.ticks.map((t) => <line key={t} x1={X0} x2={X1} y1={Y(t)} y2={Y(t)} stroke={T.ink3} strokeOpacity={0.35 * (1 - g(f, sA, 20))} strokeWidth={2} />)}   {/* 계단 면이 오면 눈금 선은 빠진다(면 안이 칸으로 잘려 상자로 읽힘 — bgcheck ⑥), 눈금 글자는 남음 */}
        {/* 바닥 끊김(0원부터가 아님) */}
        <polyline points={`${X0 - 56},${YB + 14} ${X0 - 40},${YB - 2} ${X0 - 24},${YB + 18} ${X0 - 8},${YB + 2}`} fill="none" stroke={T.ink} strokeWidth={5} opacity={g(f, 4, 12)} />
        {/* 인가 고시일 — 위에서 내려오는 선, 그 앞 칸은 옅은 면 */}
        <line x1={mx} x2={mx} y1={YT - 40} y2={YT - 40 + (YB - YT + 60) * g(f, mA, 24, io)} stroke={T.ink} strokeWidth={5} strokeDasharray="16 10" />
        {/* 점 — 날짜 순서로 하나씩 떨어진다 */}
        {p.deals.map((q, k) => { const s = g(f, dA + k * gap, 10, Easing.out(Easing.back(2))); const hi = k === p.peak.i || k === p.last.i;
          return s > 0 ? <circle key={k} cx={X(q.d)} cy={Y(q.v) - (1 - s) * 40} r={hi ? 13 : 11} fill={hi && f >= pA ? T.ink : T.ink2} opacity={s * (1 - dim * (hi ? 0.2 : 0.6)) * (hi ? 1 : 1 - 0.45 * pkO)} /> : null; })}
        {/* 최고 한 건·마지막 한 건 */}
        <HandCircle cx={X(pk.d)} cy={Y(pk.v)} rx={34} ry={30} p={g(f, pA + 6, 20, Easing.inOut(Easing.quad)) * (1 - g(f, sA, 10))} color={T.ink} />
        <HandCircle cx={X(ls.d)} cy={Y(ls.v)} rx={34} ry={30} p={g(f, lA + 6, 20, Easing.inOut(Easing.quad)) * (1 - g(f, sA, 10))} color={T.ink} />
        {/* 높은 층끼리 차 — 두 점 높이 사이 띠(U5) + 가로 점선 + 괄호 */}
        <rect x={X(pk.d)} y={Y(pk.v)} width={(X1 + 20 - X(pk.d)) * g(f, gA, 24, io)} height={Y(ls.v) - Y(pk.v)} fill={T.ink3} opacity={0.3 * gapO} />
        <line x1={X(pk.d)} x2={X(pk.d) + (X1 + 20 - X(pk.d)) * pkO} y1={Y(pk.v)} y2={Y(pk.v)} stroke={T.ink2} strokeWidth={4} strokeDasharray="10 8" opacity={pkO > 0 ? 1 : 0} />
        <line x1={X(ls.d)} x2={X1 + 20} y1={Y(ls.v)} y2={Y(ls.v)} stroke={T.ink3} strokeWidth={3} strokeDasharray="6 8" opacity={gapO} />
        <path d={`M${X1 + 30} ${Y(pk.v)}h16V${Y(ls.v)}h-16`} fill="none" stroke={accGap ? T.accent : T.ink} strokeWidth={6} strokeLinejoin="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - gapO} />
        {/* 묶음 가운데 값 계단 — 왼쪽부터 써지고, 아래가 옅게 찬다 */}
        <path d={`${sd}L${X(sN.b).toFixed(1)} ${Y(s0.v).toFixed(1)}Z`} fill={T.ink3} opacity={stepFill} />   {/* 첫 묶음 높이에서 빠진 만큼만(바닥까지 칠하면 막대로 읽힘 — 심사 11/20) */}
        {/* 인가 앞 몫 — 계단 아래 면 중 고시일 앞만 진해진다(네모 판 대신 데이터 면, bgcheck ⑥) */}
        <clipPath id={'ddpre' + p.seed}><rect x={X0 - 10} y={0} width={Math.max(0, mx - X0 + 10) * g(f, mA + 10, 30, io)} height={1080} /></clipPath>
        <path d={`${sd}L${X(sN.b).toFixed(1)} ${Y(s0.v).toFixed(1)}Z`} fill={T.accent} opacity={0.35} clipPath={`url(#ddpre${p.seed})`} />
        <path d={sd} fill="none" stroke={T.ink} strokeWidth={8} strokeLinejoin="round" strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - g(f, sA, 70, io)} />
        {/* 계단 차 괄호(첫 묶음 → 끝 묶음), 인가 줄에서 인가 앞 몫만 주황으로 갈라진다 */}
        <path d={`M${bx + (brR ? -16 : 16)} ${Y(s0.v)}h${brR ? 16 : -16}V${Y(sN.v)}h${brR ? -16 : 16}`} fill="none" stroke={accStep ? T.accent : T.ink} strokeWidth={6} strokeLinejoin="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - g(f, sgA, 16)} />
        <path d={`M${bx} ${Y(s0.v)}V${Y(preV)}`} fill="none" stroke={T.accent} strokeWidth={12} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - g(f, bA, 18)} />
      </svg>
      {/* 눈금 글자 — 늘 보인다(바닥 자른 축) */}
      {p.ticks.map((t) => <div key={t} style={lab({left: X0 - 150, top: Y(t) - 18, width: 120, textAlign: 'right', fontWeight: 500, fontSize: 30, color: T.ink3, opacity: g(f, 4, 12)})}>{t}{p.unit}</div>)}
      {p.months.map((m) => <div key={m.d} style={lab({left: X(m.d) - 80, top: YB + 22, width: 160, textAlign: 'center', fontWeight: 500, fontSize: 34, color: T.ink2, opacity: g(f, 4, 12)})}>{m.text}</div>)}
      {/* 인가 이름 — 선 위 */}
      <div style={lab({left: mx + 18, top: YT - 92, fontWeight: 800, fontSize: 40, color: T.ink, opacity: g(f, mA + 10, 12)})}>{p.mark.text}</div>
      {/* 최고·마지막 한 건 글자 — 말이 닿을 때 */}
      <div style={lab({left: X(pk.d) + 44, top: Y(pk.v) - 88 + (1 - g(f, pA + 10, 12)) * 10, fontWeight: 800, fontSize: 46, color: T.ink, opacity: g(f, pA + 10, 12) * (1 - dim)})}>{p.peak.text}</div>
      <div style={lab({left: X(ls.d) - 470, top: Y(ls.v) + 34 + (1 - g(f, lA + 10, 12)) * 10, width: 430, textAlign: 'right', fontWeight: 800, fontSize: 46, color: T.ink, opacity: g(f, lA + 10, 12) * (1 - dim)})}>{p.last.text}</div>
      <div style={lab({left: X1 + 66, top: (Y(pk.v) + Y(ls.v)) / 2 - 40, fontWeight: 800, fontSize: 64, letterSpacing: -1, color: accGap ? T.accent : T.ink, opacity: gapO})}>{p.last.gap}</div>
      {/* 계단 값 — 묶음마다 선 위 */}
      {p.steps.map((s, k) => <div key={s.a} style={lab({left: (X(s.a) + X(s.b)) / 2 - 120, top: Y(s.v) - 66, width: 240, textAlign: 'center', fontWeight: 800, fontSize: 38, color: T.ink, opacity: g(f, sA + 10 + k * 16, 12)})}>{s.text}</div>)}
      <div style={lab({left: brR ? bx + 34 : bx - 300, top: (Y(s0.v) + Y(sN.v)) / 2 - 10, width: 260, textAlign: brR ? 'left' : 'right', fontWeight: 800, fontSize: 52, color: accStep ? T.accent : T.ink, opacity: g(f, sgA + 6, 12)})}>{p.stepGap.text}</div>
      <div style={lab({left: mx - 900, top: YT - 100, width: 860, textAlign: 'right', fontWeight: 800, fontSize: 52, color: T.accent, opacity: g(f, bA + 12, 12)})}>{p.before.text}</div>
    </div>
  );
};
