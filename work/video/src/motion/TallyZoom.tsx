// Tally 움직임 부품 ⑤ 강조 숫자 키우기 — 작게 나타났다가 살짝 넘쳐서 제자리 크기로(스프링). 핵심 숫자 하나에만 쓴다.
import React from 'react';
import {spring, useCurrentFrame, useVideoConfig, interpolate} from 'remotion';
import {T, F, CL} from '../parts/fm';

export const TallyZoom: React.FC<{text: string; start: number; x: number; y: number; size?: number; color?: string; label?: string; note?: string; from?: number}> =
  ({text, start, x, y, size = 170, color = T.accent, label, note, from = 0.55}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const s = spring({frame: f - start, fps, config: {damping: 11, stiffness: 120}});
  const o = interpolate(f, [start, start + 6], [0, 1], CL);
  const lo = interpolate(f, [start + 10, start + 20], [0, 1], CL);
  return (
    <div style={{position: 'absolute', left: x, top: y}}>
      {label ? <div style={{...F, fontWeight: 700, fontSize: 36, color: T.ink2, marginBottom: 10, opacity: o, whiteSpace: 'nowrap'}}>{label}</div> : null}
      <div style={{...F, fontWeight: 700, fontSize: size, color, lineHeight: 1, opacity: o, transform: `scale(${from + (1 - from) * s})`, transformOrigin: 'left center', whiteSpace: 'nowrap', letterSpacing: -2}}>{text}</div>
      {note ? <div style={{...F, fontWeight: 500, fontSize: 30, color: T.ink3, marginTop: 16, opacity: lo, whiteSpace: 'nowrap'}}>{note}</div> : null}
    </div>
  );
};
