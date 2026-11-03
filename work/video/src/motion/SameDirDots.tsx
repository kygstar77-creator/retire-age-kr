// 같은 쪽 달 점판(SameDirDots) — K-1 '4. 미국 때문일까' 163달 방향 맞추기(2026-11-03 motion). TallyFrame 자식.
// 판 둘(왼·오), 한 줄 = 한 해, 한 칸 = 한 달. 말이 판을 부르면 첫 달부터 칸이 차례로 찍힌다:
// 같은 쪽 = 먹 점, 반대 = 빈 동그라미, 한쪽 그대로 = 짧은 줄. 세는 숫자 = 지금 찍힌 먹 점 수(가짜 중간 숫자 없음).
// 왼쪽(답)만 다 차면 주황. 'swap' 줄에서 왼쪽 판 이름이 바뀌고, 달라지는 칸만 한 번 튀며 바뀐다 → 숫자도 그 칸 수만큼 오른다.
// 정직성: 칸 순서 = 달 순서(원자료 그대로), 점 수 = calc4 같은 쪽 달 수(k1props assert). '닮았다'까지만 — 원인 글자 없음(대본 89줄).
// 두 지표가 같은 쪽으로 움직인 날·달 수 주제에 다시 쓴다. 편마다 seed로 판 간격·찍히는 빠르기가 바뀐다.
// 글자는 전부 HTML(10/13 교훈). 판 전체 1.00→1.03 다가가기(U5 10/19).
import React from 'react';
import {interpolate, useCurrentFrame, Easing, random} from 'remotion';
import {T, F, CL} from '../parts/fm';

type Grid = {name: string; m: number[]; same: number; at: number};
export type SameDirDotsProps = {
  seed: string; first: string; n: number;          // first = 첫 칸 달 'YYYYMM'
  legend: [string, string, string]; legendAt: number;
  left: Grid; right: Grid; swap: Grid; swapR?: Grid; unit: string;   // swapR = 오른쪽도 같은 기준으로(짝 맞춤, 11/3 심사)
  beats: number[];
};

const out = Easing.out(Easing.cubic);
const g = (f: number, a: number, d = 14, e = out) => interpolate(f, [a, a + d], [0, 1], {...CL, easing: e});

const Mark: React.FC<{x: number; y: number; k: number; s: number}> = ({x, y, k, s}) =>
  k > 0 ? <circle cx={x} cy={y} r={11 * s} fill={T.ink} />
    : k < 0 ? <circle cx={x} cy={y} r={10 * s} fill="none" stroke={T.ink2} strokeWidth={3} />
      : <line x1={x - 9 * s} x2={x + 9 * s} y1={y} y2={y} stroke={T.ink3} strokeWidth={4} strokeLinecap="round" />;

export const SameDirDots: React.FC<SameDirDotsProps> = (p) => {
  const f = useCurrentFrame();
  const r = (k: string) => random(p.seed + k);
  const B = p.beats; const at = (x: number) => { const i = Math.floor(x); const a = B[i] ?? 1e9; const n = (B[i + 1] ?? a + 150) - a; return a + n * (x - i); };
  const y0 = +p.first.slice(0, 4), m0 = +p.first.slice(4) - 1;   // 첫 칸 = y0년 (m0+1)월
  const rows = Math.ceil((m0 + p.n) / 12);
  const CW = 40, RH = 30, GW = CW * 12;
  const gap = 180 + Math.round(r('g') * 60);
  const LX = 960 - gap / 2 - GW, RX = 960 + gap / 2, GY = 370;   // 14줄 × 30 = 420 → 보기 줄 820, 자막 띠(940~) 위
  const step = 0.36 + r('s') * 0.08;                  // 칸 하나 = 프레임(163칸 ≈ 60~72프레임)
  const endF = (B[B.length - 1] ?? 0) + 150;
  const push = interpolate(f, [0, endF], [1, 1.03], CL);
  const lA = at(p.left.at), rA = at(p.right.at), sA = at(p.swap.at);
  const cell = (j: number, gx: number) => { const q = m0 + j; return [gx + (q % 12) * CW + CW / 2, GY + Math.floor(q / 12) * RH + RH / 2] as const; };
  const diff = p.left.m.map((k, j) => k !== p.swap.m[j] ? j : -1).filter((j) => j >= 0);
  const flipAt = (j: number) => sA + 10 + diff.indexOf(j) * 1.2;
  const leftMark = (j: number) => (diff.includes(j) && f >= flipAt(j) ? p.swap.m[j] : p.left.m[j]);
  const diffR = p.swapR ? p.right.m.map((k, j) => k !== p.swapR!.m[j] ? j : -1).filter((j) => j >= 0) : [];
  const flipR = (j: number) => sA + 10 + diffR.indexOf(j) * 1.2;
  const rightMark = (j: number) => (p.swapR && diffR.includes(j) && f >= flipR(j) ? p.swapR.m[j] : p.right.m[j]);
  const nowL = p.left.m.map((_, j) => (f >= lA + j * step ? (leftMark(j) > 0 ? 1 : 0) : 0) as number).reduce((a, b) => a + b, 0);
  const nowR = p.right.m.reduce((a, _, j) => a + (f >= rA + j * step && rightMark(j) > 0 ? 1 : 0), 0);
  const leftDone = f >= lA + (p.n - 1) * step;
  const nameSwap = g(f, sA, 14);
  const lab = (s: React.CSSProperties) => ({position: 'absolute' as const, ...F, whiteSpace: 'nowrap' as const, ...s});
  const ghost = (gx: number, o: number) => Array.from({length: p.n}, (_, j) => { const [x, y] = cell(j, gx); return <circle key={j} cx={x} cy={y} r={3} fill={T.ink3} opacity={0.45 * o} />; });
  const pop = (start: number, j: number) => { const t = f - (start + j * step); return t < 0 ? 0 : t > 6 ? 1 : 1 + 0.35 * Math.sin(t / 6 * Math.PI); };
  const head = (gx: number, name: string, cnt: number, col: string, o: number, alt?: {name: string; o: number}) => <>
    <div style={lab({left: gx, top: GY - 150, width: GW, textAlign: 'center', fontWeight: 800, fontSize: 40, color: T.ink, opacity: o * (1 - (alt?.o ?? 0))})}>{name}</div>
    {alt ? <div style={lab({left: gx, top: GY - 150 + (1 - alt.o) * 12, width: GW, textAlign: 'center', fontWeight: 800, fontSize: 40, color: T.ink, opacity: alt.o})}>{alt.name}</div> : null}
    <div style={lab({left: gx, top: GY - 100, width: GW, textAlign: 'center', opacity: o})}>
      <span style={{fontWeight: 700, fontSize: 32, color: T.ink2}}>{p.unit} </span>
      <span style={{fontWeight: 800, fontSize: 72, letterSpacing: -2, color: col}}>{cnt}</span>
      <span style={{fontWeight: 800, fontSize: 44, color: col}}>달</span>
    </div>
  </>;
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, transform: `scale(${push})`, transformOrigin: '50% 55%'}}>
      <svg style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080}}>
        {ghost(LX, g(f, 0, 16))}{ghost(RX, g(f, 0, 16))}
        {p.left.m.map((_, j) => { const s = pop(lA, j); if (!s) return null; const [x, y] = cell(j, LX);
          const fl = diff.includes(j) && f >= flipAt(j) ? 1 + 0.5 * Math.sin(Math.min(1, (f - flipAt(j)) / 8) * Math.PI) : 1;
          return <Mark key={j} x={x} y={y} k={leftMark(j)} s={s * fl} />; })}
        {p.right.m.map((_, j) => { const s = pop(rA, j); if (!s) return null; const [x, y] = cell(j, RX);
          const fl = diffR.includes(j) && f >= flipR(j) ? 1 + 0.5 * Math.sin(Math.min(1, (f - flipR(j)) / 8) * Math.PI) : 1;
          return <Mark key={j} x={x} y={y} k={rightMark(j)} s={s * fl} />; })}
      </svg>
      {/* 해 이름 — 처음·끝 줄만(작은 글자 줄이기) */}
      {[0, rows - 1].map((rw) => <div key={rw} style={lab({left: LX - 110, top: GY + rw * RH + 2, width: 96, textAlign: 'right', fontWeight: 500, fontSize: 26, color: T.ink3, opacity: g(f, 6, 12)})}>{y0 + rw}년</div>)}
      {/* 보기 — 판 아래 가운데 한 줄 */}
      <div style={lab({left: 0, width: 1920, top: GY + rows * RH + 30, display: 'flex', justifyContent: 'center', gap: 56, opacity: g(f, at(p.legendAt), 14)})}>
        {p.legend.map((t, i) => <div key={i} style={{display: 'flex', alignItems: 'center', gap: 14}}>
          <svg width={28} height={28}><Mark x={14} y={14} k={[1, -1, 0][i]} s={1} /></svg>
          <span style={{...F, fontWeight: 700, fontSize: 34, color: T.ink2}}>{t}</span></div>)}
      </div>
      {head(LX, p.left.name, nowL, leftDone && f >= lA ? T.accent : T.ink, g(f, lA - 6, 12), {name: p.swap.name, o: nameSwap})}
      {head(RX, p.right.name, nowR, T.ink, g(f, rA - 6, 12), p.swapR ? {name: p.swapR.name, o: nameSwap} : undefined)}
    </div>
  );
};
