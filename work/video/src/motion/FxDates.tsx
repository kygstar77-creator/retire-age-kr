// 환율 선 + 바꾼 날 네 개 → 같은 1억 막대(FxDates) — X-1 '1. 왜 날짜가 네 개인가'·'2. 달러로만 바꿔 뒀다면'(2026-10-16 motion). TallyFrame 자식.
// phase 'line'(1장): 선이 그려지고 → 가장 높던 날과 지금 선 사이 빨간 폭('제일 나쁜 날') → 말에 맞춰 날짜 점 네 개.
// phase 'bars'(2장): 선 판이 왼쪽으로 줄고 오른쪽에 같은 1억 막대 네 개(날짜 순) → 말 순서대로 막대가 10/12 원화 값으로 내려앉음.
//   왼쪽 빨간 세로 = 그날보다 내린 환율, 오른쪽 빨간 틈 = 줄어든 원화(같은 색 = 같은 원인). 막대 높이는 0부터 값 비례.
// 정직성: 선은 ECOS 일별 원문 그대로, 글자 숫자는 props(calc_out·대본 원문)만. 날짜 순서는 바꾸지 않는다(순위로 읽힘 방지).
// 글자는 전부 HTML(SVG <text> mp4 어긋남 10/13 교훈). 카메라 변형 없음.
import React from 'react';
import {interpolate, useCurrentFrame, Easing, random, spring, useVideoConfig} from 'remotion';
import {T, F, CL} from '../parts/fm';

export type FxMark = {i: number; name: string; date: string; rate: string; won: number; pct: string; say: string};
export type FxDatesProps = {
  seed: string; phase: 'line' | 'bars';
  vals: number[]; min: number; max: number; yticks: [number, string][]; months: [number, string][];
  now: number; nowText: string; nowAll: string;
  marks: FxMark[]; peak: number; peakTag: string; markAt: number[];
  fill: number[]; base: number; baseText: string; allDown: string; barHead: string; legendDrop: string; legendGap: string;
  b1: number[]; b2: number[];
};

const out = Easing.out(Easing.cubic);
const g = (f: number, a: number, d = 16) => interpolate(f, [a, a + d], [0, 1], {...CL, easing: out});

export const FxDates: React.FC<FxDatesProps> = (p) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const r = (k: string) => random(p.seed + k);
  const bars = p.phase === 'bars';
  const n = p.vals.length;
  const sp = (a: number) => spring({frame: f - a, fps, config: {damping: 14}});
  // 판 y 236~852 · 위 254~330 [자막] 띠 → 그래프 y 400~790.
  const sh = bars ? g(f, 0, 24) : 0;                     // 2장 첫 0.8초에 선 판이 왼쪽으로
  const X0 = 280 + Math.round(r('x') * 24), X1 = 1680 - sh * 860;
  const YT = 410, YB = 780;
  const X = (i: number) => X0 + i / (n - 1) * (X1 - X0);
  const Y = (v: number) => YB - (v - p.min) / (p.max - p.min) * (YB - YT);
  const B1 = p.b1, B2 = p.b2;
  // 1장 시점
  const draw = bars ? 1 : interpolate(f, [B1[0] + 4, B1[0] + (B1[1] - B1[0]) * 0.7], [0, 1], {...CL, easing: Easing.inOut(Easing.cubic)});
  const nowIn = bars ? 1 : g(f, B1[1], 20);
  const peakGap = bars ? 0 : g(f, B1[1] + 16, 18) * (1 - g(f, B1[2] + 6, 14));
  const pk = p.marks[p.peak];
  const markOn = (k: number) => bars ? 1 : (k === p.peak ? sp(B1[0] + (B1[1] - B1[0]) * 0.7 * pk.i / (n - 1) + 6) : sp(p.markAt[k]));
  const nameOn = (k: number) => bars ? 0 : (k === p.peak ? g(f, B1[0] + (B1[1] - B1[0]) * 0.7) : g(f, p.markAt[k], 10));
  // 2장 시점: 막대 k가 말 줄 fill.indexOf(k)+1에서 내려앉음
  const dropAt = (k: number) => B2[p.fill.indexOf(k) + 1] + 8;
  const dk = (k: number) => bars ? g(f, dropAt(k), 22) : 0;
  const allAt = bars ? B2[5] : 1e9, lowAt = bars ? B2[6] : 1e9;
  const pulse = (a: number) => f >= a ? 0.5 + 0.5 * Math.cos(Math.min(1, (f - a) / 24) * Math.PI * 2) : 1;
  // 선 경로(그려진 만큼)
  const m = Math.max(1, Math.round(draw * (n - 1)));
  const path = p.vals.slice(0, m + 1).map((v, i) => `${i ? 'L' : 'M'}${X(i).toFixed(1)},${Y(v).toFixed(1)}`).join(' ');
  const yn = Y(p.now);
  // 막대 자리(오른쪽 x 1000~1760)
  const bw = 112 + Math.round(r('bw') * 24), gap = 70 + Math.round(r('bg') * 20);
  const BX0 = 1000 + Math.round(r('bx') * 30);
  const BX = (k: number) => BX0 + k * (bw + gap);
  const BY0 = 790, BH = 320;                              // 0원 = y 790, 1억 = y 470
  const by = (won: number) => BY0 - won / p.base * BH;
  const barIn = bars ? sp(B2[0] + 10) : 0;
  const hot = (k: number) => bars && f >= dropAt(k) && f < (B2[p.fill.indexOf(k) + 2] ?? 1e9);   // 지금 말하는 날
  return (
    <>
      <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
        {p.yticks.map(([v], i) => <line key={i} x1={X0 - 16} x2={X1 + 10} y1={Y(v)} y2={Y(v)} stroke={T.line} strokeWidth={2} />)}
        <path d={path} fill="none" stroke={T.ink2} strokeWidth={4} strokeLinejoin="round" />
        {/* 지금 선(10/12 값) — 오른쪽에서 쓸며 */}
        {nowIn > 0 && <line x1={X1 - nowIn * (X1 - X0)} x2={X1 + 10} y1={yn} y2={yn} stroke={T.accent} strokeWidth={5} strokeDasharray="16 10" />}
        {/* 1장: 가장 높던 날 → 지금 선 빨간 폭 */}
        {peakGap > 0 && <rect x={X(pk.i) - 10} y={Y(p.vals[pk.i])} width={20} height={(yn - Y(p.vals[pk.i])) * peakGap} rx={4} fill={T.rise} opacity={0.85} />}
        {/* 2장: 날마다 내린 환율(빨간 세로) */}
        {bars && p.marks.map((mk, k) => { const d = dk(k); return d > 0 && <line key={k} x1={X(mk.i)} x2={X(mk.i)} y1={Y(p.vals[mk.i])} y2={Y(p.vals[mk.i]) + (yn - Y(p.vals[mk.i])) * d} stroke={T.rise} strokeWidth={hot(k) ? 9 : 6} strokeLinecap="round" opacity={f >= lowAt ? pulse(lowAt) : 1} />; })}
        {/* 점 */}
        {p.marks.map((mk, k) => { const o = markOn(k); const big = (bars && hot(k)) || (!bars && k === p.peak && f >= B1[1]);
          return <circle key={k} cx={X(mk.i)} cy={Y(p.vals[mk.i])} r={(big ? 15 : 11) * Math.max(0, o)} fill={T.ink} stroke={T.surface} strokeWidth={4} opacity={Math.min(1, Math.max(0, o))} />; })}
        <circle cx={X(n - 1)} cy={yn} r={11 * Math.max(0, bars ? 1 : sp(B1[2] + L(B1, 2, 0.8)))} fill={T.accent} stroke={T.surface} strokeWidth={4} />
        {/* 막대: 0~값 잉크, 값~1억 빨간 틈 */}
        {bars && p.marks.map((mk, k) => { const top = by(p.base + (mk.won - p.base) * dk(k)); const h0 = (BY0 - top) * barIn;
          return <g key={k}>
            <rect x={BX(k)} y={BY0 - h0} width={bw} height={h0} rx={4} fill={hot(k) ? T.ink : T.ink2} opacity={bars && p.fill.some((q) => hot(q)) && !hot(k) ? 0.45 : 1} />
            {dk(k) > 0 && <rect x={BX(k)} y={by(p.base)} width={bw} height={Math.max(0, top - by(p.base) - 2)} rx={4} fill={T.rise} opacity={0.88 * (f >= allAt ? pulse(allAt) * 0.4 + 0.6 : 1)} />}
          </g>; })}
        {bars && <line x1={BX(0) - 24} x2={BX(3) + bw + 16} y1={by(p.base)} y2={by(p.base)} stroke={T.ink} strokeWidth={3} strokeDasharray="10 8" opacity={g(f, B2[0] + 20)} />}
        {bars && <line x1={BX(0) - 24} x2={BX(3) + bw + 24} y1={BY0} y2={BY0} stroke={T.ink3} strokeWidth={2} opacity={barIn} />}
      </svg>
      {/* 세로 눈금·가로 달 */}
      {p.yticks.map(([v, s], i) => <div key={i} style={{...F, position: 'absolute', left: X0 - 150, width: 130, textAlign: 'right', top: Y(v) - 17, fontSize: 25, fontWeight: 500, color: T.ink3}}>{s}</div>)}
      {p.months.map(([i, s], k) => <div key={k} style={{...F, position: 'absolute', left: X(i) - 50, width: 100, textAlign: 'center', top: YB + 18, fontSize: bars ? 22 : 26, fontWeight: 500, color: T.ink3,
        opacity: (bars ? (k % 2 ? 0 : 1) : 1) * (bars ? 1 : g(f, B1[0] + (B1[1] - B1[0]) * 0.7 * i / (n - 1)))}}>{s}</div>)}
      {/* 선 이름 */}
      <div style={{...F, position: 'absolute', left: X0, top: YT - 62, fontSize: 30, fontWeight: 700, color: T.ink2, opacity: g(f, B1[0] + 2)}}>원/달러 매매기준율</div>
      {/* 지금 값 글자 */}
      {nowIn > 0 && <div style={{...F, position: 'absolute', left: bars ? X0 : X1 - 340, width: 340, textAlign: bars ? 'left' : 'right', top: yn + 14, fontSize: bars ? 26 : 32, fontWeight: 700, color: T.accent, whiteSpace: 'nowrap', opacity: g(f, B1[1] + 10)}}>{p.nowText}</div>}
      {/* 1장: 날짜 이름표(점 위) */}
      {!bars && p.marks.map((mk, k) => { const o = nameOn(k); const up = k % 2 === 0 ? 1 : 0; const px = X(mk.i), py = Y(p.vals[mk.i]);
        const lx = k === 0 ? px + 6 : px - 130, ty = k === 3 || k === 1 ? py + 30 : py - 104 - up * 18;
        return <div key={k} style={{position: 'absolute', left: lx, width: 260, textAlign: k === 0 ? 'left' : 'center', top: ty, opacity: o, transform: `translateY(${(1 - o) * 12}px)`}}>
          <div style={{display: 'inline-block', background: T.surface, borderRadius: 10, padding: '4px 12px', boxShadow: `0 0 0 2px ${T.line}`}}>
          <div style={{...F, fontSize: 30, fontWeight: 700, color: T.ink, whiteSpace: 'nowrap'}}>{mk.name}</div>
          <div style={{...F, fontSize: 24, fontWeight: 500, color: T.ink2, whiteSpace: 'nowrap'}}>{mk.date} · {mk.rate}</div>
          </div>
        </div>; })}
      {/* 1장 둘째 줄: 제일 나쁜 날 띠 */}
      {peakGap > 0.05 && <div style={{position: 'absolute', left: X(pk.i) + 30, top: yn - 104,   /* 10/20 PD: 가운데 높이면 '석 달 전' 이름표(1,507.1원)를 덮음(overlap) — 지금 선 바로 위로 */ opacity: peakGap, background: T.ink, borderRadius: 12, padding: '12px 24px', ...F, fontSize: 32, fontWeight: 700, color: T.dink, whiteSpace: 'nowrap'}}>{p.peakTag}</div>}
      {/* 2장: 막대 머리·이름·값 */}
      {bars && <div style={{...F, position: 'absolute', left: BX(0) - 24, top: 350, fontSize: 28, fontWeight: 700, color: T.ink2, whiteSpace: 'nowrap',
        opacity: barIn * (f >= allAt - 3 && f < lowAt + 16 ? g(f, lowAt + 8, 8) : 1)}}>{p.barHead}</div>}{/* X-1 PD 10/16: '네 날짜 모두' 띠가 덮는 동안 막대 머리를 숨김(overlap 1:07) */}
      {bars && <div style={{...F, position: 'absolute', left: BX(0) - 150, width: 120, textAlign: 'right', top: by(p.base) - 18, fontSize: 28, fontWeight: 700, color: T.ink, opacity: g(f, B2[0] + 20), whiteSpace: 'nowrap'}}>{p.baseText}</div>}
      {bars && p.marks.map((mk, k) => <div key={k} style={{position: 'absolute', left: BX(k) - 40, width: bw + 80, textAlign: 'center', top: BY0 + 10, opacity: barIn}}>
        <div style={{...F, fontSize: 26, fontWeight: 700, color: hot(k) ? T.ink : T.ink2, whiteSpace: 'nowrap'}}>{mk.name}</div>
        <div style={{...F, fontSize: 21, fontWeight: 500, color: T.ink3, whiteSpace: 'nowrap'}}>{mk.date}</div>
      </div>)}
      {bars && p.marks.map((mk, k) => { const o = g(f, dropAt(k) + 14); const ty = by(mk.won) + 14;
        return o > 0 && <div key={k} style={{position: 'absolute', left: BX(k) - 30, width: bw + 60, textAlign: 'center', top: ty, opacity: o}}>
          <div style={{...F, fontSize: 27, fontWeight: 700, color: T.dink, whiteSpace: 'nowrap'}}>{mk.pct}</div>
        </div>; })}
      {/* 지금 말하는 날의 말 속 금액 — 막대 위 */}
      {bars && p.marks.map((mk, k) => { const o = hot(k) ? g(f, dropAt(k) + 18) : 0;
        return o > 0 && <div key={k} style={{position: 'absolute', left: Math.min(BX(k) + bw / 2 - 180, 1800 - 360), width: 360, textAlign: 'center', top: by(p.base) - 74, opacity: o, ...F, fontSize: 42, fontWeight: 700, color: T.rise, whiteSpace: 'nowrap'}}>{mk.say} ↓</div>; })}
      {/* 2장 여섯째 줄: 네 날짜 모두 */}
      {f >= allAt && f < lowAt + 8 && <div style={{position: 'absolute', left: BX(0) - 24, top: 360 - 4 + (1 - sp(allAt)) * 16, opacity: sp(allAt) * (1 - g(f, lowAt, 8)), background: T.ink, borderRadius: 12, padding: '10px 22px', ...F, fontSize: 30, fontWeight: 700, color: T.dink, whiteSpace: 'nowrap'}}>{p.allDown}</div>}
      {/* 2장 일곱째 줄: 지금 환율이 네 날보다 다 낮다 */}
      {f >= lowAt && <div style={{position: 'absolute', left: X0 + 10, top: 640 + (1 - sp(lowAt)) * 16, opacity: sp(lowAt), background: T.ink, borderRadius: 12, padding: '10px 22px', ...F, fontSize: 28, fontWeight: 700, color: T.dink, whiteSpace: 'nowrap'}}>{p.nowAll}</div>}
      {/* 범례(2장) */}
      {bars && <div style={{...F, position: 'absolute', left: X0, top: YB + 52, fontSize: 22, fontWeight: 700, color: T.ink2, whiteSpace: 'nowrap', opacity: g(f, dropAt(0) + 10)}}>
        <span style={{display: 'inline-block', width: 8, height: 26, background: T.rise, borderRadius: 3, verticalAlign: 'middle', marginRight: 10}} />{p.legendDrop}
        <span style={{display: 'inline-block', width: 26, height: 18, background: T.rise, borderRadius: 3, verticalAlign: 'middle', margin: '0 10px 0 26px'}} />{p.legendGap}</div>}
    </>
  );
};
// 줄 k 안 비율 q 시점
const L = (B: number[], k: number, q: number) => (B[k + 1] ?? B[k] + 200) - B[k] > 0 ? Math.round(((B[k + 1] ?? B[k] + 200) - B[k]) * q) : 0;
