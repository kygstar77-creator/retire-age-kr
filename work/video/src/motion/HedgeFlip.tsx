// 같은 1억 막대 두 개 — 환노출 vs 환헤지(H)(HedgeFlip) — X-1 v3 '질문 2'(2026-10-17 motion). TallyFrame 자식.
// 세 쌍은 날짜 순 자리(왼쪽 = 옛날), 켜지는 순서만 말을 따른다(order). 막대 높이 0부터 값 비례, 1억 점선.
// 색: 환노출 = 잉크, 환헤지 = fall(파랑), 1억 아래로 줄어든 몫 = rise(빨강), 두 막대 차 = accent 괄호. 글자는 전부 HTML.
import React from 'react';
import {interpolate, useCurrentFrame, Easing, random, spring, useVideoConfig} from 'remotion';
import {T, F, CL, HandCircle} from '../parts/fm';

export type HedgePair = {date: string; name: string; a: number; ap: string; b: number; bp: string; gap: string};
export type HedgeFlipProps = {
  seed: string; pairs: HedgePair[]; order: number[]; base: number; baseText: string;
  nameA: string; tagA: string; nameB: string; tagB: string; sayA: string; sayB: string;
  why: string; ask: string; flip: string; rate24: string; rates: string[]; fx24: number[]; fx24pk: number; end: string; beats: number[];
};

const out = Easing.out(Easing.cubic);
const g = (f: number, a: number, d = 16) => interpolate(f, [a, a + d], [0, 1], {...CL, easing: out});

export const HedgeFlip: React.FC<HedgeFlipProps> = (p) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const r = (k: string) => random(p.seed + k);
  const B = p.beats; const at = (i: number) => B[i] ?? 1e9; const mid = (i: number, q: number) => at(i) + ((B[i + 1] ?? at(i) + 200) - at(i)) * q;
  const sp = (a: number) => spring({frame: f - a, fps, config: {damping: 15}});
  // 판: 막대 바닥 y 800, 1.9억 = y 392
  const BY0 = 800, TOP = 1.9e8, BH = 408;
  const y = (won: number) => BY0 - won / TOP * BH;
  const bw = 118 + Math.round(r('bw') * 18), inner = 14;
  const GX0 = 250 + Math.round(r('gx') * 24), GS = 440;   // 오른쪽 쌍의 '차' 글자가 판(x 1820) 안에
  const gx = (k: number) => GX0 + k * GS;
  const [g2, g1, g0] = p.order;                       // 말 순서: 7.2 → 1년 전 → 재작년 첫날
  // 막대가 자라는 시점
  const grow = (k: number, side: 'a' | 'b') => {
    if (k === g2) return side === 'a' ? sp(at(0) + 6) : sp(at(1) + 4);
    if (k === g1) return sp(at(3) + (side === 'a' ? 4 : 12));
    return sp(at(7) + (side === 'a' ? 6 : 14));
  };
  const gapAt = (k: number) => k === g2 ? at(2) + 4 : k === g1 ? mid(3, 0.45) : at(10) + 4;
  // 지금 비추는 쌍(나머지는 흐리게)
  const focus = f < at(3) ? g2 : f < at(4) ? g1 : f < at(5) ? g2 : f < at(6) ? -2 : f < at(11) ? g0 : -1;
  const dim = (k: number) => focus === -1 || focus === -2 ? 1 : focus === k ? 1 : 0.38;
  const aOnly = f >= at(5) && f < at(6);              // 5줄: 환노출 막대만 또렷
  const ph = (k: number) => k === g0 && f >= at(6) && f < at(7) + 10;   // 6줄: 빈 자리 물음표
  const pulse = (a: number) => f >= a ? 0.55 + 0.45 * Math.cos(Math.min(1, (f - a) / 26) * Math.PI * 2) : 1;
  const yb = y(p.base);
  return (
    <>
      <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
        <line x1={GX0 - 60} x2={gx(2) + 2 * bw + inner + 50} y1={BY0} y2={BY0} stroke={T.ink3} strokeWidth={2} opacity={g(f, at(0))} />
        <line x1={GX0 - 60} x2={gx(2) + 2 * bw + inner + 50} y1={yb} y2={yb} stroke={T.ink} strokeWidth={3} strokeDasharray="12 9" opacity={g(f, at(0) + 4)} />
        {p.pairs.map((pr, k) => {
          const ga = grow(k, 'a'), gb = grow(k, 'b'); const xa = gx(k), xb = gx(k) + bw + inner;
          const ha = (BY0 - y(pr.a)) * ga, hb = (BY0 - y(pr.b)) * gb; const o = dim(k);
          const lossA = pr.a < p.base && ga > 0.98, lossB = pr.b < p.base && gb > 0.98;
          const gp = g(f, gapAt(k), 18); const top = Math.min(y(pr.a), y(pr.b)), bot = Math.max(y(pr.a), y(pr.b));
          const bx = xb + bw + 26;   // 괄호는 늘 오른쪽(왼쪽 끝 쌍이 판 밖으로 나가지 않게)
          return <g key={k} opacity={o}>
            {ph(k) && <>
              <rect x={xa} y={yb} width={bw} height={BY0 - yb} rx={5} fill="none" stroke={T.ink3} strokeWidth={3} strokeDasharray="10 8" opacity={g(f, at(6))} />
              <rect x={xb} y={yb} width={bw} height={BY0 - yb} rx={5} fill="none" stroke={T.ink3} strokeWidth={3} strokeDasharray="10 8" opacity={g(f, at(6))} />
            </>}
            <rect x={xa} y={BY0 - ha} width={bw} height={ha} rx={5} fill={T.ink} opacity={aOnly ? 1 : f >= at(5) && f < at(6) ? 1 : 1} />
            {lossA && <rect x={xa} y={yb} width={bw} height={y(pr.a) - yb - 2} rx={4} fill={T.rise} opacity={0.9 * (k === g2 && f >= at(4) ? pulse(at(4)) : 1)} />}
            <rect x={xb} y={BY0 - hb} width={bw} height={hb} rx={5} fill={T.fall} opacity={aOnly ? 0.3 : 1} />
            {lossB && <rect x={xb} y={yb} width={bw} height={y(pr.b) - yb - 2} rx={4} fill={T.rise} opacity={0.9} />}
            {gp > 0 && <path d={`M${bx - 14},${top} H${bx} V${top + (bot - top) * gp} H${bx - 14}`} fill="none" stroke={pr.a > pr.b ? T.ink : T.fall} strokeWidth={6} strokeLinejoin="round" />}
          </g>;
        })}
      </svg>
      {/* 범례: 두 상품 이름 — 왼쪽 위 */}
      <div style={{position: 'absolute', left: GX0 - 60, top: 346, display: 'flex', gap: 34, opacity: g(f, at(0) + 2) * (1 - 0.85 * g(f, at(8), 8) * (1 - g(f, at(10), 8))),   // 8·9줄 작은 환율 선과 겹치지 않게 범례를 잠깐 흐림
 ...F, whiteSpace: 'nowrap'}}>
        <div style={{display: 'flex', alignItems: 'center', gap: 12, opacity: f >= at(1) || f < at(0) + 1 ? 1 : 1}}>
          <span style={{width: 26, height: 26, borderRadius: 5, background: T.ink, display: 'inline-block'}} />
          <span style={{fontSize: 28, fontWeight: 700, color: T.ink}}>{p.nameA}</span><span style={{fontSize: 24, fontWeight: 500, color: T.ink2}}>{p.tagA}</span>
        </div>
        <div style={{display: 'flex', alignItems: 'center', gap: 12, opacity: g(f, at(1))}}>
          <span style={{width: 26, height: 26, borderRadius: 5, background: T.fall, display: 'inline-block'}} />
          <span style={{fontSize: 28, fontWeight: 700, color: T.fall}}>{p.nameB}</span><span style={{fontSize: 24, fontWeight: 500, color: T.ink2}}>{p.tagB}</span>
        </div>
      </div>
      <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0, pointerEvents: 'none', opacity: 1 - 0.85 * g(f, at(8), 8) * (1 - g(f, at(10), 8))}}>
        <HandCircle cx={GX0 + 672} cy={362} rx={30} ry={26} p={g(f, at(1) + 6, 20)} />
      </svg>
      {/* 1억 선 이름 */}
      <div style={{...F, position: 'absolute', left: GX0 - 210, width: 140, textAlign: 'right', top: yb - 18, fontSize: 27, fontWeight: 700, color: T.ink, opacity: g(f, at(0) + 4), whiteSpace: 'nowrap'}}>{p.baseText}</div>
      {/* 쌍 이름·날짜(막대 아래) */}
      {p.pairs.map((pr, k) => <div key={k} style={{position: 'absolute', left: gx(k) - 40, width: 2 * bw + inner + 80, textAlign: 'center', top: BY0 + 8, opacity: g(f, k === g2 ? at(0) : k === g1 ? at(3) : at(6)) * dim(k)}}>
        <div style={{...F, fontSize: 27, fontWeight: 700, color: T.ink, whiteSpace: 'nowrap'}}>{pr.name}</div>
        <div style={{...F, fontSize: 21, fontWeight: 500, color: T.ink3, whiteSpace: 'nowrap'}}>{pr.date} → 10.16</div>
      </div>)}
      {/* 막대 위 % */}
      {p.pairs.map((pr, k) => [['a', pr.a, pr.ap, gx(k)], ['b', pr.b, pr.bp, gx(k) + bw + inner]].map(([s, won, pct, x]) => {
        const o = g(f, (k === g2 ? (s === 'a' ? at(0) : at(1)) : k === g1 ? at(3) : at(7)) + 18) * dim(k);
        const t = y(won as number) - 40;
        return o > 0 && <div key={k + (s as string)} style={{position: 'absolute', left: (x as number) - 30, width: bw + 60, textAlign: 'center', top: t, opacity: o, ...F, fontSize: 26, fontWeight: 700, color: s === 'a' ? T.ink : T.fall, whiteSpace: 'nowrap'}}>{pct as string}</div>;
      }))}
      {/* 차 글자(괄호 옆) */}
      {p.pairs.map((pr, k) => { const o = g(f, gapAt(k) + 12) * dim(k) * (k === g1 && f >= mid(5, 0.42) - 6 && f < at(10) ? 0 : 1)   /* 띠·작은 선이 그 자리에 오는 5~9줄엔 숨김 */; const top = Math.min(y(pr.a), y(pr.b)), bot = Math.max(y(pr.a), y(pr.b));
        // 가운데 쌍은 오른쪽에 다음 쌍 % 글자가 있어 위로(레드팀 10/17 겹침)
        const up = k === g1; const left = up ? gx(k) - 40 : gx(k) + 2 * bw + inner + 44;
        return o > 0 && <div key={k} style={{position: 'absolute', left, width: up ? 2 * bw + inner + 80 : 230, textAlign: up ? 'center' : 'left', top: up ? top - 74 : (top + bot) / 2 - 24, opacity: o, ...F, fontSize: 30, fontWeight: 700, color: pr.a > pr.b ? T.ink : T.fall, whiteSpace: 'nowrap'}}>{pr.gap}</div>; })}   {/* 이긴 쪽 색 — 2024 쌍은 환노출(잉크)이 더 남음(레드팀 10/17) */}
      {/* 7.2 말 속 금액(0·1줄) */}
      {f >= at(0) && f < at(3) && <div style={{position: 'absolute', left: gx(g2) - 60, width: 2 * bw + inner + 120, textAlign: 'center', top: 470, ...F, fontSize: 36, fontWeight: 700, color: f < at(1) ? T.rise : T.fall, opacity: g(f, f < at(1) ? at(0) + 20 : at(1) + 16) * (1 - g(f, at(2), 8)), whiteSpace: 'nowrap'}}>{f < at(1) ? p.sayA : p.sayB}</div>}
      {/* 5줄 이유 띠 · 6줄 물음 · 7줄 뒤집힘 · 11줄 끝 — 검은 띠 하나가 줄마다 바뀜 */}
      {(() => {
        const items: [number, number, string][] = [[mid(5, 0.42), at(6), p.why], [at(6), at(7), p.ask], [at(7) + 16, at(8), p.flip], [at(11), 1e9, p.end]];
        return items.map(([a, b, s], i) => f >= a && f < b + 6 && <div key={i} style={{position: 'absolute', left: i === 2 ? gx(g0) + 2 * bw + inner + 40 : gx(1) + (i === 0 ? 40 : i === 3 ? 300 : 100), top: i === 2 ? 450 : 412 + (1 - sp(a)) * 16,
          opacity: Math.min(sp(a), 1 - g(f, b, 6)), background: T.ink, borderRadius: 12, padding: i === 0 ? '20px 34px' : '12px 24px', ...F, fontSize: i === 0 ? 40 : 32, fontWeight: 700, color: T.dink, whiteSpace: 'nowrap'}}>{s}</div>);
      })()}
      {/* 8·9줄: 그때 환율 1,289원 → 올랐다가 1,554원 → 지금 1,339원 — 작은 환율 선(ECOS 원문)이 말 따라 그려짐 */}
      {f >= at(8) && f < at(10) + 6 && (() => {
        const v = p.fx24, nn = v.length, lo = Math.min(...v), hi = Math.max(...v);
        const mx0 = gx(1) - 10, mx1 = gx(2) + 2 * bw + inner, my0 = 400, my1 = 488;
        const mX = (i: number) => mx0 + i / (nn - 1) * (mx1 - mx0), mY = (x: number) => my1 - (x - lo) / (hi - lo) * (my1 - my0);
        const dr = interpolate(f, [at(8) + 6, mid(9, 0.8)], [0, 1], {...CL, easing: Easing.inOut(Easing.cubic)});
        const m = Math.max(1, Math.round(dr * (nn - 1))); const o = 1 - g(f, at(10), 6);
        const d = v.slice(0, m + 1).map((x, i) => `${i ? 'L' : 'M'}${mX(i).toFixed(1)},${mY(x).toFixed(1)}`).join(' ');
        const lab = [[0, p.rates[0], mX(0) - 128, mY(v[0]) - 22, sp(at(8) + 4)], [p.fx24pk, p.rates[1], mX(p.fx24pk) - 70, my0 - 60, m >= p.fx24pk ? sp(at(8) + 6 + (mid(9, 0.8) - at(8) - 6) * p.fx24pk / (nn - 1)) : 0],
          [nn - 1, p.rates[2], mX(nn - 1) + 16, mY(v[nn - 1]) - 22, m >= nn - 1 ? sp(mid(9, 0.8)) : 0]] as [number, string, number, number, number][];
        return <>
          <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0, opacity: o}}>
            <rect x={mx0 - 16} y={my0 - 14} width={mx1 - mx0 + 32} height={my1 - my0 + 28} rx={12} fill={T.ink} />
            <path d={`${d} L${mX(m).toFixed(1)},${my1 + 8} L${mX(0).toFixed(1)},${my1 + 8} Z`} fill={T.daccent} opacity={0.3} />   {/* 선 아래 칠 — 그려지는 만큼 판이 바뀜 */}
            <path d={d} fill="none" stroke={T.dink} strokeWidth={3.5} strokeLinejoin="round" />
            {lab.map(([i], k) => (k === 0 || m >= i) && <circle key={k} cx={mX(i)} cy={mY(v[i])} r={9} fill={k === 0 ? T.accent : k === 1 ? T.rise : T.fall} stroke={T.surface} strokeWidth={3} />)}
          </svg>
          {lab.map(([, s, x, y, q], k) => q > 0 && <div key={k} style={{position: 'absolute', left: x, top: y, opacity: Math.min(1, q) * o, ...F, fontSize: 30, fontWeight: 700, whiteSpace: 'nowrap',
            color: k === 0 ? T.accent : k === 1 ? T.rise : T.fall, background: k === 0 ? T.soft : 'transparent', borderRadius: 8, padding: k === 0 ? '2px 10px' : 0}}>{s}</div>)}
        </>;
      })()}
    </>
  );
};
