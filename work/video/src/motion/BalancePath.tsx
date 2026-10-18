// 잔액 경로 선 그래프(10/19 벤치마크 지시, research/longform/quality-gap-1019.md ①) — 사람 2~3줄, 해마다 점이 찍히며 선이 이어지고 바닥 난 해에 표시.
// X1.tsx LineS(TallyLineChart: 선 전체를 왼→오 한 번에 닦아 그림)와 다른 점: 사람마다 시작 해가 다르고(가로축 = 달력 해), 점이 하나씩 '찍히며' 선이 따라오고,
// 머리 꼬리표(이름·지금 값)가 끝을 따라가며, 바닥 난 해에 빨간 세로 띠 + 꼬리표, 끝까지 버틴 줄은 끝 꼬리표가 붙는다.
// 8초 안에 새 요소가 붙는 판(design-spec-1016 §10 — 40초까지)이 되도록 점이 1초 안팎마다 하나씩 붙는다. 판 전체는 1.00→1.03 천천히 다가간다.
// 숫자는 props로만(예 ep/C-2/motion_preview/balprops.py가 calc_n1_out.txt에서 뽑음). 글자는 HTML(카메라 안 SVG 글자가 mp4에서 어긋난 10/14 교훈), 선·점만 SVG.
import React from 'react';
import {interpolate, useCurrentFrame, useVideoConfig, spring, Easing} from 'remotion';
import {T, F, CL} from '../parts/fm';

export type BalPerson = {name: string; color: string; start: number; vals: number[]; at: number; per: number;
  floor?: {year: number; text: string}; end?: string};
export type BalancePathProps = {seed: string; y0: number; y1: number; min: number; max: number;
  ticks: [number, string][]; xlabels: [number, string][]; base?: [number, string]; people: BalPerson[];
  box?: {x: number; y: number; w: number; h: number}; beats?: number[]};

const COL: Record<string, string> = {accent: T.accent, ink: T.ink, fall: T.fall, rise: T.rise, gray: T.ink3};
const hash = (s: string) => [...s].reduce((a, c) => (a * 31 + c.charCodeAt(0)) >>> 0, 7);
const fmt = (v: number) => v >= 1 ? `${v.toFixed(2)}억` : `${Math.round(v * 10000).toLocaleString()}만원`;

export const BalancePath: React.FC<BalancePathProps> = ({seed, y0, y1, min, max, ticks, xlabels, base, people, box}) => {
  const f = useCurrentFrame(); const {fps, durationInFrames} = useVideoConfig();
  const h0 = hash(seed);
  const B = box ?? {x: 300 + (h0 % 3) * 20, y: 330, w: 1220, h: 420};
  const R = 9 + (h0 % 4);                       // 점 크기 — 편마다 조금씩
  const X = (yr: number) => B.x + ((yr - y0) / (y1 - y0)) * B.w;
  const Y = (v: number) => B.y + B.h - ((v - min) / (max - min)) * B.h;
  const zoom = interpolate(f, [0, durationInFrames], [1, 1.03], CL);
  const grid = interpolate(f, [0, 14], [0, 1], {...CL, easing: Easing.out(Easing.cubic)});

  const lines = people.map((p) => {
    const c = COL[p.color] || p.color; const n = p.vals.length;
    const u = Math.max(-1, Math.min(n - 1, (f - p.at) / p.per));      // 선 끝이 지금 몇 번째 점까지 왔나(소수)
    const k = Math.floor(u);
    const pts = p.vals.map((v, i) => [X(p.start + i), Y(v)] as const);
    let d = '';
    if (u >= 0) {
      d = pts.slice(0, k + 1).map(([x, y], i) => `${i ? 'L' : 'M'}${x.toFixed(1)} ${y.toFixed(1)}`).join(' ');
      if (k < n - 1) { const t = Easing.inOut(Easing.quad)(u - k); const [ax, ay] = pts[k]; const [bx, by] = pts[k + 1]; d += ` L${(ax + (bx - ax) * t).toFixed(1)} ${(ay + (by - ay) * t).toFixed(1)}`; }
    }
    const done = u >= n - 1; const doneAt = p.at + (n - 1) * p.per;
    return {p, c, n, u, k, pts, d, done, doneAt};
  });

  return (
    <div style={{position: 'absolute', inset: 0, transform: `scale(${zoom})`, transformOrigin: `${B.x + B.w / 2}px ${B.y + B.h / 2}px`}}>
      {/* 바닥 난 해: 빨간 세로 띠(SVG 밖 div — 선보다 아래) */}
      {lines.map(({p, done, doneAt}, i) => p.floor && done ? (
        <div key={'fb' + i} style={{position: 'absolute', left: X(p.floor.year) - 22, top: B.y - 10, width: 44, height: B.h + 10,
          background: T.rise, opacity: 0.14 * interpolate(f, [doneAt, doneAt + 12], [0, 1], CL), borderRadius: 10}} />) : null)}
      <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0, opacity: grid}}>
        {ticks.map(([v], i) => <line key={i} x1={B.x} x2={B.x + B.w} y1={Y(v)} y2={Y(v)} stroke={v === min ? T.ink3 : T.line} strokeWidth={v === min ? 3 : 2} />)}
        {base ? <line x1={B.x} x2={B.x + B.w} y1={Y(base[0])} y2={Y(base[0])} stroke={T.ink2} strokeWidth={3} strokeDasharray="10 9" /> : null}
        {lines.map(({c, d, pts, u, p}, i) => (
          <g key={i}>
            {d ? <path d={d} fill="none" stroke={c} strokeWidth={6} strokeLinejoin="round" strokeLinecap="round" /> : null}
            {pts.map(([x, y], j) => {
              if (j > u) return null;
              const s = spring({frame: f - (p.at + j * p.per), fps, config: {damping: 11, stiffness: 180}});
              return <circle key={j} cx={x} cy={y} r={R * (0.4 + 0.6 * s)} fill="#fff" stroke={c} strokeWidth={4} />;
            })}
          </g>
        ))}
      </svg>
      {/* 축 글자(HTML) */}
      {ticks.map(([v, t], i) => <div key={'t' + i} style={{...F, position: 'absolute', left: B.x - 120, width: 104, top: Y(v) - 15, textAlign: 'right', fontSize: 24, fontWeight: 500, color: T.ink3, opacity: grid}}>{t}</div>)}
      {xlabels.map(([yr, t], i) => <div key={'x' + i} style={{...F, position: 'absolute', left: X(yr) - 80, width: 160, top: B.y + B.h + 14, textAlign: 'center', fontSize: 24, fontWeight: 500, color: T.ink3, opacity: grid}}>{t}</div>)}
      {base ? <div style={{...F, position: 'absolute', left: B.x + B.w * 0.6, top: Y(base[0]) + 8, fontSize: 24, fontWeight: 700, color: T.ink2, opacity: grid}}>{base[1]}</div> : null}
      {/* 머리 꼬리표: 이름 · 지금 1월 값 — 끝을 따라간다 */}
      {lines.map(({p, c, u, k, pts, done}, i) => {
        if (u < 0) return null;
        const kk = Math.max(0, k); const t = k < pts.length - 1 ? Easing.inOut(Easing.quad)(u - k) : 0;
        const [ax, ay] = pts[kk]; const [bx, by] = pts[Math.min(kk + 1, pts.length - 1)];
        const hx = ax + (bx - ax) * t; const hy = ay + (by - ay) * t;
        const o = interpolate(f, [p.at, p.at + 8], [0, 1], CL);
        const fin = done && (p.end || p.floor);
        return (
          <div key={'h' + i} style={{position: 'absolute', left: hx + 18, top: hy - 64, opacity: fin ? 0 : o, whiteSpace: 'nowrap', ...F}}>
            <span style={{fontSize: 30, fontWeight: 700, color: c}}>{p.name}</span>
            <span style={{fontSize: 30, fontWeight: 700, color: T.ink2, marginLeft: 12}}>{p.start + kk}년 1월 · {fmt(p.vals[kk])}</span>
          </div>
        );
      })}
      {/* 끝: 바닥 꼬리표(빨강) 또는 끝 값 꼬리표(그 줄 색) */}
      {lines.map(({p, c, pts, done, doneAt}, i) => {
        if (!done) return null;
        const s = spring({frame: f - doneAt - 4, fps, config: {damping: 12, stiffness: 160}});
        const [ex, ey] = pts[pts.length - 1];
        const hot = !!p.floor; const bg = hot ? T.rise : c;
        const text = hot ? `${p.name} ${p.floor!.text}` : `${p.name} ${p.end}`;
        const left = ex + 22 > B.x + B.w - 420;   // 오른쪽 끝이면 왼쪽으로
        return (
          <div key={'e' + i} style={{position: 'absolute', left: ex, top: ey, opacity: s,
            transform: `translate(${left ? 'calc(-100% - 22px)' : '22px'}, ${hot ? '-130%' : '-140%'}) scale(${0.7 + 0.3 * s})`, transformOrigin: left ? 'right center' : 'left center',
            ...F, fontSize: 32, fontWeight: 700, color: '#fff', background: bg, borderRadius: 10, padding: '8px 16px', whiteSpace: 'nowrap', boxShadow: '0 8px 20px rgba(0,0,0,0.16)'}}>{text}</div>
        );
      })}
    </div>
  );
};
