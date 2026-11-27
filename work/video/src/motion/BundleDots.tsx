// 묶음 점 그림(BundleDots) — NDG-1 3장 '2021년 꼭대기의 몇 %'(2026-11-27 motion). TallyFrame 자식. H-6 DealDots를 고쳐 씀:
// 가로 = 날짜가 아니라 묶음(같은 단지·같은 면적) 하나하나, 세로 = 2021 최고 대비 %(100% 선 = 그때 꼭대기).
// 줄마다 화면에 새 일 하나(U5): ① 점이 아무 순서로 떨어짐 → 낮은 것부터 줄 서기(가운데 점 = 가운데 값) → 답 자리 '?'
// ② '?' → 가운데 값 열고 손 동그라미 + 100% 선까지 괄호 ③ 80% 선 내려옴 ④ 100% 위 점 주황 + 개수 ⑤ 80% 아래 점 먹색 + 개수.
// 주황은 '넘은 곳' 하나만(앞의 가운데 값 답은 ④에서 먹색으로). 세로 축은 0%부터가 아니다 → 물결 끊김 + 눈금 글자 늘 보임(11/1 교훈).
// 숫자는 전부 props(편 스크립트가 calc 출력에서 만들고 assert). 반복 방지: seed로 떨어지는 순서·여백·카메라 쪽을 바꾼다.
import React from 'react';
import {interpolate, useCurrentFrame, Easing, random} from 'remotion';
import {T, F, CL, HandCircle} from '../parts/fm';

export type BundleDotsProps = {
  seed: string;
  r: number[];                                       // 묶음마다 지금/2021최고(1 = 100%), 들어온 순서 그대로
  min: number; max: number; ticks: number[];        // % 단위
  axis: string;                                      // 세로 축 이름
  topLine: string;                                   // 100% 선 이름
  dropAt: number; sortAt: number;
  mid: {v: number; text: string; ask: string; at: number};
  lowLine: {v: number; text: string; at: number};
  over: {text: string; at: number};
  under: {text: string; at: number};
  beats: number[];
};

const io = Easing.inOut(Easing.cubic), out = Easing.out(Easing.cubic);
const g = (f: number, a: number, d = 14, e = out) => interpolate(f, [a, a + d], [0, 1], {...CL, easing: e});

export const BundleDots: React.FC<BundleDotsProps> = (p) => {
  const f = useCurrentFrame();
  const rnd = (k: string) => random(p.seed + k);
  const B = p.beats; const at = (x: number) => { if (x < 0) return -1e9; const i = Math.floor(x); const a = B[i] ?? 1e9; const n = (B[i + 1] ?? a + 150) - a; return a + n * (x - i); };
  const N = p.r.length;
  const X0 = 300 + Math.round(rnd('x') * 40), X1 = 1600, YT = 300, YB = 800;
  const Y = (pct: number) => YB - (pct - p.min) / (p.max - p.min) * (YB - YT);
  const XI = (i: number) => X0 + (i + 0.5) / N * (X1 - X0);
  // 줄 서기 자리: 낮은 것부터
  const order = p.r.map((v, i) => [v, i] as [number, number]).sort((a, b) => a[0] - b[0] || a[1] - b[1]);
  const rank = new Array<number>(N); order.forEach(([, i], k) => { rank[i] = k; });
  const midK = Math.floor((N - 1) / 2);
  // 떨어지는 순서(seed) — 들어온 순서를 섞는다
  const fall = p.r.map((_, i) => rnd('f' + i));
  const dA = at(p.dropAt), sA = at(p.sortAt), mA = at(p.mid.at), lA = at(p.lowLine.at), oA = at(p.over.at), uA = at(p.under.at);
  const dropLen = Math.max(40, sA - dA - 10);
  const sortP = g(f, sA, 50, io);
  const endF = (B[B.length - 1] ?? 0) + 200;
  // 카메라: 늘 천천히 다가감(U5), 가운데 값 줄엔 가운데 점 쪽, 넘은 곳 줄엔 오른쪽 위, 80% 아래 줄엔 왼쪽 아래로 옮겨 간다
  const push = interpolate(f, [0, endF], [1, 1.035], CL);
  const zm = g(f, mA, 36, io) * (1 - g(f, lA, 36, io));
  const zo = g(f, oA, 36, io) * (1 - g(f, uA, 36, io)), zu = g(f, uA, 36, io);
  const z = push * (1 + 0.12 * zm + 0.08 * zo + 0.08 * zu);
  const cx0 = (X0 + X1) / 2, cy0 = (YT + YB) / 2;
  const wsum = zm + zo + zu + 1e-6;
  const tx = (XI(midK) * zm + (X0 + (X1 - X0) * 0.85) * zo + (X0 + (X1 - X0) * 0.12) * zu) / wsum, ty = (Y(p.mid.v) * zm + Y(112) * zo + Y(72) * zu) / wsum;
  const w = Math.min(1, wsum);
  const ox = cx0 * (1 - w) + tx * w, oy = cy0 * (1 - w) + ty * w;
  const lab = (s: React.CSSProperties) => ({position: 'absolute' as const, ...F, whiteSpace: 'nowrap' as const, ...s});
  const askO = g(f, sA + 40, 12) * (1 - g(f, mA, 8));
  const midO = g(f, mA + 4, 12);
  const midAcc = f < oA;                              // 다음 답(넘은 곳)이 열리면 가운데 값은 먹색
  const lowO = g(f, lA, 24, io);
  const oO = g(f, oA, 16), uO = g(f, uA, 16);
  const xm = XI(midK), ym = Y(p.mid.v);
  const nOver = p.r.filter((v) => v >= 1).length, nUnder = p.r.filter((v) => v < 0.8).length;
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, transform: `translate(${ox * (1 - z)}px, ${oy * (1 - z)}px) scale(${z})`, transformOrigin: '0 0'}}>
      <svg style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080}}>
        {p.ticks.filter((t) => t !== 100).map((t) => <line key={t} x1={X0} x2={X1} y1={Y(t)} y2={Y(t)} stroke={T.ink3} strokeOpacity={0.3} strokeWidth={2} />)}
        {/* 바닥 끊김(0%부터가 아님) */}
        <polyline points={`${X0 - 56},${YB + 14} ${X0 - 40},${YB - 2} ${X0 - 24},${YB + 18} ${X0 - 8},${YB + 2}`} fill="none" stroke={T.ink} strokeWidth={5} opacity={g(f, 4, 12)} />
        {/* 100% 선 — 그때 꼭대기 */}
        <line x1={X0} x2={X0 + (X1 - X0) * g(f, 6, 30, io)} y1={Y(100)} y2={Y(100)} stroke={T.ink} strokeWidth={5} />
        {/* 80% 선 — 위에서 내려와 자리 잡는다 */}
        <line x1={X0} x2={X1} y1={Y(p.lowLine.v) - (1 - lowO) * 60} y2={Y(p.lowLine.v) - (1 - lowO) * 60} stroke={T.ink} strokeWidth={4} strokeDasharray="14 10" opacity={lowO} />
        {/* 점 — 섞인 순서로 떨어지고, 낮은 것부터 줄 선다 */}
        {p.r.map((v, i) => {
          const s = g(f, dA + fall[i] * dropLen, 10, Easing.out(Easing.back(2)));
          if (s <= 0) return null;
          const x0 = X0 + fall[i] * (X1 - X0), x = x0 + (XI(rank[i]) - x0) * sortP, y = Y(v * 100) - (1 - s) * 40;
          const isOver = v >= 1, isUnder = v < 0.8, isMid = rank[i] === midK;
          const fill = isOver && f >= oA ? T.accent : isUnder && f >= uA ? T.ink : isMid && f >= mA ? T.ink : T.ink3;
          const fade = (f >= oA && !isOver && !(isUnder && f >= uA)) ? 1 - 0.45 * Math.min(oO, 1 - uO * (isUnder ? 1 : 0)) : 1;
          return <circle key={i} cx={x} cy={y} r={isMid && f >= mA && f < oA ? 10 : 7} fill={fill} opacity={s * fade * 0.9} />;
        })}
        {/* 가운데 값 — 손 동그라미 + 100% 선까지 괄호 */}
        <HandCircle cx={xm} cy={ym} rx={34} ry={30} p={g(f, mA + 6, 20, Easing.inOut(Easing.quad)) * (1 - g(f, oA, 10))} color={midAcc ? T.accent : T.ink} />
        <path d={`M${xm + 52} ${Y(100)}h16V${ym}h-16`} fill="none" stroke={T.ink} strokeWidth={5} strokeLinejoin="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - g(f, mA + 30, 20)} opacity={1 - g(f, oA, 10)} />
      </svg>
      {/* 눈금 글자 — 늘 보인다(바닥 자른 축) */}
      {p.ticks.map((t) => <div key={t} style={lab({left: X0 - 150, top: Y(t) - 18, width: 120, textAlign: 'right', fontWeight: t === 100 ? 700 : 500, fontSize: 30, color: t === 100 ? T.ink : T.ink3, opacity: g(f, 4, 12)})}>{t}%</div>)}
      <div style={lab({left: X0 - 150, top: YT - 40, fontWeight: 700, fontSize: 34, color: T.ink2, opacity: g(f, 4, 12)})}>{p.axis}</div>
      <div style={lab({left: X1 - 600, top: Y(100) - 58, width: 600, textAlign: 'right', fontWeight: 700, fontSize: 36, color: T.ink, opacity: g(f, 20, 12) * (1 - oO * 0.6)})}>{p.topLine}</div>
      <div style={lab({left: X1 - 400, top: Y(p.lowLine.v) + 12, width: 400, textAlign: 'right', fontWeight: 700, fontSize: 36, color: T.ink, opacity: g(f, lA + 16, 12)})}>{p.lowLine.text}</div>
      {/* 답 자리 '?' → 가운데 값 */}
      <div style={lab({left: xm - 140, top: ym + 44, width: 280, textAlign: 'center', fontWeight: 700, fontSize: 96, color: T.ink2, opacity: askO})}>{p.mid.ask}</div>
      <div style={lab({left: xm - 200, top: ym + 40 + (1 - midO) * 14, width: 400, textAlign: 'center', fontWeight: 700, fontSize: 104, letterSpacing: -2, color: midAcc ? T.accent : T.ink, opacity: midO * (1 - 0.65 * oO)})}>{p.mid.text}</div>
      {/* 넘은 곳 · 80% 아래 — 점 무리 옆에 개수 */}
      <div style={lab({left: X0 + (X1 - X0) * (1 - nOver / N) - 40, top: Y(Math.min(p.max - 6, 118)) - 120 + (1 - oO) * 12, width: 420, textAlign: 'center', fontWeight: 700, fontSize: 72, color: T.accent, opacity: oO})}>{p.over.text}</div>
      <div style={lab({left: X0 + (X1 - X0) * (nUnder / N) + 30, top: Y(p.min + 6) - 20 + (1 - uO) * 12, fontWeight: 700, fontSize: 72, color: T.ink, opacity: uO})}>{p.under.text}</div>
    </div>
  );
};
