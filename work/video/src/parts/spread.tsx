// 사고팔 때 벌어지는 띠(SpreadBand) — X-1 '4. 바꾸는 순간 드는 돈'(2026-10-16 PD). TallyFrame 자식.
// 가운데 매매기준율 선 → 현찰 살 때 선이 위로 벌어지고(위 띠 = 살 때 더 내는 돈) → 현찰 팔 때 선이 아래로(아래 띠) →
// 사서 바로 팔면 동전이 위 선에서 아래 선까지 떨어짐(두 띠 합 = 사라지는 돈) → 우대를 받으면 위 띠가 줄어듦(75%·90% 자리 점선).
// 높이 = 원 차이 비례(0부터가 아닌 가운데 기준 — 축 눈금 없음, 값은 글자로). 숫자 글자는 전부 props(calc_out 5b·은행연합회 원문).
import React from 'react';
import {interpolate, useCurrentFrame, Easing} from 'remotion';
import {T, F, CL} from './fm';

export type SpreadBandProps = {
  mid: number; buy: number; sell: number; midText: string; buyText: string; sellText: string; pct: string;
  k1: string[]; k2: string[]; k3: string[]; pref: number[];
  beats: number[];   // [시작, 천 달러, 사서 바로 팔면, 우대] 프레임
};

const ease = (f: number, a: number, d = 18) => interpolate(f, [a, a + d], [0, 1], {...CL, easing: Easing.inOut(Easing.cubic)});
const fade = (f: number, a: number, d = 10) => interpolate(f, [a, a + d], [0, 1], CL);

export const SpreadBand: React.FC<SpreadBandProps> = (p) => {
  const f = useCurrentFrame(); const B = p.beats;
  const CY = 575, PX = 6.6, X0 = 640, X1 = 1160;
  const up = (p.buy - p.mid) * PX, dn = (p.mid - p.sell) * PX;
  const gUp = ease(f, 8, 22), gDn = ease(f, B[2], 22);
  const shrink = 1 - p.pref[0] * ease(f, B[3] + 6, 26);   // 1 → 0.25(75% 우대)
  const upNow = up * gUp * (f >= B[3] ? shrink : 1);
  const yBuy = CY - up * gUp, yBuyNow = CY - upNow, ySell = CY + dn * gDn;
  const coin = interpolate(f, [B[2] + 26, B[2] + 56], [0, 1], {...CL, easing: Easing.in(Easing.quad)});
  const k = f >= B[3] ? p.k3 : f >= B[2] ? p.k2 : f >= B[1] ? p.k1 : null;
  const kAt = f >= B[3] ? B[3] : f >= B[2] ? B[2] : B[1];
  const lab = (y: number, t: string, o: number, c: string, big = false) => (
    <div style={{...F, position: 'absolute', left: 140, width: X0 - 170, textAlign: 'right', top: y - (big ? 22 : 19), fontSize: big ? 36 : 32, fontWeight: 700, color: c, opacity: o, whiteSpace: 'nowrap'}}>{t}</div>
  );
  return (
    <>
      <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
        {/* 위 띠: 살 때 더 내는 돈 */}
        <rect x={X0} y={yBuyNow} width={X1 - X0} height={Math.max(0, upNow)} fill={T.soft} />
        {f >= B[3] && <rect x={X0} y={yBuy} width={X1 - X0} height={Math.max(0, yBuyNow - yBuy)} fill="none" stroke={T.accent} strokeWidth={3} strokeDasharray="10 8" opacity={fade(f, B[3] + 6)} />}
        {/* 아래 띠: 팔 때 덜 받는 돈 */}
        {gDn > 0 && <rect x={X0} y={CY} width={X1 - X0} height={dn * gDn} fill="#dbe6fb" />}
        <line x1={X0 - 20} x2={X1 + 20} y1={CY} y2={CY} stroke={T.ink} strokeWidth={5} />
        <line x1={X0 - 20} x2={X1 + 20} y1={yBuy} y2={yBuy} stroke={T.accent} strokeWidth={5} opacity={f >= B[3] ? 0.45 : 1} />
        {f >= B[3] && <line x1={X0 - 20} x2={X1 + 20} y1={yBuyNow} y2={yBuyNow} stroke={T.accent} strokeWidth={5} />}
        {f >= B[3] && <line x1={X0} x2={X1} y1={CY - up * (1 - p.pref[1])} y2={CY - up * (1 - p.pref[1])} stroke={T.accent} strokeWidth={3} strokeDasharray="6 8" opacity={fade(f, B[3] + 30)} />}
        {gDn > 0 && <line x1={X0 - 20} x2={X1 + 20} y1={ySell} y2={ySell} stroke={T.fall} strokeWidth={5} />}
        {/* 사서 바로 팔면: 동전이 위 선에서 아래 선까지 */}
        {f >= B[2] + 20 && f < B[3] && <>
          <line x1={X1 + 70} x2={X1 + 70} y1={yBuy} y2={yBuy + (CY + dn - yBuy) * coin} stroke={T.rise} strokeWidth={6} strokeDasharray="12 8" />
          <circle cx={X1 + 70} cy={yBuy + (CY + dn - yBuy) * coin} r={26} fill={T.accent} stroke="#fff" strokeWidth={4} />
        </>}
      </svg>
      {lab(yBuy, p.buyText, gUp * (f >= B[3] ? 0.55 : 1), T.accent)}
      {lab(CY, p.midText, 1, T.ink, true)}
      {gDn > 0 && lab(ySell, p.sellText, gDn, T.fall)}
      {f >= B[3] && <div style={{...F, position: 'absolute', left: X0 + 14, top: yBuyNow - 38, fontSize: 28, fontWeight: 700, color: T.accent, opacity: fade(f, B[3] + 24), whiteSpace: 'nowrap'}}>우대 받으면 ↓</div>}
      {/* 위 띠 안 % */}
      <div style={{...F, position: 'absolute', left: X0, width: X1 - X0, textAlign: 'center', top: (f >= B[3] ? yBuy - 50 : (yBuy + CY) / 2 - 22), fontSize: 36, fontWeight: 700, color: T.ink, opacity: fade(f, 26), whiteSpace: 'nowrap'}}>{p.pct}</div>
      {/* 오른쪽 카드 */}
      {k && <div style={{position: 'absolute', left: 1290, top: 380 + (1 - fade(f, kAt)) * 12, width: 480, opacity: fade(f, kAt), background: f >= B[3] ? '#fff' : T.ink, border: f >= B[3] ? `4px solid ${T.accent}` : 'none',
        borderRadius: 20, padding: '26px 30px', boxSizing: 'border-box'}}>
        <div style={{...F, fontSize: 32, fontWeight: 700, color: f >= B[3] ? T.ink2 : T.dink3, whiteSpace: 'nowrap'}}>{k[0]}</div>
        <div style={{...F, fontSize: 50, fontWeight: 700, color: f >= B[3] ? T.ink : '#fff', whiteSpace: 'nowrap', marginTop: 10}}>{k[1]}</div>
        <div style={{...F, fontSize: 30, fontWeight: 700, color: f >= B[3] ? T.accent : T.daccent, whiteSpace: 'nowrap', marginTop: 12}}>{k[2]}</div>
      </div>}
    </>
  );
};
