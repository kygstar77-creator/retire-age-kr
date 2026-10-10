// 꺼내 쓰기(인출) 그림 부품 — C-1(배당으로 받기 vs 팔아서 쓰기)에서 처음 씀(2026-10-08 PD, parts.md 기록). 숫자 글자는 전부 props(c1props.py가 calc_out에서 뽑음).
// ScoreBoard(오른쪽 위 고갈 연차 점수판) · Tank(통장 통 + 매달 빠지는 돈) · VsTiles(두 칸 대결) · Duo(두 사람) · Ruler(문턱 자) · YearBars(해마다 막대 37개) · StartTiles(시작 해 칸 줄)
import React from 'react';
import {interpolate, useCurrentFrame, Easing, spring, useVideoConfig} from 'remotion';
import {T, F, CL} from './fm';

const grow = (f: number, at: number, d = 20) => interpolate(f, [at, at + d], [0, 1], {...CL, easing: Easing.out(Easing.cubic)});
const fade = (f: number, at: number, d = 10) => interpolate(f, [at, at + d], [0, 1], CL);
export const COLW: Record<string, string> = {accent: T.accent, fall: T.fall, ink: T.ink2, rise: T.rise};
const lift = '0 10px 30px rgba(0,0,0,0.07)';

// 점수판: 보드 오른쪽 위 고정 칸. cells = [이름, 값, 바뀌는 프레임] — 같은 이름 칸이 여러 장면에 이어지며 값만 바뀐다
export const ScoreBoard: React.FC<{cells: [string, string, number][]; x?: number; y?: number; w?: number}> = ({cells, x = 1420, y = 316, w = 360}) => {
  const f = useCurrentFrame();
  return (
    <div style={{position: 'absolute', left: x, top: y, width: w, background: T.ink, borderRadius: 18, padding: '16px 22px 14px', opacity: fade(f, 0, 8)}}>
      <div style={{...F, fontWeight: 700, fontSize: 22, color: T.daccent, marginBottom: 6}}>점수판 · 바닥나는 해</div>
      {cells.map(([n, v, at], i) => {
        const o = fade(f, at, 8); const pop = spring({frame: f - at, fps: 30, config: {damping: 12}});
        return (
          <div key={i} style={{display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', borderTop: i ? `1px solid ${T.dsurface}` : undefined, padding: '6px 0'}}>
            <span style={{...F, fontWeight: 700, fontSize: 26, color: T.dink3, whiteSpace: 'nowrap'}}>{n}</span>
            <span style={{...F, fontWeight: 700, fontSize: 40, color: f >= at ? T.dink : T.dink3, opacity: f >= at ? o : 0.4, transform: `scale(${0.8 + 0.2 * pop})`, transformOrigin: 'right center', whiteSpace: 'nowrap'}}>{f >= at ? v : '—'}</span>
          </div>
        );
      })}
    </div>
  );
};

// 통장 통: 위에서 '들어옴'(평균 수익), 아래로 매달 빠지는 동전 12개. 높이는 그대로(평균이면 안 줄어든다)
export const Tank: React.FC<{x: number; y: number; w: number; h: number; label: string; out: string; inText: string}> = ({x, y, w, h, label, out, inText}) => {
  const f = useCurrentFrame();
  const o = fade(f, 0, 10); const lvl = 0.82 + 0.03 * Math.sin(f / 9);
  return (
    <div style={{position: 'absolute', left: x, top: y, opacity: o}}>
      <div style={{position: 'absolute', left: 0, top: 0, width: w, height: h, borderRadius: 26, border: `4px solid ${T.ink}`, overflow: 'hidden', background: '#fff'}}>
        <div style={{position: 'absolute', left: 0, right: 0, bottom: 0, height: `${lvl * 100}%`, background: T.soft}} />
        <div style={{...F, position: 'absolute', left: 0, right: 0, top: h * 0.38, textAlign: 'center', fontWeight: 700, fontSize: 84, color: T.ink, letterSpacing: -2}}>{label}</div>
      </div>
      <div style={{...F, position: 'absolute', left: w + 40, top: 10, fontWeight: 700, fontSize: 34, color: T.rise, opacity: fade(f, 20), whiteSpace: 'nowrap'}}>↓ {inText} 불어남</div>
      {Array.from({length: 12}).map((_, i) => {
        const t = (f - 14 - i * 9) / 40; if (t < 0) return null; const p = t % 1;
        return <div key={i} style={{position: 'absolute', left: w / 2 - 18 + (i % 3 - 1) * 26, top: h + 10 + p * 90, width: 36, height: 36, borderRadius: 18, background: T.accent, opacity: 1 - p}} />;
      })}
      <div style={{...F, position: 'absolute', left: w + 40, top: h - 40, fontWeight: 700, fontSize: 40, color: T.accent, opacity: fade(f, 14), whiteSpace: 'nowrap'}}>{out}씩 빠져나감 →</div>
    </div>
  );
};

// 두 칸 대결: tiles = [머리, 큰 값, 아래 글, 시작, 색]
export const VsTiles: React.FC<{tiles: [string, string, string, number, string][]; x?: number; y?: number; w?: number}> = ({tiles, x = 150, y = 330, w = 1200}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig(); const g = 40; const cw = (w - g) / 2;
  return (
    <>
      {tiles.map(([head, big, sub, at, col], i) => {
        const s = spring({frame: f - at, fps, config: {damping: 13}}); const c = COLW[col] ?? T.ink;
        if (f < at) return <div key={i} style={{position: 'absolute', left: x + i * (cw + g), top: y, width: cw, height: 400, borderRadius: 22, border: `3px dashed ${T.line}`}} />;
        return (
          <div key={i} style={{position: 'absolute', left: x + i * (cw + g), top: y + (1 - s) * 30, width: cw, height: 400, background: T.surface, borderRadius: 22, opacity: s, boxShadow: `inset 0 10px 0 ${c}, ${lift}`}}>
            <div style={{...F, position: 'absolute', left: 40, top: 46, fontWeight: 700, fontSize: 44, color: T.ink2, whiteSpace: 'nowrap'}}>{head}</div>
            <div style={{...F, position: 'absolute', left: 40, top: 130, fontWeight: 700, fontSize: 92, color: c, letterSpacing: -2, whiteSpace: 'nowrap'}}>{big}</div>
            <div style={{...F, position: 'absolute', left: 40, top: 268, fontWeight: 700, fontSize: 32, color: T.ink3, whiteSpace: 'nowrap'}}>{sub}</div>
          </div>
        );
      })}
    </>
  );
};

// 두 사람: 왼쪽 a, 오른쪽 b(이름, 설명, 시작), 가운데 같은 돈 상자 · Person은 C-1 v5 사람 장면(persona)에서도 씀
export const Person: React.FC<{x: number; y: number; name: string; desc: string; at: number; color: string}> = ({x, y, name, desc, at, color}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig(); const s = spring({frame: f - at, fps, config: {damping: 12}});
  if (f < at) return null;
  return (
    <div style={{position: 'absolute', left: x, top: y + (1 - s) * 30, width: 420, opacity: s, textAlign: 'center'}}>
      <svg width={180} height={180} viewBox="0 0 100 100" style={{display: 'block', margin: '0 auto'}}>
        <circle cx={50} cy={34} r={20} fill={color} /><path d="M14 96 C14 66 30 58 50 58 C70 58 86 66 86 96 Z" fill={color} />
      </svg>
      <div style={{...F, fontWeight: 700, fontSize: 56, color: T.ink, marginTop: 14}}>{name}</div>
      <div style={{...F, fontWeight: 700, fontSize: 32, color, marginTop: 6, whiteSpace: 'nowrap'}}>{desc}</div>
    </div>
  );
};
export const Duo: React.FC<{mid: string; a: [string, string, number]; b: [string, string, number]}> = ({mid, a, b}) => {
  const f = useCurrentFrame();
  return (
    <>
      <Person x={180} y={320} name={a[0]} desc={a[1]} at={a[2]} color={T.accent} />
      <div style={{position: 'absolute', left: 760, top: 400, width: 400, height: 200, borderRadius: 22, background: T.ink, opacity: fade(f, 0), display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
        <span style={{...F, fontWeight: 700, fontSize: 60, color: '#fff'}}>{mid}</span>
      </div>
      <div style={{...F, position: 'absolute', left: 640, top: 470, fontWeight: 700, fontSize: 60, color: T.accent, opacity: fade(f, a[2] + 10)}}>←</div>
      <div style={{...F, position: 'absolute', left: 1210, top: 470, fontWeight: 700, fontSize: 60, color: T.fall, opacity: fade(f, b[2] + 10)}}>→</div>
      <Person x={1320} y={320} name={b[0]} desc={b[1]} at={b[2]} color={T.fall} />
    </>
  );
};

// 문턱 자: 0~max 가로 자 + 문턱 선(marks = [값, 글자, 설명, 시작]) + 채움(fill = [값, 글자, 시작])
export const Ruler: React.FC<{x: number; y: number; w: number; max: number; marks: [number, string, string, number][]; fill: [number, string, number]}> = ({x, y, w, max, marks, fill}) => {
  const f = useCurrentFrame(); const X = (v: number) => (v / max) * w; const p = grow(f, fill[2], 36);
  return (
    <div style={{position: 'absolute', left: x, top: y}}>
      <div style={{position: 'absolute', left: 0, top: 0, width: w, height: 90, borderRadius: 14, background: T.bg, border: `2px solid ${T.line}`}} />
      <div style={{position: 'absolute', left: 0, top: 0, width: X(fill[0]) * p, height: 90, borderRadius: 14, background: T.accent, opacity: 0.9}} />
      <div style={{...F, position: 'absolute', left: Math.max(0, X(fill[0]) * p - 560), top: 108, width: 560, textAlign: 'right', fontWeight: 700, fontSize: 34, color: T.accent, opacity: fade(f, fill[2] + 20), whiteSpace: 'nowrap'}}>{fill[1]}</div>
      {marks.map(([v, t, d, at], i) => (
        <div key={i} style={{position: 'absolute', left: X(v) - 2, top: -150 + i * 0, opacity: fade(f, at)}}>
          <div style={{position: 'absolute', left: 0, top: 120, width: 5, height: 150, background: T.ink}} />
          <div style={{...F, position: 'absolute', left: 14, top: 0, fontWeight: 700, fontSize: 40, color: T.ink, whiteSpace: 'nowrap'}}>{t}</div>
          <div style={{...F, position: 'absolute', left: 14, top: 54, fontWeight: 700, fontSize: 26, color: T.ink2, whiteSpace: 'nowrap'}}>{d}</div>
        </div>
      ))}
      <div style={{...F, position: 'absolute', left: 0, top: 108, fontWeight: 500, fontSize: 24, color: T.ink3}}>0</div>
    </div>
  );
};

// 해마다 막대: vals(%) — 0 위는 회색, 0 아래는 파랑(하락). tags = [i, 값, 글자, 시작]
export const YearBars: React.FC<{x: number; y: number; w: number; h: number; years: number[]; vals: number[]; min: number; max: number; start: number; tags: [number, number, string, number][]}> =
  ({x, y, w, h, years, vals, min, max, start, tags}) => {
  const f = useCurrentFrame(); const n = vals.length; const bw = w / n;
  const Y = (v: number) => h - ((v - min) / (max - min)) * h; const y0 = Y(0);
  return (
    <div style={{position: 'absolute', left: x, top: y}}>
      <div style={{position: 'absolute', left: 0, top: y0, width: w, height: 3, background: T.ink3}} />
      {vals.map((v, i) => {
        const p = grow(f, start + i * 1.5, 14); const hh = Math.abs(Y(v) - y0) * p; const hot = tags.some((t) => t[0] === i);
        return <div key={i} style={{position: 'absolute', left: i * bw + bw * 0.18, width: bw * 0.64, top: v >= 0 ? y0 - hh : y0 + 3, height: hh, borderRadius: 3,
          background: v < 0 ? T.fall : T.line, boxShadow: hot && f >= tags.find((t) => t[0] === i)![3] ? `0 0 0 3px ${T.ink}` : undefined}} />;
      })}
      {years.map((yv, i) => yv % 5 === 0 || (i === 0 && years[1] % 5 !== 0) ? <div key={i} style={{...F, position: 'absolute', left: i * bw - 20, width: bw + 40, textAlign: 'center', top: h + 10, fontWeight: 500, fontSize: 22, color: T.ink3}}>{yv}</div> : null)}
      {tags.map(([i, v, t, at], k) => (
        <div key={k} style={{...F, position: 'absolute', left: Math.min(i * bw - 60, w - 300), top: Y(v) + 14 + k * 0, fontWeight: 700, fontSize: 28, color: T.fall, opacity: fade(f, at), whiteSpace: 'nowrap',
          background: '#fff', border: `2px solid ${T.fall}`, borderRadius: 10, padding: '2px 10px'}}>{t}</div>
      ))}
    </div>
  );
};

// 시작 해 칸 줄: rows = [이름, 색, [[해, 연차문자]], 켜지는 프레임]. 20년 안에 바닥난 칸(‘+’ 없고 ≤20)이 그 색으로 켜진다. box = [첫 해, 끝 해, 시작, 글]
export const StartTiles: React.FC<{x: number; y: number; w: number; rows: [string, string, [number, string][], number][]; box?: [number, number, number, string] | null; count?: [string, number][]}> =
  ({x, y, w, rows, box, count = []}) => {
  const f = useCurrentFrame(); const lw = 190; const n = rows[0][2].length; const cw = (w - lw - 170) / n; const rh = 128;
  const years = rows[0][2].map(([yv]) => yv);
  return (
    <div style={{position: 'absolute', left: x, top: y}}>
      {years.map((yv, i) => <div key={i} style={{...F, position: 'absolute', left: lw + i * cw, width: cw, textAlign: 'center', top: 0, fontWeight: 700, fontSize: 21, color: T.ink3}}>{String(yv).slice(2)}</div>)}
      <div style={{...F, position: 'absolute', left: lw - 4, top: -30, fontWeight: 500, fontSize: 20, color: T.ink3, whiteSpace: 'nowrap'}}>시작 해(19xx·20xx)</div>
      {rows.map(([name, col, cells, at], r) => (
        <div key={r} style={{position: 'absolute', left: 0, top: 36 + r * rh}}>
          <div style={{...F, position: 'absolute', left: 0, top: 0, height: rh - 22, lineHeight: `${rh - 22}px`, fontWeight: 700, fontSize: 38, color: COLW[col], whiteSpace: 'nowrap'}}>{name}</div>
          {cells.map(([yv, v], i) => {
            const dead = !v.endsWith('+') && Number(v) <= 20; const on = dead && f >= at + i * 2; const c = COLW[col];
            return <div key={i} style={{position: 'absolute', left: lw + i * cw + 3, width: cw - 6, top: 0, height: rh - 22, borderRadius: 10, background: on ? c : T.bg,
              display: 'flex', alignItems: 'center', justifyContent: 'center', ...F, fontWeight: 700, fontSize: v.length > 3 ? 20 : 26, color: on ? '#fff' : T.ink3}}>{v}</div>;
          })}
          {count[r] ? <div style={{...F, position: 'absolute', left: lw + n * cw + 24, top: 0, height: rh - 22, lineHeight: `${rh - 22}px`, fontWeight: 700, fontSize: 52, color: COLW[col],
            opacity: fade(f, count[r][1]), whiteSpace: 'nowrap'}}>{count[r][0]}</div> : null}
        </div>
      ))}
      {box && f >= box[2] ? (() => {
        const i0 = years.indexOf(box[0]); const i1 = years.indexOf(box[1]);
        return <>
          <div style={{position: 'absolute', left: lw + i0 * cw - 4, top: 26, width: (i1 - i0 + 1) * cw + 8, height: rows.length * rh - 2, border: `5px solid ${T.ink}`, borderRadius: 14, opacity: fade(f, box[2])}} />
          <div style={{...F, position: 'absolute', left: lw + i0 * cw, top: 36 + rows.length * rh, fontWeight: 700, fontSize: 30, color: T.ink, opacity: fade(f, box[2] + 6), whiteSpace: 'nowrap'}}>{box[3]}</div>
        </>;
      })() : null}
    </div>
  );
};
