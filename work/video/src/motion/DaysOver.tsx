// 선 넘은 날 세기(DaysOver) — K-1 '1. 미국 국채금리 5%' 일별 선(2026-11-03 motion). TallyFrame 자식.
// 일별 선이 그어지고 기준 점선(5%) → 말이 '처음 닿은 날'에 가면 보는 칸(x·y 범위)이 끝 두 달로 좁혀진다(카메라 확대가 아니라 축을 다시 잡아 선이 굵어지지 않음).
// 넘은 날마다 점이 하나씩 찍히고 세는 숫자 = 지금 찍힌 점 수(가짜 중간 숫자 없음), 다 차면 주황. 최고점은 먹 손 동그라미.
// 지난번(past) 줄에서 다시 전체로 물러나 그 달 칸에 옅은 띠 + 그 달 평균 짧은 선(주황은 이때 평균 글자로 넘어감).
// 금리·환율·주가가 '어떤 선을 넘은 날 수' 주제에 다시 쓴다. 편마다 seed로 왼쪽 여백이 바뀐다.
// 글자는 전부 HTML(10/13 교훈). 판 전체 1.00→1.03 다가가기(U5 10/19).
import React from 'react';
import {interpolate, useCurrentFrame, Easing, random} from 'remotion';
import {T, F, CL, HandCircle} from '../parts/fm';

export type DaysOverProps = {
  seed: string;
  v: number[]; min: number; max: number;            // 일별 값(원자료 그대로)
  line: number; lineText: string;                   // 기준 점선
  ticks: number[]; years: {i: number; text: string}[];
  first: {i: number; text: string; at: number};     // 처음 넘은 날 — 이 말에서 끝 두 달로 좁힌다
  days: number[]; countText: string; countN: number; countUnit: string; countAt: number;
  peak: {i: number; text: string; at: number};
  past: {a: number; b: number; name: string; below?: string; text: string; at: number; avg: number; avgAt: number};   // below = 그때 기준선에 못 닿았다는 말(붙어 보여서 — 레드팀 11/3)
  beats: number[];
};

const io = Easing.inOut(Easing.cubic), out = Easing.out(Easing.cubic);
const g = (f: number, a: number, d = 14, e = out) => interpolate(f, [a, a + d], [0, 1], {...CL, easing: e});
const lerp = (a: number, b: number, t: number) => a + (b - a) * t;

export const DaysOver: React.FC<DaysOverProps> = (p) => {
  const f = useCurrentFrame();
  const r = (k: string) => random(p.seed + k);
  const B = p.beats; const at = (x: number) => { const i = Math.floor(x); const a = B[i] ?? 1e9; const n = (B[i + 1] ?? a + 150) - a; return a + n * (x - i); };
  const N = p.v.length;
  const X0 = 200 + Math.round(r('x') * 40), X1 = 1700, YT = 290, YB = 760;   // 아래 글자(해·날짜)가 출처 줄(y 860대)과 겹치지 않게(11/3 눈 검사)
  const endF = (B[B.length - 1] ?? 0) + 150;
  const push = interpolate(f, [0, endF], [1, 1.03], CL);
  // 보는 칸: 전체 → 끝 두 달(넘은 첫날 20거래일 앞부터) → 다시 전체
  const fA = at(p.first.at), cA = at(p.countAt), pA = at(p.peak.at), bA = at(p.past.at), aA = at(p.past.avgAt);
  const zin = g(f, fA, 70, io) * (1 - g(f, bA, 34, io));
  const lo = lerp(0, Math.max(0, p.first.i - 20), zin), hi = N - 1;
  const ymin = lerp(p.min, 4.5, zin), ymax = lerp(p.max, 5.4, zin);
  const X = (i: number) => X0 + (i - lo) / (hi - lo) * (X1 - X0);
  const Y = (v: number) => YB - (v - ymin) / (ymax - ymin) * (YB - YT);
  const draw = g(f, 0, 26, io);
  const last = Math.max(1, Math.floor((N - 1) * draw));
  let d = '';
  for (let i = Math.max(0, Math.floor(lo) - 1); i <= last; i++) d += `${d ? 'L' : 'M'}${X(i).toFixed(1)} ${Y(p.v[i]).toFixed(1)}`;
  const ly = Y(p.line);
  const shown = p.days.filter((_, k) => f >= cA + k * 3).length;
  const cntO = g(f, cA, 10) * (1 - g(f, bA, 16));
  const cntLeft = true;   // 오른쪽 위는 최고점 글자 자리(겹침) — 편마다 바뀌는 건 왼쪽 여백
  const pkO = g(f, pA, 12) * (1 - g(f, bA, 16));
  const pastO = g(f, bA + 30, 16);
  const avgO = g(f, aA, 14);
  const lab = (s: React.CSSProperties) => ({position: 'absolute' as const, ...F, whiteSpace: 'nowrap' as const, ...s});
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, transform: `scale(${push})`, transformOrigin: '50% 60%'}}>
      <svg style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080}}>
        <defs><clipPath id={'dov' + p.seed}><rect x={X0} y={YT - 40} width={X1 - X0 + 30} height={YB - YT + 80} /></clipPath></defs>
        {p.ticks.map((t) => <line key={t} x1={X0} x2={X1} y1={Y(t)} y2={Y(t)} stroke={T.ink3} strokeOpacity={0.35} strokeWidth={2} />)}
        {/* 지난번 그 달 띠 + 평균 짧은 선 */}
        <rect x={X(p.past.a)} y={YT - 20} width={Math.max(6, X(p.past.b) - X(p.past.a))} height={YB - YT + 20} fill={T.ink3} opacity={0.18 * pastO} />
        <line x1={X(p.past.a) - 30} x2={X(p.past.b) + 30} y1={Y(p.past.avg)} y2={Y(p.past.avg)} stroke={T.accent} strokeWidth={6} strokeLinecap="round"
          pathLength={1} strokeDasharray={1} strokeDashoffset={1 - avgO} />
        <line x1={X0} x2={X0 + (X1 - X0 + 20) * g(f, 4, 18)} y1={ly} y2={ly} stroke={T.ink} strokeWidth={4} strokeDasharray="14 10" />
        {/* 넘은 칸 면 — 점이 찍히는 만큼 오른쪽으로 번진다(U5: 점만으론 화면 4%를 못 바꿈) */}
        <clipPath id={'dovu' + p.seed}><rect x={X0} y={0} width={Math.max(0, (p.days[Math.max(0, shown - 1)] !== undefined && shown > 0 ? X(p.days[shown - 1]) - X0 : 0))} height={ly} /></clipPath>
        <path d={`${d}L${X(last).toFixed(1)} ${ly}L${X(Math.max(0, Math.floor(lo))).toFixed(1)} ${ly}Z`} fill={T.ink3} opacity={0.35 * cntO} clipPath={`url(#dovu${p.seed})`} />
        <path d={d} fill="none" stroke={T.ink2} strokeWidth={4} strokeLinejoin="round" clipPath={`url(#dov${p.seed})`} />
        {/* 넘은 날 점 — 하나씩 */}
        {p.days.map((i, k) => { const s = g(f, cA + k * 3, 8); return s > 0 ? <circle key={i} cx={X(i)} cy={Y(p.v[i])} r={10 * s * (0.4 + 0.6 * zin)} fill={T.ink} opacity={1 - g(f, bA, 16) * 0.85} /> : null; })}
        {/* 처음 닿은 날 */}
        <circle cx={X(p.first.i)} cy={Y(p.v[p.first.i])} r={14 * g(f, fA + 30, 10) * (1 - g(f, cA, 10))} fill="none" stroke={T.ink} strokeWidth={4} />
        <HandCircle cx={X(p.peak.i)} cy={Y(p.v[p.peak.i])} rx={40} ry={34} p={g(f, pA + 8, 20, Easing.inOut(Easing.quad)) * (1 - g(f, bA, 10))} color={T.ink} />
      </svg>
      {/* 기준선 이름 — 왼쪽 끝 위 */}
      <div style={lab({left: X0 - 150, top: ly - 26, width: 130, textAlign: 'right', fontWeight: 800, fontSize: 44, color: T.ink, opacity: g(f, 10, 12)})}>{p.lineText}</div>
      {p.ticks.filter((t) => t !== p.line).map((t) => <div key={t} style={lab({left: X0 - 150, top: Y(t) - 16, width: 130, textAlign: 'right', fontWeight: 500, fontSize: 28, color: T.ink3, opacity: g(f, 6, 12) * (Y(t) > YT - 10 && Y(t) < YB + 10 ? 1 : 0)})}>{t}%</div>)}
      {p.years.map((y) => <div key={y.i} style={lab({left: X(y.i) - 60, top: YB + 18, width: 120, textAlign: 'center', fontWeight: 500, fontSize: 28, color: T.ink3, opacity: g(f, 6, 12) * (1 - zin)})}>{y.text}</div>)}
      <div style={lab({left: X(p.first.i) - 200, top: YB + 18, width: 400, textAlign: 'center', fontWeight: 700, fontSize: 36, color: T.ink, opacity: g(f, fA + 30, 12) * (1 - g(f, bA, 12))})}>{p.first.text}</div>
      {/* 세는 숫자 = 지금 찍힌 점 수 */}
      <div style={lab({left: cntLeft ? X0 + 40 : X1 - 560, top: YT - 10, width: 520, textAlign: cntLeft ? 'left' : 'right', opacity: cntO})}>
        <span style={{fontWeight: 700, fontSize: 40, color: T.ink2}}>{p.countText} </span>
        <span style={{fontWeight: 800, fontSize: 96, letterSpacing: -2, color: shown >= p.countN ? T.accent : T.ink}}>{shown}</span>
        <span style={{fontWeight: 800, fontSize: 56, color: shown >= p.countN ? T.accent : T.ink}}>{p.countUnit}</span>
      </div>
      <div style={lab({left: X(p.peak.i) - 420, top: Y(p.v[p.peak.i]) - 104 + (1 - pkO) * 10, width: 400, textAlign: 'right', fontWeight: 800, fontSize: 48, color: T.ink, opacity: pkO})}>{p.peak.text}</div>
      {/* 지난번 — 평균 글자는 띠 오른쪽·5% 선 위(왼쪽은 축 글자, 선 옆은 선과 겹침 — 11/3 눈 검사) */}
      <div style={lab({left: X(p.past.a) - 40, top: YT - 70, fontWeight: 800, fontSize: 48, color: T.ink, opacity: pastO})}>{p.past.name}{p.past.below ? <span style={{fontWeight: 700, fontSize: 34, color: T.ink2}}> · {p.past.below}</span> : null}</div>
      <div style={lab({left: X(p.past.b) + 40, top: Y(p.line) - 78, fontWeight: 800, fontSize: 52, color: T.accent, opacity: avgO})}>{p.past.text}</div>
    </div>
  );
};
