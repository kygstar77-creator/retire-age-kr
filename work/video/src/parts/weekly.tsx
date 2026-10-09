// 주간 뉴스 영수증 그림 부품 — W-1(이번 주 뉴스가 내 돈에 얼마)에서 처음 씀(2026-10-09 PD, parts.md 기록). 숫자 글자는 전부 props(w1props.py가 calc_out·raw에서 뽑음).
// WeekStrip(월~금 다섯 칸, 쉬는 날 빗금·연 날만 막대) · BridgeBars(바닥을 잘라 낸 다리 막대 — 큰 금액 위 작은 차이) · DotCount(n개 점이 차례로 — '몇 번과 같은 크기')
// · NextCal(다음 주 달력 줄 + 뒤에 올 날짜 칩) · MiniLine(작은 선 그래프, 처음·끝 값 꼬리표 — 두 개를 위아래로 놓아 축이 다른 두 값 비교)
import React from 'react';
import {interpolate, useCurrentFrame, Easing, spring, useVideoConfig} from 'remotion';
import {T, F, CL} from './fm';

const grow = (f: number, at: number, d = 20) => interpolate(f, [at, at + d], [0, 1], {...CL, easing: Easing.out(Easing.cubic)});
const fade = (f: number, at: number, d = 10) => interpolate(f, [at, at + d], [0, 1], CL);
const hatch = `repeating-linear-gradient(135deg, ${T.line} 0 12px, ${T.surface} 12px 24px)`;
const lift = '0 10px 30px rgba(0,0,0,0.07)';

// 다섯 칸 띠: days = [요일, 날짜, 쉬는 날 이름|null, 값|null, 값 글자|null, 나타날 프레임]. 연 날은 값 높이 막대(lo~hi 구간), 쉬는 날은 빗금
export const WeekStrip: React.FC<{days: [string, string, string | null, number | null, string | null, number][]; lo: number; hi: number; x?: number; y?: number; w?: number; h?: number; barAt?: number}> =
  ({days, lo, hi, x = 150, y = 320, w = 1620, h = 480, barAt = 0}) => {
  const f = useCurrentFrame();
  const g = 24; const cw = (w - g * (days.length - 1)) / days.length; const bh = h - 150;
  return (
    <>
      {days.map(([dow, date, off, v, vt, at], i) => {
        const o = fade(f, at, 10); const p = grow(f, Math.max(at, barAt) + i * 5, 22);
        const bar = v == null ? 0 : ((v - lo) / (hi - lo)) * bh;
        return (
          <div key={i} style={{position: 'absolute', left: x + i * (cw + g), top: y, width: cw, height: h, opacity: o, transform: `translateY(${(1 - o) * 16}px)`}}>
            <div style={{...F, fontWeight: 700, fontSize: 40, color: off ? T.ink3 : T.ink, textAlign: 'center', whiteSpace: 'nowrap'}}>{dow}</div>
            <div style={{...F, fontWeight: 500, fontSize: 26, color: T.ink3, textAlign: 'center', marginTop: 4, whiteSpace: 'nowrap'}}>{date}</div>
            <div style={{position: 'absolute', left: 0, right: 0, top: 110, height: h - 110, borderRadius: 18, background: off ? hatch : T.surface, boxShadow: off ? undefined : lift}}>
              {off ? <div style={{...F, position: 'absolute', left: 0, right: 0, top: (h - 110) / 2 - 22, textAlign: 'center', fontWeight: 700, fontSize: off.length > 7 ? 26 : 32, color: T.ink2, whiteSpace: 'nowrap'}}>{off}</div> : null}
              {v != null ? <>
                <div style={{position: 'absolute', left: cw * 0.22, width: cw * 0.56, bottom: 20, height: bar * p, background: T.ink2, borderRadius: '12px 12px 4px 4px'}} />
                <div style={{...F, position: 'absolute', left: 0, right: 0, bottom: 30 + bar * p, textAlign: 'center', fontWeight: 700, fontSize: 32, color: T.ink, opacity: p, whiteSpace: 'nowrap'}}>{vt}</div>
              </> : null}
            </div>
          </div>
        );
      })}
    </>
  );
};

// 다리 막대: steps = [이름, 값(첫·끝은 금액, 가운데는 차이), 글자, 나타날 프레임]. 바닥(lo)을 잘라 작은 차이도 보이게 하고, 잘랐다는 물결 표시를 둔다
export const BridgeBars: React.FC<{steps: [string, number, string, number][]; lo: number; hi: number; x?: number; y?: number; w?: number; h?: number; unit?: string}> =
  ({steps, lo, hi, x = 200, y = 320, w = 1500, h = 440, unit = ''}) => {
  const f = useCurrentFrame();
  const sy = (v: number) => y + h - ((v - lo) / (hi - lo)) * h;
  const slot = w / steps.length; const bw = slot * 0.56;
  let run = 0;
  return (
    <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
      <line x1={x - 10} x2={x + w} y1={y + h} y2={y + h} stroke={T.ink3} strokeWidth={2} />
      <path d={`M${x - 30} ${y + h - 6} l14 -10 l14 10 l14 -10`} stroke={T.ink3} strokeWidth={3} fill="none" />
      <text x={x - 34} y={y + h + 88} fontFamily="PD" fontWeight={500} fontSize={22} fill={T.ink3}>{`아래 ${lo.toLocaleString()}${unit} 생략`}</text>
      {steps.map(([n, v, t, at], i) => {
        const o = grow(f, at, 20); const first = i === 0; const last = i === steps.length - 1; const bx = x + i * slot + (slot - bw) / 2;
        let y0: number, y1: number, col: string;
        if (first || last) { y0 = sy(v); y1 = y + h; col = last ? T.accent : T.ink2; if (first) run = v; }
        else { const a = run, b = run + v; y0 = sy(Math.max(a, b)); y1 = sy(Math.min(a, b)); col = v < 0 ? T.fall : T.rise; run = b; }
        const prevTop = i > 0 ? sy(first ? v : (last ? v : run - v)) : 0;
        const hh = (y1 - y0);
        return <g key={i} opacity={Math.min(1, o * 2)}>
          {i > 0 ? <line x1={bx - (slot - bw)} x2={bx} y1={prevTop} y2={prevTop} stroke={T.ink3} strokeWidth={2} strokeDasharray="6 6" /> : null}
          {first || last
            ? <rect x={bx} y={y1 - hh * o} width={bw} height={hh * o} rx={8} fill={col} />
            : <rect x={bx} y={v < 0 ? y0 : y1 - hh * o} width={bw} height={Math.max(4, hh * o)} rx={6} fill={col} />}
          <text x={bx + bw / 2} y={(first || last) ? y0 - 18 : y0 - 18} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={last ? 46 : 38} fill={first || last ? (last ? T.accent : T.ink) : col} opacity={o}>{t}</text>
          <text x={bx + bw / 2} y={y + h + 46} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={28} fill={T.ink2} opacity={o}>{n}</text>
        </g>;
      })}
    </svg>
  );
};

// 점 n개가 차례로 찍힌다(한 점 = 한 번). 오른쪽에 큰 숫자 하나
export const DotCount: React.FC<{n: number; at: number; label: string; big: string; per?: number; x?: number; y?: number; w?: number; color?: string}> =
  ({n, at, label, big, per = 11, x = 150, y = 340, w = 900, color = T.accent}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const g = 14; const d = (w - g * (per - 1)) / per;
  const done = fade(f, at + n * 1.2, 12);
  return (
    <>
      {Array.from({length: n}).map((_, i) => {
        const s = spring({frame: f - at - i * 1.2, fps, config: {damping: 14}});
        return <div key={i} style={{position: 'absolute', left: x + (i % per) * (d + g), top: y + Math.floor(i / per) * (d + g), width: d, height: d, borderRadius: '50%', background: color,
          opacity: f >= at + i * 1.2 ? 0.25 + 0.75 * s : 0, transform: `scale(${0.4 + 0.6 * s})`}} />;
      })}
      <div style={{position: 'absolute', left: x + w + 90, top: y + 10, opacity: done}}>
        <div style={{...F, fontWeight: 700, fontSize: 150, color, letterSpacing: -3, lineHeight: 1, whiteSpace: 'nowrap'}}>{big}</div>
        <div style={{...F, fontWeight: 700, fontSize: 30, color: T.ink2, marginTop: 18, whiteSpace: 'nowrap'}}>{label}</div>
      </div>
    </>
  );
};

// 다음 주 달력: cells = [요일, 날짜, 일 글자|null, 나타날 프레임, 강조?] + later = [날짜, 일 글자, 프레임] 칩 줄
export const NextCal: React.FC<{cells: [string, string, string | null, number, boolean][]; later: [string, string, number][]; x?: number; y?: number; w?: number}> =
  ({cells, later, x = 150, y: y0 = 320, w = 1620}) => {
  const y = later.length ? y0 : y0 + 100; // 아래 칩 줄이 없으면 보드 가운데로
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  // 일 있는 칸은 넓게(3배), 빈 날은 좁은 점선 칸 — 흰 면이 화면을 차지하지 않게(10/9 artist 지적)
  const g = 18; const wt = cells.map((c) => (c[2] ? 3 : 1)); const unit = (w - g * (cells.length - 1)) / wt.reduce((a, b) => a + b, 0); const ch = 270;
  const lefts = wt.map((_, i) => x + wt.slice(0, i).reduce((a, b) => a + b * unit + g, 0));
  return (
    <>
      {cells.map(([dow, date, ev, at, hot], i) => {
        const o = fade(f, at, 10); const s = spring({frame: f - at, fps, config: {damping: 13}}); const cw = wt[i] * unit;
        return (
          <div key={i} style={{position: 'absolute', left: lefts[i], top: y, width: cw, height: ch, borderRadius: 18, background: hot ? T.soft : ev ? T.surface : 'transparent',
            border: ev ? undefined : `3px dashed ${T.ink3}`, boxSizing: 'border-box',
            boxShadow: hot ? `inset 0 0 0 4px ${T.accent}` : ev ? lift : undefined, opacity: ev ? o : o * 0.55, transform: `scale(${hot ? 0.94 + 0.06 * s : 1})`}}>
            <div style={{...F, position: 'absolute', left: 22, top: 18, fontWeight: 700, fontSize: 30, color: T.ink2, whiteSpace: 'nowrap'}}>{dow}</div>
            <div style={{...F, position: 'absolute', ...(ev ? {right: 22, top: 18} : {left: 22, top: 64}), fontWeight: 700, fontSize: 30, color: T.ink3, whiteSpace: 'nowrap'}}>{date}</div>
            {ev ? ev.split('\n').map((t, k) => <div key={k} style={{...F, position: 'absolute', left: 22, right: 22, top: 100 + k * 44, fontWeight: 700, fontSize: 32, color: hot ? T.accent : T.ink, whiteSpace: 'nowrap'}}>{t}</div>) : null}
          </div>
        );
      })}
      {later.map(([date, ev, at], i) => {
        const o = fade(f, at, 10);
        return (
          <div key={i} style={{position: 'absolute', left: x + i * 560, top: y + ch + 60, opacity: o, transform: `translateX(${(1 - o) * 30}px)`, display: 'flex', alignItems: 'baseline', gap: 16}}>
            <span style={{...F, fontWeight: 700, fontSize: 34, color: T.surface, background: T.ink, borderRadius: 12, padding: '6px 16px', whiteSpace: 'nowrap'}}>{date}</span>
            <span style={{...F, fontWeight: 700, fontSize: 34, color: T.ink, whiteSpace: 'nowrap'}}>{ev}</span>
          </div>
        );
      })}
    </>
  );
};

// 오른쪽 위 고정 칸 '이번 주 영수증': cells = [이름, 값, 채워지는 프레임]. 장마다 한 줄씩 채워진다(앞 장 값은 0프레임에 이미 채움). C-1 ScoreBoard와 같은 모양, 머리글만 props
export const WeekTotal: React.FC<{head: string; cells: [string, string, number][]; x?: number; y?: number; w?: number}> = ({head, cells, x = 1440, y = 300, w = 340}) => {
  const f = useCurrentFrame();
  return (
    <div style={{position: 'absolute', left: x, top: y, width: w, background: T.ink, borderRadius: 18, padding: '16px 22px 14px', opacity: fade(f, 0, 8)}}>
      <div style={{...F, fontWeight: 700, fontSize: 22, color: T.daccent, marginBottom: 6, whiteSpace: 'nowrap'}}>{head}</div>
      {cells.map(([n, v, at], i) => {
        const o = fade(f, at, 8); const pop = spring({frame: f - at, fps: 30, config: {damping: 12}});
        return (
          <div key={i} style={{borderTop: i ? `1px solid ${T.dsurface}` : undefined, padding: '6px 0'}}>
            <div style={{...F, fontWeight: 700, fontSize: 22, color: T.dink3, whiteSpace: 'nowrap'}}>{n}</div>
            <div style={{...F, fontWeight: 700, fontSize: 36, color: f >= at ? T.dink : T.daccent, opacity: f >= at ? o : 0.85, textAlign: 'right', transform: `scale(${0.8 + 0.2 * pop})`, transformOrigin: 'right center', whiteSpace: 'nowrap'}}>{f >= at ? v : '?'}</div>
          </div>
        );
      })}
    </div>
  );
};

// 작은 선 그래프: pts = [x 글자, 값]. 처음·끝 점에 값 꼬리표. 위아래 두 개를 놓아 축이 다른 두 값(주가·환율)을 같은 날짜 순서로 비교
export const MiniLine: React.FC<{name: string; pts: [string, number][]; vt: [string, string]; color: string; at: number; x: number; y: number; w: number; h: number; note?: string}> =
  ({name, pts, vt, color, at, x, y, w, h, note}) => {
  const f = useCurrentFrame();
  const vs = pts.map((p) => p[1]); const lo = Math.min(...vs), hi = Math.max(...vs); const pad = (hi - lo) * 0.25 || 1;
  const sx = (i: number) => x + 240 + (i / (pts.length - 1)) * (w - 480); const sy = (v: number) => y + h - ((v - lo + pad) / (hi - lo + 2 * pad)) * h;
  const p = grow(f, at, 40); const len = (pts.length - 1) * p; const k = Math.floor(len);
  const path = pts.slice(0, k + 1).map((q, i) => `${i ? 'L' : 'M'}${sx(i)} ${sy(q[1])}`).join(' ') + (k < pts.length - 1 ? ` L${sx(k) + (sx(k + 1) - sx(k)) * (len - k)} ${sy(pts[k][1]) + (sy(pts[k + 1][1]) - sy(pts[k][1])) * (len - k)}` : '');
  const o = fade(f, at, 10);
  return (
    <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}} opacity={o}>
      <text x={x} y={y + h / 2 + 12} fontFamily="PD" fontWeight={700} fontSize={34} fill={color}>{name}</text>
      {note ? <text x={x} y={y + h / 2 + 52} fontFamily="PD" fontWeight={500} fontSize={22} fill={T.ink3}>{note}</text> : null}
      <line x1={sx(0)} x2={sx(pts.length - 1)} y1={y + h} y2={y + h} stroke={T.line} strokeWidth={2} />
      {pts.map((q, i) => <text key={i} x={sx(i)} y={y + h + 32} textAnchor="middle" fontFamily="PD" fontWeight={500} fontSize={22} fill={T.ink3}>{q[0]}</text>)}
      <path d={path} stroke={color} strokeWidth={6} fill="none" strokeLinejoin="round" strokeLinecap="round" />
      <circle cx={sx(0)} cy={sy(vs[0])} r={9} fill={color} />
      <text x={sx(0) - 20} y={sy(vs[0]) + 10} textAnchor="end" fontFamily="PD" fontWeight={700} fontSize={30} fill={T.ink2}>{vt[0]}</text>
      <g opacity={fade(f, at + 40, 8)}>
        <circle cx={sx(pts.length - 1)} cy={sy(vs[vs.length - 1])} r={11} fill={color} />
        <text x={sx(pts.length - 1) + 22} y={sy(vs[vs.length - 1]) + 12} fontFamily="PD" fontWeight={700} fontSize={36} fill={color}>{vt[1]}</text>
      </g>
    </svg>
  );
};
