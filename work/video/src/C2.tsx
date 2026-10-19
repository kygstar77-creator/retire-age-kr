// C-2 v3.3 "퇴직금 3억, 매달 200만원 팔아 쓰면 평생 가나" 화면 — 재료 work/video/c2.json(ep/C-2/c2props.py가 script.md·voice.json·calc 두 개로 만듦)
// 10/17 롱폼 화면 기준(visual-gap-1017 7절, 관문 work/bgcheck.py): 판(TallyFrame, 큰 제목·아이콘·큰 숫자 하나) ↔ 꽉 찬 실사(TallyBroll) ↔ 정우 씨 그림(visual/N1-person)을 번갈아.
// 판은 글자 줄 8개 이하(제목·큰 값·작은 줄·출처·자막), 같은 판 20초 이하는 c2props가 잰다. 말 줄이 7초를 넘으면 줄 가운데에서 강조 칸이 한 번 바뀐다(lfrender '같은 화면 8초').
// 10/18 견본 방식(순돌이 지시·research/strategy/director-1018.md, 견본 src/Sample1017.tsx): 판 = 종이 결(paper.png 곱하기) · 큰 숫자는 '?'로 묻고 말이 닿을 때(data.rv) 열며 손 동그라미 한 번 ·
//   그림 인물(pic) 대신 얼굴 없는 손·창가 실사(live, 옛날은 바랜 색) · 처음·끝 고정 말(brand) · 식 한 장(eq) · 말 밑 잔잔한 음(sample1017/pad.wav, 자체 합성)과 넘김·딩·펜 소리.
// 10/19 '클로드 티' 빼기(research/visual/no-claude-look-1019.md): 종이 바탕은 TallyFrame이 화면 전체에 깐다(흰 둥근 보드 없음) · 알약·둥근 칸·작은 회색 줄 뺌 ·
//   표는 가운데 맞춤 + 손 밑줄 · 판마다 들어오는 움직임을 다르게(찍기·쓰기·나란히) · data.over(실사)면 큰 숫자를 꽉 찬 실사 위에 흰 글자로 ·
//   소리: 휙 없음, 장 카드(질문 ①…)에만 띠링(앞 줄 꼬리 무음 안, CH_PRE), 답 열기는 펜 소리만, 배경 음은 말 파형 덕킹(parts/human).
// 숫자 글자는 전부 c2.json에서 온다(c2props.py가 calc·대본과 기계 대조). 옛 v2 화면은 ep/C-2/C2.v2.tsx.bak.
import React from 'react';
import {AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, Freeze, interpolate, staticFile, useCurrentFrame, Easing, delayRender, continueRender} from 'remotion';
import {HandUnderline, HandDivider, sfxPlan, SfxTrack, Chime, CH_PRE, isChapter, DuckedMusic} from './parts/human';
import {T, F, CL, FONT_CSS, Flame, HandCircle} from './parts/fm';
import {TallyFrame, TallyCaption, TallyLine, TallyArt, SAFE} from './motion/TallyFrame';
import {TallyBroll} from './motion/TallyBroll';
import {TallyBars} from './motion/TallyBars';

type CLine = {text: string; audio: string | null; frames: number; cap?: string | null};
type CScene = {kind: string; lines: CLine[]; frames: number; data: any};
export type C2Props = {fps: number; scenes: CScene[]; boxOn: number; boxOff?: number | null; boxFlip: number; boxQ: string; boxA: string; boxLabel: string; badge: string};
export const c2Frames = (p: C2Props) => p.scenes.reduce((a, s) => a + s.frames, 0);

const COL: Record<string, string> = {accent: T.accent, fall: T.fall, rise: T.rise, ink: T.ink};
const col = (c?: string) => COL[c || 'ink'] || T.ink;
const out = Easing.out(Easing.cubic);
const ease = (f: number, a: number, d = 14) => interpolate(f, [a, a + d], [0, 1], {...CL, easing: out});
const starts = (ls: CLine[]) => { const o: number[] = []; let a = 0; for (const l of ls) { o.push(a); a += l.frames; } return o; };
const lineAt = (ls: CLine[], f: number) => { const st = starts(ls); let k = 0; st.forEach((a, i) => { if (f >= a) k = i; }); return k; };
// 줄 안 박자: 7초 넘는 줄은 가운데에서 한 번 더 바뀐다 → 장면 안 박자 번호(0,1,2…)
const beatAt = (ls: CLine[], f: number) => { const st = starts(ls); let b = 0; ls.forEach((l, i) => { if (f >= st[i] && i > 0) b++; if (l.frames > 210 && f >= st[i] + l.frames / 2) b++; }); return b; };
const tl = (ls: CLine[]): TallyLine[] => ls.map(l => ({text: l.text.replace(/^"|"$/g, ''), frames: l.frames, cap: l.cap ?? null}));
const bigSize = (t: string, room: number, max: number) => { const u = [...t].reduce((a, c) => a + (/[ㄱ-힝]/.test(c) ? 1 : /\s/.test(c) ? 0.3 : 0.6), 0); return Math.max(84, Math.min(max, Math.floor(room / Math.max(1, u)))); };
const art = (icon?: string, color?: string): TallyArt | null => icon ? {kind: 'icon', icon, license: 'lucide ISC', color} : null;

// 강조 칸: 박자가 홀수면 큰 값 뒤에 연주황 띠가 깔린다(화면 그래픽 영역 4% 넘게 바뀜)
const Pulse: React.FC<{s: CScene; x: number; y: number; w: number; h: number}> = ({s, x, y, w, h}) => {
  const f = useCurrentFrame(); const b = beatAt(s.lines, f);
  return b % 2 === 1 ? <div style={{position: 'absolute', left: x, top: y, width: w, height: h, background: T.soft, borderRadius: 28}} /> : null;
};

// ───────── 판 ─────────
// 종이 결: 판 위에 paper.png를 곱하기로 — 흰 판이 노트처럼(디렉터 노트 '구겨진 흰 종이')
const Paper: React.FC = () => null;   // 10/19: 종이 결은 TallyFrame(PaperBg)이 깐다
const textW = (t: string, z: number) => [...t].reduce((a, c) => a + (/[ㄱ-힝]/.test(c) ? 0.92 : /\s/.test(c) ? 0.25 : /[,.]/.test(c) ? 0.28 : /%/.test(c) ? 0.85 : 0.6), 0) * z;
// 답 열기: rv 전에는 '?', rv에 열리고 rv+10부터 손 동그라미
const Reveal: React.FC<{f: number; rv?: number | null; v: string; z: number; c: string; cy: number; dark?: boolean}> = ({f, rv, v, z, c, cy, dark}) => {
  const q = rv != null && f < rv; const ao = rv != null ? ease(f, rv, 12) : 1;
  const circ = rv != null ? interpolate(f, [rv + 10, rv + 34], [0, 1], {...CL, easing: Easing.inOut(Easing.quad)}) : 0; const w = textW(v, z);
  return <div style={{position: 'relative'}}>
    {q ? <div style={{...F, fontWeight: 800, fontSize: z, lineHeight: 1.18, color: dark ? 'rgba(255,255,255,0.85)' : T.ink3, whiteSpace: 'nowrap', textShadow: dark ? SH2 : undefined}}>?</div>
      : <div style={{...F, fontWeight: 800, fontSize: z, lineHeight: 1.18, color: c, letterSpacing: -4, whiteSpace: 'nowrap', opacity: ao, transform: `scale(${0.9 + 0.1 * ao})`, textShadow: dark ? SH2 : undefined}}>{v}</div>}
    {!q && rv != null ? <svg width={w + z} height={z * 1.6} style={{position: 'absolute', left: '50%', top: cy - z * 0.8, marginLeft: -(w + z) / 2, overflow: 'visible'}}><HandCircle cx={(w + z) / 2} cy={z * 0.8} rx={w / 2 + z * 0.35} ry={z * 0.7} p={circ} color={dark ? T.daccent : T.accent} /></svg> : null}
  </div>;
};

// 꽉 찬 실사 위 큰 글자(data.over = {src, license, from?, x?}) — 판 대신 실사 장면에서 숫자를 보여 줄 때. 흰 글자 + 굵은 그림자, 답 하나만 주황
const SH2 = '0 3px 0 rgba(0,0,0,0.55), 0 0 30px rgba(0,0,0,0.6), 0 0 6px rgba(0,0,0,0.8)';
const OverBg: React.FC<{o: any; n: number}> = ({o, n}) => {
  const f = useCurrentFrame(); const z = interpolate(f, [0, n], [1.03, 1.1], CL);
  if (!o.license) throw new Error('over: license 칸 비었음');
  return <>
    <AbsoluteFill style={{transform: `scale(${z})`, filter: 'saturate(0.85) brightness(0.62)'}}>
      {/\.(mp4|webm|mov)$/i.test(o.src) ? <OffthreadVideo src={staticFile(o.src)} trimBefore={o.from || 0} muted style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: `${o.x ?? 50}% 50%`}} />
        : <Img src={staticFile(o.src)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />}
    </AbsoluteFill>
    <div style={{position: 'absolute', right: 40, bottom: 18, ...F, fontWeight: 500, fontSize: 15, color: 'rgba(255,255,255,0.65)'}}>{o.license}</div>
  </>;
};
const OverTop: React.FC<{title?: string}> = ({title}) => {
  const f = useCurrentFrame(); const o = ease(f, 0, 10);
  return <>
    <div style={{position: 'absolute', left: SAFE.left, top: 18, display: 'flex', alignItems: 'center', gap: 10}}><Flame size={20} /><span style={{...F, fontWeight: 700, fontSize: 22, color: '#fff', textShadow: SH2}}>파이어맵</span></div>
    {title ? <div style={{position: 'absolute', left: 0, width: 1920, top: 84, textAlign: 'center', opacity: o, ...F, fontWeight: 800, fontSize: Math.min(96, bigSize(title, 1500, 96)), color: '#fff', letterSpacing: -2, textShadow: SH2, whiteSpace: 'nowrap'}}>{title}</div> : null}
  </>;
};
const BigOver: React.FC<{s: CScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const z = bigSize(d.v, 1600, 230); const st = interpolate(f, [4, 14], [1.18, 1], {...CL, easing: out}); const o = ease(f, 4, 8);
  return (
    <AbsoluteFill style={{background: '#000', overflow: 'hidden'}}>
      <style>{FONT_CSS}</style>
      <OverBg o={d.over} n={s.frames} /><OverTop title={d.title} />
      <div style={{position: 'absolute', left: 0, width: 1920, top: 330 + (230 - z) * 0.5, display: 'flex', flexDirection: 'column', alignItems: 'center', opacity: o, transform: `scale(${st})`}}>
        <Reveal f={f} rv={d.rv} v={d.v} z={z} c={d.c === 'accent' ? T.daccent : '#fff'} cy={z * 0.59} dark />
        {d.s ? <div style={{...F, fontWeight: 700, fontSize: 54, color: '#fff', marginTop: 24, whiteSpace: 'nowrap', textShadow: SH2}}>{d.s}</div> : null}
      </div>
      <TallyCaption lines={tl(s.lines)} />
    </AbsoluteFill>
  );
};

const Big: React.FC<{s: CScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data;
  if (d.over) return <BigOver s={s} />;
  // 찍기: 큰 숫자는 살짝 크게 들어와 제자리에 박힌다(다른 판의 '아래에서 떠오르기'와 다르게)
  const o = ease(f, 4, 8); const st = interpolate(f, [4, 14], [1.14, 1], {...CL, easing: out}); const z = bigSize(d.v, 1600, 210);
  return (
    <TallyFrame title={d.title} art={art(d.icon, d.c ? col(d.c) : undefined)} source={d.source} chapter={d.chapter} lines={tl(s.lines)}>
      <div style={{position: 'absolute', left: 100, width: 1720, top: 330 + (210 - z) * 0.5, display: 'flex', flexDirection: 'column', alignItems: 'center', opacity: o, transform: `scale(${st})`}}>
        <Reveal f={f} rv={d.rv} v={d.v} z={z} c={col(d.c)} cy={z * 0.59} />
        {d.s ? <div style={{...F, fontWeight: 700, fontSize: 46, color: T.ink2, marginTop: 22, whiteSpace: 'nowrap'}}>{d.s}</div> : null}
      </div>
    </TallyFrame>
  );
};

// 식 한 장(견본 Eq): 윗줄 '달러로 a × 1달러 값 b1→b2', 아랫줄 '= 원화로 ?' → rv에 답이 열리고 동그라미
const Cell: React.FC<{label: string; v: string; o: number; size: number; w: number}> = ({label, v, o, size, w}) => (
  <div style={{width: w, display: 'flex', flexDirection: 'column', alignItems: 'center', opacity: o, transform: `translateY(${(1 - o) * 24}px)`}}>
    <div style={{...F, fontWeight: 700, fontSize: 40, color: T.ink2, marginBottom: 14, whiteSpace: 'nowrap'}}>{label}</div>
    <div style={{...F, fontWeight: 800, fontSize: size, color: T.ink, letterSpacing: -4, lineHeight: 1.05, whiteSpace: 'nowrap'}}>{v}</div>
  </div>
);
const Eq: React.FC<{s: CScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const o1 = ease(f, 14); const o2 = ease(f, 28);
  return (
    <TallyFrame title={d.title} art={null} source={d.source} chapter={d.chapter} lines={tl(s.lines)}>
      <div style={{position: 'absolute', left: 0, width: 1920, top: 330, display: 'flex', justifyContent: 'center', alignItems: 'flex-end', gap: 48}}>
        <Cell label="달러로" v={d.a} o={ease(f, 0)} size={110} w={430} />
        <div style={{...F, fontWeight: 700, fontSize: 96, color: T.ink3, opacity: o1, lineHeight: 1.1}}>×</div>
        <Cell label="1달러 값" v={`${d.b1} → ${d.b2}`} o={o1} size={84} w={900} />
      </div>
      <div style={{position: 'absolute', left: 0, width: 1920, top: 570, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 110, opacity: o2}}>
        <div style={{...F, fontWeight: 700, fontSize: 96, color: T.ink3}}>=</div>
        <div style={{...F, fontWeight: 700, fontSize: 48, color: T.ink2}}>원화로</div>
        <div style={{minWidth: 300, display: 'flex', justifyContent: 'center'}}><Reveal f={f} rv={d.rv} v={d.ans} z={180} c={T.accent} cy={106} /></div>
      </div>
    </TallyFrame>
  );
};

// 얼굴 없는 실사(견본 Live): 옛날 이야기는 바랜 색, who = 왼쪽 위 이름표, say = 큰 한 줄(숫자 금지)
const PAST = 'sepia(0.28) saturate(0.82) contrast(1.06) brightness(0.92)';
const Live: React.FC<{s: CScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const z = interpolate(f, [0, s.frames], d.zoom || [1.04, 1.12], CL); const o = ease(f, 0, 8); const so = ease(f, 10, 16);
  if (!d.license) throw new Error('live: license 칸 비었음');
  if (d.say && /\d/.test(d.say)) throw new Error('live: say에 숫자 금지');
  return (
    <AbsoluteFill style={{background: '#000', overflow: 'hidden'}}>
      <style>{FONT_CSS}</style>
      <AbsoluteFill style={{transform: `scale(${z})`, filter: `${d.past ? PAST : 'saturate(0.95)'} brightness(${0.55 + 0.45 * o})`}}>
        <OffthreadVideo src={staticFile(d.src)} trimBefore={d.from || 0} muted style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: `${d.x ?? 50}% 50%`}} />
      </AbsoluteFill>
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.45) 100%)'}} />
      <AbsoluteFill style={{background: 'linear-gradient(0deg, rgba(10,11,14,0.6) 0%, rgba(10,11,14,0) 30%)'}} />
      <div style={{position: 'absolute', left: SAFE.left, top: 18, display: 'flex', alignItems: 'center', gap: 10}}>
        <Flame size={20} /><span style={{...F, fontWeight: 700, fontSize: 22, color: '#fff', textShadow: SH2}}>파이어맵</span></div>
      {d.who ? <div style={{position: 'absolute', left: SAFE.left, top: 64, opacity: so, ...F, fontWeight: 700, fontSize: 30, color: '#fff', textShadow: SH2}}>{d.who}</div> : null}
      {d.say ? <AbsoluteFill style={{background: 'linear-gradient(90deg, rgba(10,11,14,0.6) 0%, rgba(10,11,14,0) 55%)'}} /> : null}
      {d.say ? <div style={{position: 'absolute', left: SAFE.left + 20, top: 340, width: 1300, opacity: so, transform: `translateY(${(1 - so) * 18}px)`, ...F, fontWeight: 700, fontSize: bigSize(d.say, 2400, 92), lineHeight: 1.2, color: '#fff', letterSpacing: -2, wordBreak: 'keep-all', textShadow: '0 2px 30px rgba(0,0,0,0.6)'}}>{d.say}</div> : null}
      <div style={{position: 'absolute', right: 40, bottom: 18, ...F, fontWeight: 500, fontSize: 15, color: 'rgba(255,255,255,0.65)'}}>{d.license}</div>
      <TallyCaption lines={tl(s.lines)} />
    </AbsoluteFill>
  );
};

// 고정 여는 말·맺는 말 판: 어두운 바탕 + 파이어맵 + 한 줄(날짜·다음 편은 화면 글자로만)
const Brand: React.FC<{s: CScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const o = ease(f, 2, 16); const o2 = ease(f, 18, 16);
  return (
    <AbsoluteFill style={{background: T.dbg}}>
      <style>{FONT_CSS}</style>
      <div style={{position: 'absolute', left: 0, width: 1920, top: 300, display: 'flex', flexDirection: 'column', alignItems: 'center', opacity: o, transform: `scale(${0.96 + 0.04 * o})`}}>
        <div style={{display: 'flex', alignItems: 'center', gap: 24}}><Flame size={96} /><span style={{...F, fontWeight: 800, fontSize: 120, color: '#fff', letterSpacing: -3}}>파이어맵</span></div>
        <div style={{...F, fontWeight: 700, fontSize: 56, color: T.daccent, marginTop: 48, opacity: o2, whiteSpace: 'nowrap'}}>{d.line}</div>
        {d.sub ? <div style={{...F, fontWeight: 500, fontSize: 34, color: 'rgba(255,255,255,0.7)', marginTop: 22, opacity: o2, whiteSpace: 'nowrap'}}>{d.sub}</div> : null}
      </div>
      <TallyCaption lines={tl(s.lines)} />
    </AbsoluteFill>
  );
};

const Pair: React.FC<{s: CScene}> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const st = starts(s.lines);
  const at2 = d.at2 != null ? st[Math.min(d.at2, st.length - 1)] : (s.lines.length > 1 ? st[1] : Math.round(s.lines[0].frames * 0.45));
  const one = (v: string, sub: string, c: string, a: number, x: number, rv?: number) => { const o = rv != null ? ease(f, 4, 14) : ease(f, a, 14); const z = bigSize(v, 760, 170);
    return <div style={{position: 'absolute', left: x, width: 800, top: 350, display: 'flex', flexDirection: 'column', alignItems: 'center', opacity: o, transform: `translateY(${(1 - o) * 20}px)`}}>
      {rv != null ? <Reveal f={f} rv={rv} v={v} z={z} c={col(c)} cy={z * 0.57} /> : <div style={{...F, fontWeight: 800, fontSize: z, lineHeight: 1.15, color: col(c), letterSpacing: -4, whiteSpace: 'nowrap'}}>{v}</div>}
      <div style={{...F, fontWeight: 700, fontSize: 44, color: T.ink2, marginTop: 18, whiteSpace: 'nowrap'}}>{sub}</div></div>; };
  if (d.over) {   // 실사 위 앞·뒤: 먼저 v1, 말이 닿으면 v2가 오른쪽에 — 손 화살표로 잇는다
    const z1 = bigSize(d.v1, 700, 150), z2 = bigSize(d.v2, 760, 170); const o1 = ease(f, 4, 10); const rv = d.rv ?? at2; const ar = interpolate(f, [rv - 14, rv], [0, 1], CL);
    return <AbsoluteFill style={{background: '#000', overflow: 'hidden'}}><style>{FONT_CSS}</style><OverBg o={d.over} n={s.frames} /><OverTop title={d.title} />
      <div style={{position: 'absolute', left: 100, width: 800, top: 400, textAlign: 'center', opacity: o1}}>
        <div style={{...F, fontWeight: 800, fontSize: z1, color: '#fff', letterSpacing: -3, textShadow: SH2, whiteSpace: 'nowrap', lineHeight: 1.15}}>{d.v1}</div>
        <div style={{...F, fontWeight: 700, fontSize: 52, color: '#fff', marginTop: 10, textShadow: SH2}}>{d.s1}</div></div>
      <svg style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, overflow: 'visible'}}><polyline points="905,492 958,484 1005,494" fill="none" stroke="#fff" strokeWidth={9} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - ar} /><polyline points="982,468 1008,494 982,520" fill="none" stroke="#fff" strokeWidth={9} strokeLinecap="round" strokeLinejoin="round" opacity={ar > 0.9 ? 1 : 0} /></svg>
      <div style={{position: 'absolute', left: 1020, width: 800, top: 390, display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
        <Reveal f={f} rv={rv} v={d.v2} z={z2} c={T.daccent} cy={z2 * 0.57} dark />
        <div style={{...F, fontWeight: 700, fontSize: 52, color: '#fff', marginTop: 10, textShadow: SH2}}>{d.s2}</div></div>
      <TallyCaption lines={tl(s.lines)} /></AbsoluteFill>;
  }
  return (
    <TallyFrame title={d.title} art={art(d.icon)} source={d.source} chapter={d.chapter} lines={tl(s.lines)}>
      {one(d.v1, d.s1, d.c1, 4, 160)}
      <HandDivider x={960} y={360} h={230} p={ease(f, 2, 14)} />
      {one(d.v2, d.s2, d.c2, at2, 960, d.rv ?? at2)}
    </TallyFrame>
  );
};

const Rows: React.FC<{s: CScene}> = ({s}) => {   // 10/19: 가운데 맞춤 표(이름은 가운데 선에 오른쪽 끝 맞춤, 값은 왼쪽 끝 맞춤) · 줄 선 없음 · 지금 줄 값에 손 밑줄 · 왼쪽부터 '써지듯' 들어옴
  const f = useCurrentFrame(); const d = s.data; const st = starts(s.lines); const rows: [string, string?, string?, number?][] = d.rows;
  const n = rows.length; const fs = n >= 4 ? 54 : 62; const rh = n >= 4 ? 112 : 136;
  const show = (i: number) => { const at = rows[i][3]; if (at == null) return 4 + i * 8; return at >= st.length ? st[st.length - 1] + s.lines[st.length - 1].frames / 2 : st[at]; };
  const k = (() => { let j = 0; rows.forEach((_, i) => { if (f >= show(i)) j = i; }); return j; })();
  return (
    <TallyFrame title={d.title} art={art(d.icon)} source={d.source} chapter={d.chapter} lines={tl(s.lines)}>
      <div style={{position: 'absolute', left: 0, width: 1920, top: 340 + (4 - Math.min(4, n)) * 30}}>
        {rows.map((r, i) => { const o = ease(f, show(i), 16); const hot = d.hot !== false && i === k && n > 1; const on = hot || n === 1;
          return <div key={i} style={{position: 'relative', display: 'flex', alignItems: 'center', height: rh, clipPath: `inset(-30px ${(1 - o) * 100}% -30px -30px)`}}>
            <div style={{width: r[1] ? 940 : 1920, paddingRight: r[1] ? 50 : 0, boxSizing: 'border-box', textAlign: r[1] ? 'right' : 'center', ...F, fontWeight: 700, fontSize: fs, color: on ? T.ink : T.ink2, whiteSpace: 'nowrap'}}>{r[0]}</div>
            {r[1] ? <div style={{position: 'relative', width: 980, paddingLeft: 50, boxSizing: 'border-box', ...F, fontWeight: 800, fontSize: fs + 6, color: on ? T.accent : T.ink, whiteSpace: 'nowrap'}}>{r[1]}
              {hot ? <div style={{position: 'absolute', left: 50, top: fs * 1.3}}><HandUnderline x={0} y={0} w={textW(r[1], fs + 6)} p={interpolate(f, [show(i) + 8, show(i) + 22], [0, 1], CL)} seed={i} /></div> : null}</div> : null}
          </div>; })}
      </div>
    </TallyFrame>
  );
};

const Bars: React.FC<{s: CScene}> = ({s}) => {
  const d = s.data; const st = starts(s.lines);
  const at = (a?: number) => a == null ? 6 : a >= st.length ? st[st.length - 1] + s.lines[st.length - 1].frames / 2 : st[a] + 4;
  // 주황은 답 하나: 가장 흔한 색 막대는 회색, 다른 색(답) 막대만 주황(10/18 견본 방식)
  const raw = d.bars as [string, number, string, string, number?][]; const cnt: Record<string, number> = {}; raw.forEach((b) => { cnt[b[3]] = (cnt[b[3]] || 0) + 1; });
  const major = Object.keys(cnt).sort((a, b) => cnt[b] - cnt[a])[0]; const one = Object.keys(cnt).length === 1;
  const bars = raw.map(([label, value, valueText, c, a]) => ({label, value: Math.abs(value), valueText, color: one ? T.ink2 : c === major ? '#a3a8b0' : T.accent, start: at(a)}));
  const v = d.dir === 'v';
  return (
    <TallyFrame title={d.title} art={art(d.icon)} source={d.source} chapter={d.chapter} lines={tl(s.lines)}>
      <TallyBars bars={bars} x={v ? 300 : 420} y={v ? 350 : 345} w={v ? 1320 : 1180} h={v ? 400 : 450} max={d.max} min={0} dir={v ? 'v' : 'h'} labelSize={v ? 44 : 46} valueSize={v ? 60 : 62} />
    </TallyFrame>
  );
};

const Grid: React.FC<{s: CScene}> = ({s}) => {   // 바닥난 6명: 3×2 칸
  const f = useCurrentFrame(); const d = s.data; const st = starts(s.lines); const cells: [string, string, number][] = d.cells;
  const k = lineAt(s.lines, f);
  return (
    <TallyFrame title={d.title} art={art(d.icon)} source={d.source} chapter={d.chapter} lines={tl(s.lines)}>
      <div style={{position: 'absolute', left: 200, top: 330, width: 1520, display: 'flex', flexWrap: 'wrap', gap: 28}}>
        {cells.map(([a, b, ln], i) => { const o = ease(f, (st[ln] ?? 0) + 4 + (i % 5) * 6, 12); const lit = (d.lit as number[][])[k]?.includes(i);
          return <div key={i} style={{width: 488, height: 220, opacity: o,
            display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center'}}>
            <div style={{...F, fontWeight: 800, fontSize: 92, color: lit ? T.accent : T.ink, lineHeight: 1.1}}>{a}</div>
            <div style={{...F, fontWeight: 700, fontSize: 42, color: T.ink2, marginTop: 6}}>{b}</div></div>; })}
      </div>
    </TallyFrame>
  );
};

const Ask: React.FC<{s: CScene}> = ({s}) => {   // 질문(장) 카드 — 10/19: 주황 알약·작은 회색 줄 없이, 장 번호는 큰 주황 글자 + 손 밑줄
  const f = useCurrentFrame(); const d = s.data; const o = ease(f, 2, 14); const z = bigSize(d.q, 1560, 112); const no = ease(f, 0, 8);
  const tag = String(d.n || ''); const tz = 64;
  return (
    <AbsoluteFill style={{background: '#1d1c1a'}}>
      <style>{FONT_CSS}</style>
      <div style={{position: 'absolute', left: SAFE.left, top: 18, display: 'flex', alignItems: 'center', gap: 10}}>
        <Flame size={20} /><span style={{...F, fontWeight: 700, fontSize: 22, color: '#fff'}}>파이어맵</span></div>
      <div style={{position: 'absolute', left: 180, width: 1560, top: 270, display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
        <div style={{position: 'relative', ...F, fontWeight: 800, fontSize: tz, color: T.daccent, opacity: no, whiteSpace: 'nowrap'}}>{tag}
          <div style={{position: 'absolute', left: 0, top: tz * 1.25}}><HandUnderline x={0} y={0} w={textW(tag, tz)} p={interpolate(f, [4, 18], [0, 1], CL)} color={T.daccent} stroke={7} /></div></div>
        <div style={{...F, fontWeight: 800, fontSize: z, color: '#fff', marginTop: 48, lineHeight: 1.2, letterSpacing: -2, textAlign: 'center', wordBreak: 'keep-all', maxWidth: 1560, opacity: o, transform: `translateY(${(1 - o) * 14}px)`}}>{d.q}</div>
      </div>
      <TallyCaption lines={tl(s.lines)} />
    </AbsoluteFill>
  );
};

const List5: React.FC<{s: CScene}> = ({s}) => {   // 질문 다섯 줄
  const f = useCurrentFrame(); const d = s.data;
  return (
    <TallyFrame title={d.title} art={art(d.icon)} source={d.source} lines={tl(s.lines)}>
      <div style={{position: 'absolute', left: 260, top: 268, width: 1400}}>
        {(d.items as string[]).map((t, i) => { const o = ease(f, 6 + i * 14, 12);
          return <div key={i} style={{display: 'flex', alignItems: 'center', gap: 24, height: 104, opacity: o, transform: `translateX(${(1 - o) * -24}px)`}}>
            <div style={{...F, fontWeight: 800, fontSize: 64, color: T.accent, width: 74, textAlign: 'center'}}>{i + 1}</div>
            <div style={{...F, fontWeight: 700, fontSize: 54, color: T.ink, whiteSpace: 'nowrap'}}>{t}</div></div>; })}
      </div>
    </TallyFrame>
  );
};

// ───────── 그림 장면(정우 씨·영호 씨·민수 씨) ─────────
const Pic: React.FC<{s: CScene; badge: string}> = ({s, badge}) => {
  const f = useCurrentFrame(); const d = s.data; const z = interpolate(f, [0, s.frames], d.zoom || [1.0, 1.1], CL);
  const st = starts(s.lines); const ca = d.chipAt != null ? st[Math.min(d.chipAt, st.length - 1)] : 10; const co = ease(f, ca, 14);
  const q = d.quote ? ease(f, 6, 12) : 0;
  return (
    <AbsoluteFill style={{background: '#000', overflow: 'hidden'}}>
      <style>{FONT_CSS}</style>
      <AbsoluteFill style={{transform: `scale(${z}) translateX(${interpolate(f, [0, s.frames], [0, d.pan || 0], CL)}px)`, transformOrigin: `${d.cx ?? 50}% ${d.cy ?? 40}%`, filter: d.gray ? 'grayscale(0.85)' : undefined}}>
        <Img src={staticFile(d.pic)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
      </AbsoluteFill>
      <AbsoluteFill style={{background: 'linear-gradient(0deg, rgba(10,11,14,0.55) 0%, rgba(10,11,14,0) 30%)'}} />
      <div style={{position: 'absolute', left: SAFE.left, top: 18, display: 'flex', alignItems: 'center', gap: 10}}>
        <Flame size={20} /><span style={{...F, fontWeight: 700, fontSize: 22, color: '#fff', textShadow: '0 1px 8px rgba(0,0,0,0.6)'}}>파이어맵</span>
        <div style={{...F, fontWeight: 700, fontSize: 22, color: T.ink, background: 'rgba(255,255,255,0.9)', borderRadius: 8, padding: '1px 10px', marginLeft: 8}}>{badge}</div></div>
      {d.year ? <div style={{position: 'absolute', left: SAFE.left, top: 70, ...F, fontWeight: 800, fontSize: 104, lineHeight: 1.1, color: '#fff', background: 'rgba(16,17,20,0.82)', borderRadius: 20, padding: '4px 30px'}}>{d.year}</div> : null}
      {d.chip ? <div style={{position: 'absolute', ...(d.chipPos === 'left' ? {left: SAFE.left, top: d.year ? 230 : 90} : {right: 100, top: 250}), opacity: co, transform: `translateY(${(1 - co) * 20}px)`, background: 'rgba(255,255,255,0.95)', borderRadius: 24, padding: '20px 40px', maxWidth: 1000}}>
        <div style={{...F, fontWeight: 800, fontSize: bigSize(d.chip[0], 900, 120), color: col(d.chipC || 'accent'), lineHeight: 1.1, whiteSpace: 'nowrap'}}>{d.chip[0]}</div>
        {d.chip[1] ? <div style={{...F, fontWeight: 700, fontSize: 40, color: T.ink2, marginTop: 8, whiteSpace: 'nowrap'}}>{d.chip[1]}</div> : null}</div> : null}
      {d.quote ? <div style={{position: 'absolute', left: SAFE.left, top: 600, opacity: q, transform: `scale(${0.9 + 0.1 * q})`, transformOrigin: 'left center',
        ...F, fontWeight: 800, fontSize: bigSize(d.quote, 1150, 104), color: T.ink, background: '#fff', borderRadius: 30, padding: '22px 44px', whiteSpace: 'nowrap', boxShadow: '0 12px 40px rgba(0,0,0,0.35)'}}>“{d.quote}”</div> : null}
      <TallyCaption lines={tl(s.lines)} />
    </AbsoluteFill>
  );
};

const KIND: Record<string, React.FC<{s: CScene}>> = {big: Big, pair: Pair, rows: Rows, bars: Bars, grid: Grid, ask: Ask, list5: List5, eq: Eq, live: Live, brand: Brand};

// 글꼴(PD)을 다 받은 뒤 그린다 — 10/17 미리보기에서 숫자가 대체 글꼴로 찍힌 프레임이 섞였다(@font-face만으로는 렌더가 기다리지 않음)
const useFont = () => {
  const [h] = React.useState(() => delayRender('PD 글꼴'));
  React.useEffect(() => {
    Promise.all([['700', 'fonts/pd700.ttf'], ['500', 'fonts/pd500.ttf']].map(([w, u]) => new FontFace('PD', `url(${staticFile(u)})`, {weight: w}).load()))
      .then((fs) => { fs.forEach((x) => document.fonts.add(x)); continueRender(h); }).catch((e) => { console.error(e); continueRender(h); });
  }, [h]);
};

// ───────── 고정 칸: 바닥나는 해 ─────────
const FloorBox: React.FC<{p: C2Props}> = ({p}) => {   // 10/19: 알약 상자 없이 글자만 — 판 위는 잉크, 실사·어두운 카드 위는 흰 글자 + 그림자
  const f = useCurrentFrame(); if (f < p.boxOn || (p.boxOff != null && f >= p.boxOff)) return null;
  const o = ease(f, p.boxOn, 12); const flip = f >= p.boxFlip;
  let a = 0, kind = ''; for (const s of p.scenes) { if (f < a + s.frames) { kind = s.data && s.data.over ? 'live' : s.kind; break; } a += s.frames; }
  const dark = LIVEK.has(kind); const sh = dark ? '0 2px 10px rgba(0,0,0,0.7), 0 0 3px rgba(0,0,0,0.8)' : undefined;
  return (
    <div style={{position: 'absolute', right: 60, top: 14, opacity: o, display: 'flex', alignItems: 'baseline', gap: 12}}>
      <span style={{...F, fontWeight: 700, fontSize: 24, color: dark ? '#fff' : T.ink2, whiteSpace: 'nowrap', textShadow: sh}}>{p.boxLabel}</span>
      <span style={{...F, fontWeight: 800, fontSize: 34, color: flip ? (dark ? T.daccent : T.accent) : dark ? '#FFD000' : T.accent, whiteSpace: 'nowrap', textShadow: sh}}>{flip ? p.boxA : p.boxQ}</span>
    </div>
  );
};

// 소리(10/19 사장님 '화면 바뀔 때마다 휙 휙 소리 별로, 챕터 바뀔 때 띠링'): 휙 없음 · 장 카드에 띠링 · 답 열기에 펜 소리 — parts/human sfxPlan·Chime·DuckedMusic
const LIVEK = new Set(['live', 'broll', 'pic', 'brand', 'ask']);
const voiceLines = (p: C2Props) => { const r: {at: number; audio: string; frames: number}[] = []; let a = 0; for (const s of p.scenes) { let b = a; for (const l of s.lines) { if (l.audio) r.push({at: b, audio: l.audio, frames: l.frames}); b += l.frames; } a += s.frames; } return r; };

// 10/19 PD: 렌더본 화면 관문(U5 같은 화면 8초 이하)에 판이 8.5~14초 걸림 — 5초 넘는 판·카드는 천천히 다가가기(1.00→1.03, 실사 live의 zoom과 같은 수법)
const Push: React.FC<{n: number; children: React.ReactNode}> = ({n, children}) => {
  const f = useCurrentFrame(); const z = interpolate(f, [0, n], [1, 1.03], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return <AbsoluteFill style={{transform: `scale(${z})`, transformOrigin: '50% 38%'}}>{children}</AbsoluteFill>;
};

export const C2: React.FC<C2Props> = (p) => {
  useFont();
  let from = 0;
  return (
    <AbsoluteFill style={{background: T.bg}}>
      <style>{FONT_CSS}</style>
      {p.scenes.map((s, i) => {
        const st = starts(s.lines); const K = KIND[s.kind];
        const el = <Sequence key={i} from={from} durationInFrames={s.frames}>
          {s.kind === 'pic' ? <Pic s={s} badge={p.badge} /> : s.kind === 'broll' ? <TallyBroll src={s.data.src} license={s.data.license} from={s.data.from} say={s.data.say} side={s.data.side} x={s.data.x} chapter={s.data.chapter} lines={tl(s.lines)} /> : K ? (s.kind !== 'live' && s.frames > 150 ? <Push n={s.frames}><K s={s} /></Push> : <K s={s} />) : null}
          {s.lines.map((l, j) => l.audio ? <Sequence key={j} from={st[j]} durationInFrames={l.frames}><Audio src={staticFile(l.audio)} /></Sequence> : null)}
          <SfxTrack list={sfxPlan(p.scenes, i)} />
        </Sequence>;
        // 장 카드: 앞 줄 꼬리 무음(CH_PRE 프레임) 동안 카드를 빈 채로 먼저 띄우고 띠링 — 말 시각·전체 길이는 그대로
        const lead = i > 0 && isChapter(s) ? <Sequence key={'c' + i} from={from - CH_PRE} durationInFrames={CH_PRE}><Freeze frame={0}>{K ? <K s={s} /> : null}</Freeze><Chime at={0} /></Sequence> : null;
        from += s.frames; return lead ? [el, lead] : el;
      })}
      <DuckedMusic lines={voiceLines(p)} />
      <FloorBox p={p} />
    </AbsoluteFill>
  );
};
