// Tally 움직임 부품 ③ 막대 자라기 — 막대마다 시작 프레임이 있고 바닥(또는 lo)에서 자란다. 세로(v)·가로(h).
// 막대는 서로 겹치지 않는 대상만 받는다(누적 구간 금지 — RULES '화면 글자·그래프 규칙' 1). lo를 주면 '최저~최고' 범위 막대.
// 값 글자(valueText)는 다 자란 뒤 나타나고, facts.txt 문구 그대로 넘겨받는다(코드에서 숫자를 만들지 않음).
import React from 'react';
import {interpolate, useCurrentFrame, Easing} from 'remotion';
import {T, F, CL} from '../parts/fm';

export type TallyBar = {label: string; value: number; lo?: number; valueText: string; start: number; color?: string; sub?: string; loText?: string};

export const TallyBars: React.FC<{bars: TallyBar[]; x: number; y: number; w: number; h: number; max: number; min?: number; dir?: 'v' | 'h';
  grow?: number; labelSize?: number; valueSize?: number; gap?: number; marker?: {value: number; text: string; start: number}}> =
  ({bars, x, y, w, h, max, min = 0, dir = 'v', grow = 22, labelSize = 32, valueSize = 40, gap, marker}) => {
  const f = useCurrentFrame();
  const n = bars.length;
  const sc = (v: number) => (v - min) / (max - min);
  if (dir === 'v') {
    const g = gap ?? Math.min(80, w / n * 0.35); const bw = (w - g * (n - 1)) / n;
    return (
      <div style={{position: 'absolute', left: x, top: y, width: w, height: h}}>
        <div style={{position: 'absolute', left: 0, right: 0, top: h, borderTop: `3px solid ${T.ink}`}} />
        {bars.map((b, i) => {
          const p = interpolate(f, [b.start, b.start + grow], [0, 1], {...CL, easing: Easing.out(Easing.cubic)});
          const lo = b.lo != null ? sc(b.lo) : 0; const hi = sc(b.value);
          const bh = (hi - lo) * h * p; const bottom = lo * h;
          const vo = interpolate(f, [b.start + grow - 6, b.start + grow + 4], [0, 1], CL);
          const lo2 = interpolate(f, [b.start - 8, b.start], [0, 1], CL);
          return (
            <div key={i}>
              <div style={{position: 'absolute', left: i * (bw + g), width: bw, bottom: 0, top: h - bottom - bh, height: bh, background: b.color ?? T.ink2, borderRadius: '10px 10px 0 0'}} />
              <div style={{...F, position: 'absolute', left: i * (bw + g) - 30, width: bw + 60, top: h - bottom - bh - valueSize - 16, textAlign: 'center', fontWeight: 700, fontSize: valueSize, color: b.color ?? T.ink, opacity: vo, whiteSpace: 'nowrap'}}>{b.valueText}</div>
              <div style={{...F, position: 'absolute', left: i * (bw + g) - 20, width: bw + 40, top: h + 14, textAlign: 'center', fontWeight: 700, fontSize: labelSize, color: T.ink, opacity: lo2, lineHeight: 1.2, wordBreak: 'keep-all'}}>{b.label}</div>
              {b.sub ? <div style={{...F, position: 'absolute', left: i * (bw + g) - 20, width: bw + 40, top: h + 14 + labelSize * 1.3, textAlign: 'center', fontWeight: 500, fontSize: labelSize * 0.72, color: T.ink3, opacity: lo2}}>{b.sub}</div> : null}
            </div>
          );
        })}
      </div>
    );
  }
  // 가로 막대: 이름 왼쪽(lw), 막대는 오른쪽으로 자람
  const lw = 300; const g = gap ?? 34; const bh = (h - g * (n - 1)) / n; const W = w - lw;
  const mo = marker ? interpolate(f, [marker.start, marker.start + 10], [0, 1], CL) : 0;
  return (
    <div style={{position: 'absolute', left: x, top: y, width: w, height: h}}>
      {bars.map((b, i) => {
        const p = interpolate(f, [b.start, b.start + grow], [0, 1], {...CL, easing: Easing.out(Easing.cubic)});
        const lo = b.lo != null ? sc(b.lo) : 0; const hi = sc(b.value);
        const vo = interpolate(f, [b.start + grow - 6, b.start + grow + 4], [0, 1], CL);
        const lo2 = interpolate(f, [b.start - 8, b.start], [0, 1], CL);
        const top = i * (bh + g);
        return (
          <div key={i}>
            <div style={{...F, position: 'absolute', left: 0, width: lw - 24, top, height: bh, display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'flex-end', opacity: lo2}}>
              <div style={{fontWeight: 700, fontSize: labelSize, color: T.ink, whiteSpace: 'nowrap'}}>{b.label}</div>
              {b.sub ? <div style={{fontWeight: 500, fontSize: labelSize * 0.68, color: T.ink3, whiteSpace: 'nowrap'}}>{b.sub}</div> : null}
            </div>
            <div style={{position: 'absolute', left: lw, width: W, top, height: bh, background: T.line, borderRadius: 10, opacity: 0.55 * lo2}} />
            <div style={{position: 'absolute', left: lw + lo * W, width: (hi - lo) * W * p, top, height: bh, background: b.color ?? T.ink2, borderRadius: 10}} />
            {b.loText ? <div style={{...F, position: 'absolute', left: lw + lo * W - 12, top: top + bh / 2 - valueSize * 0.6, transform: 'translateX(-100%)', fontWeight: 700, fontSize: valueSize * 0.8, color: T.ink3, opacity: vo, whiteSpace: 'nowrap'}}>{b.loText}</div> : null}
            <div style={{...F, position: 'absolute', left: lw + hi * W * 1 + 14 - (1 - p) * (hi - lo) * W, top: top + bh / 2 - valueSize * 0.6, fontWeight: 700, fontSize: valueSize, color: b.color ?? T.ink, opacity: vo, whiteSpace: 'nowrap'}}>{b.valueText}</div>
          </div>
        );
      })}
      {marker ? (
        <div style={{position: 'absolute', left: lw + sc(marker.value) * W - 3, top: -46, height: h + 56, width: 6, background: T.accent, borderRadius: 3, opacity: mo}}>
          <div style={{...F, position: 'absolute', top: -40, left: 0, transform: 'translateX(-50%)', fontWeight: 700, fontSize: 28, color: T.accent, whiteSpace: 'nowrap'}}>{marker.text}</div>
        </div>
      ) : null}
    </div>
  );
};
