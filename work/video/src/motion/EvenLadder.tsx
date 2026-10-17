// 본전 환율 눈금(EvenLadder) — X-1 v3 '질문 1 · 그래서 내 계좌는'(2026-10-17 motion). TallyFrame 자식.
// 오른쪽 세로 환율 눈금 + 지금 환율 점선, 날짜마다 '본전 줄'이 떨어져 꽂힌다. 지금보다 위 = 빨강 틈(아직 손실), 아래 = 파랑 틈(이미 이익).
// 왼쪽 카드 = 식(본전 환율 = 산 날 환율 ÷ 주가 배수)이 말 따라 조립 → 보기 숫자 → 조심(줄이 흔들림 = 주가가 움직이면 같이 움직임).
// 숫자 글자는 props(calc_out·대본)만. 글자는 HTML.
import React from 'react';
import {interpolate, useCurrentFrame, Easing, random, spring, useVideoConfig} from 'remotion';
import {T, F, CL} from '../parts/fm';

export type EvenRow = {name: string; rate: string; mult: string; even: number; evenText: string; say: string};
export type EvenLadderProps = {
  seed: string; now: number; nowText: string; min: number; max: number; ticks: [number, string][];
  evens: EvenRow[]; show: (number | null)[]; formula: string[]; ex: string[]; app: string[];
  gapSay: string; aboveTag: string; belowTag: string; warn: string; both: string; end: string; beats: number[];
};

const out = Easing.out(Easing.cubic);
const g = (f: number, a: number, d = 16) => interpolate(f, [a, a + d], [0, 1], {...CL, easing: out});

export const EvenLadder: React.FC<EvenLadderProps> = (p) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const r = (k: string) => random(p.seed + k);
  const B = p.beats; const at = (i: number) => B[i] ?? 1e9; const mid = (i: number, q: number) => at(i) + ((B[i + 1] ?? at(i) + 200) - at(i)) * q;
  const sp = (a: number) => spring({frame: f - a, fps, config: {damping: 14}});
  // 눈금 x 1080~1700, y 390(max)~800(min)
  const SX0 = 1090 + Math.round(r('sx') * 30), SX1 = 1700;
  const YT = 392, YB = 800;
  const Y = (v: number) => YB - (v - p.min) / (p.max - p.min) * (YB - YT);
  const yn = Y(p.now);
  // 줄 k가 꽂히는 시점: 4줄 가장 비싸던 날 · 6줄 석 달 전 · 7줄 1년 전 → 올해 첫날(줄 안 55%)
  const dropAt = [at(4) + 4, at(6) + 4, mid(7, 0.55), at(7) + 4];
  const wob = f >= at(9) && f < at(11) ? Math.sin((f - at(9)) / 9) * 14 * g(f, at(9), 10) * (1 - g(f, at(10) + 30, 20)) : 0;
  const yk = (k: number) => Y(p.evens[k].even) + wob * (k % 2 ? -1 : 1) * (0.7 + 0.3 * k / 3);
  const caution = f >= at(8);
  const hot = (k: number) => !caution && f >= dropAt[k] && (k === 0 ? f < at(6) : k === 1 ? f < at(7) : true);
  const pulse = (a: number) => f >= a ? 0.55 + 0.45 * Math.cos(Math.min(1, (f - a) / 24) * Math.PI * 2) : 1;
  const card = (a: number, b: number) => Math.min(sp(a), 1 - g(f, b, 8));
  const cardX = 150 + Math.round(r('cx') * 20);
  return (
    <>
      <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
        {p.ticks.map(([v], i) => <line key={i} x1={SX0} x2={SX1} y1={Y(v)} y2={Y(v)} stroke={T.line} strokeWidth={2} opacity={g(f, at(0) + i * 3)} />)}
        <line x1={SX0} x2={SX0} y1={YT - 6} y2={YB + 6} stroke={T.ink3} strokeWidth={3} opacity={g(f, at(0))} />
        {/* 본전 줄과 지금 사이 틈 */}
        {p.evens.map((e, k) => { const d = g(f, dropAt[k], 20); if (d <= 0) return null; const up = e.even > p.now; const y0 = yk(k);
          const x = SX1 - 70 - (3 - k) * 76;   // 틈 막대는 오른쪽, 이름표는 왼쪽(SX0 옆) — 겹침 없게
          return <g key={k} opacity={caution && f < at(9) ? 0.5 : 1}>
            <rect x={x} y={up ? y0 : yn} width={60} height={Math.abs(yn - y0) * d} rx={5} fill={up ? T.rise : T.fall} opacity={hot(k) ? 0.92 : 0.5} />
            <line x1={SX0} x2={SX1} y1={y0 - (1 - d) * 60} y2={y0 - (1 - d) * 60} stroke={up ? T.rise : T.fall} strokeWidth={hot(k) ? 6 : 4} opacity={d} />
          </g>; })}
        {/* 1~3줄: 빈 고리가 눈금을 오르내리며 '본전 자리'를 찾음 → 4줄 첫 본전 줄 자리에 앉음 */}
        {f >= at(1) && f < at(4) + 20 && (() => { const t = (f - at(1)) / 30; const land = g(f, at(4) - 6, 22);
          const v = (p.now + 60 + Math.sin(t * 1.3) * 110 + Math.sin(t * 2.9) * 30) * (1 - land) + p.evens[0].even * land;
          return <circle cx={SX0} cy={Y(v)} r={26} fill="none" stroke={T.ink} strokeWidth={6} strokeDasharray="8 6" opacity={g(f, at(1), 10) * (1 - g(f, at(4) + 12, 8))} />; })()}
        {/* 5줄: 지금~가장 비싸던 날 본전 사이를 눈금 폭 전체로 붉게(160원쯤 위) */}
        {f >= at(5) && f < at(6) + 10 && <rect x={SX0} y={Y(p.evens[0].even)} width={SX1 - SX0} height={yn - Y(p.evens[0].even)} fill={T.rise} opacity={0.28 * Math.min(g(f, at(5), 10), 1 - g(f, at(6), 10))} />}
        {/* 지금 환율 점선 */}
        <line x1={SX1 - g(f, at(0) + 6, 22) * (SX1 - SX0)} x2={SX1} y1={yn} y2={yn} stroke={T.accent} strokeWidth={6} strokeDasharray="16 10" />
        <circle cx={SX0} cy={yn} r={13 * sp(at(0) + 18) * (f >= at(10) ? pulse(at(10)) : 1)} fill={T.accent} stroke={T.surface} strokeWidth={4} />
        {/* 10줄: 오를 요인·내릴 요인 화살표 */}
        {f >= at(10) && [[-1, T.rise], [1, T.fall]].map(([s, c], i) => { const o = sp(at(10) + 6 + i * 6);
          const yy = yn + (s as number) * 30; const tip = yn + (s as number) * (30 + 90 * o);
          return <g key={i} opacity={Math.min(1, o)}>
            <line x1={SX0 - 50} x2={SX0 - 50} y1={yy} y2={tip} stroke={c as string} strokeWidth={8} strokeLinecap="round" />
            <path d={`M${SX0 - 66},${tip - (s as number) * 14} L${SX0 - 50},${tip + (s as number) * 6} L${SX0 - 34},${tip - (s as number) * 14}`} fill="none" stroke={c as string} strokeWidth={8} strokeLinejoin="round" strokeLinecap="round" />
          </g>; })}
      </svg>
      {/* 눈금 글자 */}
      {p.ticks.map(([v, s], i) => <div key={i} style={{...F, position: 'absolute', left: SX1 + 12, top: Y(v) - 16, fontSize: 24, fontWeight: 500, color: T.ink3, opacity: g(f, at(0) + i * 3), whiteSpace: 'nowrap'}}>{s}</div>)}
      <div style={{...F, position: 'absolute', left: SX0 + 16, top: yn - 44, fontSize: 30, fontWeight: 700, color: T.accent, whiteSpace: 'nowrap', opacity: g(f, at(0) + 20)}}>{p.nowText}</div>
      {/* 본전 줄 이름표(줄 위 왼쪽) */}
      {p.evens.map((e, k) => { const d = g(f, dropAt[k] + 12, 14); const up = e.even > p.now; const y0 = yk(k);
        const ty = k === 0 ? y0 - 44 : y0 + 8;
        return d > 0 && <div key={k} style={{position: 'absolute', left: SX0 + 16, top: ty, opacity: d * (caution && f < at(9) ? 0.5 : 1), ...F, whiteSpace: 'nowrap',
          fontSize: hot(k) ? 30 : 24, fontWeight: 700, color: up ? T.rise : T.fall}}>{e.name} · {e.say}</div>; })}
      {/* 5줄: 160원쯤 위 */}
      {f >= at(5) && f < at(6) + 6 && <div style={{position: 'absolute', left: SX0 + 16, top: Y(p.evens[0].even) + 14,   // '지금 1,339원' 글자(점선 위)와 안 겹치게 1,500 줄 바로 아래
 opacity: Math.min(sp(at(5)), 1 - g(f, at(6), 6)),
        background: T.rise, borderRadius: 10, padding: '6px 16px', ...F, fontSize: 30, fontWeight: 700, color: T.surface, whiteSpace: 'nowrap'}}>{p.gapSay}</div>}
      {/* 위·아래 뜻(7줄 끝부터) */}
      {[[p.aboveTag, YT - 44, T.rise], [p.belowTag, YB + 8, T.fall]].map(([s, t, c], i) => { const o = g(f, i === 0 ? at(6) + 18 : mid(7, 0.3)) * (caution ? 0.5 : 1);
        return <div key={i} style={{position: 'absolute', left: SX0, top: t as number, opacity: o, ...F, fontSize: 28, fontWeight: 700, color: c as string, whiteSpace: 'nowrap'}}>{s}</div>; })}
      {/* 왼쪽 카드 바탕 — 줄마다 한 칸씩 자라 판이 바뀐 게 보이게(1줄 식 → 3줄 앱 → 4줄 보기 → 6·7줄 두 줄) */}
      {(() => { const h = 130 * g(f, at(1), 18) + 100 * g(f, at(3), 18) + 100 * g(f, at(4), 18) + 64 * g(f, at(6), 14) + 64 * g(f, at(7), 14);
        return h > 1 && <div style={{position: 'absolute', left: cardX - 30, top: 380, width: 880, height: h, borderRadius: 18, background: T.ink, opacity: 1 - g(f, at(8), 8)}} />; })()}
      {/* 왼쪽 카드: 식 */}
      <div style={{position: 'absolute', left: cardX, top: 400, width: 820, opacity: card(at(1), at(8)), transform: `translateY(${(1 - Math.min(1, sp(at(1)))) * 14}px)`}}>
        {/* 식 = 큰 칸 셋이 말 따라 하나씩 튀어 들어옴(1줄 첫 칸, 2줄 둘째·셋째) */}
        <div style={{display: 'flex', alignItems: 'center', gap: 16, ...F, whiteSpace: 'nowrap'}}>
          {[[p.formula[0], at(1) + 4, T.accent, T.surface], ['=', at(1) + 14, 'transparent', T.dink3], [p.formula[1], at(2) + 4, T.dsurface, T.dink], ['÷', mid(2, 0.5), 'transparent', T.daccent], [p.formula[2], mid(2, 0.5) + 6, T.dsurface, T.daccent]].map(([s, a, bg, c], i) => {
            const q = sp(a as number); return <span key={i} style={{display: 'inline-block', opacity: Math.min(1, q), transform: `translateY(${(1 - Math.min(1, q)) * 30}px) scale(${0.85 + 0.15 * Math.min(1, q)})`,
              background: bg as string, boxShadow: 'none', borderRadius: 14, padding: bg === 'transparent' ? 0 : '14px 22px', fontSize: 42, fontWeight: 700, color: c as string}}>{s}</span>; })}
        </div>
        <div style={{display: 'flex', gap: 14, marginTop: 30, opacity: g(f, at(3) + 4), transform: `translateX(${(1 - g(f, at(3) + 4, 20)) * -60}px)`}}>
          {p.app.map((s, i) => <span key={i} style={{...F, fontSize: 29, fontWeight: 700, background: i ? T.daccent : T.dsurface, borderRadius: 10, padding: '8px 18px', color: i ? T.dbg : T.dink, whiteSpace: 'nowrap', opacity: i ? g(f, mid(3, 0.45)) : 1}}>{i ? '→ ' : ''}{s}</span>)}
        </div>
        <div style={{height: 2, background: T.dink3, opacity: 0.4 * g(f, at(4) + 8), marginTop: 22}} />   {/* 앱 16%(1년 전) 줄과 가장 비싸던 날 보기 줄을 나눔 — 16%가 그날 수익률로 읽힘(레드팀) */}
        <div style={{...F, marginTop: 18, fontSize: 34, fontWeight: 700, color: T.dink3, opacity: g(f, at(4) + 8), whiteSpace: 'nowrap'}}>
          {p.evens[0].name}: <span style={{color: T.dink}}>{p.ex[0]} ÷ {p.ex[1]}</span> = <span style={{color: T.daccent}}>{p.ex[2]}원</span></div>
        <div style={{...F, marginTop: 14, fontSize: 28, fontWeight: 500, color: T.dink, opacity: g(f, at(6) + 8), whiteSpace: 'nowrap'}}>
          {p.evens[1].name}: {p.evens[1].rate} ÷ {p.evens[1].mult} = {p.evens[1].evenText}</div>
        <div style={{...F, marginTop: 10, fontSize: 28, fontWeight: 500, color: T.dink, opacity: g(f, at(7) + 8), whiteSpace: 'nowrap'}}>
          {p.evens[3].name}: {p.evens[3].rate} ÷ {p.evens[3].mult} = {p.evens[3].evenText}</div>
      </div>
      {/* 8~10줄 조심 카드 · 11줄 끝 띠 */}
      {[[at(8), at(10), p.warn], [at(10), at(11), p.both], [at(11), 1e9, p.end]].map(([a, b, s], i) => f >= (a as number) && f < (b as number) + 8 &&
        <div key={i} style={{position: 'absolute', left: cardX, top: 470 + (1 - Math.min(1, sp(a as number))) * 16, opacity: card(a as number, b as number), background: T.ink, borderRadius: 14, padding: '18px 28px'}}>
          <div style={{...F, fontSize: 33, fontWeight: 700, color: T.dink, lineHeight: 1.35, whiteSpace: 'nowrap'}}>{i === 1 ? `“${s}”` : s}</div>
          {i === 1 && <div style={{...F, fontSize: 22, fontWeight: 500, color: T.dink3, marginTop: 8}}>재정경제부 2026.8.21</div>}
        </div>)}
    </>
  );
};
