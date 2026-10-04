// Tally 움직임 부품 ② 숫자 굴러가기 — from에서 to로 굴러간다(내려가는 것도 됨). 천 단위 쉼표·소수 자릿수 고정.
// 끝값 글자는 받은 그대로(text) 보여 준다 — 굴러가는 중간값만 계산값이고, 멈춘 뒤 화면 숫자는 facts.txt 문구와 같다.
import React from 'react';
import {interpolate, useCurrentFrame, Easing} from 'remotion';
import {T, F, CL} from '../parts/fm';

export const tallyFmt = (v: number, digits = 0) => Math.abs(v).toLocaleString('en-US', {minimumFractionDigits: digits, maximumFractionDigits: digits});

export const TallyCountUp: React.FC<{from?: number; to: number; text: string; start: number; dur?: number; digits?: number; prefix?: string; suffix?: string;
  size?: number; color?: string; x: number; y: number; label?: string; labelSize?: number; note?: string}> =
  ({from = 0, to, text, start, dur = 36, digits = 0, prefix = '', suffix = '', size = 150, color = T.accent, x, y, label, labelSize = 34, note}) => {
  const f = useCurrentFrame();
  const p = interpolate(f, [start, start + dur], [0, 1], {...CL, easing: Easing.out(Easing.cubic)});
  const o = interpolate(f, [start - 6, start], [0, 1], CL);
  const v = from + (to - from) * p;
  const shown = p >= 1 ? text : `${prefix}${v < 0 ? '−' : ''}${tallyFmt(v, digits)}${suffix}`;
  return (
    <div style={{position: 'absolute', left: x, top: y, opacity: o}}>
      {label ? <div style={{...F, fontWeight: 700, fontSize: labelSize, color: T.ink2, marginBottom: 6, whiteSpace: 'nowrap'}}>{label}</div> : null}
      <div style={{...F, fontWeight: 700, fontSize: size, color, lineHeight: 1, whiteSpace: 'nowrap', letterSpacing: -2}}>{shown}</div>
      {note ? <div style={{...F, fontWeight: 500, fontSize: 28, color: T.ink3, marginTop: 12, whiteSpace: 'nowrap'}}>{note}</div> : null}
    </div>
  );
};
