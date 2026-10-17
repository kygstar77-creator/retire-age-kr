// 지금보다 쌌던 날(DaysBelow) — X-1 v3 '질문 5 · 지금 바꿔 둘까'(2026-10-17 motion). TallyFrame 자식.
// 0줄: 선이 지금까지 그려지고 오른쪽 '앞날'은 빈 점선 칸 → 1줄: 지금 높이 가로줄이 과거 쪽으로 쓸어 감 → 2줄: 날 수 세기(679)
// → 3줄: 줄 아래로 내려간 날만 주황 점으로 켜짐(81일) → 4줄: 엔화 선으로 바뀜(4일) → 5줄: 두 결론 칩 → 6줄: 끝 띠.
// 선 = ECOS 일별 원문 그대로(679거래일). 날 수 글자는 props(calc_out assert)만. 글자는 HTML.
import React from 'react';
import {interpolate, useCurrentFrame, Easing, random, spring, useVideoConfig} from 'remotion';
import {T, F, CL} from '../parts/fm';

export type DaysBelowProps = {
  seed: string; usd: number[]; jpy: number[]; years: [number, string][];
  usdMin: number; usdMax: number; jpyMin: number; jpyMax: number; usdNow: number; jpyNow: number;
  usdNowText: string; jpyNowText: string; usdName: string; jpyName: string; noAns: string; past: string;
  total: string; usdCount: string; usdRatio: string; jpyCount: string; sumUp: string[]; mid: string; beats: number[];
};

const out = Easing.out(Easing.cubic);
const g = (f: number, a: number, d = 16) => interpolate(f, [a, a + d], [0, 1], {...CL, easing: out});

export const DaysBelow: React.FC<DaysBelowProps> = (p) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const r = (k: string) => random(p.seed + k);
  const B = p.beats; const at = (i: number) => B[i] ?? 1e9; const mid = (i: number, q: number) => at(i) + ((B[i + 1] ?? at(i) + 200) - at(i)) * q;
  const sp = (a: number) => spring({frame: f - a, fps, config: {damping: 14}});
  const n = p.usd.length;
  const X0 = 250 + Math.round(r('x') * 20), XN = 1400, XF = 1720;   // XN = 지금, XN~XF = 앞날 빈 칸
  const YT = 420, YB = 780;
  const X = (i: number) => X0 + i / (n - 1) * (XN - X0);
  const yen = g(f, at(4), 22);                                        // 0 = 달러, 1 = 엔화
  const mn = p.usdMin + (p.jpyMin - p.usdMin) * yen, mx = p.usdMax + (p.jpyMax - p.usdMax) * yen;
  const vals = (k: number) => p.usd[k] + (p.jpy[k] - p.usd[k]) * yen;   // 바뀌는 동안 선이 엔화 모양으로 옮겨 감
  const now = p.usdNow + (p.jpyNow - p.usdNow) * yen;
  const Y = (v: number) => YB - (v - mn) / (mx - mn) * (YB - YT);
  const draw = interpolate(f, [at(0) + 4, mid(0, 0.75)], [0, 1], {...CL, easing: Easing.inOut(Easing.cubic)});
  const m = Math.max(1, Math.round(draw * (n - 1)));
  let path = ''; for (let i = 0; i <= m; i++) path += `${i ? 'L' : 'M'}${X(i).toFixed(1)},${Y(vals(i)).toFixed(1)}`;
  const yn = Y(now);
  const sweep = g(f, at(1) + 4, 30);                                  // 지금 줄이 과거 쪽으로
  const cnt = Math.round(interpolate(f, [at(2) + 4, mid(2, 0.8)], [0, 679], CL));
  const dotsOn = g(f, at(3) + 4, 26);
  const below = (k: number) => yen < 0.5 ? p.usd[k] <= p.usdNow : p.jpy[k] <= p.jpyNow;
  const dotK: number[] = []; for (let k = 0; k < n; k++) if (below(k)) dotK.push(k);
  const showDots = f >= at(3) || yen > 0.5;
  const dotP = (j: number) => yen > 0.5 ? g(f, at(4) + 26 + j * 5, 10) : interpolate(dotsOn, [j / dotK.length * 0.9, j / dotK.length * 0.9 + 0.1], [0, 1], CL);
  const chip = (a: number, b: number) => Math.min(sp(a), 1 - g(f, b, 8));
  return (
    <>
      <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
        {/* 앞날 칸 */}
        <rect x={XN + 12} y={YT - 10} width={XF - XN - 12} height={YB - YT + 20} rx={14} fill="none" stroke={T.ink3} strokeWidth={3} strokeDasharray="10 9" opacity={g(f, mid(0, 0.7)) * (1 - 0.6 * g(f, at(1)))} />
        {/* 지금 높이 가로줄 — 1줄에 과거 쪽으로 쓸어 감 */}
        <line x1={XN - sweep * (XN - X0)} x2={XN} y1={yn} y2={yn} stroke={T.accent} strokeWidth={5} strokeDasharray="16 10" opacity={g(f, mid(0, 0.75))} />
        {/* 줄 아래 칠 */}
        {showDots && <rect x={X0} y={yn} width={XN - X0} height={YB + 10 - yn} fill={T.soft} opacity={0.55 * (yen > 0.5 ? g(f, at(4) + 20) : dotsOn)} />}
        <path d={path} fill="none" stroke={T.ink2} strokeWidth={3.5} strokeLinejoin="round" />
        {showDots && dotK.map((k, j) => { const o = dotP(j); return o > 0 && <circle key={k} cx={X(k)} cy={Y(vals(k))} r={(yen > 0.5 ? 11 : 6) * o} fill={T.accent} stroke={T.surface} strokeWidth={yen > 0.5 ? 3 : 1.5} />; })}
        {/* 4줄: 엔화 4일은 선 끝에 몰려 있어 점이 지금 점에 묻힘 → 끝을 감싸는 고리 */}
        {yen > 0.5 && f < at(5) + 8 && <ellipse cx={X(n - 4)} cy={Y(p.jpyNow)} rx={46 * g(f, at(4) + 30, 14)} ry={34 * g(f, at(4) + 30, 14)} fill="none" stroke={T.accent} strokeWidth={5} opacity={1 - g(f, at(5), 8)} />}
        {/* 5줄부터: 달러 선을 흐리게 다시(제 눈금) — 결론 칩 둘이 두 선을 가리키게 */}
        {f >= at(5) && <path d={p.usd.map((v, i) => `${i ? 'L' : 'M'}${X(i).toFixed(1)},${(YB - (v - p.usdMin) / (p.usdMax - p.usdMin) * (YB - YT)).toFixed(1)}`).join(' ')} fill="none" stroke={T.fall} strokeWidth={3} opacity={0.45 * g(f, at(5), 18)} pathLength={1} strokeDasharray={`${g(f, at(5), 30)} 1`} />}
        <circle cx={XN} cy={yn} r={12 * sp(mid(0, 0.75))} fill={T.accent} stroke={T.surface} strokeWidth={4} />
        {/* 2줄: 세는 막대(시간 축 아래 진행 띠) */}
        {f >= at(2) && <rect x={X0} y={YB + 4} width={(XN - X0) * cnt / 679} height={16} rx={6} fill={T.ink} opacity={1 - g(f, at(4), 10)} />}
      </svg>
      {/* 5줄부터: 두 선 이름(선 시작 왼쪽) — 단위가 달라 어느 선이 무엇인지(레드팀) */}
      {f >= at(5) && [[p.usdName.replace('원/', ''), YB - (p.usd[0] - p.usdMin) / (p.usdMax - p.usdMin) * (YB - YT), T.fall], [p.jpyName.replace('원/', ''), YB - (p.jpy[0] - p.jpyMin) / (p.jpyMax - p.jpyMin) * (YB - YT), T.ink]].map(([s, y, c], i) =>
        <div key={i} style={{...F, position: 'absolute', left: X0 - 130, width: 118, textAlign: 'right', top: (y as number) - 18, fontSize: 28, fontWeight: 700, color: c as string, whiteSpace: 'nowrap', opacity: g(f, at(5) + 10)}}>{s}</div>)}
      {/* 5줄부터: 달러 지금 값도(파랑, 제 눈금 자리) — 오른쪽 라벨이 엔화 하나면 달러도 846.65원으로 읽힘(레드팀 2차) */}
      {f >= at(5) && <div style={{...F, position: 'absolute', left: XN + 26, top: YB - (p.usdNow - p.usdMin) / (p.usdMax - p.usdMin) * (YB - YT) - 52, fontSize: 26, fontWeight: 700, color: T.fall, whiteSpace: 'nowrap', opacity: g(f, at(5) + 10)}}>{p.usdNowText}</div>}
      {/* 해 눈금 */}
      {p.years.map(([i, s], k) => <div key={k} style={{...F, position: 'absolute', left: X(i) - 4, top: YB + 20, fontSize: 24, fontWeight: 500, color: T.ink3, opacity: g(f, at(0) + 4 + k * 8), whiteSpace: 'nowrap'}}>{s}</div>)}
      {/* 선 이름 */}
      <div style={{...F, position: 'absolute', left: X0, top: YT - 70, fontSize: 30, fontWeight: 700, color: T.ink2, whiteSpace: 'nowrap', opacity: g(f, at(0) + 2) * (1 - g(f, at(5), 6))}}>{yen > 0.5 ? p.jpyName : p.usdName} 매매기준율</div>
      {/* 지금 값 */}
      <div style={{...F, position: 'absolute', left: XN + 26, width: XF - XN - 30, textAlign: 'left', top: yn - 18, fontSize: 26, fontWeight: 700, color: T.accent, whiteSpace: 'nowrap', opacity: g(f, mid(0, 0.8))}}>{yen > 0.5 ? p.jpyNowText : p.usdNowText}</div>
      {/* 앞날 칸 글자 */}
      <div style={{position: 'absolute', left: XN + 24, width: XF - XN - 36, top: (YT + YB) / 2 - 50, textAlign: 'center', ...F, fontSize: 64, fontWeight: 700, color: T.ink3, opacity: g(f, mid(0, 0.8)) * (1 - 0.6 * g(f, at(1)))}}>?</div>
      {f < at(1) + 8 && <div style={{position: 'absolute', left: XN - 520, top: YT - 70, width: 760, textAlign: 'right', ...F, fontSize: 28, fontWeight: 700, color: T.ink, whiteSpace: 'nowrap', opacity: chip(mid(0, 0.45), at(1))}}>{p.noAns}</div>}
      {/* 1줄: 지나간 날과 견주면 */}
      {f >= at(1) && f < at(2) + 8 && <div style={{position: 'absolute', left: X0 + 20, top: yn - 70, opacity: chip(at(1) + 14, at(2)), background: T.ink, borderRadius: 12, padding: '10px 22px', ...F, fontSize: 30, fontWeight: 700, color: T.dink, whiteSpace: 'nowrap'}}>← {p.past}</div>}
      {/* 2줄: 679일 세기 */}
      {f >= at(2) && f < at(4) + 8 && <div style={{position: 'absolute', left: 900, top: 340, opacity: chip(at(2), at(4)), ...F, whiteSpace: 'nowrap', background: T.ink, borderRadius: 14, padding: '12px 30px'}}>
        <span style={{fontSize: 32, fontWeight: 700, color: T.dink3}}>환율이 나온 날 </span><span style={{fontSize: 56, fontWeight: 700, color: T.dink}}>{cnt >= 679 ? p.total : `${cnt}일`}</span></div>}
      {/* 3줄: 81일 · 열흘에 하루꼴 */}
      {f >= at(3) && f < at(4) + 8 && <div style={{position: 'absolute', left: X0 + 20, top: YT - 6, opacity: chip(mid(3, 0.35), at(4)), display: 'flex', gap: 14, alignItems: 'center', ...F, whiteSpace: 'nowrap'}}>
        <span style={{background: T.accent, color: T.surface, borderRadius: 12, padding: '8px 20px', fontSize: 36, fontWeight: 700}}>지금보다 쌌던 날 {p.usdCount}</span>
        <span style={{background: T.ink, color: T.dink, borderRadius: 12, padding: '8px 20px', fontSize: 32, fontWeight: 700, opacity: g(f, mid(3, 0.65))}}>{p.usdRatio}</span></div>}
      {/* 4줄: 엔화 4일 */}
      {f >= at(4) && f < at(5) + 8 && <div style={{position: 'absolute', left: 960, top: YT - 76,   // 엔화 선 봉우리(y 451)와 안 겹치게 위로
 opacity: chip(at(4) + 30, at(5)), ...F, whiteSpace: 'nowrap',
        background: T.accent, color: T.surface, borderRadius: 12, padding: '8px 20px', fontSize: 36, fontWeight: 700}}>엔화가 지금보다 쌌던 날 {p.jpyCount}</div>}
      {/* 5줄: 두 결론 · 6줄: 끝 띠 */}
      {f >= at(5) && f < at(6) + 8 && <div style={{position: 'absolute', left: X0, top: YT - 84,   // 4줄 칩 자리와 다른 곳 — 같은 자리면 U5가 같은 화면으로 셈
 display: 'flex', gap: 16, opacity: chip(at(5), at(6)), ...F, whiteSpace: 'nowrap'}}>
        {p.sumUp.map((s, i) => <span key={i} style={{opacity: i ? g(f, mid(5, 0.5)) : 1, background: i ? T.accent : T.fall, color: T.dink, borderRadius: 14, padding: '12px 26px', fontSize: 38, fontWeight: 700}}>{s}</span>)}</div>}
      {f >= at(6) && <div style={{position: 'absolute', left: X0 + 20, top: YT - 6 + (1 - Math.min(1, sp(at(6)))) * 14, opacity: sp(at(6)), background: T.ink, borderRadius: 12, padding: '10px 22px', ...F, fontSize: 34, fontWeight: 700, color: T.dink, whiteSpace: 'nowrap'}}>{p.mid}</div>}
    </>
  );
};
