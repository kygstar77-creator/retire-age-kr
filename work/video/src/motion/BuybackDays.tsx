// 회사가 산 날들 vs 오늘 종가(BuybackDays) — W-1 2화 '2. 삼성전자 100주와 15조원'(2026-10-15 motion). TallyFrame 자식.
// 점 = 그날 회사가 산 하루 평균단가(DART 원문, props.days). 세로축이 0부터가 아니므로 막대가 아니라 점으로 그린다(막대 길이 왜곡 금지).
// 줄기 = 점에서 종가 점선까지(종가보다 얼마나 위인지) — 점선이 오른쪽에서 들어오며 지나가는 날마다 줄기가 생긴다.
// 정직성: 차액 숫자는 만들지 않는다. 글자 숫자는 props(calc_out·script 자막 원문)만. 점선 = 종가 한 뜻, 가는 회색 선 = 회사 평균 한 뜻.
// U5: beats[i] = 말 줄 시작. ① 점이 날짜 순으로 찍힘 → ② 종가 점선이 쓸고 지나가며 줄기·최저·최고 → ③ 점 흐려지고 100주 카드.
// 글자는 전부 HTML(카메라 변형 없음 — SVG <text> mp4 어긋남 10/13 교훈).
import React from 'react';
import {interpolate, useCurrentFrame, Easing, random, spring, useVideoConfig} from 'remotion';
import {T, F, CL} from '../parts/fm';

export type BuybackDaysProps = {
  seed: string;
  days: {d: string; v: number}[];
  min: number; max: number; yticks: [number, string][]; months: [number, string][];
  close: number; avg: number; lo: number; hi: number;
  card: [string, string, string];   // [머리, 큰 금액, 회사 평균 대비] — 대본 '(화면: 삼성전자 마감 …)' 그대로
  closeText: string; avgText: string; loText: string; hiText: string; first: string; last: string;
  total: string; allAbove: string; dotName: string; stemName: string; unsold: string;
  beats: number[];
};

const out = Easing.out(Easing.cubic);
const g = (f: number, a: number, d = 16) => interpolate(f, [a, a + d], [0, 1], {...CL, easing: out});

export const BuybackDays: React.FC<BuybackDaysProps> = (p) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const r = (k: string) => random(p.seed + k);
  const B = p.beats; const n = p.days.length;
  // 판 y 236~852 · 위 254~330 [자막] 띠 → 그래프 y 380~760. 오른쪽 카드 자리 x 1250~1760.
  const third = f >= B[2];
  const shrink = g(f, B[2], 22);
  const X0 = 300 + Math.round(r('x') * 20), X1full = 1640, X1 = X1full - shrink * 460;
  const YT = 420, YB = 740;
  const X = (i: number) => X0 + (i + 0.5) / n * (X1 - X0);
  const Y = (v: number) => YB - (v - p.min) / (p.max - p.min) * (YB - YT);
  // ① 점: 첫 줄 길이의 75% 안에 29개 차례로
  const l0 = (B[1] - B[0]) * 0.75; const dotAt = (i: number) => B[0] + 6 + i * l0 / n;
  // ② 종가 점선: 오른쪽 끝에서 왼쪽으로 쓸며 들어온다(둘째 줄 처음 45%)
  const sweep = interpolate(f, [B[1], B[1] + (B[2] - B[1]) * 0.45], [0, 1], {...CL, easing: Easing.inOut(Easing.cubic)});
  const lineLeft = X1 - sweep * (X1 - X0 + 30);
  const yc = Y(p.close), ya = Y(p.avg);
  const dim = 1 - 0.6 * shrink;
  const labLo = g(f, B[1] + (B[2] - B[1]) * 0.5), labHi = g(f, B[1] + (B[2] - B[1]) * 0.58);
  const allAt = B[1] + (B[2] - B[1]) * 0.62;
  const sp = (a: number) => spring({frame: f - a, fps, config: {damping: 14}});
  return (
    <>
      <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
        {/* 가로 눈금 */}
        {p.yticks.map(([v], i) => <line key={i} x1={X0 - 20} x2={X1 + 10} y1={Y(v)} y2={Y(v)} stroke={T.line} strokeWidth={2} />)}
        {/* 줄기: 점선이 지나간 날만 */}
        <g opacity={dim}>
          {p.days.map((d, i) => { const x = X(i); const on = sweep > 0 && x >= lineLeft; const k = on ? g(f, B[1] + (X1 - x) / (X1 - X0 + 30) * (B[2] - B[1]) * 0.45, 8) : 0;
            return <line key={i} x1={x} x2={x} y1={yc} y2={yc + (Y(d.v) - yc) * k} stroke={i === p.lo || i === p.hi ? T.ink : T.ink3} strokeWidth={i === p.lo || i === p.hi ? 5 : 3} />; })}
        </g>
        {/* 회사 평균(가는 회색 실선) — 셋째 줄에서 */}
        <line x1={X0} x2={X0 + (X1 - X0) * g(f, B[2] + 10, 20)} y1={ya} y2={ya} stroke={T.ink2} strokeWidth={3} opacity={third ? 1 : 0} />
        {/* 점 */}
        <g opacity={dim}>
          {p.days.map((d, i) => { const k = sp(dotAt(i)); const key = i === p.lo || i === p.hi;
            return <circle key={i} cx={X(i)} cy={Y(d.v) + (1 - k) * 18} r={(key && f >= B[1] ? 12 : 9) * Math.max(0, k)} fill={key && f >= B[1] ? T.ink : T.ink2} opacity={Math.min(1, Math.max(0, k))} />; })}
        </g>
        {/* 종가 점선 */}
        {sweep > 0 && <line x1={lineLeft} x2={X1 + 10} y1={yc} y2={yc} stroke={T.accent} strokeWidth={6} strokeDasharray="18 12" />}
      </svg>
      {/* 세로 눈금 글자 */}
      {p.yticks.map(([v, s], i) => <div key={i} style={{...F, position: 'absolute', left: X0 - 150, width: 120, textAlign: 'right', top: Y(v) - 18, fontSize: 26, fontWeight: 500, color: T.ink3}}>{s}</div>)}
      {/* 가로: 첫날·끝날·달 */}
      <div style={{...F, position: 'absolute', left: X(0) - 40, top: YB + 22, fontSize: 28, fontWeight: 700, color: T.ink2, opacity: g(f, dotAt(0))}}>{p.first}</div>
      <div style={{...F, position: 'absolute', left: X(n - 1) - 40, top: YB + 22, fontSize: 28, fontWeight: 700, color: T.ink2, opacity: g(f, dotAt(n - 1))}}>{p.last}</div>
      {p.months.slice(1).map(([i, m]) => <div key={m} style={{...F, position: 'absolute', left: X(i) - 30, top: YB + 22, fontSize: 26, fontWeight: 500, color: T.ink3, opacity: g(f, dotAt(i)) * (third ? 0 : 1)}}>{m}</div>)}
      {/* 점 이름 + 15조원·29거래일 (첫 줄) */}
      <div style={{...F, position: 'absolute', left: X0, top: YT - 50, fontSize: 30, fontWeight: 700, color: T.ink2, opacity: g(f, B[0] + 4) * dim}}>● {p.dotName}</div>
      <div style={{...F, position: 'absolute', left: X1full - 520, top: YT - 54, width: 520, textAlign: 'right', fontSize: 44, fontWeight: 700, color: T.ink,
        opacity: g(f, dotAt(n - 1)) * (1 - g(f, B[1], 10)), transform: `translateY(${(1 - g(f, dotAt(n - 1))) * 16}px)`}}>{p.total}</div>
      {/* 종가 글자: 점선 머리를 따라감 */}
      {sweep > 0 && <div style={{...F, position: 'absolute', left: Math.max(X0, lineLeft), top: yc + 14, fontSize: 32, fontWeight: 700, color: T.accent, whiteSpace: 'nowrap', opacity: g(f, B[1], 8)}}>{p.closeText}</div>}
      {/* 최저·최고 */}
      <div style={{...F, position: 'absolute', left: X(p.lo) - 140, width: 280, textAlign: 'center', top: yc + 16, fontSize: 30, fontWeight: 700, color: T.ink, whiteSpace: 'nowrap', opacity: labLo * (1 - shrink), transform: `translateY(${(1 - labLo) * 12}px)`}}>최저 {p.loText}</div>
      <div style={{...F, position: 'absolute', left: X(p.hi) - 140, width: 280, textAlign: 'center', top: Y(p.days[p.hi].v) - 58, fontSize: 30, fontWeight: 700, color: T.ink, whiteSpace: 'nowrap', opacity: labHi * (1 - shrink), transform: `translateY(${(1 - labHi) * 12}px)`}}>최고 {p.hiText}</div>
      {/* 29일 모두 — 검은 띠 */}
      {f >= allAt && !third && <div style={{position: 'absolute', right: 1920 - X1full, top: 326 + (1 - sp(allAt)) * 20, opacity: sp(allAt), background: T.ink, borderRadius: 14, padding: '18px 34px',
        ...F, fontWeight: 700, fontSize: 38, color: T.dink, whiteSpace: 'nowrap'}}>{p.allAbove}</div>}
      {/* 범례: 줄기 뜻(둘째 줄) → 회사 평균선(셋째 줄). 점 위를 덮지 않게 범례 줄에만 둔다(레드팀 10/15) */}
      <div style={{...F, position: 'absolute', left: X0 + 330, top: YT - 50, fontSize: 30, fontWeight: 700, color: T.ink2, whiteSpace: 'nowrap', opacity: g(f, allAt) * (1 - shrink)}}>┃ {p.stemName}</div>
      {third && <div style={{...F, position: 'absolute', left: X0 + 330, top: YT - 50, fontSize: 30, fontWeight: 700, color: T.ink, whiteSpace: 'nowrap', opacity: g(f, B[2] + 18)}}>
        <span style={{display: 'inline-block', width: 44, height: 4, background: T.ink2, verticalAlign: 'middle', marginRight: 12}} />{p.avgText}</div>}
      {/* 셋째 줄: 대본 마감 화면 그대로 — 100주 이번 주 금액 + 회사 평균보다 몇 % */}
      {third && <div style={{position: 'absolute', left: 1220 + (1 - sp(B[2] + 6)) * 60, top: 400, width: 560, opacity: sp(B[2] + 6), background: T.ink, borderRadius: 20, padding: '32px 38px', boxSizing: 'border-box'}}>
        <div style={{...F, fontSize: 30, fontWeight: 500, color: T.dink3, whiteSpace: 'nowrap'}}>{p.card[0]}</div>
        <div style={{...F, fontSize: 88, fontWeight: 700, color: T.dfall, whiteSpace: 'nowrap', lineHeight: 1.1, marginTop: 8, opacity: g(f, B[2] + 12), transform: `translateY(${(1 - g(f, B[2] + 12)) * 14}px)`}}>{p.card[1]}</div>
        <div style={{...F, fontSize: 27, fontWeight: 700, color: T.dink, marginTop: 18, paddingTop: 16, borderTop: `2px solid ${T.dink3}`, lineHeight: 1.35, opacity: g(f, B[2] + 30)}}>{p.card[2].split(' = ').map((t, i) => <div key={i} style={{whiteSpace: 'nowrap', color: i ? T.dink : T.dink3, fontWeight: i ? 700 : 500}}>{t}</div>)}</div>
        <div style={{...F, marginTop: 22, paddingTop: 18, borderTop: `2px solid ${T.dink3}`, fontSize: 26, fontWeight: 700, color: T.daccent, opacity: g(f, B[2] + 50), whiteSpace: 'nowrap'}}>{p.unsold}</div>
      </div>}
    </>
  );
};
