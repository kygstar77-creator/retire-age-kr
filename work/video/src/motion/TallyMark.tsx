// Tally 움직임 부품 ⑥ 표시 — 손그림 동그라미(그려지며 나타남) · 검은 값 꼬리표(톡 튀어나옴) · 화살표 말풍선
// 경쟁 상위 영상(소수몽키·수페TV 프레임)에서 판 안의 숫자에 동그라미·꼬리표를 차례로 붙여 시선을 끄는 방식을 파이어맵 색으로(2026-10-03)
import React from 'react';
import {interpolate, spring, useCurrentFrame, useVideoConfig, Easing} from 'remotion';
import {T, F, CL, HandCircle} from '../parts/fm';

export const TallyCircle: React.FC<{cx: number; cy: number; rx: number; ry: number; start: number; color?: string}> = ({cx, cy, rx, ry, start, color = T.accent}) => {
  const f = useCurrentFrame();
  const p = interpolate(f, [start, start + 16], [0, 1], {...CL, easing: Easing.inOut(Easing.cubic)});
  if (p <= 0) return null;
  return <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0, pointerEvents: 'none'}}><HandCircle cx={cx} cy={cy} rx={rx} ry={ry} p={p} color={color} /></svg>;
};

// 값 꼬리표: 잉크 바탕 흰 글자(강조면 주황 바탕). anchor = 꼬리 끝 좌표, side = 꼬리표가 놓일 쪽
export const TallyTag: React.FC<{x: number; y: number; text: string; start: number; side?: 'up' | 'down' | 'left' | 'right'; hot?: boolean; size?: number}> =
  ({x, y, text, start, side = 'up', hot, size = 24}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const s = spring({frame: f - start, fps, config: {damping: 12, stiffness: 160}});
  if (f < start) return null;
  const off = 18;
  const tr = side === 'up' ? `translate(-50%, calc(-100% - ${off}px))` : side === 'down' ? `translate(-50%, ${off}px)` : side === 'left' ? `translate(calc(-100% - ${off}px), -50%)` : `translate(${off}px, -50%)`;
  const bg = hot ? T.accent : T.ink;
  return (
    <>
      <div style={{position: 'absolute', left: x - 6, top: y - 6, width: 12, height: 12, borderRadius: 6, background: bg, opacity: s}} />
      <div style={{position: 'absolute', left: x, top: y, transform: `${tr} scale(${0.6 + 0.4 * s})`, transformOrigin: 'center', opacity: s,
        ...F, fontWeight: 700, fontSize: size, color: '#fff', background: bg, borderRadius: 8, padding: '5px 12px', whiteSpace: 'nowrap', boxShadow: '0 6px 16px rgba(0,0,0,0.18)'}}>{text}</div>
    </>
  );
};

// 말풍선: 흰 바탕 주황 테두리 짧은 문장 + 꼬리 삼각형(아래쪽)
export const TallyCallout: React.FC<{x: number; y: number; text: string; start: number; w?: number; size?: number}> = ({x, y, text, start, w, size = 28}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const s = spring({frame: f - start, fps, config: {damping: 13}});
  if (f < start) return null;
  return (
    <div style={{position: 'absolute', left: x, top: y, width: w, opacity: s, transform: `translateY(${(1 - s) * 16}px)`}}>
      <div style={{...F, fontWeight: 700, fontSize: size, color: T.ink, background: '#fff', border: `3px solid ${T.accent}`, borderRadius: 14, padding: '10px 18px', lineHeight: 1.3, wordBreak: 'keep-all'}}>{text}</div>
    </div>
  );
};
