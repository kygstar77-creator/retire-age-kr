// 영상미 고칠 점 5개(2026-10-02 motion — E-1 실측 vs 경쟁 3편, research/longform/motion-bench.md) — 새 편부터 골라 쓰는 부품. 기존 편(D-1 등)은 안 바뀐다.
// ① HookNumber: 첫 1초 안에 숫자가 보인다(E-1은 첫 16.8초 화면 변화 없음)
// ② Beat: 장면 안 6초마다 시선이 옮겨 간다(E-1 10초 넘는 정지 8곳, 매경 2.5~3초)
// ③ HeroNumber: 숫자 많은 장은 한 번에 숫자 하나를 화면 가득(E-1 3장 2분 숫자 30개)
// ④ PenMark: 말에 맞춰 밑줄·화살표가 그려진다(신과대 필기·매경 빨간 화살표 — 우리는 주황 한 색)
// ⑤ Wipe: 장면 사이 미는 전환, 방향·속도는 편마다 seed로 바꾼다(E-1 큰 전환 10번 전부 맞붙은 컷)
// 같은 틀 반복 방지: 색은 fm.T 토큰 안에서만, 배치·방향은 seed로 편마다 다르게(유튜브 '진정성 없는 콘텐츠' 정책).
import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig, Easing} from 'remotion';
import {T, F, CL, CountUp} from './fm';

// 편마다 다른 값 — 편 이름을 넣으면 0~1 사이 고정 난수
export const seeded = (key: string, i = 0) => { let h = 2166136261 ^ i; for (const c of key) h = Math.imul(h ^ c.charCodeAt(0), 16777619); return ((h >>> 0) % 10000) / 10000; };

// ① 첫 숫자 — 0프레임부터 그려져 있고 36프레임(1.2초) 안에 목표값에 닿는다. 카운트 마지막 프레임 = 사실표 값 그대로.
export const HookNumber: React.FC<{to: number; digits?: number; prefix?: string; suffix?: string; label: string; color?: string; dark?: boolean; x?: number; y?: number; size?: number}> =
  ({to, digits = 0, prefix = '', suffix = '', label, color = T.accent, dark, x = 140, y = 300, size = 200}) => {
    const f = useCurrentFrame(); const {fps} = useVideoConfig();
    const p = interpolate(f, [0, 36], [0.35, 1], {...CL, easing: Easing.out(Easing.cubic)});
    const pop = spring({frame: f, fps, config: {damping: 14, stiffness: 160}, durationInFrames: 20});
    return (
      <div style={{position: 'absolute', left: x, top: y}}>
        <div style={{...F, fontWeight: 700, fontSize: size * 0.24, color: dark ? T.dink3 : T.ink3}}>{label}</div>
        <div style={{...F, fontWeight: 700, fontSize: size, color, lineHeight: 1.05, transform: `scale(${0.92 + 0.08 * pop})`, transformOrigin: 'left center'}}>
          <CountUp to={to} p={p} digits={digits} prefix={prefix} suffix={suffix} /></div>
      </div>
    );
  };

// ② 시선 이동 — 장면 안의 요소 n개에 차례로 초점. 초점 아닌 것은 흐려진다(무대 연출: 한 화면 주목점 하나).
// cues = 각 요소에 초점이 오는 프레임(문장 시작 at(s,i)). cue가 6초 넘게 비면 maxGap마다 다음 요소로 스스로 넘어간다.
export const beatCues = (cues: number[], total: number, fps: number, maxGap = 6) => {
  const out: number[] = []; const g = Math.round(maxGap * fps); const c = [...cues].sort((a, b) => a - b);
  for (let i = 0; i < c.length; i++) { out.push(c[i]); const nx = i + 1 < c.length ? c[i + 1] : total; for (let t = c[i] + g; t < nx - fps; t += g) out.push(t); }
  return out;
};
export const focusOf = (f: number, cues: number[]) => { let k = -1; for (let i = 0; i < cues.length; i++) if (f >= cues[i]) k = i; return k; };
export const Beat: React.FC<{cues: number[]; n: number; children: (focus: number, o: (i: number) => number) => React.ReactNode}> = ({cues, n, children}) => {
  const f = useCurrentFrame(); const k = focusOf(f, cues); const idx = k < 0 ? -1 : k % n;
  const since = k < 0 ? 0 : f - cues[k];
  const o = (i: number) => (idx < 0 ? 1 : i === idx ? 1 : interpolate(since, [0, 8], [1, 0.5], CL));
  return <>{children(idx, o)}</>;
};

// 아주 느린 밀어 들어가기 — 표·원문처럼 오래 머무는 판이 '멈춘 그림'으로 안 읽히게(장면 길이 동안 1.00→1.035)
export const Drift: React.FC<{frames: number; seed: string; children: React.ReactNode}> = ({frames, seed, children}) => {
  const f = useCurrentFrame(); const s = interpolate(f, [0, frames], [1, 1.035], CL);
  const ox = 30 + seeded(seed, 1) * 40, oy = 30 + seeded(seed, 2) * 40;
  return <AbsoluteFill style={{transform: `scale(${s})`, transformOrigin: `${ox}% ${oy}%`}}>{children}</AbsoluteFill>;
};

// ③ 화면 가득 숫자 하나 — 앞뒤 맥락 한 줄씩, 숫자는 굴러 오르고 끝에서 멈춘다. 한 편에 2번까지, 여는 장면에는 안 쓴다(자극 훅 템플릿으로 읽힘 — 레드팀 10/2)
export const HeroNumber: React.FC<{to: number; digits?: number; prefix?: string; suffix?: string; top: string; bottom?: string; source: string; start?: number; color?: string; dark?: boolean}> =
  ({to, digits = 0, prefix = '', suffix = '', top, bottom, source, start = 0, color = T.accent, dark}) => {
    const f = useCurrentFrame();
    const p = interpolate(f, [start, start + 30], [0, 1], {...CL, easing: Easing.out(Easing.cubic)});
    const o = interpolate(f, [start, start + 10], [0, 1], CL);
    const ob = interpolate(f, [start + 30, start + 42], [0, 1], CL);
    return (
      <AbsoluteFill style={{background: dark ? T.dbg : T.bg, alignItems: 'center', justifyContent: 'center', flexDirection: 'column'}}>
        <div style={{...F, fontWeight: 700, fontSize: 54, color: dark ? T.dink3 : T.ink2, opacity: o}}>{top}</div>
        <div style={{...F, fontWeight: 700, fontSize: 300, color, lineHeight: 1.05, opacity: o}}><CountUp to={to} p={p} digits={digits} prefix={prefix} suffix={suffix} /></div>
        {bottom ? <div style={{...F, fontWeight: 500, fontSize: 64, color: dark ? T.dink : T.ink, opacity: ob}}>{bottom}</div> : null}
        <div style={{...F, fontWeight: 500, fontSize: 22, color: dark ? T.dink3 : T.ink3, position: 'absolute', left: 120, bottom: 24}}>출처 {source}</div>
      </AbsoluteFill>
    );
  };

// ④ 펜 표시 — 펜을 긋는 숫자는 글자색을 잉크로 둔다(주황 글자+주황 밑줄 = 이중 강조, 레드팀 10/2). 밑줄(under)·화살표(arrow)·괄호(bracket)가 cue 프레임부터 12프레임에 그려진다. 주황 한 색(의미 색 빨강·파랑과 안 부딪침).
export const PenMark: React.FC<{kind: 'under' | 'arrow' | 'bracket'; x: number; y: number; w: number; h?: number; cue: number; color?: string; seed?: string}> =
  ({kind, x, y, w, h = 60, cue, color = T.accent, seed = 'fm'}) => {
    const f = useCurrentFrame(); const p = interpolate(f, [cue, cue + 12], [0, 1], {...CL, easing: Easing.inOut(Easing.quad)});
    if (p <= 0) return null;
    const j = (i: number) => (seeded(seed, i) - 0.5) * 6; // 손 떨림 — 편마다 다름
    const d = kind === 'under' ? `M${x} ${y + j(1)} Q${x + w / 2} ${y + 8 + j(2)} ${x + w} ${y - 4 + j(3)}`
      : kind === 'arrow' ? `M${x} ${y + h} Q${x + w * 0.3} ${y + h * 0.2 + j(4)} ${x + w} ${y} M${x + w - 26} ${y - 4} L${x + w} ${y} L${x + w - 8} ${y + 26}`
      : `M${x} ${y} Q${x - 18 + j(5)} ${y} ${x - 18} ${y + 20} L${x - 18} ${y + h - 20} Q${x - 18} ${y + h} ${x} ${y + h}`;
    return (
      <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0, pointerEvents: 'none'}}>
        <path d={d} fill="none" stroke={color} strokeWidth={8} strokeLinecap="round" strokeLinejoin="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p} />
      </svg>
    );
  };

// ⑤ 장면 사이 미는 전환 — 다음 장면 맨 앞 dur 프레임 동안 잉크 띠가 지나간다. 방향(좌·우·위)과 띠 색(잉크·주황 옅은 색)은 편 seed.
export const Wipe: React.FC<{seed: string; dur?: number; at?: number}> = ({seed, dur = 12, at = 0}) => {
  const f = useCurrentFrame(); const t = interpolate(f, [at, at + dur], [0, 1], {...CL, easing: Easing.inOut(Easing.cubic)});
  if (t <= 0 || t >= 1) return null;
  const dir = Math.floor(seeded(seed, 7) * 3); const band = seeded(seed, 8) < 0.5 ? T.ink : T.soft;
  const pos = interpolate(t, [0, 1], [-110, 110]);
  const tr = dir === 0 ? `translateX(${pos}%)` : dir === 1 ? `translateX(${-pos}%)` : `translateY(${pos}%)`;
  return <AbsoluteFill style={{background: band, transform: tr}} />;
};
