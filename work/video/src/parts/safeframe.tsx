// 쇼츠 안전 영역 틀 v2(10/16 오후 쇼츠 디자인 담당) — v1(12시대)은 판 전체를 작은 상자로 줄여 위 15%·아래 35%가 검은 빈칸, 오른쪽도 빈 채로 떠 있었다(사장님 '디자인 별로'가 더 심해짐).
// 원칙: 안전 영역은 '글자'만 지키는 규칙이다. 바탕(색·그라데이션·흰 띠)은 1080×1920 전체를 깔고, 글자·숫자만 x 48~888 · y 288~1248 안에 둔다.
// 기준(work/safezone.py와 같은 값): Google Ads 세로 동영상 안전 영역 — 위 288 · 아래 672 · 왼쪽 48 · 오른쪽 192 px. 근거 work/research/cardshorts/safe-zone-1016.md
// 안전 영역(840×960) 배치(위→아래): 질문 2줄(최대 76px) · 답 줄(이름표 한 줄 + 큰 답 숫자 한 줄, 최대 128px) · 판(내용이 실제로 있는 곳만 잘라 남은 칸을 꽉 채움) · 자막 한 줄 · 출처 한 줄(작게).
import React, {useLayoutEffect, useEffect, useRef, useState} from 'react';
import {Freeze, continueRender, delayRender, Sequence, OffthreadVideo, Img, staticFile, useCurrentFrame, interpolate} from 'remotion';
import {Flame, F, T, CL} from './fm';

// ── 10/16 디자인 기준 v3 (근거: work/research/visual/design-spec-1016.md — 돈 분야 30일 조회 상위 쇼츠 10편 실측 중앙값) ──
// 자막: 한 줄 · 가운데 y 61.3%(경쟁 중앙 61.6%) · 글자 높이 3.3%(경쟁 중앙 3.28%, 우리 v2 2.29%) · 흰 글자 + 검은 테두리, 상자 없음(경쟁 8/9 상자 없음)
// 한 번에 9~11자(경쟁 중앙 9.1자) · 숫자는 노랑(#FFD000). 제목: 흰 굵은 글자 2줄, 핵심 낱말 노랑, 최대 92px(경쟁 글자 높이 중앙 4.6% — 안전 영역 너비 812에 맞춰 줄인다)
// 배경: 장면마다 실사 영상·사진을 화면 전체(1080×1920)에 깐다(경쟁 9/10 실사) · 한 배경 최장 6초(경쟁 장면 길이 중앙 5.0초)
export const DS = {
  capCy: 1168, capH: 84, capMax: 72, capMin: 44, capTarget: 10, capLimit: 14,
  titleMax: 92, hot: '#FFD000', bigMax: 128, segMax: 6,
  stroke: '#000',
};
// 글자 테두리(검정 6px) — textShadow 여러 방향으로(paint-order 없이도 같은 모양)
export const outline = (px = 6, c = DS.stroke) => {
  const out: string[] = [];
  for (let a = 0; a < 16; a++) { const r = (a / 16) * Math.PI * 2; out.push(`${(Math.cos(r) * px).toFixed(1)}px ${(Math.sin(r) * px).toFixed(1)}px 0 ${c}`); }
  out.push(`0 ${px + 2}px ${px * 2}px rgba(0,0,0,0.55)`);
  return out.join(', ');
};

// ── 배경 실사(장면마다 영상·사진). seg.from·frames는 영상 전체 프레임 기준, start는 클립 안 시작 초 ──
export type BgSeg = {src: string; from: number; frames: number; start?: number; kind?: 'video' | 'image'; x?: number};
const BgOne: React.FC<{g: BgSeg; W: number; H: number}> = ({g, W, H}) => {
  const f = useCurrentFrame();
  const z = interpolate(f, [0, g.frames], [1.04, 1.12], CL);
  const o = interpolate(f, [0, 6], [0.4, 1], CL);
  const st: React.CSSProperties = {position: 'absolute', left: 0, top: 0, width: W, height: H, objectFit: 'cover', objectPosition: `${g.x ?? 50}% 50%`, transform: `scale(${z})`, opacity: o};
  const vid = g.kind === 'video' || /\.mp4$/i.test(g.src);
  return vid ? <OffthreadVideo src={staticFile(g.src)} muted startFrom={Math.round((g.start ?? 0) * 30)} style={st} /> : <Img src={staticFile(g.src)} style={st} />;
};
export const BgLayer: React.FC<{bg: BgSeg[]; W?: number; H?: number}> = ({bg, W = 1080, H = 1920}) => (
  <div style={{position: 'absolute', left: 0, top: 0, width: W, height: H, overflow: 'hidden', background: '#000'}}>
    {bg.map((g, i) => <Sequence key={i} from={g.from} durationInFrames={g.frames} layout="none"><BgOne g={g} W={W} H={H} /></Sequence>)}
  </div>
);
// 쇼츠용 어둡게 덮기: 위(제목·답)와 아래(유튜브 제목 자리)는 진하게, 가운데는 사진이 보이게
export const ShortScrim: React.FC<{hdrEnd: number}> = ({hdrEnd}) => (
  <>
    <div style={{position: 'absolute', left: 0, top: 0, width: 1080, height: 1920, background: 'rgba(0,0,0,0.12)'}} />
    <div style={{position: 'absolute', left: 0, top: 0, width: 1080, height: hdrEnd + 120, background: `linear-gradient(rgba(0,0,0,0.66), rgba(0,0,0,0.5) ${Math.round((hdrEnd / (hdrEnd + 120)) * 100)}%, rgba(0,0,0,0))`}} />
    <div style={{position: 'absolute', left: 0, top: DS.capCy - 160, width: 1080, height: 1920 - DS.capCy + 160, background: 'linear-gradient(rgba(0,0,0,0), rgba(0,0,0,0.35) 30%, rgba(0,0,0,0.5))'}} />
  </>
);

// 자막 조각(10/16 22시 사장님 "문장·뜻 단위로 끊는다"): 낱말 단위, 한 조각 최대 14자(공백 포함). 끊는 자리 점수 —
//   문장부호(.,?!) 뒤·말 이음(~고·~서·~면·~는데·~지만·~니까·~요·~다) 뒤는 끊기 좋음, 꾸미는 말('내·이·그·한·몇·약·같은·지난' 등) 뒤와 숫자 덩이('1억 6천만원') 안·'~의' 뒤는 끊지 않음.
const CAP_DET = new Set(['내', '이', '그', '저', '한', '두', '세', '네', '몇', '약', '총', '각', '첫', '이번', '지난', '같은', '다른', '이런', '그런', '저런', '모든', '어느', '무슨', '이 돈', '매달', '한 달', '올해', '작년', '지금']);
const CAP_GOOD = /([.,?!]|고|서|며|면|는데|은데|인데|지만|니까|라서|해서|려면|으면|어요|에요|예요|아요|죠|다|요|게)$/;
export const capChunks = (t: string) => {
  const out: string[] = [];
  for (const sen of t.split(/(?<=[.?!])\s+/).filter(Boolean)) {
    const w = sen.split(/\s+/).filter(Boolean); const n = w.length; const L = sen.length; const k = Math.max(1, Math.round(L / DS.capTarget)); const tg = L / k;
    const len = (i: number, j: number) => w.slice(i, j).join(' ').length;
    const best: number[] = Array(n + 1).fill(Infinity); const prev: number[] = Array(n + 1).fill(0); best[0] = 0;
    for (let j = 1; j <= n; j++) for (let i = 0; i < j; i++) {
      const l = len(i, j); if (l > DS.capLimit && j - i > 1) continue;
      const last = w[j - 1];
      let c = best[i] + 0.6 * (l - tg) * (l - tg) + (l < 4 ? 80 : 0);
      if (j < n) {
        if (/\d[억만천원%년월일분]*$/.test(last) && /^\d|^[천만억원]/.test(w[j])) c += 400;          // 숫자 덩이 안
        if (CAP_DET.has(last) || last.length === 1) c += 300;                             // 꾸미는 말·한 글자 뒤
        if (/의$/.test(last)) c += 150;
        if (CAP_GOOD.test(last)) c -= 35;                                                  // 말 이음·문장부호 뒤
      }
      if (c < best[j]) { best[j] = c; prev[j] = i; }
    }
    const cut: string[] = []; for (let j = n; j > 0; j = prev[j]) cut.unshift(w.slice(prev[j], j).join(' '));
    out.push(...cut);
  }
  return out.map((c) => c.replace(/[.,]$/, ''));
};
const CAP_NUM = /(\d[\d,.]*\s?(?:천만원|만원|억|원|%|배|번|달러|년째|년|월|세|살|m|km)?)/;
// 한 줄 테두리 자막(상자 없음). lines = 장면 말 줄들(frames), 장면 안 프레임으로 지금 조각을 고른다.
export const OutlineCaption: React.FC<{lines: {text: string; frames: number}[]; first?: boolean}> = ({lines, first}) => {
  const f = useCurrentFrame(); const st: number[] = []; let a0 = 0; for (const l of lines) { st.push(a0); a0 += l.frames; }
  let k = 0; st.forEach((a, i) => { if (f >= a) k = i; });
  const l = lines[k]; const cs = capChunks(l.text); const tot = cs.reduce((a, x) => a + x.replace(/\s/g, '').length, 0) || 1;
  const speak = l.frames - 8; let acc = 0, j = 0, from = st[k];
  for (let i = 0; i < cs.length; i++) { const a = st[k] + (acc / tot) * speak; if (f >= a) { j = i; from = a; } acc += cs[i].replace(/\s/g, '').length; }
  const o = first && k === 0 && j === 0 ? 1 : interpolate(f, [from, from + 3], [0, 1], CL);
  const t = cs[j] ?? '';
  const fs = fit(t, IW - 24, DS.capMax, DS.capMin);
  return (
    <div style={{position: 'absolute', left: SZ.x0 + PAD, top: DS.capCy - DS.capH / 2, width: IW, height: DS.capH, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
      <div style={{...F, fontWeight: 800, fontSize: fs, lineHeight: 1.1, color: '#fff', whiteSpace: 'nowrap', letterSpacing: -1.5, textShadow: outline(6), opacity: 0.55 + 0.45 * o, transform: `scale(${0.96 + 0.04 * o})`}}>
        {t.split(CAP_NUM).map((x, i) => (i % 2 ? <span key={i} style={{color: DS.hot}}>{x}</span> : <React.Fragment key={i}>{x}</React.Fragment>))}
      </div>
    </div>
  );
};

export const SZ = {x0: 48, y0: 288, x1: 888, y1: 1248};
export const PAD = 14;                                   // 안전 영역 안쪽 여백
export const CX = (SZ.x0 + SZ.x1) / 2;                   // 글자 가운데 맞춤 기준(안전 영역 가운데 468 — 오른쪽 버튼 줄을 피한다)
export const IW = SZ.x1 - SZ.x0 - PAD * 2;               // 글자 줄 최대 너비 812
export const YEL = '#FFD000';

// 글자 너비 어림(Pretendard 굵게): 한글 0.96em · 숫자 0.6em · 영문 0.62em · 공백 0.28em · 기호 0.4em
export const units = (t: string) => {
  let u = 0;
  for (const ch of t) u += /[가-힣ㄱ-ㅎ㎡]/.test(ch) ? 0.96 : /\d/.test(ch) ? 0.6 : /[A-Za-z]/.test(ch) ? 0.62 : ch === ' ' ? 0.28 : /[−~→%+]/.test(ch) ? 0.62 : 0.4;
  return u;
};
export const fit = (t: string, w: number, max: number, min = 16) => Math.max(min, Math.min(max, Math.floor(w / Math.max(1, units(t)))));

export type Answer = {label: string; items: string[]; arrow?: boolean; note?: string; key?: number; solo?: boolean} | null | undefined;   // key: 큰 숫자로 쓸 item · solo: 이름표 줄에 다른 item을 붙이지 않음(다른 대상이 큰 숫자와 섞여 읽힐 때)

// ── 배치 계산 ──
const Q_TOP = SZ.y0 + 6, Q_LH = 1.08, Q_MAX = DS.titleMax;   // v3: 76 → 92(경쟁 제목 글자 높이 중앙 4.6%)
export const qSize = (q: string[]) => Math.min(...q.map((l) => fit(l, IW, Q_MAX)));
export const SRC_H = 32;                                  // 출처 한 줄(맨 아래)
export const CAP_H = 72;
export const capTop = () => DS.capCy - DS.capH / 2;    // v3: 자막 가운데 y 1176(61.3%)
export const capSize = (t: string) => fit(t, IW - 40, 50, 28);

// 답: 이름표 한 줄(작게) + 답 숫자(크게). 기본은 item 전부를 한 줄에(화살표면 →) — 한 줄에 60px 밑으로 작아지면 item마다 한 줄(최대 96px).
// solo면 items[key ?? 0] 하나만 크게(괄호 덧붙임은 같은 줄에 작게) — 다른 대상(예: 삼성전자 100주)이 큰 숫자와 섞여 읽힐 때. note는 뺀다(작은 글자 줄 줄이기).
// 10/16 58세 이해 시험: 큰 숫자 하나만 남기면(g1s_why 웃돈 −7.26%, h1s_gap 사려면…) 그 숫자를 영상 전체의 답으로 읽어 뜻이 틀림 → 기본은 item 전부.
export const answerParts = (a: Answer) => {
  if (!a) return null;
  const ss = fit(a.label, IW, 34, 22);
  if (a.solo) {
    const m = a.items[a.key ?? 0].match(/^(.*?)\s*\(([^)]*)\)\s*$/);
    const big = m ? m[1] : a.items[a.key ?? 0]; const paren = m ? m[2] : '';
    const pu = paren ? units(paren) * 0.42 + 0.3 : 0;
    const bs = Math.max(56, Math.min(128, Math.floor(IW / (units(big) + pu))));
    return {small: a.label, ss, lines: [[big]] as string[][], paren, bs, arrow: false};
  }
  const sep = a.arrow ? ' → ' : ' · ';
  const one = fit(a.items.join(sep), IW, 128, 20);
  // 화살표는 무엇→무엇인지(note: '세금 떼기 전 → 뗀 뒤')가 없으면 뜻이 안 섬(r1s_gap) — 단 26px 밑으로 작아지면 이름표만(d1s_pension: 휴대폰에서 못 읽음)
  if (a.arrow && a.note) { const sm = a.label + ' · ' + a.note; if (units(sm) * 26 <= IW) a = {...a, label: sm}; }
  const ss3 = fit(a.label, IW, 34, 22);
  if (one >= 60 || a.items.length < 2) return {small: a.label, ss: ss3, lines: [a.items], paren: '', bs: one, arrow: !!a.arrow};
  const lines = a.items.map((x, i) => (a.arrow && i < a.items.length - 1 ? [x + ' →'] : [x]));
  const bs = Math.min(...lines.map((l) => fit(l[0], IW, 96, 40)));
  return {small: a.label, ss: ss3, lines, paren: '', bs, arrow: !!a.arrow};
};

export const layout = (question: string[], answer: Answer) => {
  const qs = qSize(question); const qEnd = Q_TOP + question.length * qs * Q_LH;
  const ap = answerParts(answer);
  const aTop = qEnd + 6; const bTop = ap ? aTop + Math.round(ap.ss * 1.3) : aTop; const heroEnd = ap ? bTop + Math.round(ap.bs * 1.06 * ap.lines.length) : qEnd;
  const hdrEnd = heroEnd + 14;                             // 어두운 머리 띠 끝(바탕은 화면 위 끝 0부터)
  const boardTop = hdrEnd + 8, boardBottom = capTop() - 6;
  return {qs, qEnd, ap, aTop, bTop, heroEnd, hdrEnd, boardTop, boardBottom};
};

export const BAND_END = SZ.y1 + 40;                       // 흰 띠 끝(자막·출처까지 흰 바탕, 그 밑은 유튜브 제목 자리라 어두운 바탕)
// ── 바탕: 화면 전체(0~1920)를 깐다. 위 = 어두운 띠(질문·답), 가운데 = 흰 띠(판, 가장자리 0~1080까지), 아래 = 어두운 그라데이션(유튜브 제목·채널 이름이 흰 글자라 어두운 바탕에서 읽힘) + 진행 막대 ──
export const Backdrop: React.FC<{question: string[]; answer: Answer; progress?: number; bg?: BgSeg[] | null}> = ({question, answer, bg}) => {
  const L = layout(question, answer);
  if (bg && bg.length) return <><BgLayer bg={bg} /><ShortScrim hdrEnd={L.hdrEnd} /></>;   // v3: 실사 배경이 화면 전체
  return (
    <>
      <div style={{position: 'absolute', left: 0, top: 0, width: 1080, height: 1920, background: `linear-gradient(180deg, #23252d 0%, ${T.dbg} 34%, ${T.dbg} 70%, #1a1410 100%)`}} />
      <div style={{position: 'absolute', left: 0, top: 0, width: 1080, height: L.hdrEnd, background: 'radial-gradient(120% 60% at 85% 0%, rgba(255,90,0,0.22), rgba(255,90,0,0) 60%)'}} />
      <div style={{position: 'absolute', left: 0, top: L.hdrEnd, width: 1080, height: BAND_END - L.hdrEnd, background: '#fff'}} />
      <div style={{position: 'absolute', left: 0, top: 1920 - 520, width: 1080, height: 520, background: 'radial-gradient(90% 70% at 50% 100%, rgba(255,90,0,0.16), rgba(255,90,0,0) 70%)'}} />
    </>
  );
};
export const Progress: React.FC<{progress: number}> = ({progress}) => (
  <div style={{position: 'absolute', left: 0, top: BAND_END, width: 1080, height: 10, background: '#2a2c33'}}>
    <div style={{width: `${Math.max(0, Math.min(1, progress)) * 100}%`, height: 10, background: T.accent}} />
  </div>
);

// ── 질문(안전 영역 맨 위, 크게) + 답(이름표 한 줄 + 큰 숫자 한 줄) ──
export const Hero: React.FC<{question: string[]; hot: string; answer: Answer; hotColor?: string; until?: number}> = ({question, hot, answer, hotColor = YEL, until}) => {
  const fr = useCurrentFrame();   // v3(10/16 22시 '같은 숫자 되풀이 금지'): 답 숫자는 첫 장면(until 프레임 전)에만
  const L = layout(question, until != null && fr >= until ? null : answer); const ap = L.ap;
  return (
    <>
      <div style={{position: 'absolute', left: SZ.x0 + PAD, top: Q_TOP, width: IW, textAlign: 'center'}}>
        {question.map((line, i) => {
          const k = hot ? line.indexOf(hot) : -1;
          return <div key={i} style={{...F, fontWeight: 800, fontSize: L.qs, lineHeight: Q_LH, color: '#fff', letterSpacing: -2, whiteSpace: 'nowrap', textShadow: outline(5)}}>
            {k < 0 ? line : <>{line.slice(0, k)}<span style={{color: hotColor}}>{hot}</span>{line.slice(k + hot.length)}</>}</div>;
        })}
      </div>
      {ap ? <>
        <div style={{position: 'absolute', left: SZ.x0 + PAD, top: L.aTop, width: IW, textAlign: 'center', ...F, fontWeight: 700, fontSize: ap.ss, lineHeight: 1.3, color: '#e3e6ec', whiteSpace: 'nowrap', textShadow: outline(3)}}>{ap.small}</div>
        {ap.lines.map((line, li) => {
          const items = line;
          const sep = ap.arrow ? '→' : '·';
          return <div key={li} style={{position: 'absolute', left: SZ.x0 + PAD, top: L.bTop + li * Math.round(ap.bs * 1.06), width: IW, display: 'flex', alignItems: 'baseline', justifyContent: 'center', gap: Math.round(ap.bs * 0.14), whiteSpace: 'nowrap'}}>
            {items.map((x, i) => {
              const last = ap.arrow ? (ap.lines.length > 1 ? li === ap.lines.length - 1 : i === items.length - 1) : true;
              return <React.Fragment key={i}>
                {i ? <span style={{...F, fontWeight: 700, fontSize: Math.round(ap.bs * 0.7), color: T.dink3}}>{sep}</span> : null}
                <span style={{...F, fontWeight: 800, fontSize: ap.bs, lineHeight: 1.04, color: last ? T.daccent : '#e9ebef', letterSpacing: ap.bs > 90 ? -4 : -2, textShadow: outline(5)}}>{x}</span>
              </React.Fragment>;
            })}
            {ap.paren ? <span style={{...F, fontWeight: 700, fontSize: Math.round(ap.bs * 0.42), color: T.daccent, letterSpacing: -1}}>{ap.paren}</span> : null}
          </div>;
        })}
      </> : null}
    </>
  );
};

// ── 출처 한 줄(안전 영역 안 아래, 작게) ──
export const SourceLine: React.FC<{text: string; badge?: string; dark?: boolean}> = ({text, badge, dark}) => (   // 사진 위에서는 dark(밝은 글자)로 쓴다
  <div style={{position: 'absolute', left: SZ.x0 + PAD, top: SZ.y1 - SRC_H, width: IW, height: SRC_H - 4, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8, whiteSpace: 'nowrap', overflow: 'hidden'}}>
    <Flame size={18} /><span style={{...F, fontWeight: 700, fontSize: 22, color: dark ? '#f2f3f5' : T.ink2, textShadow: dark ? outline(2) : undefined}}>파이어맵</span>
    {badge ? <span style={{...F, fontWeight: 700, fontSize: 19, color: T.ink, background: 'rgba(255,255,255,0.85)', borderRadius: 6, padding: '1px 8px'}}>{badge}</span> : null}
    <span style={{...F, fontWeight: 500, fontSize: fit(text, IW - 130 - (badge ? units(badge) * 19 + 30 : 0), 22, 14), color: dark ? '#e3e6ec' : T.ink3, textShadow: dark ? outline(2) : undefined}}>{text}</span>
  </div>
);

// ── 판: 내용이 실제로 그려진 곳(장면 중간·끝 두 장면의 글자·면·선)만 재서 잘라, 판 칸(안전 영역 너비 840 × boardTop~boardBottom)을 꽉 채우게 키운다 ──
type Box = {x0: number; y0: number; x1: number; y1: number};
const alpha = (c: string) => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return c === 'transparent' ? 0 : 1; const p = m[1].split(',').map((x) => parseFloat(x)); return p.length > 3 ? p[3] : 1; };
const SHAPES = new Set(['path', 'rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'text', 'image', 'tspan']);
const measure = (root: HTMLElement): Box | null => {
  const R = root.getBoundingClientRect(); let b: Box | null = null;
  const add = (r: DOMRect) => { if (r.width < 1 || r.height < 1) return; const x0 = r.left - R.left, y0 = r.top - R.top, x1 = r.right - R.left, y1 = r.bottom - R.top; b = b ? {x0: Math.min(b.x0, x0), y0: Math.min(b.y0, y0), x1: Math.max(b.x1, x1), y1: Math.max(b.y1, y1)} : {x0, y0, x1, y1}; };
  const op = (el: Element) => { let o = 1; for (let e: Element | null = el; e && e !== root; e = e.parentElement) { const v = parseFloat(getComputedStyle(e).opacity); o *= isNaN(v) ? 1 : v; } return o; };
  root.querySelectorAll('*').forEach((el) => {
    if (op(el) < 0.05) return;
    const cs = getComputedStyle(el);
    if (cs.display === 'none') return;
    if (el instanceof SVGElement) { if (SHAPES.has(el.tagName.toLowerCase())) add(el.getBoundingClientRect()); return; }
    const deco = alpha(cs.backgroundColor) > 0.02 || cs.backgroundImage !== 'none' || cs.boxShadow !== 'none' ||
      ['Top', 'Right', 'Bottom', 'Left'].some((s) => parseFloat((cs as any)[`border${s}Width`]) > 0 && (cs as any)[`border${s}Style`] !== 'none' && alpha((cs as any)[`border${s}Color`]) > 0.02);
    if (deco) add(el.getBoundingClientRect());
    el.childNodes.forEach((n) => { if (n.nodeType === 3 && (n.textContent || '').trim()) { const rg = document.createRange(); rg.selectNodeContents(n); add(rg.getBoundingClientRect()); } });
  });
  return b;
};

export const FitBoard: React.FC<{bw: number; bh: number; frames: number; top: number; bottom: number; zoom?: number; card?: boolean; children: React.ReactNode}> = ({bw, bh, frames, top, bottom, zoom = 1, card = false, children}) => {
  const r1 = useRef<HTMLDivElement>(null), r2 = useRef<HTMLDivElement>(null);
  const [box, setBox] = useState<Box | null>(null);
  const [handle] = useState(() => delayRender('판 내용 재기'));
  useLayoutEffect(() => {
    let live = true;
    (document as any).fonts.ready.then(() => {
      if (!live) return;
      const bs = [r1.current, r2.current].map((r) => (r ? measure(r) : null)).filter(Boolean) as Box[];
      const pad = 12;
      const u = bs.length ? {x0: Math.min(...bs.map((b) => b.x0)), y0: Math.min(...bs.map((b) => b.y0)), x1: Math.max(...bs.map((b) => b.x1)), y1: Math.max(...bs.map((b) => b.y1))} : {x0: 0, y0: 0, x1: bw, y1: bh};
      setBox({x0: Math.max(0, u.x0 - pad), y0: Math.max(0, u.y0 - pad), x1: Math.min(bw, u.x1 + pad), y1: Math.min(bh, u.y1 + pad)});
    });
    return () => { live = false; };
  }, []);
  useEffect(() => { if (box) continueRender(handle); }, [box, handle]);
  const b = box ?? {x0: 0, y0: 0, x1: bw, y1: bh};
  const cw = b.x1 - b.x0, ch = b.y1 - b.y0; const W = SZ.x1 - SZ.x0, H = bottom - top;
  const s = Math.min((W * 0.97) / cw, (H * 0.95) / ch, card ? 1.4 : 1.05);   // v3 card: 내용이 좁으면 1.4배까지 키운다(10/16 사장님 '작은 막대·작은 글씨')
  const ox = (b.x0 + b.x1) / 2, oy = (b.y0 + b.y1) / 2; const midY = (top + bottom) / 2;
  const hidden: React.CSSProperties = {position: 'absolute', left: 0, top: 0, width: bw, height: bh, opacity: 0, pointerEvents: 'none'};
  return (
    <>
      {box ? null : <div style={{position: 'absolute', left: -4000, top: 0, width: bw, height: bh}}>
        <div ref={r1} style={hidden}><Freeze frame={Math.max(0, Math.round(frames * 0.5))}>{children}</Freeze></div>
        <div ref={r2} style={hidden}><Freeze frame={Math.max(0, frames - 1)}>{children}</Freeze></div>
      </div>}
      {/* v3 card: 실사 배경 위 흰 카드(모서리 24) — 판 칸만 흰색, 둘레·아래는 사진이 보인다 */}
      {card ? <div style={{position: 'absolute', left: SZ.x0, top, width: W, height: H, background: 'rgba(255,255,255,0.95)', borderRadius: 24, boxShadow: '0 18px 50px rgba(0,0,0,0.45)'}} /> : <>
      {/* 아래 유튜브 제목 자리(글자 금지): 같은 판을 크게·흐리게 깔아 빈 검은 칸이 아니게 — 바탕 그림(글자는 흐려 읽히지 않음) */}
      <div style={{position: 'absolute', left: 0, top: BAND_END + 10, width: 1080, height: 1920 - BAND_END - 10, overflow: 'hidden', opacity: 0.4, filter: 'blur(22px)'}}>
        <div style={{position: 'absolute', left: 540 - ox, top: 300 - oy, width: bw, height: bh, transform: `scale(${s * 1.5 * zoom})`, transformOrigin: `${ox}px ${oy}px`}}>{children}</div>
      </div>
      <div style={{position: 'absolute', left: 0, top: BAND_END + 10, width: 1080, height: 1920 - BAND_END - 10, background: `linear-gradient(rgba(16,17,20,0.35), rgba(16,17,20,0.55) 45%, rgba(16,17,20,0.9))`}} /></>}
      <div style={{position: 'absolute', left: SZ.x0, top, width: W, height: H, overflow: 'hidden', borderRadius: card ? 24 : 0}}>
        <div style={{position: 'absolute', left: CX - SZ.x0 - ox, top: midY - top - oy, width: bw, height: bh, transform: `scale(${s * zoom})`, transformOrigin: `${ox}px ${oy}px`}}>{children}</div>
      </div>
    </>
  );
};
