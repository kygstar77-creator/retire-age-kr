// 단지별 1년 변화 가로 막대(GapBars) — H-6 2장 '은마만 내렸나'(2026-11-21 motion). TallyFrame 자식.
// 0선 가운데, 내린 곳은 왼쪽·오른 곳은 오른쪽. 주황은 그 줄의 답 하나(가운데 값 → 은마).
// 줄마다 화면에 새 일 하나(U5): ① 0선이 위→아래로 그어지고 줄마다 점이 하나씩 찍힘(단지 세기) ② '21곳' 찍기
// ③ 내린 곳 막대가 왼쪽으로, 오른 곳이 오른쪽으로 자람 + '내림 14 · 오름 7' ④ 가운데 값 세로 점선 + 그 단지 밑줄
// ⑤ 은마 막대 주황·손 동그라미·'21곳 중 2번째'(옆으로 조금 옮겨 감) ⑥ 은마 막대 중 가운데 값 몫이 회색으로 덮여 넘친 몫만 주황.
// bgcheck ⑥: 막대 두께 18px(852폭 축소 시 8px < 16) — 닫힌 네모로 안 셈. 눈금 칸 없음. 이름표는 은마·가운데 단지 둘만(작은 글자 줄 늘리지 않음).
// 숫자는 전부 props(편 스크립트가 calc3_out과 assert). 반복 방지: seed로 0선 위치·막대 자라는 순서(위→아래/아래→위)·카메라 방향.
import React from 'react';
import {interpolate, useCurrentFrame, Easing, random} from 'remotion';
import {T, F, CL, HandCircle} from '../parts/fm';
import {HandUnderline} from '../parts/human';

export type GapRow = {name: string; v: number; n0: number; n1: number};
export type GapBarsProps = {
  seed: string;
  rows: GapRow[];                         // 변화 오름차순(가장 많이 내린 곳이 위)
  min: number; max: number;               // % 축 끝
  hi: number; mid: number;                // 은마·가운데 단지 줄 번호
  ticks: number[];
  countText: string; downText: string; upText: string;
  hiText: string; hiRank: string; midText: string;
  countAt: number; growAt: number; midAt: number; hiAt: number; backAt: number;
  beats: number[];
};

const io = Easing.inOut(Easing.cubic), out = Easing.out(Easing.cubic);
const g = (f: number, a: number, d = 14, e = out) => interpolate(f, [a, a + d], [0, 1], {...CL, easing: e});

export const GapBars: React.FC<GapBarsProps> = (p) => {
  const f = useCurrentFrame();
  const r = (k: string) => random(p.seed + k);
  const B = p.beats; const at = (x: number) => { if (x < 0) return -1e9; const i = Math.floor(x); const a = B[i] ?? 1e9; const n = (B[i + 1] ?? a + 150) - a; return a + n * (x - i); };
  const N = p.rows.length, YT = 262, YB = 836, RH = (YB - YT) / N, BH = 18;
  const XL = 230, XR = 1600;
  const X = (v: number) => XL + (v - p.min) / (p.max - p.min) * (XR - XL);
  const X0 = X(0);
  const Yc = (i: number) => YT + RH * (i + 0.5);
  const cA = at(p.countAt), grA = at(p.growAt), mA = at(p.midAt), hA = at(p.hiAt), bkA = at(p.backAt);
  const endF = (B[B.length - 1] ?? 0) + 160;
  const upFirst = r('ord') > 0.5;
  // 카메라: 늘 천천히 다가감(1.00→1.04) + 은마 줄에서 그 끝 쪽으로 1.22, 마지막 줄에 물러남
  const push = interpolate(f, [0, endF], [1, 1.04], CL);
  const zin = g(f, hA, 40, io) * (1 - g(f, bkA, 40, io));
  const z = push;   // 은마 줄 다가가기는 빼다 — 1.22면 위 축 글자가 제목에, 아래 줄이 출처 줄에 닿음(스틸 11/21). 줄 일은 주황·동그라미·글자가 맡음
  const hx = X(p.rows[p.hi].v), hy = Yc(p.hi);
  const ox = 960 + (hx + 220 - 960) * zin * 0.5, oy = YT - 70;   // 위(축 글자)는 제자리, 은마 줄에선 그쪽으로 조금 옮겨 감
  const lab = (s: React.CSSProperties) => ({position: 'absolute' as const, ...F, whiteSpace: 'nowrap' as const, ...s});
  // ① 0선 + 점(단지 세기) — 첫 줄 내내
  const zl = g(f, 6, Math.max(30, cA - 20), io);
  const dotGap = Math.max(3, (cA - 40) / N);
  const accMid = f >= mA && f < hA, accHi = f >= hA;
  const mx = X(p.rows[p.mid].v);
  const midO = g(f, mA, 26, io);
  const cntO = g(f, cA, 10, Easing.out(Easing.back(1.6))) * (1 - g(f, grA + 30, 14));
  const udO = g(f, grA + 40, 14) * (1 - g(f, mA, 14));
  const hiO = g(f, hA + 14, 14);
  const arrow = g(f, bkA + 20, 30, io);
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, transform: `translate(${ox * (1 - z)}px, ${oy * (1 - z)}px) scale(${z})`, transformOrigin: '0 0'}}>
      <svg style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080}}>
        <line x1={X0} x2={X0} y1={YT - 20} y2={YT - 20 + (YB - YT + 14) * zl} stroke={T.ink} strokeWidth={5} strokeLinecap="round" />
        {p.rows.map((q, i) => {
          const down = q.v < 0; const k = down ? i : i;                              // 자라는 순서: 내림 위→아래, 오름은 따로
          const di = down ? (upFirst ? i + 7 : i) : (upFirst ? i - 14 : i);
          const s = g(f, 16 + i * dotGap, 22, io);   // 첫 줄 내내 위→아래로 하나씩 자람(심사 11/21: ①② 빈 화면)
          const split = g(f, grA + di * 3, 18);         // ③ 내림·오름 색이 갈라짐
          const w = (X(q.v) - X0) * s;
          const dot = g(f, 10 + i * dotGap, 8, Easing.out(Easing.back(2)));
          const isHi = i === p.hi, isMid = i === p.mid;
          const col = isHi && accHi ? T.accent : isMid && accMid ? T.accent : down ? (split > 0.5 ? T.ink2 : T.ink3) : T.ink3;
          const dim = accHi && !isHi ? (down ? 0.55 : 0.3) - 0.2 * arrow : down ? 1 : 1 - 0.45 * split;   // 오른 곳은 옅게 — 은마보다 눈을 끌지 않게   // 마지막 줄엔 더 옅게 — 화살이 읽히게
          return <g key={k}>
            <circle cx={X0} cy={Yc(i)} r={6} fill={T.ink2} opacity={dot * (1 - s)} />
            {s > 0 ? <rect x={Math.min(X0, X0 + w)} y={Yc(i) - BH / 2} width={Math.abs(w)} height={BH} rx={3} fill={col} opacity={dim} /> : null}
          </g>;
        })}
        {/* 가운데 값 — 세로 점선이 위→아래 */}
        <line x1={mx} x2={mx} y1={YT - 30} y2={YT - 30 + (YB - YT + 24) * midO} stroke={accMid ? T.accent : T.ink} strokeWidth={4} strokeDasharray="12 9" opacity={midO > 0 ? 1 : 0} />
        {/* 은마 끝 손 동그라미 */}
        <HandCircle cx={hx + 2} cy={hy} rx={40} ry={28} p={g(f, hA + 8, 20, Easing.inOut(Easing.quad))} color={T.ink} />
        {/* 마지막 줄: 가운데 선 → 은마 끝 화살(숫자 더하지 않음) */}
        <rect x={mx} y={hy - BH / 2 - 1} width={(X0 - mx) * arrow} height={BH + 2} rx={3} fill={T.ink3} />   {/* 마지막 줄: 은마 막대 중 '가운데 단지만큼'은 먹회색, 넘친 몫만 주황으로 남음(화살은 주황 막대에 묻혀 안 보였음) */}
      </svg>
      <HandUnderline x={X0 + 24} y={Yc(p.mid) + 26} w={300} p={g(f, mA + 18, 18, io) * (1 - g(f, hA, 12))} color={T.accent} seed={3} stroke={6} />
      {/* 축 끝 글자 — 0선 위 */}
      <div style={lab({left: X0 - 60, top: YT - 70, width: 120, textAlign: 'center', fontWeight: 700, fontSize: 32, color: T.ink2, opacity: g(f, 6, 12)})}>0%</div>
      {/* 눈금 글자 — 0선 줄 높이(선은 긋지 않음: 막대와 만나 칸이 되면 bgcheck ⑥) */}
      {p.ticks.map((t) => <div key={t} style={lab({left: X(t) - 70, top: YT - 70, width: 140, textAlign: 'center', fontWeight: 500, fontSize: 30, color: T.ink3, opacity: g(f, 6, 12)})}>{t > 0 ? '+' : '−'}{Math.abs(t)}%</div>)}
      {/* ② 21곳 찍기 */}
      <div style={lab({left: X0 + 150, top: YT + 70, fontWeight: 800, fontSize: 150, letterSpacing: -4, color: T.ink, opacity: cntO, transform: `scale(${1.25 - 0.25 * g(f, cA, 10)})`, transformOrigin: 'left center'})}>{p.countText}</div>
      {/* ③ 내림·오름 수 — 그 막대 묶음 바로 옆(재심사 11/21: 떨어진 빈자리면 어느 묶음인지 안 이어짐) */}
      <div style={lab({left: XL, top: Yc(11) - 50, fontWeight: 800, fontSize: 72, color: T.ink2, opacity: udO})}>{p.downText}</div>
      <div style={lab({left: X(14), top: Yc(15) - 50, fontWeight: 800, fontSize: 72, color: T.ink3, opacity: udO})}>{p.upText}</div>
      {/* ④ 가운데 단지 */}
      <div style={lab({left: X0 + 24, top: Yc(p.mid) - 34, fontWeight: 800, fontSize: 48, color: accMid ? T.accent : T.ink, opacity: midO * (accHi ? 0.6 + 0.4 * arrow : 1)})}>{p.midText}</div>
      {/* ⑤ 은마 */}
      <div style={lab({left: X0 + 24, top: hy - 40 + (1 - hiO) * 12, fontWeight: 800, fontSize: 56, color: T.accent, opacity: hiO})}>{p.hiText}</div>
      <div style={lab({left: X0 + 24, top: hy + 26, fontWeight: 700, fontSize: 38, color: T.ink, opacity: g(f, hA + 30, 14)})}>{p.hiRank}</div>
    </div>
  );
};
