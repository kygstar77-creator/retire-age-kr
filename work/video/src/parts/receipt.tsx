// 영수증 그림 부품 — R-1(1억의 1년 영수증, X-SERIES-1)에서 처음 씀. 시리즈 다음 편도 같은 모양으로 쓴다(parts.md 기록).
// 영수증 종이(위에서 내려오며 한 줄씩 인쇄, 빈 줄 '확인 안 함' 도장) · 점 띠(상품 하나 = 점 하나, 중앙·최저·최고) · 동전 떨어짐
import React from 'react';
import {interpolate} from 'remotion';
import {T, F, CL, appear} from './fm';

export type RLine = {label: string; v?: number | null; tone?: 'in' | 'tax' | 'net' | 'blank' | 'note'; o: number; text?: string};
const n0 = (v: number) => Math.abs(v).toLocaleString();
// 종이: 톱니 아래끝 · 줄마다 o(0~1)로 인쇄 · net 줄은 굵은 주황 · blank 줄은 회색 빗금 + 도장
export const ReceiptPaper: React.FC<{x: number; y: number; w: number; head: string; lines: RLine[]; o: number; dim?: number; size?: number}> =
  ({x, y, w, head, lines, o, dim = 1, size = 34}) => {
  const rowH = size * 1.9;
  const h = 110 + lines.length * rowH + 40;
  const teeth = Math.floor(w / 24);
  return (
    <div style={{position: 'absolute', left: x, top: y - (1 - o) * 120, width: w, opacity: Math.min(1, o * 1.5) * dim}}>
      <div style={{position: 'relative', width: w, height: h, background: T.surface, boxShadow: '0 14px 40px rgba(0,0,0,0.09)', borderRadius: '14px 14px 0 0'}}>
        <div style={{...F, fontWeight: 700, fontSize: size * 0.82, color: T.ink2, padding: '30px 36px 0', whiteSpace: 'nowrap'}}>{head}</div>
        <div style={{position: 'absolute', left: 36, right: 36, top: 92, borderTop: `3px dashed ${T.line}`}} />
        {lines.map((l, i) => {
          const top = 110 + i * rowH; const tone = l.tone ?? 'in';
          const col = tone === 'tax' ? T.rise : tone === 'net' ? T.accent : tone === 'blank' ? T.ink3 : tone === 'note' ? T.ink3 : T.ink;
          const val = l.text ?? (l.v == null ? '' : (l.v < 0 ? '−' : tone === 'in' && l.v > 0 && i > 0 ? '+' : '') + n0(l.v));
          return (
            <div key={i} style={{position: 'absolute', left: 36, right: 36, top: top + (1 - l.o) * 10, height: rowH, opacity: l.o, display: 'flex', alignItems: 'center',
              borderTop: tone === 'net' ? `3px solid ${T.ink}` : undefined,
              background: tone === 'blank' ? `repeating-linear-gradient(135deg, ${T.bg} 0 10px, ${T.surface} 10px 20px)` : undefined, borderRadius: tone === 'blank' ? 8 : 0}}>
              <span style={{...F, fontWeight: tone === 'net' ? 700 : 500, fontSize: tone === 'net' ? size * 0.95 : size * 0.8, color: tone === 'blank' ? T.ink3 : T.ink2, paddingLeft: tone === 'blank' ? 12 : 0, whiteSpace: 'nowrap'}}>{l.label}</span>
              <span style={{...F, fontWeight: 700, fontSize: tone === 'net' ? size * 1.25 : size, color: col, marginLeft: 'auto', paddingRight: tone === 'blank' ? 12 : 0, whiteSpace: 'nowrap'}}>{val}</span>
            </div>
          );
        })}
      </div>
      <svg width={w} height={18} style={{display: 'block'}}>
        <path d={`M0 0 ${Array.from({length: teeth}).map((_, i) => `L${(i + 0.5) * (w / teeth)} 16 L${(i + 1) * (w / teeth)} 0`).join(' ')} Z`} fill={T.surface} />
      </svg>
    </div>
  );
};

// '확인 안 함' 도장 — 비스듬히 찍힘
export const Stamp: React.FC<{x: number; y: number; o: number; text: string; color?: string; rot?: number; size?: number}> = ({x, y, o, text, color = T.ink3, rot = -8, size = 30}) => (
  <div style={{...F, position: 'absolute', left: x, top: y, opacity: o, transform: `rotate(${rot}deg) scale(${1.4 - 0.4 * o})`, fontWeight: 700, fontSize: size, color,
    border: `4px solid ${color}`, borderRadius: 12, padding: '6px 18px', whiteSpace: 'nowrap', background: 'rgba(255,255,255,0.7)'}}>{text}</div>
);

// 점 띠: 상품마다 점 하나(살짝 위아래로 흩뿌림), 중앙 막대, 최저·최고 숫자
export const DotStrip: React.FC<{x: number; y: number; w: number; dom: [number, number]; vals: number[]; label: string; o: number; color?: string; seed?: number; band?: number}> =
  ({x, y, w, dom, vals, label, o, color = T.ink2, seed = 7, band = 70}) => {
  const sx = (v: number) => x + ((v - dom[0]) / (dom[1] - dom[0])) * w;
  const med = vals[Math.floor(vals.length / 2)];
  const jit = (i: number) => (((Math.sin((i + 1) * 12.9898 * seed) * 43758.5453) % 1) + 1) % 1;
  return (
    <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
      <text x={x - 24} y={y + 10} textAnchor="end" fontFamily="PD" fontWeight={700} fontSize={32} fill={T.ink} opacity={o}>{label}</text>
      <text x={x - 24} y={y + 46} textAnchor="end" fontFamily="PD" fontWeight={500} fontSize={24} fill={T.ink3} opacity={o}>{vals.length}개</text>
      <line x1={x} x2={x + w} y1={y} y2={y} stroke={T.line} strokeWidth={2} opacity={o} />
      {vals.map((v, i) => {
        const oi = interpolate(o * vals.length * 1.6, [i * 0.6, i * 0.6 + 4], [0, 1], CL);
        return <circle key={i} cx={sx(v)} cy={y + (jit(i) - 0.5) * band} r={7} fill={color} opacity={0.55 * oi} />;
      })}
      <g opacity={appear(o * 60, 40, 15)}>
        <line x1={sx(med)} x2={sx(med)} y1={y - band / 2 - 14} y2={y + band / 2 + 14} stroke={T.accent} strokeWidth={6} strokeLinecap="round" />
        <text x={sx(med)} y={y - band / 2 - 26} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={30} fill={T.accent}>{`중앙 ${med.toFixed(2)}%`}</text>
        <text x={sx(vals[0])} y={y + band / 2 + 44} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={26} fill={T.ink3}>{`${vals[0].toFixed(2)}%`}</text>
        <text x={sx(vals[vals.length - 1])} y={y + band / 2 + 44} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={26} fill={T.ink}>{`${vals[vals.length - 1].toFixed(2)}%`}</text>
      </g>
    </svg>
  );
};

// 동전 n개가 차례로 떨어져 쌓임
export const Coins: React.FC<{x: number; y: number; n: number; f: number; start: number; label: string}> = ({x, y, n, f, start, label}) => (
  <div style={{position: 'absolute', left: x, top: y}}>
    {Array.from({length: n}).map((_, i) => {
      const p = interpolate(f, [start + i * 9, start + i * 9 + 14], [0, 1], CL);
      return <div key={i} style={{position: 'absolute', left: 0, top: -i * 18 - (1 - p) * 260, width: 110, height: 30, borderRadius: '50%', background: T.accent,
        border: `4px solid ${T.soft}`, opacity: p > 0 ? 1 : 0}} />;
    })}
    <div style={{...F, position: 'absolute', left: 140, top: -n * 9 - 6, fontWeight: 700, fontSize: 32, color: T.ink, whiteSpace: 'nowrap', opacity: appear(f, start + n * 9)}}>{label}</div>
  </div>
);
