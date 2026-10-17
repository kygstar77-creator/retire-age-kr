// 10/17 영상 디렉터 견본 60초 — C-2 여는 30초 + 숫자 설명 30초를 '잘된 영상의 맛' 세 가지로 다시 짰다.
// 근거: work/research/strategy/sample-1017/director-note.md
//   맛 1  여는 장면은 시청자 자신의 상황 한 문장 + 얼굴 없는 실사 한 컷(손·창가·뒷모습). 그림 인물(클립아트) 대신.   (수페 노후편 B#2~5, 지식한입 C#1·#81~87)
//   맛 2  숫자는 '식 한 장'으로 — 달러 수익 × 환율 = 원화 수익을 조각씩 쌓고, 답 자리는 '?'로 한 번 묻고 쉰 뒤 연다.   (수페 A#33 '0.5% + −0.5% = 0.0%', B#131 '371만원×12÷4%')
//   10/18 이어받음: 영호 장면 실사를 '손 잡은 노부부'(말과 따로 놂)→정우 씨와 같은 '돈 세는 손'(같은 돈·같은 규칙을 그림이 받음), 인물 이름표에 해·달.
//   맛 3  한 화면 강조색 하나 + 손으로 그린 동그라미 한 번 + 소리(잔잔한 음악·넘김 소리·딩).                        (지식한입 C#11·#35 동그라미, 수페 B '띵')
// 재료: 말 = C-2 Chirp 녹음 그대로(public/audio/c-2, 새 녹음 0) · 실사 = Pexels(ep/C-2/bg_plan.json에 출처) · 음악·효과음 = 자체 합성(public/sample1017, scratchpad synth.py)
// 숫자 = c2.json(c2props가 calc_n1_out과 기계 대조한 값) — 1996 844.2원·1997 1,415.2원·1998 1,207.8원(ECOS 연말), ^SP500TR 1997 +33.4%·1998 +28.6%, 원화 +123.6%·+9.7%, 민수 2.72억원.
// 렌더: npx remotion render src/Sample1017.tsx Sample60 out/sample60.mp4  ·  옛 방식 같은 구간: ... C2Old out/sample60_old.mp4
import React from 'react';
import {AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, interpolate, registerRoot, Composition, staticFile, useCurrentFrame, Easing, delayRender, continueRender} from 'remotion';
import {T, F, CL, FONT_CSS, Flame, HandCircle} from './parts/fm';
import {TallyCaption, SAFE} from './motion/TallyFrame';
import {C2, C2Props} from './C2';
import c2 from '../c2.json';

const out = Easing.out(Easing.cubic);
const ease = (f: number, a: number, d = 14) => interpolate(f, [a, a + d], [0, 1], {...CL, easing: out});
const A = (n: string) => `audio/c-2/${n}.wav`;
type Line = {text: string; audio: string; frames: number};
// 장면 = 말 한 줄(또는 없음) + 뒤 쉼. 쉼 동안 화면은 그대로, 음악만 조금 올라온다.
type Beat = {line?: Line; pause?: number; el: (f: number, len: number) => React.ReactNode; sfx?: {at: number; src: string; vol: number}[]};

const L = (text: string, audio: string, frames: number): Line => ({text: text.replace(/^"|"$/g, ''), audio: A(audio), frames});
const LINES = {
  winter: L('외환위기가 한창이던 겨울, 쉰다섯 살 정우 씨가 통장 하나를 펼칩니다.', 'bb18693eeb1afeca', 138),
  put: L('퇴직금 3억을 미국 큰 회사들 주가를 한꺼번에 따라가는 상품에 넣었어요.', '62616c3972b221ba', 134),
  quote: L('"매달 200만원씩만 팔아 쓰자. 이 정도면 평생 가겠지."', 'e5d4ac140a694a8e', 116),
  minsu: L('같은 돈, 같은 규칙으로 5년 늦게 시작한 민수 씨는 지난해 말에도 2억 7천만원이 남아 있었습니다.', '2b0cf7be4333e071', 187),
  ask: L('정우 씨 통장은 언제 바닥났을까요? 그리고 둘을 가른 건 뭐였을까요?', '362cb15e9b68c3ab', 136),
  end2: L('끝에는 내 통장에서 해마다 볼 숫자 두 개를 남겨 드릴게요.', '8877e5c63c2a8711', 110),
  yeongho: L('먼저 정우 씨보다 딱 1년 먼저, 같은 돈과 같은 규칙으로 시작한 옛 동료 영호 씨가 있어요.', '5dd38919f2188bed', 164),
  crash: L('영호 씨가 들어간 해에 원화 값이 무너졌습니다. 1달러를 사려면 원화가 훨씬 많이 들게 된 거예요.', '57b344213c078d83', 166),
  grew: L('달러로 사 둔 주식은 원화로 바꾸면 그만큼 커졌죠. 첫해에만 원화로 두 배 넘게 불었어요.', 'bff0df5525b12e95', 199),
  late: L('정우 씨는 달러가 이미 한참 비싸진 다음에 들어갔어요.', '0b3e7b19122c9187', 109),
  small: L('그래서 첫해 지수가 30% 가까이 올랐는데도, 원화로는 10%가 안 됐습니다.', 'c5c9d8a1bd8ecd6e', 150),
};

// ───────── 실사(얼굴 없는 손·창가) ─────────
const PAST = 'sepia(0.28) saturate(0.82) contrast(1.06) brightness(0.92)';   // 1998년 이야기 = 바랜 색
const Live: React.FC<{src: string; license: string; f: number; len: number; from?: number; who?: string; say?: string; past?: boolean; zoom?: [number, number]; x?: number}> = ({src, license, f, len, from = 0, who, say, past = true, zoom = [1.04, 1.12], x = 50}) => {
  const z = interpolate(f, [0, len], zoom, CL); const o = ease(f, 0, 8); const so = ease(f, 10, 16);
  return (
    <AbsoluteFill style={{background: '#000', overflow: 'hidden'}}>
      <AbsoluteFill style={{transform: `scale(${z})`, filter: `${past ? PAST : 'saturate(0.95)'} brightness(${0.55 + 0.45 * o})`}}>
        <OffthreadVideo src={staticFile(src)} trimBefore={from} muted style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: `${x}% 50%`}} />
      </AbsoluteFill>
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.45) 100%)'}} />
      <AbsoluteFill style={{background: 'linear-gradient(0deg, rgba(10,11,14,0.6) 0%, rgba(10,11,14,0) 30%)'}} />
      {who ? <div style={{position: 'absolute', left: SAFE.left, top: 64, opacity: so, ...F, fontWeight: 700, fontSize: 26, color: '#fff', background: 'rgba(16,17,20,0.62)', borderRadius: 8, padding: '4px 14px'}}>{who}</div> : null}
      {say ? <AbsoluteFill style={{background: 'linear-gradient(90deg, rgba(10,11,14,0.6) 0%, rgba(10,11,14,0) 55%)'}} /> : null}
      {say ? <div style={{position: 'absolute', left: SAFE.left + 20, top: 360, width: 1200, opacity: so, transform: `translateY(${(1 - so) * 18}px)`, ...F, fontWeight: 700, fontSize: 92, lineHeight: 1.2, color: '#fff', letterSpacing: -2, wordBreak: 'keep-all', textShadow: '0 2px 30px rgba(0,0,0,0.6)'}}>{say}</div> : null}
      <div style={{position: 'absolute', right: 40, bottom: 18, ...F, fontWeight: 500, fontSize: 15, color: 'rgba(255,255,255,0.65)'}}>{license}</div>
    </AbsoluteFill>
  );
};

// ───────── 종이 판(제목 하나 + 큰 것 하나) ─────────
const Paper: React.FC<{f: number; len: number; title?: string; source?: string; children: React.ReactNode}> = ({f, len, title, source, children}) => {
  const z = interpolate(f, [0, len], [1.0, 1.035], CL); const o = ease(f, 0, 10);
  return (
    <AbsoluteFill style={{background: '#ececec', overflow: 'hidden'}}>
      <AbsoluteFill style={{transform: `scale(${z})`}}>
        <Img src={staticFile('paper.png')} style={{width: '100%', height: '100%'}} />
        {title ? <div style={{position: 'absolute', left: 0, width: 1920, top: 96, textAlign: 'center', opacity: o, ...F, fontWeight: 700, fontSize: 84, color: T.ink, letterSpacing: -2}}>{title}</div> : null}
        {children}
      </AbsoluteFill>
      {source ? <div style={{position: 'absolute', left: SAFE.left, top: 900, ...F, fontWeight: 500, fontSize: 19, color: T.ink3}}>출처 {source}</div> : null}
    </AbsoluteFill>
  );
};

// 숫자 한 칸: 작은 이름표 + 큰 값
const Cell: React.FC<{label: string; v: string; o: number; c?: string; size?: number; w?: number}> = ({label, v, o, c = T.ink, size = 120, w = 520}) => (
  <div style={{width: w, display: 'flex', flexDirection: 'column', alignItems: 'center', opacity: o, transform: `translateY(${(1 - o) * 24}px)`}}>
    <div style={{...F, fontWeight: 700, fontSize: 40, color: T.ink2, marginBottom: 14, whiteSpace: 'nowrap'}}>{label}</div>
    <div style={{...F, fontWeight: 800, fontSize: size, color: c, letterSpacing: -4, lineHeight: 1.05, whiteSpace: 'nowrap'}}>{v}</div>
  </div>
);
const Op: React.FC<{t: string; o: number}> = ({t, o}) => <div style={{...F, fontWeight: 700, fontSize: 96, color: T.ink3, opacity: o, width: 90, textAlign: 'center', marginTop: 50}}>{t}</div>;

// 식 한 장(수페 B#131처럼 두 줄): 윗줄 '달러로 a × 1달러 값 b1→b2', 아랫줄 '= 원화로 ?' → 쉼 뒤 답이 열리고 동그라미
const Eq: React.FC<{f: number; t0: number; t1: number; t2: number; tAns: number; a: string; b1: string; b2: string; ans: string; y: number}> = ({f, t0, t1, t2, tAns, a, b1, b2, ans, y}) => {
  const ao = ease(f, tAns, 12); const q = f < tAns; const o1 = ease(f, t1); const o2 = ease(f, t2);
  const circ = interpolate(f, [tAns + 10, tAns + 34], [0, 1], {...CL, easing: Easing.inOut(Easing.quad)});
  const w = [...ans].reduce((x, c) => x + (/[0-9]/.test(c) ? 0.6 : c === '.' ? 0.3 : 0.62), 0) * 200;
  return (
    <>
      <div style={{position: 'absolute', left: 0, width: 1920, top: y, display: 'flex', justifyContent: 'center', alignItems: 'flex-end', gap: 36}}>
        <Cell label="달러로" v={a} o={ease(f, t0)} size={110} w={430} />
        <div style={{...F, fontWeight: 700, fontSize: 96, color: T.ink3, opacity: o1, lineHeight: 1.1}}>×</div>
        <Cell label="1달러 값" v={`${b1} → ${b2}`} o={o1} size={96} w={760} />
      </div>
      <div style={{position: 'absolute', left: 0, width: 1920, top: y + 250, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 70, opacity: o2}}>
        <div style={{...F, fontWeight: 700, fontSize: 96, color: T.ink3}}>=</div>
        <div style={{...F, fontWeight: 700, fontSize: 48, color: T.ink2}}>원화로</div>
        <div style={{position: 'relative', minWidth: 300, textAlign: 'center'}}>
          {q ? <div style={{...F, fontWeight: 800, fontSize: 200, color: T.ink3, lineHeight: 1.05}}>?</div>
            : <div style={{...F, fontWeight: 800, fontSize: 200, color: T.accent, letterSpacing: -6, lineHeight: 1.05, opacity: ao, transform: `scale(${0.9 + 0.1 * ao})`, whiteSpace: 'nowrap'}}>{ans}</div>}
          {!q ? <svg width={w + 160} height={300} style={{position: 'absolute', left: '50%', top: -24, marginLeft: -(w + 160) / 2, overflow: 'visible'}}><HandCircle cx={(w + 160) / 2} cy={128} rx={w / 2 + 34} ry={112} p={circ} /></svg> : null}
        </div>
      </div>
    </>
  );
};

// ───────── 장면 차례(쉼 포함 1,735프레임 = 57.8초) ─────────
const BEATS: Beat[] = [
  {line: LINES.winter, el: (f, n) => <Live src="sample1017/6219901_30.mp4" license="Pexels 6219901 · Monstera Production" f={f} len={n} from={60} who="1998년 1월 · 정우 씨 · 가상 인물" />},
  {line: LINES.put, el: (f, n) => <Live src="sample1017/6326929_30.mp4" license="Pexels 6326929 · Kaboompics" f={f} len={n} zoom={[1.1, 1.02]} />, sfx: [{at: 0, src: 'whoosh', vol: 0.25}]},
  {line: LINES.quote, pause: 18, el: (f, n) => <Live src="sample1017/27860328_30.mp4" license="Pexels 27860328 · Thanh-Thang Phan" f={f} len={n} say="“이 정도면 평생 가겠지.”" />},
  {line: LINES.minsu, sfx: [{at: 0, src: 'whoosh', vol: 0.3}, {at: 120, src: 'pen', vol: 0.5}], el: (f, n) => (
    <Paper f={f} len={n} title="5년 늦게 시작한 민수 씨" source="S&P500 총수익 지수(야후 파이낸스) · 한국은행 ECOS 원/달러 연말 환율 · 파이어맵 계산 · 가상 인물">
      <div style={{position: 'absolute', left: 0, width: 1920, top: 330, display: 'flex', flexDirection: 'column', alignItems: 'center', opacity: ease(f, 40), transform: `translateY(${(1 - ease(f, 40)) * 30}px)`}}>
        <div style={{...F, fontWeight: 800, fontSize: 230, color: T.accent, letterSpacing: -8, lineHeight: 1}}>2억 7천만원</div>
        <div style={{...F, fontWeight: 700, fontSize: 48, color: T.ink2, marginTop: 34}}>같은 3억 · 같은 규칙 · 지난해 말에도 남은 돈</div>
      </div>
      <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}><HandCircle cx={960} cy={445} rx={700} ry={150} p={interpolate(f, [120, 150], [0, 1], {...CL, easing: Easing.inOut(Easing.quad)})} /></svg>
    </Paper>)},
  {line: LINES.ask, pause: 36, sfx: [{at: 0, src: 'whoosh', vol: 0.3}], el: (f, n) => {
    const o = ease(f, 4, 16); const z = interpolate(f, [0, n], [1, 1.06], CL);
    return <AbsoluteFill style={{background: T.dbg}}>
      <div style={{position: 'absolute', left: 0, width: 1920, top: 300, textAlign: 'center', opacity: o, transform: `scale(${z})`, ...F, fontWeight: 800, fontSize: 124, lineHeight: 1.25, color: '#fff', letterSpacing: -3}}>
        정우 씨 통장은<br /><span style={{color: T.daccent}}>언제</span> 바닥났을까?</div>
    </AbsoluteFill>;
  }},
  {line: LINES.end2, el: (f, n) => <Live src="sample1017/7490517_30.mp4" license="Pexels 7490517 · RDNE Stock project" f={f} len={n} past={false} say="해마다 볼 숫자 두 개" />},
  // ── 숫자 설명 30초 ──
  {line: LINES.yeongho, sfx: [{at: 0, src: 'whoosh', vol: 0.25}], el: (f, n) => <Live src="sample1017/6326928_30.mp4" license="Pexels 6326928 · Kaboompics" f={f} len={n} zoom={[1.02, 1.1]} who="1997년 1월 · 영호 씨 · 가상 인물" />},
  {line: LINES.crash, pause: 24, sfx: [{at: 0, src: 'whoosh', vol: 0.3}, {at: 70, src: 'ding', vol: 0.35}], el: (f, n) => {
    const ar = interpolate(f, [40, 66], [0, 1], {...CL, easing: Easing.inOut(Easing.quad)});
    return <Paper f={f} len={n} title="1달러를 사는 데 드는 원화" source="한국은행 ECOS 731Y004 원/달러 연말 환율">
      <div style={{position: 'absolute', left: 0, width: 1920, top: 360, display: 'flex', justifyContent: 'center', alignItems: 'flex-end', gap: 40}}>
        <Cell label="1996년 말" v="844.2원" o={ease(f, 8)} size={150} w={560} />
        <svg width={260} height={120} style={{marginBottom: 30}}><path d="M10 60 L230 60 M190 22 L238 60 L190 98" fill="none" stroke={T.ink} strokeWidth={10} strokeLinecap="round" strokeLinejoin="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - ar} /></svg>
        <Cell label="1997년 말" v="1,415.2원" o={ease(f, 66)} c={T.accent} size={150} w={640} />
      </div>
    </Paper>;
  }},
  {line: LINES.grew, sfx: [{at: 104, src: 'ding', vol: 0.4}, {at: 114, src: 'pen', vol: 0.45}], el: (f, n) => (
    <Paper f={f} len={n} title="1997년, 영호 씨 첫해" source="S&P500 총수익 지수 1997 +33.4%(달러) · 한국은행 ECOS 원/달러 연말 · 파이어맵 계산">
      <Eq f={f} t0={0} t1={14} t2={28} tAns={104} a="+33.4%" b1="844원" b2="1,415원" ans="+123.6%" y={250} />
    </Paper>)},
  {line: LINES.late, pause: 18, sfx: [{at: 0, src: 'whoosh', vol: 0.25}], el: (f, n) => <Live src="sample1017/15161525_30.mp4" license="Pexels 15161525 · Phil Desforges" f={f} len={n} say="이미 비싸진 달러" who="정우 씨 · 가상 인물" />},
  {line: LINES.small, pause: 30, sfx: [{at: 0, src: 'whoosh', vol: 0.3}, {at: 104, src: 'ding', vol: 0.4}, {at: 114, src: 'pen', vol: 0.45}], el: (f, n) => (
    <Paper f={f} len={n} title="1998년, 정우 씨 첫해" source="S&P500 총수익 지수 1998 +28.6%(달러) · 한국은행 ECOS 원/달러 연말 1997 1,415.2원 → 1998 1,207.8원 · 파이어맵 계산">
      <div style={{position: 'absolute', left: 0, width: 1920, top: 200, textAlign: 'center', ...F, fontWeight: 700, fontSize: 30, color: T.ink3, opacity: ease(f, 6)}}>영호 씨 1997년: 달러로 +33.4% × 844원 → 1,415원 = 원화로 +123.6%</div>
      <Eq f={f} t0={6} t1={18} t2={30} tAns={104} a="+28.6%" b1="1,415원" b2="1,208원" ans="+9.7%" y={250} />
    </Paper>)},
];
const lenOf = (b: Beat) => (b.line?.frames ?? 0) + (b.pause ?? 0);
export const SAMPLE_FRAMES = BEATS.reduce((a, b) => a + lenOf(b), 0);

// 음악: 말할 때 0.07, 쉼에서 0.2까지 올라온다(말 끝 4프레임 뒤부터 10프레임에 걸쳐)
const voiceAt = (() => { const r: [number, number][] = []; let a = 0; for (const b of BEATS) { if (b.line) r.push([a, a + b.line.frames]); a += lenOf(b); } return r; })();
const musicVol = (f: number) => {
  let d = 1e9; for (const [s, e] of voiceAt) { if (f >= s - 6 && f <= e + 4) return 0.07; d = Math.min(d, Math.abs(f - (e + 4)), Math.abs(s - 6 - f)); }
  return 0.07 + 0.13 * Math.min(1, d / 10);
};

const useFont = () => {
  const [h] = React.useState(() => delayRender('PD 글꼴'));
  React.useEffect(() => {
    Promise.all([['700', 'fonts/pd700.ttf'], ['500', 'fonts/pd500.ttf']].map(([w, u]) => new FontFace('PD', `url(${staticFile(u)})`, {weight: w}).load()))
      .then((fs) => { fs.forEach((x) => document.fonts.add(x)); continueRender(h); }).catch(() => continueRender(h));
  }, [h]);
};

const Beat1: React.FC<{b: Beat; n: number}> = ({b, n}) => { const f = useCurrentFrame(); return <>{b.el(f, n)}</>; };

export const Sample60: React.FC = () => {
  useFont();
  let from = 0;
  return (
    <AbsoluteFill style={{background: '#000'}}>
      <style>{FONT_CSS}</style>
      {BEATS.map((b, i) => {
        const n = lenOf(b); const st = from; from += n;
        return <Sequence key={i} from={st} durationInFrames={n}>
          <Beat1 b={b} n={n} />
          {b.line ? <Sequence durationInFrames={b.line.frames}><Audio src={staticFile(b.line.audio)} /><TallyCaption lines={[{text: b.line.text, frames: b.line.frames}]} /></Sequence> : null}
          {(b.sfx ?? []).map((s, j) => <Sequence key={j} from={s.at} durationInFrames={45}><Audio src={staticFile(`sample1017/${s.src}.wav`)} volume={s.vol} /></Sequence>)}
        </Sequence>;
      })}
      <Audio src={staticFile('sample1017/pad.wav')} volume={musicVol} />
      <div style={{position: 'absolute', left: SAFE.left, top: 18, display: 'flex', alignItems: 'center', gap: 10}}>
        <div style={{display: 'flex', alignItems: 'center', gap: 8, background: 'rgba(16,17,20,0.55)', borderRadius: 8, padding: '2px 10px'}}><Flame size={18} /><span style={{...F, fontWeight: 700, fontSize: 21, color: '#fff'}}>파이어맵</span></div></div>
    </AbsoluteFill>
  );
};

// 옛 방식(지금 C-2 화면) 같은 구간 — 장면 0~4 + 9~13, 쉼도 견본과 같은 자리에 넣어 나란히 볼 때 말이 맞게
const PICK = [0, 1, 2, 3, 4, 9, 10, 11, 12, 13];
const PAUSE: Record<number, number> = {1: 18, 3: 36, 10: 24, 12: 18, 13: 30};
const cp = c2 as unknown as C2Props;
const oldProps: C2Props = {...cp, boxOn: 593, boxFlip: 1e9, scenes: PICK.map((i) => {
  const s = cp.scenes[i]; const p = PAUSE[i] ?? 0; if (!p) return s;
  const lines = s.lines.map((l, j) => j === s.lines.length - 1 ? {...l, frames: l.frames + p} : l);
  return {...s, lines, frames: s.frames + p};
})};
const OLD_FRAMES = oldProps.scenes.reduce((a, s) => a + s.frames, 0);


// 나란히 보기(compare.mp4): 왼쪽 지금 C-2 같은 구간 | 오른쪽 견본. 소리는 견본 쪽(말·쉼 위치가 같다). 렌더 전 out/의 두 mp4를 public/sample1017/로 잠시 복사, 렌더 뒤 지운다.
const Side: React.FC = () => (
  <AbsoluteFill style={{background: '#101114'}}>
    <style>{FONT_CSS}</style>
    {[['sample1017/_old.mp4', '지금 C-2 (같은 말, 같은 자리)', T.ink3], ['sample1017/_new.mp4', '견본 — 실사·식 한 장·소리', T.accent]].map(([src, label, c], i) => (
      <div key={i} style={{position: 'absolute', left: i * 960, top: 250, width: 960}}>
        <div style={{...F, fontWeight: 700, fontSize: 34, color: c as string, textAlign: 'center', marginBottom: 18}}>{label}</div>
        <OffthreadVideo src={staticFile(src as string)} muted={i === 0} style={{width: 952, height: 535.5, marginLeft: 4}} />
      </div>
    ))}
  </AbsoluteFill>
);

const Root: React.FC = () => (
  <>
    <Composition id="Sample60" component={Sample60} durationInFrames={SAMPLE_FRAMES} fps={30} width={1920} height={1080} />
    <Composition id="Compare" component={Side} durationInFrames={SAMPLE_FRAMES} fps={30} width={1920} height={1080} />
    <Composition id="C2Old" component={C2 as unknown as React.FC<Record<string, unknown>>} durationInFrames={OLD_FRAMES} fps={30} width={1920} height={1080} defaultProps={oldProps as unknown as Record<string, unknown>} />
  </>
);
registerRoot(Root);
