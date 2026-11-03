// 두 선 순서 바뀜(CrossOver) — K-1 '3. 고정형과 변동형' 월별 두 선(2026-11-03 motion). TallyFrame 자식.
// 두 선이 왼쪽부터 그어지고, 말이 한쪽을 부르면 그 선만 진해지며 시작값 위 면(오른 폭)이 옅게 칠해지고 처음·끝 값과 오른 폭 글자가 붙는다.
// '1년 전엔' 줄: 두 선 사이(엇갈리기 전)가 옅은 먹으로 칠해짐 → '순서가 바뀌어' 줄: 엇갈린 뒤 칸이 연주황으로 칠해지고 엇갈린 자리에 손 동그라미 + 주황 답 글자.
// 정직성: 엇갈린 자리는 두 달 사이 직선으로 이은 교점(월 값 사이를 지어내지 않음 — 동그라미는 두 달 사이를 감쌀 만큼 크게).
// 두 금리·두 값의 순서가 바뀌는 주제에 다시 쓴다. 편마다 seed로 왼쪽 여백이 바뀐다(오른 폭 글자는 겹침 때문에 위 선은 위·아래 선은 아래 고정).
// 글자는 전부 HTML(10/13 교훈). 판 전체 1.00→1.03 다가가기(U5 10/19).
import React from 'react';
import {interpolate, useCurrentFrame, Easing, random} from 'remotion';
import {T, F, CL, HandCircle} from '../parts/fm';

type Ser = {name: string; v: number[]; from: string; to: string; up: string; at: number};
export type CrossOverProps = {
  seed: string; months: string[]; min: number; max: number; ticks: number[];
  a: Ser; b: Ser;                                     // a = 나중에 위로 올라서는 쪽
  start: {text: string; at: number}; swap: {i: number; text: string; at: number}; draw: number;
  beats: number[];
};

const io = Easing.inOut(Easing.cubic), out = Easing.out(Easing.cubic);
const g = (f: number, a: number, d = 14, e = out) => interpolate(f, [a, a + d], [0, 1], {...CL, easing: e});

export const CrossOver: React.FC<CrossOverProps> = (p) => {
  const f = useCurrentFrame();
  const r = (k: string) => random(p.seed + k);
  const B = p.beats; const at = (x: number) => { const i = Math.floor(x); const a = B[i] ?? 1e9; const n = (B[i + 1] ?? a + 150) - a; return a + n * (x - i); };
  const N = p.months.length;
  const X0 = 300 + Math.round(r('x') * 40), X1 = 1540, YT = 320, YB = 770;   // 달 글자가 출처 줄(y 860대)과 겹치지 않게(11/3 눈 검사)
  const X = (i: number) => X0 + i / (N - 1) * (X1 - X0);
  const Y = (v: number) => YB - (v - p.min) / (p.max - p.min) * (YB - YT);
  const endF = (B[B.length - 1] ?? 0) + 150;
  const push = interpolate(f, [0, endF], [1, 1.03], CL);
  const dA = at(p.draw), aA = at(p.a.at), bA = at(p.b.at), sA = at(p.start.at), wA = at(p.swap.at);
  const draw = g(f, 0, 40, io);
  const path = (v: number[]) => v.map((y, i) => `${i ? 'L' : 'M'}${X(i).toFixed(1)} ${Y(y).toFixed(1)}`).join(' ');
  // 교점(두 달 사이 직선)
  const k = p.swap.i; const da0 = p.a.v[k - 1] - p.b.v[k - 1], da1 = p.a.v[k] - p.b.v[k]; const t = da0 / (da0 - da1);
  const cx = X(k - 1 + t), cy = Y(p.a.v[k - 1] + (p.a.v[k] - p.a.v[k - 1]) * t);
  const band = (i0: number, i1: number, x0?: number, x1?: number) => {
    const top: string[] = [], bot: string[] = [];
    if (x0 !== undefined) top.push(`${x0},${cy}`);
    for (let i = i0; i <= i1; i++) { top.push(`${X(i)},${Y(p.a.v[i])}`); bot.unshift(`${X(i)},${Y(p.b.v[i])}`); }
    if (x1 !== undefined) top.push(`${x1},${cy}`);
    return [...top, ...bot].join(' ');
  };
  const hiA = g(f, aA, 12) * (1 - g(f, bA, 12)), hiB = g(f, bA, 12) * (1 - g(f, sA, 12));
  const wA_ = (s: 'a' | 'b') => (s === 'a' ? 4 + 4 * hiA : 4 + 4 * hiB);
  const preO = g(f, sA, 16), postO = g(f, wA, 16);
  const lab = (s: React.CSSProperties) => ({position: 'absolute' as const, ...F, whiteSpace: 'nowrap' as const, ...s});
  const ends = (s: Ser, o: number, col: string, dy: number, isTop: boolean) => <>
    <div style={lab({left: X0 - 190, top: Y(s.v[0]) - 24 + dy, width: 170, textAlign: 'right', fontWeight: 800, fontSize: 40, color: col, opacity: o})}>{s.from}</div>
    <div style={lab({left: X1 + 20, top: Y(s.v[N - 1]) - 24, fontWeight: 800, fontSize: 40, color: col, opacity: o})}>{s.to}</div>
    <div style={lab({left: X1 + 20, top: Y(s.v[N - 1]) + (isTop ? -74 : 26), fontWeight: 800, fontSize: 48, color: col, opacity: o})}>{s.up}</div>
  </>;
  const sideA = Y(p.a.v[N - 1]) < Y(p.b.v[N - 1]);   // 끝에서 a가 위면 a 끝 이름 위, b 끝 이름 아래
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, transform: `scale(${push})`, transformOrigin: '50% 60%'}}>
      <svg style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080}}>
        <defs><clipPath id={'cov' + p.seed}><rect x={X0 - 10} y={0} width={(X1 - X0 + 20) * draw} height={1080} /></clipPath></defs>
        {p.ticks.map((tk) => <line key={tk} x1={X0} x2={X1} y1={Y(tk)} y2={Y(tk)} stroke={T.ink3} strokeOpacity={0.35} strokeWidth={2} />)}
        {/* 부른 선의 오른 폭 — 시작값 높이 위로 옅은 면(U5: 선 굵기만으론 화면 4%를 못 바꿈, 11/3) */}
        {([['a', hiA], ['b', hiB]] as const).map(([w, o]) => { const v = p[w].v; return <polygon key={w} points={[...v.map((y, i) => `${X(i)},${Y(Math.max(y, v[0]))}`), `${X(N - 1)},${Y(v[0])}`, `${X(0)},${Y(v[0])}`].join(' ')} fill={T.ink3} opacity={0.22 * o} />; })}
        <polygon points={band(0, k - 1, undefined, cx)} fill={T.ink3} opacity={0.28 * preO} />
        <polygon points={band(k, N - 1, cx)} fill={T.accent} opacity={0.22 * postO} />
        <g clipPath={`url(#cov${p.seed})`}>
          <path d={path(p.b.v)} fill="none" stroke={T.ink2} strokeWidth={wA_('b')} strokeDasharray="16 10" strokeLinejoin="round" />
          <path d={path(p.a.v)} fill="none" stroke={T.ink} strokeWidth={wA_('a')} strokeLinejoin="round" />
          {p.a.v.map((v, i) => <circle key={'a' + i} cx={X(i)} cy={Y(v)} r={6} fill={T.ink} />)}
          {p.b.v.map((v, i) => <circle key={'b' + i} cx={X(i)} cy={Y(v)} r={6} fill={T.ink2} />)}
        </g>
        <HandCircle cx={cx} cy={cy} rx={(X1 - X0) / (N - 1) * 0.9} ry={56} p={g(f, wA + 10, 22, Easing.inOut(Easing.quad))} />
      </svg>
      {p.ticks.map((tk) => <div key={tk} style={lab({left: X0 - 300, top: Y(tk) - 16, width: 80, textAlign: 'right', fontWeight: 500, fontSize: 26, color: T.ink3, opacity: g(f, 6, 12)})}>{tk}%</div>)}   {/* 눈금은 끝까지(축이 3.6%부터라 칠한 면 크기를 재는 자 — 레드팀 11/3) */}
      {p.months.map((m, i) => (i % 3 === 0 || i === N - 1) ? <div key={i} style={lab({left: X(i) - 80, top: YB + 22, width: 160, textAlign: 'center', fontWeight: i === k ? 800 : 500, fontSize: i === k ? 34 : 28, color: i === k && postO > 0 ? T.accent : T.ink3, opacity: g(f, 8, 12)})}>{m}</div> : null)}
      {k % 3 !== 0 ? <div style={lab({left: X(k) - 80, top: YB + 22, width: 160, textAlign: 'center', fontWeight: 800, fontSize: 34, color: T.accent, opacity: postO})}>{p.months[k]}</div> : null}
      {/* 선 이름 — 그어질 때부터 끝에 */}
      <div style={lab({left: X1 + 20, top: Y(p.a.v[N - 1]) + (sideA ? -132 : 80), fontWeight: 800, fontSize: 40, color: T.ink, opacity: g(f, dA + 30, 12)})}>{p.a.name}</div>
      <div style={lab({left: X1 + 20, top: Y(p.b.v[N - 1]) + (sideA ? 80 : -132), fontWeight: 800, fontSize: 40, color: T.ink2, opacity: g(f, dA + 30, 12)})}>{p.b.name}</div>
      {ends(p.a, g(f, aA, 12), T.ink, 18, sideA)}
      {ends(p.b, g(f, bA, 12), T.ink2, -18, !sideA)}
      <div style={lab({left: X0 + 10, top: YT - 40, fontWeight: 800, fontSize: 48, color: T.ink, opacity: preO * (1 - postO * 0.6)})}>{p.start.text}</div>
      <div style={lab({left: cx - 340, top: cy + 76 + (1 - postO) * 12, width: 680, textAlign: 'center', fontWeight: 800, fontSize: 64, color: T.accent, opacity: postO})}>{p.swap.text}</div>
    </div>
  );
};
