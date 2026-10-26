// 쇼츠 틀 'c2person'(1080×1920) — 흰 판 대신 장면마다 그림 1장 + 큰 3줄 자막 + 숫자 하나 (today.md 10/14 지시, 근거 fOdDiP5-Auc 68만: 말에 맞춰 장소가 바뀌는 인물 장면·가운데 큰 3줄 자막·숫자는 하나)
// c1clip(흰 판·칸 두 개·검은 자막 상자·주황 답 띠)과 겉모양을 다르게: 그림이 화면 위 63%를 꽉 채우고, 자막은 어두운 아래쪽에 상자 없이 3줄, 숫자는 그림 아래 가장자리에 걸친 흰 카드 하나.
// 재료: work/video/<편>.json (research/cardshorts/<편>/c2pclip.py가 만든다) · 그림 = public/c2p/*.png(1920×1080, 그림 안 글자 0) · 숫자 글자는 전부 props. 코드 안 숫자는 배치 값뿐.
import React from 'react';
import {AbsoluteFill, Audio, Img, Sequence, interpolate, spring, staticFile, useCurrentFrame, Easing} from 'remotion';
import {T, F, CL, FONT_CSS, Flame} from './parts/fm';
import {SZ, PAD, IW, TX0, TOP_Y0, TOP_X0, TW, fit, Progress, SourceLine, SRC_H, DS, OutlineCaption, outline} from './parts/safeframe';

type PLine = {text: string; audio: string; frames: number};
type PScene = {pic: string; cx: number; year: string | null; num: string; sub: string; zoom: [number, number]; pan: number; focus: number; gray: boolean; blur?: boolean; red: string[]; green: string[]; lines: PLine[]; frames: number};
export type C2PProps = {fps: number; name: string; layout: string; question: string[]; hot: string; badge: string; base: string; scenes: PScene[]};
export const c2pFrames = (p: C2PProps) => p.scenes.reduce((a, s) => a + s.frames, 0);

const W = 1080, PH = SZ.y1 + 120;         // 선명한 그림 칸 — 10/16 v2: 1368까지 선명, 그 밑(유튜브 제목 자리)은 같은 그림을 흐리게 깔아 화면 끝까지 채운다
const Q_TOP = TOP_Y0 + 6; const qs = (q: string[]) => Math.min(...q.map((l) => fit(l, TW, DS.titleMax)));   // B-03(10/19): 가운데 x 180~900은 y 150부터   // v3 10/16: 84 → 92(경쟁 제목 중앙)
let Q_END = Q_TOP + 2 * 84 * 1.1;   // C2P가 그릴 때 질문 크기로 다시 잰다
const YEL = '#FFD000', RED = '#FF6B5E', GRN = '#4ADE80';
const starts = (lines: PLine[]) => { const o: number[] = []; let a = 0; for (const l of lines) { o.push(a); a += l.frames; } return o; };

// 그림: 인물 가운데(cx)를 화면 가운데에 두고, 장면 동안 확대·옆 흐름(켄 번스). 장면 첫 8프레임은 4% 큰 데서 들어온다(컷이 보이게).
const Picture: React.FC<{s: PScene; first?: boolean}> = ({s, first}) => {
  const f = useCurrentFrame();
  const t = interpolate(f, [0, s.frames], [0, 1], {...CL, easing: Easing.inOut(Easing.sin)});
  const punch = interpolate(f, [0, 8], [1.04, 1], {...CL, easing: Easing.out(Easing.cubic)});
  const z = (s.zoom[0] + (s.zoom[1] - s.zoom[0]) * t) * punch;
  const sc = (PH / 1080) * z; const iw = 1920 * sc; const ih = 1080 * sc;
  let x = W / 2 - s.cx * sc + s.pan * t; x = Math.min(0, Math.max(W - iw, x));
  let y = s.focus * 1080 * (PH / 1080) * (1 - z);   // 확대 기준점 = 얼굴 높이(focus) — 그 높이는 화면에서 제자리
  y = Math.min(0, Math.max(PH - ih, y));
  const o = first ? 1 : interpolate(f, [0, 5], [0.35, 1], CL);   // A51(10/21): 영상 0초 장면은 처음부터 다 보이게 — 표지 첫 장 반투명 금지
  const bs = 1920 / 1080 * 1.05; const bw = 1920 * bs;   // 흐린 바탕: 같은 그림을 화면 전체(0~1920) 높이로 덮는다
  return (
    <>
      <div style={{position: 'absolute', left: 0, top: 0, width: W, height: 1920, overflow: 'hidden', background: '#000'}}>
        <Img src={staticFile(s.pic)} style={{position: 'absolute', left: Math.min(0, Math.max(W - bw, W / 2 - s.cx * bs)), top: -0.025 * 1920, width: bw, height: 1080 * bs, opacity: o, filter: `blur(28px) brightness(0.9)${s.gray || s.blur ? ' grayscale(1)' : ''}`}} />
      </div>
      <div style={{position: 'absolute', left: 0, top: 0, width: W, height: PH, overflow: 'hidden', WebkitMaskImage: 'linear-gradient(#000 82%, rgba(0,0,0,0))', maskImage: 'linear-gradient(#000 82%, rgba(0,0,0,0))'}}>
        <Img src={staticFile(s.pic)} style={{position: 'absolute', left: x, top: y, width: iw, height: ih, opacity: o, filter: s.blur ? 'grayscale(1) blur(22px) brightness(0.6)' : s.gray ? 'grayscale(1) brightness(0.78)' : undefined}} />
      </div>
    </>
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
    <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2, transform: `translateY(${(1 - pin) * 18}px)`, opacity: 0.3 + 0.7 * pin}}>
      {shown.map((p, i) => {
        const on = page * 3 + i <= j; const now = page * 3 + i === j;
        return <div key={i} style={{...F, fontWeight: 700, fontSize: fit(p, IW, 58, 30), lineHeight: 1.18, letterSpacing: -2, whiteSpace: 'nowrap', color: '#fff', opacity: on ? 1 : 0.32,
          transform: `scale(${now ? 1 + 0.03 * interpolate(f, [from, from + 4], [0, 1], CL) : 1})`, textShadow: '0 4px 0 rgba(0,0,0,0.35)'}}><Colored t={p} red={s.red} green={s.green} /></div>;
      })}
    </div>
  );
};

// 10/16 안전 영역: 숫자 카드는 자막(아래 3줄) 바로 위, 안전 영역 왼쪽 안. 글자 크기는 너비에 맞춰 줄인다.
const CAP3_TOP = DS.capCy - DS.capH / 2;      // v3 10/16: 자막은 한 줄 테두리(parts/safeframe OutlineCaption, 가운데 y 1168) — 경쟁 9편 중 8편이 한 줄. 숫자 카드는 그 위
const NumCard: React.FC<{s: PScene; first?: boolean}> = ({s, first}) => {
  const f = useCurrentFrame(); const sp = first ? 1 : spring({frame: f - 3, fps: 30, config: {damping: 13, mass: 0.7}});   // A51: 0초 장면은 이미 들어온 꼴
  // 카드 안쪽 여백(26×2)+글자 폭 어림 오차 — 10/16 g1s_asym '4% ~ 34% 손해'가 카드 끝에 닿음
  const big = fit(s.num, IW - 110, 140, 40); const sub = Math.max(44, Math.min(52, fit(s.sub, (IW - 60) * 2, 52, 44)));   // 23시 사장님: 회색 작은 설명은 화면 높이 2.5%(48px) 안팎 이상 — 넘치면 두 줄
  // 23시 사장님 '가운데 정렬': 경쟁 쇼츠 10편 제목·자막 가운데 → 숫자 카드도 안전 영역 가운데
  return (
    <div style={{position: 'absolute', left: TX0 + PAD, width: IW, bottom: 1920 - CAP3_TOP + 18, display: 'flex', justifyContent: 'center'}}>
      {/* 10/19 '클로드 티' 빼기: 흰 카드·그림자 없이 실사 위 테두리 글자(숫자 주황 하나 + 한마디 흰 글자) */}
      <div style={{maxWidth: IW, boxSizing: 'border-box', textAlign: 'center',
        transform: `translateY(${(1 - sp) * 40}px) scale(${0.9 + 0.1 * sp})`, transformOrigin: 'center bottom', opacity: Math.min(1, sp * 1.4)}}>
        <div style={{...F, fontWeight: 800, fontSize: big, lineHeight: 1.05, color: '#FF7A1A', letterSpacing: -2, whiteSpace: 'nowrap', textShadow: outline(7)}}>{s.num}</div>
        <div style={{...F, fontWeight: 800, fontSize: sub, lineHeight: 1.2, color: '#fff', marginTop: 8, wordBreak: 'keep-all', textShadow: outline(5)}}>{s.sub}</div>
      </div>
    </div>
  );
};

const Scene: React.FC<{s: PScene; from: number; total: number; p: C2PProps}> = ({s, from, total, p}) => {
  const first = from === 0;
  const f = useCurrentFrame(); const st = starts(s.lines);
  const yo = first ? 1 : interpolate(f, [2, 10], [0, 1], CL);
  return (
    <AbsoluteFill>
      <Picture s={s} first={first} />
      <div style={{position: 'absolute', left: 0, top: 0, width: W, height: 640, background: 'linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.3) 60%, rgba(0,0,0,0))'}} />   {/* 10/26 B-46 밝기: 0.82·0.6 → 0.5·0.3 */}
      <div style={{position: 'absolute', left: 0, top: CAP3_TOP - 240, width: W, height: 1920 - (CAP3_TOP - 240), background: 'linear-gradient(rgba(16,17,20,0), rgba(16,17,20,0.48) 35%, rgba(16,17,20,0.45) 75%, rgba(16,17,20,0.35))'}} />   {/* 10/26 B-46: 자막 뒤만 — 시작 −520→−240, 짙기 0.82→0.48(흰 글자는 검은 테두리 outline(5)가 받침) */}
      {s.year ? <div style={{position: 'absolute', left: TX0 + PAD, width: IW, textAlign: 'center', top: Q_END + 14, opacity: yo}}>
        <span style={{...F, fontWeight: 800, fontSize: fit(s.year, IW - 40, 52, 30), color: '#FFD000', whiteSpace: 'nowrap', textShadow: outline(5)}}>{s.year}</span></div> : null}
      <NumCard s={s} first={first} />
      <OutlineCaption lines={s.lines} first={first} />
      {/* 10/19: 진행 막대 뺌(템플릿 티) */}
      {s.lines.map((l, i) => <Sequence key={i} from={st[i]} durationInFrames={l.frames}><Audio src={staticFile(l.audio)} /></Sequence>)}
    </AbsoluteFill>
  );
};

export const C2P: React.FC<C2PProps> = (p) => {
  const total = c2pFrames(p); let from = 0;
  Q_END = Q_TOP + p.question.length * qs(p.question) * 1.12;
  return (
    <AbsoluteFill style={{background: T.dbg}}>
      <style>{FONT_CSS}</style>
      {p.scenes.map((s, i) => { const el = <Sequence key={i} from={from} durationInFrames={s.frames}><Scene s={s} from={from} total={total} p={p} /></Sequence>; from += s.frames; return el; })}
      <SourceLine text={p.base} badge={p.badge} dark />
      <div style={{position: 'absolute', left: TOP_X0 + PAD, top: Q_TOP, width: TW, textAlign: 'center'}}>
        {p.question.map((line, i) => {
          const k = line.indexOf(p.hot);
          return <div key={i} style={{...F, fontSize: qs(p.question), lineHeight: 1.12, color: '#fff', letterSpacing: -2, whiteSpace: 'nowrap', fontWeight: 800, textShadow: outline(5)}}>
            {k < 0 ? line : <>{line.slice(0, k)}<span style={{color: YEL}}>{p.hot}</span>{line.slice(k + p.hot.length)}</>}</div>;
        })}
      </div>
    </AbsoluteFill>
  );
};
