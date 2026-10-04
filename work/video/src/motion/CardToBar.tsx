// 바닥이 기준선이 된다(2026-10-04 motion) — 근거 research/longform/motion-bench.md '모션 475' ③
// daniel-haida 'Taxtello' 규칙 6 "물체로 넘어간다" + gdgtify 'BUILD THE FLOOR' "끝 문장은 앞 글자가 지은 바닥 위에 선다":
//   숫자 밑에 그어진 바닥 선이 그대로 내려가 차트의 0 기준선이 되고, 숫자 자체가 날아가 제 막대 위 이름표가 된다. 컷 없음.
// v2(심사 6.9 반려 뒤): v1은 카드가 막대로 찌그러지는 도중 막대가 기준선에서 40px 떠 있었다(심사관 '정직성 위반') →
//   막대는 처음부터 기준선에 붙어서만 자란다.
// 차트 규칙(dataviz): 축 하나·막대는 0 기준선에서·높이는 값에 비례·글자는 잉크색, 강조색은 막대에만.
import React from 'react';
import {interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {settle} from './RollNumber';

const CL = {extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const};
const lerp = (a: number, b: number, t: number) => a + (b - a) * t;

export type CardToBarProps = {
  floor: {x: number; y: number; w: number; h: number};      // 앞 장면 바닥 선 자리
  num: {x: number; y: number; size: number};                // 앞 장면 숫자 왼쪽 위·크기(날아갈 출발점)
  a: {label: string; value: number; text: string};         // 숫자였던 막대(강조)
  b: {label: string; value: number; text: string};         // 옆에 새로 자라는 막대(비교)
  unit: string;
  baseY: number; maxH: number; barW: number; gapX: number; left: number;
  start: number;
  accent: string; muted: string; ink: string; ink2: string; font: string; numFont: string;
  aFirst?: boolean;
};

export const CardToBar: React.FC<CardToBarProps> = (P) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const t = settle(Math.max(0, f - P.start), fps, 150, 9);         // 바닥 선 → 기준선, 숫자 → 이름표(9프레임 안에 기준선이 제자리 — 그 뒤 기준선은 안 움직인다)
  const ga = settle(Math.max(0, f - P.start - 6), fps, 120, 16);   // 강조 막대 자람
  const gb = settle(Math.max(0, f - P.start - 12), fps, 120, 16);  // 비교 막대(한 번에 하나만 주목)
  const vmax = Math.max(P.a.value, P.b.value);
  const ha = (P.a.value / vmax) * P.maxH, hb = (P.b.value / vmax) * P.maxH;
  const aFirst = P.aFirst ?? true;
  const xa = P.left + (aFirst ? 0 : P.barW + P.gapX), xb = P.left + (aFirst ? P.barW + P.gapX : 0);
  const bw = (P.barW + P.gapX) * 2 - P.gapX + 48;
  const L = {x: lerp(P.floor.x, P.left - 24, t), y: lerp(P.floor.y, P.baseY, t), w: lerp(P.floor.w, bw, t), h: lerp(P.floor.h, 3, t)};
  const vs = 64;
  // 숫자: 큰 숫자 왼쪽 위 → 강조 막대 머리 위 가운데(크기 size → vs). 막대가 자라는 동안 막대 머리를 따라간다.
  const na = {x: xa + P.barW / 2, y: P.baseY - ha * ga - vs * 1.25};
  const sz = lerp(P.num.size, vs, t);
  const nx = lerp(P.num.x, na.x, t), ny = lerp(P.num.y, na.y, t);
  const lab = interpolate(f, [P.start + 10, P.start + 18], [0, 1], CL);
  return (
    <>
      <div style={{position: 'absolute', left: L.x, top: L.y, width: L.w, height: L.h, background: t < 0.6 ? P.accent : P.ink2, borderRadius: 3}} />
      <div style={{position: 'absolute', left: xa, top: P.baseY - ha * ga, width: P.barW, height: ha * ga, background: P.accent, borderRadius: '4px 4px 0 0'}} />
      <div style={{position: 'absolute', left: xb, top: P.baseY - hb * gb, width: P.barW, height: hb * gb, background: P.muted, borderRadius: '4px 4px 0 0'}} />
      {/* 날아가는 숫자(강조 막대 이름표가 된다) — 색은 노랑 → 잉크 */}
      <div style={{position: 'absolute', left: nx, top: ny, transform: `translateX(${-50 * t}%)`, fontFamily: P.numFont, fontSize: sz, lineHeight: 1.08,
        color: t < 0.7 ? P.accent : P.ink, fontVariantNumeric: 'tabular-nums', whiteSpace: 'nowrap'}}>{P.a.text}</div>
      <div style={{position: 'absolute', left: xb - 40, width: P.barW + 80, top: P.baseY - hb * gb - vs * 1.25, textAlign: 'center', opacity: gb,
        fontFamily: P.numFont, fontSize: vs, color: P.ink, fontVariantNumeric: 'tabular-nums'}}>{P.b.text}</div>
      {[{x: xa, v: P.a, o: lab}, {x: xb, v: P.b, o: lab * gb}].map((q, i) => (
        <div key={i} style={{position: 'absolute', left: q.x - 60, width: P.barW + 120, top: P.baseY + 20, textAlign: 'center', opacity: q.o,
          fontFamily: P.font, fontWeight: 700, fontSize: 46, color: i === 0 ? P.ink : P.ink2}}>{q.v.label}</div>
      ))}
      <div style={{position: 'absolute', left: P.left - 24, width: bw, textAlign: 'right', top: P.baseY + 96, fontFamily: P.font, fontWeight: 500, fontSize: 30, color: P.ink2, opacity: lab}}>단위 {P.unit}</div>
    </>
  );
};
