// 파이어맵 영상 공통 부품(RULES 6-3 — 새 부품은 여기, research/longform/loop/parts.md에 기록)
// 토큰은 Weekly.tsx와 같다(바탕 #f6f7f9 · 잉크 #18191d · 핵심 숫자 주황 #ff5a00 · 오르면 빨강 · 내리면 파랑 · Pretendard).
import React from 'react';
import {AbsoluteFill, interpolate, staticFile, useCurrentFrame, useVideoConfig, spring, Easing} from 'remotion';

export const T = {bg: '#f6f7f9', surface: '#ffffff', line: '#e6e9ee', ink: '#18191d', ink2: '#4b515c', ink3: '#8a909b', soft: '#ffe3d1',
  accent: '#ff5a00', rise: '#e5484d', fall: '#2f6fde', dbg: '#101114', dsurface: '#1b1c21', dink: '#f2f3f5', dink3: '#8b8f98', daccent: '#ff7a33', dfall: '#6f9cf0'};
export const FONT_CSS = `
@font-face{font-family:'PD';font-weight:700;src:url('${staticFile('fonts/pd700.ttf')}')}
@font-face{font-family:'PD';font-weight:500;src:url('${staticFile('fonts/pd500.ttf')}')}`;
export const F = {fontFamily: 'PD', fontVariantNumeric: 'tabular-nums' as const};
export const CL = {extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const};

export type VLine = {text: string; audio: string | null; frames: number};
export type VScene = {kind: string; title: string; sub?: string | null; source?: string | null; rail: number; data: any; lines: VLine[]; frames: number};

export const lineStarts = (s: VScene) => { const out: number[] = []; let a = 6; for (const l of s.lines) { out.push(a); a += l.frames; } return out; };
export const at = (s: VScene, i: number) => { const st = lineStarts(s); return st[Math.max(0, Math.min(i, st.length - 1))] ?? 0; };
export const appear = (f: number, start: number, dur = 14) => interpolate(f, [start, start + dur], [0, 1], {...CL, easing: Easing.out(Easing.cubic)});
export const fmtPct = (v: number, d = 2) => (v > 0 ? '+' : v < 0 ? '−' : '') + Math.abs(v).toFixed(d) + '%';
export const eok = (man: number) => { const e = Math.floor(man / 10000); const r = Math.round(man % 10000); return e > 0 ? (r ? `${e}억 ${r.toLocaleString()}만원` : `${e}억원`) : `${r.toLocaleString()}만원`; };

export const Flame: React.FC<{size: number}> = ({size}) => (
  <svg width={size} height={size * 1.25} viewBox="0 0 40 50">
    <path d="M20 2 C26 14 36 18 36 32 C36 42 29 48 20 48 C11 48 4 42 4 32 C4 24 9 20 12 14 C13 20 16 22 18 22 C16 14 17 8 20 2 Z" fill={T.accent} />
    <path d="M20 26 C24 32 28 34 28 39 C28 44 24 46 20 46 C16 46 12 44 12 39 C12 35 15 33 17 29 C18 32 19 33 20 33 C19 30 19 28 20 26 Z" fill="#ffc9a8" />
  </svg>
);

// 손으로 그린 듯한 주황 동그라미(Weekly.tsx와 같은 모양) — 그려지는 움직임으로 등장
export const HandCircle: React.FC<{cx: number; cy: number; rx: number; ry: number; p: number; color?: string}> = ({cx, cy, rx, ry, p, color = T.accent}) => {
  const pts: string[] = [];
  for (let i = 0; i <= 64; i++) {
    const t = (i / 64) * Math.PI * 2.15 - 0.4; const wob = 1 + 0.035 * Math.sin(t * 3.1) + (i / 64) * 0.06;
    pts.push(`${(cx + rx * wob * Math.cos(t)).toFixed(1)},${(cy + ry * wob * Math.sin(t)).toFixed(1)}`);
  }
  return <polyline points={pts.join(' ')} fill="none" stroke={color} strokeWidth={7} strokeLinecap="round" strokeLinejoin="round"
    pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p} />;
};

// 숫자 카운트업 — 0에서 목표값까지 굴러 올라간다(소수 자릿수 고정, 천 단위 쉼표)
export const CountUp: React.FC<{to: number; p: number; digits?: number; prefix?: string; suffix?: string; style?: React.CSSProperties}> = ({to, p, digits = 0, prefix = '', suffix = '', style}) => {
  const v = to * p;
  const txt = Math.abs(v).toLocaleString('en-US', {minimumFractionDigits: digits, maximumFractionDigits: digits});
  return <span style={{...F, ...style}}>{prefix}{v < 0 ? '−' : ''}{txt}{suffix}</span>;
};

// 자막 — 잉크 둥근 카드, 문장이 바뀔 때 살짝 떠오른다
export const Caption: React.FC<{s: VScene; dark?: boolean}> = ({s, dark}) => {
  const f = useCurrentFrame(); const st = lineStarts(s); let idx = -1; st.forEach((a, i) => { if (f >= a) idx = i; });
  if (idx < 0) return null;
  const a = st[idx]; const o = interpolate(f, [a, a + 5], [0, 1], CL);
  return (
    <div style={{position: 'absolute', bottom: 64, left: 0, right: 0, display: 'flex', justifyContent: 'center', opacity: o}}>
      <div style={{...F, fontWeight: 700, fontSize: 40, lineHeight: 1.35, color: dark ? T.dink : '#fff', background: dark ? 'rgba(27,28,33,0.92)' : T.ink,
        padding: '16px 34px', borderRadius: 16, maxWidth: 1480, textAlign: 'center', wordBreak: 'keep-all'}}>{s.lines[idx].text}</div>
    </div>
  );
};

// 진행 막대 — 왼쪽 세로 5칸(오늘 확인할 다섯 가지), 지금 칸만 주황. 똑재TV 목록 복귀 방식을 파이어맵 모양으로(2026-09-30 study)
export const ProgressRail: React.FC<{n: number; cur: number; labels: string[]; on?: string}> = ({n, cur, labels, on: onC = T.accent}) => {
  const f = useCurrentFrame(); const o = appear(f, 0, 12);
  const top = 250, h = 600, gap = 10, cell = (h - gap * (n - 1)) / n;
  return (
    <div style={{position: 'absolute', left: 34, top, opacity: o}}>
      {Array.from({length: n}).map((_, i) => {
        const on = i + 1 === cur, done = i + 1 < cur;
        return (
          <div key={i} style={{position: 'absolute', top: i * (cell + gap), width: on ? 58 : 44, height: cell, borderRadius: 10,
            background: on ? onC : done ? T.ink2 : T.line, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
            <span style={{...F, fontWeight: 700, fontSize: on ? 30 : 24, color: on || done ? '#fff' : T.ink3}}>{i + 1}</span>
            {on ? <div style={{...F, fontWeight: 700, fontSize: 22, color: onC, position: 'absolute', left: 70, top: cell / 2 - 16, whiteSpace: 'nowrap',
              opacity: interpolate(f, [8, 24, 70, 90], [0, 1, 1, 0], CL)}}>{labels[i]}</div> : null}
          </div>
        );
      })}
    </div>
  );
};

export const RAIL_LABELS = ['1년 뒤 남은 돈', '원금', '떨어진 해', '세금·건보료', '월 100만원 원금'];

// 한 장면 틀 — 제목 왼쪽 위 + 단위·기간 한 줄, 브랜드 오른쪽 위, 출처 왼쪽 아래(항상), 자막 아래
export const Page: React.FC<{s: VScene; sub?: string | null; children: React.ReactNode}> = ({s, sub, children}) => {
  const f = useCurrentFrame(); const o = interpolate(f, [0, 10], [0, 1], CL);
  const sb = sub ?? s.sub;
  return (
    <AbsoluteFill style={{background: T.bg}}>
      <div style={{position: 'absolute', left: 120, top: 70, opacity: o, transform: `translateY(${(1 - o) * 12}px)`}}>
        <div style={{...F, fontWeight: 700, fontSize: 62, color: T.ink}}>{s.title}</div>
        {sb ? <div style={{...F, fontWeight: 500, fontSize: 28, color: T.ink3, marginTop: 8}}>{sb}</div> : null}
      </div>
      <div style={{position: 'absolute', right: 110, top: 80, display: 'flex', alignItems: 'center', gap: 10}}>
        <Flame size={26} /><span style={{...F, fontWeight: 700, fontSize: 28, color: T.ink2}}>파이어맵</span>
      </div>
      {s.rail ? <ProgressRail n={5} cur={s.rail} labels={RAIL_LABELS} /> : null}
      {children}
      {s.source ? <div style={{...F, fontWeight: 500, fontSize: s.source.length > 150 ? 16 : s.source.length > 110 ? 18 : 22, color: T.ink3, position: 'absolute', left: 120, right: 110, bottom: 20}}>출처 {s.source}</div> : null}
      <Caption s={s} />
    </AbsoluteFill>
  );
};

export const LogoSting: React.FC<{sub: string}> = ({sub}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const sc = spring({frame: f, fps, config: {damping: 14}});
  const o = interpolate(f, [54, 72], [1, 0], CL);
  const bar = interpolate(f, [8, 34], [0, 1], {...CL, easing: Easing.out(Easing.cubic)});
  return (
    <AbsoluteFill style={{background: T.dbg, alignItems: 'center', justifyContent: 'center', opacity: o}}>
      <div style={{display: 'flex', alignItems: 'center', gap: 28, transform: `scale(${0.85 + sc * 0.15})`, opacity: sc}}>
        <Flame size={110} />
        <div>
          <div style={{...F, fontWeight: 700, fontSize: 132, color: T.dink, lineHeight: 1}}>파이어맵</div>
          <div style={{height: 6, width: 520 * bar, background: T.daccent, borderRadius: 3, margin: '18px 0 14px'}} />
          <div style={{...F, fontWeight: 500, fontSize: 38, color: T.dink3}}>{sub}</div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
