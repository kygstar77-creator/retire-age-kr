// 쇼츠 틀 'c2person'(1080×1920) — 흰 판 대신 장면마다 그림 1장 + 큰 3줄 자막 + 숫자 하나 (today.md 10/14 지시, 근거 fOdDiP5-Auc 68만: 말에 맞춰 장소가 바뀌는 인물 장면·가운데 큰 3줄 자막·숫자는 하나)
// c1clip(흰 판·칸 두 개·검은 자막 상자·주황 답 띠)과 겉모양을 다르게: 그림이 화면 위 63%를 꽉 채우고, 자막은 어두운 아래쪽에 상자 없이 3줄, 숫자는 그림 아래 가장자리에 걸친 흰 카드 하나.
// 재료: work/video/<편>.json (research/cardshorts/<편>/c2pclip.py가 만든다) · 그림 = public/c2p/*.png(1920×1080, 그림 안 글자 0) · 숫자 글자는 전부 props. 코드 안 숫자는 배치 값뿐.
import React from 'react';
import {AbsoluteFill, Audio, Img, Sequence, interpolate, spring, staticFile, useCurrentFrame, Easing} from 'remotion';
import {T, F, CL, FONT_CSS, Flame} from './parts/fm';

type PLine = {text: string; audio: string; frames: number};
type PScene = {pic: string; cx: number; year: string | null; num: string; sub: string; zoom: [number, number]; pan: number; focus: number; gray: boolean; blur?: boolean; red: string[]; green: string[]; lines: PLine[]; frames: number};
export type C2PProps = {fps: number; name: string; layout: string; question: string[]; hot: string; badge: string; base: string; scenes: PScene[]};
export const c2pFrames = (p: C2PProps) => p.scenes.reduce((a, s) => a + s.frames, 0);

const W = 1080, PH = 1210;                 // 그림 칸 높이
const YEL = '#FFD000', RED = '#FF6B5E', GRN = '#4ADE80';
const starts = (lines: PLine[]) => { const o: number[] = []; let a = 0; for (const l of lines) { o.push(a); a += l.frames; } return o; };

// 그림: 인물 가운데(cx)를 화면 가운데에 두고, 장면 동안 확대·옆 흐름(켄 번스). 장면 첫 8프레임은 4% 큰 데서 들어온다(컷이 보이게).
const Picture: React.FC<{s: PScene}> = ({s}) => {
  const f = useCurrentFrame();
  const t = interpolate(f, [0, s.frames], [0, 1], {...CL, easing: Easing.inOut(Easing.sin)});
  const punch = interpolate(f, [0, 8], [1.04, 1], {...CL, easing: Easing.out(Easing.cubic)});
  const z = (s.zoom[0] + (s.zoom[1] - s.zoom[0]) * t) * punch;
  const sc = (PH / 1080) * z; const iw = 1920 * sc; const ih = 1080 * sc;
  let x = W / 2 - s.cx * sc + s.pan * t; x = Math.min(0, Math.max(W - iw, x));
  let y = s.focus * 1080 * (PH / 1080) * (1 - z);   // 확대 기준점 = 얼굴 높이(focus) — 그 높이는 화면에서 제자리
  y = Math.min(0, Math.max(PH - ih, y));
  const o = interpolate(f, [0, 5], [0.35, 1], CL);
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: W, height: PH, overflow: 'hidden', background: '#000'}}>
      <Img src={staticFile(s.pic)} style={{position: 'absolute', left: x, top: y, width: iw, height: ih, opacity: o, filter: s.blur ? 'grayscale(1) blur(22px) brightness(0.4)' : s.gray ? 'grayscale(1) brightness(0.55)' : undefined}} />
    </div>
  );
};

// 자막: 문장을 12자 안팎 조각으로 나누고, 조각 3개(3줄)를 한 장으로 보여 준다. 말 길이(글자 비례)에 맞춰 장을 넘기고, 지금 읽는 줄만 밝게.
const pieces = (t: string) => {
  const out: string[] = [];
  for (const sen of t.replace(/["“”]/g, '').split(/(?<=[.?!,])\s+/).filter(Boolean)) {
    const w = sen.split(/\s+/).filter(Boolean); let cur = '';
    // 숫자 덩이('1억 6천만원', '2011년 1월')와 한 글자 낱말 뒤('한 / 해')는 줄을 안 가른다
    for (const x of w) { const glue = (/\d[억년천만원]*$/.test(cur) && /^\d/.test(x)) || /(^| )\S$/.test(cur); if (cur && !glue && (cur + ' ' + x).length > 13) { out.push(cur); cur = x; } else cur = cur ? cur + ' ' + x : x; }
    if (cur) { if (out.length && cur.length <= 3 && (out[out.length - 1] + ' ' + cur).length <= 18) out[out.length - 1] += ' ' + cur; else out.push(cur); }   // '쓰자'·'때' 같은 외톨이 조각은 앞 줄에 붙인다
  }
  return out.map((c) => c.replace(/[.,]$/, ''));
};
const NUMRX = /(\d[\d,.]*\s?(?:천만원|만원|억|원|%|년|월|살)?)/;
const Colored: React.FC<{t: string; red: string[]; green: string[]}> = ({t, red, green}) => (
  <>{t.split(' ').map((w, i) => {
    const c = red.some((r) => w.startsWith(r)) ? RED : green.some((g) => w.startsWith(g)) ? GRN : null;
    const body = c ? <span style={{color: c}}>{w}</span> : <>{w.split(NUMRX).map((x, j) => (j % 2 ? <span key={j} style={{color: YEL}}>{x}</span> : <React.Fragment key={j}>{x}</React.Fragment>))}</>;
    return <React.Fragment key={i}>{i ? ' ' : ''}{body}</React.Fragment>;
  })}</>
);
const Caption: React.FC<{s: PScene}> = ({s}) => {
  const f = useCurrentFrame(); const st = starts(s.lines);
  let k = 0; st.forEach((a, i) => { if (f >= a) k = i; });
  const l = s.lines[k]; const ps = pieces(l.text); const tot = ps.reduce((a, x) => a + x.length, 0); const speak = l.frames - 6;
  let acc = 0, j = 0, from = st[k];
  ps.forEach((p, i) => { const a = st[k] + (acc / tot) * speak; if (f >= a) { j = i; from = a; } acc += p.length; });
  const page = Math.floor(j / 3); const shown = ps.slice(page * 3, page * 3 + 3); const pageFrom = st[k] + (ps.slice(0, page * 3).reduce((a, x) => a + x.length, 0) / tot) * speak;
  const pin = interpolate(f, [pageFrom, pageFrom + 5], [0, 1], CL);
  return (
    <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 6, transform: `translateY(${(1 - pin) * 18}px)`, opacity: 0.3 + 0.7 * pin}}>
      {shown.map((p, i) => {
        const on = page * 3 + i <= j; const now = page * 3 + i === j;
        return <div key={i} style={{...F, fontWeight: 700, fontSize: Math.min(84, Math.floor(900 / (p.length * 0.92))), lineHeight: 1.18, letterSpacing: -2, whiteSpace: 'nowrap', color: '#fff', opacity: on ? 1 : 0.32,
          transform: `scale(${now ? 1 + 0.03 * interpolate(f, [from, from + 4], [0, 1], CL) : 1})`, textShadow: '0 4px 0 rgba(0,0,0,0.35)'}}><Colored t={p} red={s.red} green={s.green} /></div>;
      })}
    </div>
  );
};

const NumCard: React.FC<{s: PScene}> = ({s}) => {
  const f = useCurrentFrame(); const sp = spring({frame: f - 3, fps: 30, config: {damping: 13, mass: 0.7}});
  const big = s.num.length > 7 ? 92 : 118;
  return (
    <div style={{position: 'absolute', left: 40, top: PH - 150, padding: '18px 34px 20px', background: '#fff', borderRadius: 28, boxShadow: '0 14px 40px rgba(0,0,0,0.35)',
      transform: `translateY(${(1 - sp) * 40}px) scale(${0.9 + 0.1 * sp})`, transformOrigin: 'left bottom', opacity: Math.min(1, sp * 1.4)}}>
      <div style={{...F, fontWeight: 700, fontSize: big, lineHeight: 1, color: T.accent, letterSpacing: -3, whiteSpace: 'nowrap'}}>{s.num}</div>
      <div style={{...F, fontWeight: 700, fontSize: 34, color: T.ink2, marginTop: 8, whiteSpace: 'nowrap'}}>{s.sub}</div>
    </div>
  );
};

const Scene: React.FC<{s: PScene; from: number; total: number; p: C2PProps}> = ({s, from, total, p}) => {
  const f = useCurrentFrame(); const st = starts(s.lines);
  const yo = interpolate(f, [2, 10], [0, 1], CL);
  return (
    <AbsoluteFill>
      <Picture s={s} />
      <div style={{position: 'absolute', left: 0, top: 0, width: W, height: 470, background: 'linear-gradient(rgba(0,0,0,0.78), rgba(0,0,0,0.5) 55%, rgba(0,0,0,0))'}} />
      <div style={{position: 'absolute', left: 0, top: PH - 300, width: W, height: 300, background: `linear-gradient(rgba(16,17,20,0), ${T.dbg})`}} />
      {s.year ? <div style={{position: 'absolute', left: 40, top: 330, padding: '8px 22px', background: T.accent, borderRadius: 14, opacity: yo, transform: `translateX(${(1 - yo) * -30}px)`}}>
        <span style={{...F, fontWeight: 700, fontSize: 44, color: '#fff', whiteSpace: 'nowrap'}}>{s.year}</span></div> : null}
      <NumCard s={s} />
      <div style={{position: 'absolute', left: 60, top: PH + 78, width: 880, height: 310, display: 'flex', alignItems: 'flex-start', justifyContent: 'center'}}><Caption s={s} /></div>
      <div style={{position: 'absolute', left: 60, top: PH + 400, width: 880, height: 10, background: '#2a2c33', borderRadius: 5}}>
        <div style={{width: `${((from + f) / total) * 100}%`, height: 10, background: T.accent, borderRadius: 5}} />
      </div>
      {s.lines.map((l, i) => <Sequence key={i} from={st[i]} durationInFrames={l.frames}><Audio src={staticFile(l.audio)} /></Sequence>)}
    </AbsoluteFill>
  );
};

export const C2P: React.FC<C2PProps> = (p) => {
  const total = c2pFrames(p); let from = 0;
  return (
    <AbsoluteFill style={{background: T.dbg}}>
      <style>{FONT_CSS}</style>
      {p.scenes.map((s, i) => { const el = <Sequence key={i} from={from} durationInFrames={s.frames}><Scene s={s} from={from} total={total} p={p} /></Sequence>; from += s.frames; return el; })}
      <div style={{position: 'absolute', left: 40, top: 28, display: 'flex', alignItems: 'center', gap: 10}}>
        <Flame size={24} /><span style={{...F, fontWeight: 700, fontSize: 26, color: '#fff', opacity: 0.85}}>파이어맵</span>
      </div>
      <div style={{position: 'absolute', right: 40, top: 30, padding: '6px 16px', borderRadius: 10, background: 'rgba(255,255,255,0.88)'}}>
        <span style={{...F, fontWeight: 700, fontSize: 26, color: T.ink, whiteSpace: 'nowrap'}}>{p.badge}</span>
      </div>
      <div style={{position: 'absolute', left: 0, top: 84, width: W, textAlign: 'center'}}>
        {p.question.map((line, i) => {
          const k = line.indexOf(p.hot);
          return <div key={i} style={{...F, fontWeight: 700, fontSize: 92, lineHeight: 1.14, color: '#fff', letterSpacing: -3, whiteSpace: 'nowrap', textShadow: '0 4px 14px rgba(0,0,0,0.45)'}}>
            {k < 0 ? line : <>{line.slice(0, k)}<span style={{color: YEL}}>{p.hot}</span>{line.slice(k + p.hot.length)}</>}</div>;
        })}
      </div>
      <div style={{position: 'absolute', left: 60, top: PH + 426, width: 880, textAlign: 'center', ...F, fontWeight: 500, fontSize: 24, color: T.dink3, whiteSpace: 'nowrap'}}>{p.base}</div>
    </AbsoluteFill>
  );
};
