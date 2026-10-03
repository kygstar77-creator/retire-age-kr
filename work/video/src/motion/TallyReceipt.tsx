// Tally 움직임 부품 ④ 영수증 한 줄씩 인쇄 — 종이가 위에서 내려오고, 줄마다 시작 프레임에 왼쪽→오른쪽으로 찍힌다(가림막이 걷히듯).
// 줄 색: in(잉크) · tax(빨강, 빠지는 돈) · net(굵은 주황, 남은 돈) · blank(회색 빗금, '확인 안 함') · hi(주황 강조) · dim(회색)
import React from 'react';
import {interpolate, useCurrentFrame, Easing} from 'remotion';
import {T, F, CL} from '../parts/fm';

export type TallyRow = {label: string; value?: string; tone?: 'in' | 'tax' | 'net' | 'blank' | 'hi' | 'dim'; start: number; note?: string};

export const TallyReceipt: React.FC<{x: number; y: number; w: number; head: string; rows: TallyRow[]; size?: number; start?: number; printDur?: number; active?: number; stamp?: {text: string; start: number}}> =
  ({x, y, w, head, rows, size = 36, start = 0, printDur = 14, active = -1, stamp}) => {
  const f = useCurrentFrame();
  const drop = interpolate(f, [start, start + 14], [0, 1], {...CL, easing: Easing.out(Easing.cubic)});
  const rowH = size * 1.75;
  const h = 96 + rows.length * rowH + 26;
  const teeth = Math.floor(w / 26);
  return (
    <div style={{position: 'absolute', left: x, top: y - (1 - drop) * 80, width: w, opacity: drop}}>
      <div style={{position: 'relative', width: w, height: h, background: T.surface, boxShadow: '0 14px 40px rgba(0,0,0,0.09)', borderRadius: '14px 14px 0 0'}}>
        <div style={{...F, fontWeight: 700, fontSize: size * 0.8, color: T.ink2, padding: '26px 34px 0', whiteSpace: 'nowrap'}}>{head}</div>
        <div style={{position: 'absolute', left: 34, right: 34, top: 82, borderTop: `3px dashed ${T.line}`}} />
        {rows.map((r, i) => {
          const tone = r.tone ?? 'in';
          const p = interpolate(f, [r.start, r.start + printDur], [0, 1], {...CL, easing: Easing.inOut(Easing.quad)});
          const col = tone === 'tax' ? T.rise : tone === 'net' || tone === 'hi' ? T.accent : tone === 'blank' || tone === 'dim' ? T.ink3 : T.ink;
          const top = 96 + i * rowH;
          return (
            <div key={i} style={{position: 'absolute', left: 34, right: 34, top, height: rowH, clipPath: `inset(0 ${(1 - p) * 100}% 0 0)`,
              borderTop: tone === 'net' ? `3px solid ${T.ink}` : undefined, display: 'flex', alignItems: 'center',
              background: tone === 'blank' ? `repeating-linear-gradient(135deg, ${T.bg} 0 10px, ${T.surface} 10px 20px)` : i === active ? T.soft : undefined, borderRadius: tone === 'blank' || i === active ? 8 : 0,
              boxShadow: i === active ? `inset 6px 0 0 ${T.accent}` : undefined, paddingLeft: i === active ? 14 : 0, paddingRight: i === active ? 10 : 0}}>
              <span style={{...F, fontWeight: tone === 'net' || tone === 'hi' ? 700 : 500, fontSize: tone === 'net' ? size * 0.92 : size * 0.8, color: tone === 'blank' || tone === 'dim' ? T.ink3 : T.ink2,
                paddingLeft: tone === 'blank' ? 12 : 0, whiteSpace: 'nowrap'}}>{r.label}{r.note ? <span style={{fontSize: size * 0.56, color: T.ink3, marginLeft: 12}}>{r.note}</span> : null}</span>
              <span style={{...F, fontWeight: 700, fontSize: tone === 'net' ? size * 1.15 : size, color: col, marginLeft: 'auto', paddingRight: tone === 'blank' ? 12 : 0, whiteSpace: 'nowrap'}}>{r.value ?? ''}</span>
            </div>
          );
        })}
      </div>
      {stamp && f >= stamp.start ? (
        <div style={{position: 'absolute', right: 24, top: 18, ...F, fontWeight: 700, fontSize: size * 0.7, color: T.accent, border: `4px solid ${T.accent}`, borderRadius: 10, padding: '4px 14px',
          transform: `rotate(-6deg) scale(${interpolate(f, [stamp.start, stamp.start + 8], [1.6, 1], CL)})`, opacity: interpolate(f, [stamp.start, stamp.start + 6], [0, 1], CL), background: 'rgba(255,255,255,0.85)'}}>{stamp.text}</div>
      ) : null}
      <svg width={w} height={18} style={{display: 'block'}}>
        <path d={`M0 0 ${Array.from({length: teeth}).map((_, i) => `L${(i + 0.5) * (w / teeth)} 16 L${(i + 1) * (w / teeth)} 0`).join(' ')} Z`} fill={T.surface} />
      </svg>
    </div>
  );
};
